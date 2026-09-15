/**
 * Agency Care Integration API (roadmap สัปดาห์ 15-16)
 * ทุก endpoint ต้องมี header  X-API-Key: gtg_xxx
 * เป็นสัญญาที่ทีม Agency Care เรียกใช้ได้เองโดยไม่ต้องถามเรา
 */
import { all, get } from '../db.js';
import { authenticate } from '../services/apiKeys.js';
import { sendJson, badRequest, notFound, clampLimit, parseQuery, HttpError } from '../http.js';
import { contactTags, contactCustomFields, setLifecycleStage, sendOutbound, counters } from '../services/inbox.js';
import { LIFECYCLE_STAGES } from '../config.js';

// rate limit ง่าย ๆ ต่อ API key: 120 ครั้ง / นาที
const buckets = new Map();
function rateLimit(keyId, limit = 120, windowMs = 60_000) {
  const now = Date.now();
  const bucket = buckets.get(keyId);
  if (!bucket || now > bucket.resetAt) {
    buckets.set(keyId, { count: 1, resetAt: now + windowMs });
    return { remaining: limit - 1 };
  }
  bucket.count += 1;
  if (bucket.count > limit) throw new HttpError(429, 'rate_limited', 'เรียกถี่เกินไป ลองใหม่ในอีกสักครู่');
  return { remaining: limit - bucket.count };
}

const contactShape = (row) => ({
  id: row.id,
  displayName: row.display_name,
  lifecycleStage: row.lifecycle_stage,
  language: row.language,
  phone: row.phone,
  email: row.email,
  owner: row.owner_name || null,
  createdAt: row.created_at,
  updatedAt: row.updated_at,
});

