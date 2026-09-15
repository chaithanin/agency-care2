import { all, get, run, tx, nowIso } from '../db.js';
import { getAdapter } from '../channels/adapter.js';
import { emit } from './events.js';
import { badRequest, notFound } from '../http.js';
import { LIFECYCLE_STAGES } from '../config.js';
import { dispatchWebhook } from './webhooks.js';

const parseJson = (s, fallback = {}) => { try { return JSON.parse(s ?? ''); } catch { return fallback; } };

export function getChannel(idOrProvider) {
  const row = typeof idOrProvider === 'number'
    ? get('SELECT * FROM channels WHERE id = ?', [idOrProvider])
    : get('SELECT * FROM channels WHERE provider = ? AND active = 1 ORDER BY id LIMIT 1', [idOrProvider]);
  if (!row) return null;
  return { ...row, config: parseJson(row.config_json) };
}

/**
 * รับข้อความขาเข้าที่ normalize แล้ว → หา/สร้าง contact → หา/สร้าง conversation → บันทึก message
 * idempotent: ถ้า externalMessageId ซ้ำ (LINE ยิงซ้ำ) จะไม่บันทึกเบิ้ล
 */
export function ingestIncoming(channel, msg) {
  const existing = msg.externalMessageId
    ? get('SELECT * FROM messages WHERE channel_id = ? AND external_message_id = ?', [channel.id, msg.externalMessageId])
    : null;
  if (existing) return { duplicate: true, messageId: existing.id, conversationId: existing.conversation_id };

  const result = tx(() => {
    let link = get(
      'SELECT * FROM contact_channels WHERE channel_id = ? AND external_user_id = ?',
      [channel.id, msg.externalUserId],
    );
    let contactCreated = false;

    if (!link) {
      const displayName = msg.profile?.displayName || `${channel.provider.toUpperCase()} ${String(msg.externalUserId).slice(-6)}`;
      const contactId = run(
        'INSERT INTO contacts (display_name, language, lifecycle_stage) VALUES (?, ?, ?)',
        [displayName, msg.profile?.language || 'th', 'new_lead'],
      ).lastInsertRowid;
      run(
        'INSERT INTO contact_channels (contact_id, channel_id, external_user_id, profile_json) VALUES (?, ?, ?, ?)',
        [contactId, channel.id, msg.externalUserId, JSON.stringify(msg.profile || {})],
      );
      run('INSERT INTO lifecycle_events (contact_id, from_stage, to_stage, changed_by) VALUES (?, NULL, ?, ?)',
        [contactId, 'new_lead', 'system']);
      link = { contact_id: contactId };
      contactCreated = true;
    }

    let conversation = get(
      "SELECT * FROM conversations WHERE contact_id = ? AND channel_id = ? AND status = 'open' ORDER BY id DESC LIMIT 1",
      [link.contact_id, channel.id],
    );
    let conversationCreated = false;
    if (!conversation) {
      const convId = run(
        'INSERT INTO conversations (contact_id, channel_id, status, last_message_at, first_inbound_at) VALUES (?, ?, ?, ?, ?)',
        [link.contact_id, channel.id, 'open', nowIso(), nowIso()],
      ).lastInsertRowid;
      conversation = get('SELECT * FROM conversations WHERE id = ?', [convId]);
      conversationCreated = true;
    }

    const messageId = run(
      `INSERT INTO messages (conversation_id, contact_id, channel_id, direction, source, text, external_message_id, payload_json)
       VALUES (?, ?, ?, 'in', 'contact', ?, ?, ?)`,
      [conversation.id, link.contact_id, channel.id, msg.text, msg.externalMessageId || null, JSON.stringify(msg.raw || {})],
    ).lastInsertRowid;

    run('UPDATE conversations SET last_message_at = ?, first_inbound_at = COALESCE(first_inbound_at, ?) WHERE id = ?',
      [nowIso(), nowIso(), conversation.id]);

    return { contactId: link.contact_id, conversationId: conversation.id, messageId, contactCreated, conversationCreated };
  });

  emit('message.received', {
    conversationId: result.conversationId,
    contactId: result.contactId,
    messageId: result.messageId,
    text: msg.text,
  });
  if (result.conversationCreated) emit('conversation.created', { conversationId: result.conversationId, contactId: result.contactId });

  return { duplicate: false, ...result };
}

/** ส่งข้อความออกผ่าน adapter ของช่องทางนั้น แล้วบันทึกลง messages */
export async function sendOutbound({ conversationId, text, userId = null, source = 'human', replyToken = null }) {
  if (!text || !text.trim()) throw badRequest('ข้อความว่าง');
  const conv = get('SELECT * FROM conversations WHERE id = ?', [conversationId]);
  if (!conv) throw notFound('ไม่พบบทสนทนา');
  const channel = getChannel(conv.channel_id);
  const link = get('SELECT * FROM contact_channels WHERE contact_id = ? AND channel_id = ?', [conv.contact_id, channel.id]);

  const adapter = getAdapter(channel.provider);
  const sent = await adapter.sendMessage({ channel, to: link?.external_user_id, text, replyToken });

  const messageId = run(
    `INSERT INTO messages (conversation_id, contact_id, channel_id, direction, sender_user_id, source, text, external_message_id, payload_json)
     VALUES (?, ?, ?, 'out', ?, ?, ?, ?, ?)`,
    [conv.id, conv.contact_id, channel.id, userId, source, text, sent.externalMessageId || null, JSON.stringify({ dryRun: !!sent.dryRun })],
  ).lastInsertRowid;

  run('UPDATE conversations SET last_message_at = ?, first_reply_at = COALESCE(first_reply_at, ?) WHERE id = ?',
    [nowIso(), nowIso(), conv.id]);

  emit('message.sent', { conversationId: conv.id, messageId, text, dryRun: !!sent.dryRun });
  return { messageId, dryRun: !!sent.dryRun };
}

export function assignConversation(conversationId, userId, byUser = 'system') {
  const conv = get('SELECT * FROM conversations WHERE id = ?', [conversationId]);
  if (!conv) throw notFound('ไม่พบบทสนทนา');
  if (userId !== null) {
    const user = get('SELECT * FROM users WHERE id = ? AND active = 1', [userId]);
    if (!user) throw badRequest('ไม่พบผู้ใช้ที่จะมอบหมาย');
  }
  run('UPDATE conversations SET assignee_user_id = ? WHERE id = ?', [userId, conversationId]);
  emit('conversation.assigned', { conversationId, assigneeUserId: userId, by: byUser });
  return get('SELECT * FROM conversations WHERE id = ?', [conversationId]);
}

export function setConversationStatus(conversationId, status) {
  if (!['open', 'closed'].includes(status)) throw badRequest('status ต้องเป็น open หรือ closed');
  const conv = get('SELECT * FROM conversations WHERE id = ?', [conversationId]);
  if (!conv) throw notFound('ไม่พบบทสนทนา');
  run('UPDATE conversations SET status = ?, closed_at = ? WHERE id = ?',
    [status, status === 'closed' ? nowIso() : null, conversationId]);
  emit('conversation.status_changed', { conversationId, status });
  return get('SELECT * FROM conversations WHERE id = ?', [conversationId]);
}

/** เปลี่ยน lifecycle stage — จุดเดียวที่ยิง webhook ออกไปหา Agency Care */
export async function setLifecycleStage(contactId, toStage, changedBy = 'system') {
  if (!LIFECYCLE_STAGES.includes(toStage)) {
    throw badRequest(`stage ต้องเป็นหนึ่งใน: ${LIFECYCLE_STAGES.join(', ')}`);
  }
  const contact = get('SELECT * FROM contacts WHERE id = ?', [contactId]);
  if (!contact) throw notFound('ไม่พบผู้ติดต่อ');
  const fromStage = contact.lifecycle_stage;
  if (fromStage === toStage) return { contact, changed: false };

  tx(() => {
    run('UPDATE contacts SET lifecycle_stage = ?, updated_at = ? WHERE id = ?', [toStage, nowIso(), contactId]);
    run('INSERT INTO lifecycle_events (contact_id, from_stage, to_stage, changed_by) VALUES (?, ?, ?, ?)',
      [contactId, fromStage, toStage, changedBy]);
  });

  const payload = {
    contactId,
    displayName: contact.display_name,
    fromStage,
    toStage,
    changedBy,
    changedAt: new Date().toISOString(),
  };
  emit('contact.lifecycle_changed', payload);
  await dispatchWebhook('contact.lifecycle_changed', payload);

  return { contact: get('SELECT * FROM contacts WHERE id = ?', [contactId]), changed: true };
}

export function addTag(contactId, name) {
  const tagName = String(name || '').trim().toLowerCase();
  if (!tagName) throw badRequest('ชื่อแท็กว่าง');
  run('INSERT OR IGNORE INTO tags (name) VALUES (?)', [tagName]);
  const tag = get('SELECT * FROM tags WHERE name = ?', [tagName]);
  run('INSERT OR IGNORE INTO contact_tags (contact_id, tag_id) VALUES (?, ?)', [contactId, tag.id]);
  return tag;
}