export async function handleAgencyCare(req, res, url, method) {
  const segments = url.pathname.split('/').filter(Boolean); // api, v1, ...
  const route = segments.slice(2);
  const query = parseQuery(url);

  if (route[0] === 'health' && method === 'GET') {
    return sendJson(res, 200, { ok: true, service: 'gtg-chat-inbox', version: '0.1.0' });
  }

  const needsWrite = method !== 'GET';
  const apiKey = authenticate(req, needsWrite ? 'write' : 'read');
  const { remaining } = rateLimit(apiKey.id);
  res.setHeader('x-ratelimit-remaining', String(remaining));

  // GET /api/v1/contacts
  if (route[0] === 'contacts' && route.length === 1 && method === 'GET') {
    const where = ['1 = 1'];
    const params = [];
    if (query.stage) {
      if (!LIFECYCLE_STAGES.includes(query.stage)) throw badRequest(`stage ไม่ถูกต้อง: ${query.stage}`);
      where.push('c.lifecycle_stage = ?'); params.push(query.stage);
    }
    if (query.tag) {
      where.push('EXISTS (SELECT 1 FROM contact_tags ct JOIN tags t ON t.id = ct.tag_id WHERE ct.contact_id = c.id AND t.name = ?)');
      params.push(String(query.tag).toLowerCase());
    }
    if (query.channel) {
      where.push('EXISTS (SELECT 1 FROM contact_channels cc JOIN channels ch ON ch.id = cc.channel_id WHERE cc.contact_id = c.id AND ch.provider = ?)');
      params.push(query.channel);
    }
    if (query.q) { where.push('c.display_name LIKE ?'); params.push(`%${query.q}%`); }
    if (query.updated_since) { where.push('c.updated_at >= ?'); params.push(query.updated_since); }

    const limit = clampLimit(query.limit, 25, 100);
    const offset = Math.max(0, Number(query.offset) || 0);
    const total = get(`SELECT COUNT(*) AS n FROM contacts c WHERE ${where.join(' AND ')}`, params).n;
    const rows = all(
      `SELECT c.*, u.name AS owner_name FROM contacts c
         LEFT JOIN users u ON u.id = c.owner_user_id
        WHERE ${where.join(' AND ')}
        ORDER BY c.updated_at DESC, c.id DESC LIMIT ? OFFSET ?`,
      [...params, limit, offset],
    );
    return sendJson(res, 200, {
      data: rows.map((r) => ({ ...contactShape(r), tags: contactTags(r.id) })),
      pagination: { total, limit, offset, hasMore: offset + rows.length < total },
    });
  }

  // GET /api/v1/contacts/:id
  if (route[0] === 'contacts' && route.length === 2 && method === 'GET') {
    const id = Number(route[1]);
    const row = get('SELECT c.*, u.name AS owner_name FROM contacts c LEFT JOIN users u ON u.id = c.owner_user_id WHERE c.id = ?', [id]);
    if (!row) throw notFound('ไม่พบผู้ติดต่อ');
    return sendJson(res, 200, {
      data: {
        ...contactShape(row),
        tags: contactTags(id),
        customFields: contactCustomFields(id),
        channels: all(
          `SELECT ch.provider, cc.external_user_id AS externalUserId, cc.created_at AS createdAt
             FROM contact_channels cc JOIN channels ch ON ch.id = cc.channel_id WHERE cc.contact_id = ?`, [id]),
        lifecycleHistory: all(
          'SELECT from_stage AS fromStage, to_stage AS toStage, changed_by AS changedBy, created_at AS at FROM lifecycle_events WHERE contact_id = ? ORDER BY id DESC LIMIT 50', [id]),
        conversations: all(
          `SELECT c.id, c.status, c.last_message_at AS lastMessageAt, u.name AS assignee
             FROM conversations c LEFT JOIN users u ON u.id = c.assignee_user_id
            WHERE c.contact_id = ? ORDER BY c.id DESC`, [id]),
      },
    });
  }

  // POST /api/v1/contacts/:id/lifecycle   { "stage": "hot_lead" }
  if (route[0] === 'contacts' && route[2] === 'lifecycle' && method === 'POST') {
    const id = Number(route[1]);
    const stage = req.body?.stage;
    if (!stage) throw badRequest('ต้องระบุ stage');
    const result = await setLifecycleStage(id, stage, `agency-care:${apiKey.name}`);
    return sendJson(res, 200, { data: { contactId: id, lifecycleStage: result.contact.lifecycle_stage, changed: result.changed } });
  }

  // GET /api/v1/conversations
  if (route[0] === 'conversations' && route.length === 1 && method === 'GET') {
    const where = ['1 = 1'];
    const params = [];
    if (query.status) {
      if (!['open', 'closed'].includes(query.status)) throw badRequest('status ต้องเป็น open หรือ closed');
      where.push('c.status = ?'); params.push(query.status);
    }
    if (query.contact_id) { where.push('c.contact_id = ?'); params.push(Number(query.contact_id)); }
    if (query.assignee_id) { where.push('c.assignee_user_id = ?'); params.push(Number(query.assignee_id)); }
    if (query.unassigned === 'true') where.push('c.assignee_user_id IS NULL');

    const limit = clampLimit(query.limit, 25, 100);
    const offset = Math.max(0, Number(query.offset) || 0);
    const total = get(`SELECT COUNT(*) AS n FROM conversations c WHERE ${where.join(' AND ')}`, params).n;
    const rows = all(
      `SELECT c.id, c.status, c.last_message_at, c.opened_at, c.closed_at,
              ct.id AS contact_id, ct.display_name, ct.lifecycle_stage,
              ch.provider, u.name AS assignee_name
         FROM conversations c
         JOIN contacts ct ON ct.id = c.contact_id
         JOIN channels ch ON ch.id = c.channel_id
         LEFT JOIN users u ON u.id = c.assignee_user_id
        WHERE ${where.join(' AND ')}
        ORDER BY c.last_message_at DESC LIMIT ? OFFSET ?`,
      [...params, limit, offset],
    );
    return sendJson(res, 200, {
      data: rows.map((r) => ({
        id: r.id,
        status: r.status,
        channel: r.provider,
        assignee: r.assignee_name,
        lastMessageAt: r.last_message_at,
        openedAt: r.opened_at,
        closedAt: r.closed_at,
        contact: { id: r.contact_id, displayName: r.display_name, lifecycleStage: r.lifecycle_stage },
      })),
      pagination: { total, limit, offset, hasMore: offset + rows.length < total },
    });
  }

  // GET /api/v1/conversations/:id/messages
  if (route[0] === 'conversations' && route[2] === 'messages' && method === 'GET') {
    const id = Number(route[1]);
    if (!get('SELECT id FROM conversations WHERE id = ?', [id])) throw notFound('ไม่พบบทสนทนา');
    const limit = clampLimit(query.limit, 50, 200);
    const rows = all(
      `SELECT m.id, m.direction, m.source, m.text, m.created_at, u.name AS sender_name
         FROM messages m LEFT JOIN users u ON u.id = m.sender_user_id
        WHERE m.conversation_id = ? ORDER BY m.id ASC LIMIT ?`,
      [id, limit],
    );
    return sendJson(res, 200, {
      data: rows.map((m) => ({
        id: m.id, direction: m.direction, source: m.source, text: m.text,
        sender: m.sender_name || (m.direction === 'in' ? 'contact' : 'system'), at: m.created_at,
      })),
    });
  }

  // POST /api/v1/conversations/:id/messages   { "text": "..." }
  if (route[0] === 'conversations' && route[2] === 'messages' && method === 'POST') {
    const id = Number(route[1]);
    const text = req.body?.text;
    if (!text) throw badRequest('ต้องระบุ text');
    const sent = await sendOutbound({ conversationId: id, text, source: 'api' });
    return sendJson(res, 201, { data: { messageId: sent.messageId, dryRun: sent.dryRun } });
  }

  // GET /api/v1/stats/dashboard
  if (route[0] === 'stats' && route[1] === 'dashboard' && method === 'GET') {
    const lifecycle = Object.fromEntries(LIFECYCLE_STAGES.map((s) => [s, 0]));
    for (const row of all('SELECT lifecycle_stage AS stage, COUNT(*) AS n FROM contacts GROUP BY lifecycle_stage')) {
      lifecycle[row.stage] = row.n;
    }
    const responded = all(
      `SELECT (julianday(first_reply_at) - julianday(first_inbound_at)) * 24 * 60 AS minutes
         FROM conversations WHERE first_reply_at IS NOT NULL AND first_inbound_at IS NOT NULL`,
    ).map((r) => r.minutes).filter((n) => Number.isFinite(n) && n >= 0);

    return sendJson(res, 200, {
      data: {
        conversations: counters(),
        lifecycle,
        contactsTotal: get('SELECT COUNT(*) AS n FROM contacts').n,
        messages: {
          inbound: get("SELECT COUNT(*) AS n FROM messages WHERE direction = 'in'").n,
          outbound: get("SELECT COUNT(*) AS n FROM messages WHERE direction = 'out'").n,
        },
        avgFirstResponseMinutes: responded.length
          ? Number((responded.reduce((a, b) => a + b, 0) / responded.length).toFixed(2))
          : null,
        workload: all(
          `SELECT u.name, COUNT(c.id) AS openConversations
             FROM users u LEFT JOIN conversations c ON c.assignee_user_id = u.id AND c.status = 'open'
            WHERE u.role = 'agent' AND u.active = 1 GROUP BY u.id ORDER BY openConversations DESC`),
      },
    });
  }

  throw notFound(`ไม่มี endpoint นี้: ${method} ${url.pathname}`);
}