export const contactTags = (contactId) =>
  all('SELECT t.name FROM tags t JOIN contact_tags ct ON ct.tag_id = t.id WHERE ct.contact_id = ? ORDER BY t.name', [contactId])
    .map((r) => r.name);

export function contactCustomFields(contactId) {
  const rows = all(
    `SELECT d.key, d.label, d.type, d.options_json, v.value
       FROM custom_field_defs d
       LEFT JOIN contact_field_values v ON v.field_id = d.id AND v.contact_id = ?
      ORDER BY d.id`,
    [contactId],
  );
  return rows.map((r) => ({
    key: r.key, label: r.label, type: r.type,
    options: parseJson(r.options_json, []),
    value: r.value ?? null,
  }));
}

export function setCustomField(contactId, key, value) {
  const def = get('SELECT * FROM custom_field_defs WHERE key = ?', [key]);
  if (!def) throw badRequest(`ไม่รู้จัก custom field: ${key}`);
  run(
    `INSERT INTO contact_field_values (contact_id, field_id, value) VALUES (?, ?, ?)
     ON CONFLICT(contact_id, field_id) DO UPDATE SET value = excluded.value`,
    [contactId, def.id, value == null ? null : String(value)],
  );
  run('UPDATE contacts SET updated_at = ? WHERE id = ?', [nowIso(), contactId]);
  return contactCustomFields(contactId);
}

/** รายการบทสนทนาสำหรับคอลัมน์ซ้ายของ Inbox */
export function listConversations({ status = 'open', filter = 'all', assigneeUserId = null, limit = 50 } = {}) {
  const where = ['c.status = ?'];
  const params = [status];
  if (filter === 'unassigned') where.push('c.assignee_user_id IS NULL');
  if (filter === 'assigned') where.push('c.assignee_user_id IS NOT NULL');
  if (filter === 'mine') { where.push('c.assignee_user_id = ?'); params.push(assigneeUserId); }

  const rows = all(
    `SELECT c.id, c.status, c.assignee_user_id, c.last_message_at, c.channel_id,
            ct.id AS contact_id, ct.display_name, ct.lifecycle_stage,
            ch.provider, u.name AS assignee_name,
            (SELECT text FROM messages m WHERE m.conversation_id = c.id ORDER BY m.id DESC LIMIT 1) AS last_text,
            (SELECT direction FROM messages m WHERE m.conversation_id = c.id ORDER BY m.id DESC LIMIT 1) AS last_direction
       FROM conversations c
       JOIN contacts ct ON ct.id = c.contact_id
       JOIN channels ch ON ch.id = c.channel_id
       LEFT JOIN users u ON u.id = c.assignee_user_id
      WHERE ${where.join(' AND ')}
      ORDER BY c.last_message_at DESC, c.id DESC
      LIMIT ?`,
    [...params, limit],
  );
  return rows;
}

export function conversationDetail(conversationId) {
  const conv = get(
    `SELECT c.*, ct.display_name, ct.lifecycle_stage, ct.language, ct.phone, ct.email,
            ch.provider, u.name AS assignee_name
       FROM conversations c
       JOIN contacts ct ON ct.id = c.contact_id
       JOIN channels ch ON ch.id = c.channel_id
       LEFT JOIN users u ON u.id = c.assignee_user_id
      WHERE c.id = ?`,
    [conversationId],
  );
  if (!conv) throw notFound('ไม่พบบทสนทนา');
  return {
    conversation: conv,
    messages: all(
      `SELECT m.id, m.direction, m.source, m.text, m.created_at, u.name AS sender_name
         FROM messages m LEFT JOIN users u ON u.id = m.sender_user_id
        WHERE m.conversation_id = ? ORDER BY m.id ASC LIMIT 500`,
      [conversationId],
    ),
    contact: {
      id: conv.contact_id,
      displayName: conv.display_name,
      lifecycleStage: conv.lifecycle_stage,
      language: conv.language,
      phone: conv.phone,
      email: conv.email,
      tags: contactTags(conv.contact_id),
      customFields: contactCustomFields(conv.contact_id),
    },
  };
}

export function counters() {
  const row = get(
    `SELECT
       SUM(CASE WHEN status = 'open' THEN 1 ELSE 0 END) AS open,
       SUM(CASE WHEN status = 'open' AND assignee_user_id IS NULL THEN 1 ELSE 0 END) AS unassigned,
       SUM(CASE WHEN status = 'open' AND assignee_user_id IS NOT NULL THEN 1 ELSE 0 END) AS assigned,
       SUM(CASE WHEN status = 'closed' THEN 1 ELSE 0 END) AS closed
     FROM conversations`,
  );
  return { open: row.open || 0, unassigned: row.unassigned || 0, assigned: row.assigned || 0, closed: row.closed || 0 };
}
