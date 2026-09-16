import { run, all, get, tx } from '../../db.js';
import { config } from '../../config.js';
import { createClient } from './client.js';

/**
 * ดึงข้อมูลจาก respond.io ลงตาราง respondio_* (ตารางกระจกเงา)
 * ไม่แตะตารางหลักของระบบเลย — การแปลงเข้าระบบอยู่ใน map.js
 */

const J = (v) => (v == null ? null : JSON.stringify(v));

function startRun(resource) {
  const r = run('INSERT INTO respondio_sync_runs (resource) VALUES (?)', [resource]);
  return Number(r.lastInsertRowid);
}

function finishRun(id, { ok, fetched, error }) {
  run(
    `UPDATE respondio_sync_runs
        SET finished_at = datetime('now'), ok = ?, fetched = ?, error = ?
      WHERE id = ?`,
    [ok ? 1 : 0, fetched, error ? String(error).slice(0, 500) : null, id],
  );
}

/** ครอบการ sync หนึ่งชนิด ให้บันทึกผลลงตาราง run เสมอ ไม่ว่าสำเร็จหรือพัง */
async function tracked(resource, fn) {
  const runId = startRun(resource);
  try {
    const fetched = await fn();
    finishRun(runId, { ok: true, fetched });
    return { resource, ok: true, fetched };
  } catch (err) {
    finishRun(runId, { ok: false, fetched: 0, error: err.message });
    return { resource, ok: false, fetched: 0, error: err.message };
  }
}

export function upsertContact(c) {
  run(
    `INSERT INTO respondio_contacts
       (id, first_name, last_name, phone, email, language, country_code, profile_pic,
        lifecycle, status, assignee_id, assignee_name, tags_json, fields_json, created_at, synced_at)
     VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?, datetime('now'))
     ON CONFLICT(id) DO UPDATE SET
       first_name=excluded.first_name, last_name=excluded.last_name,
       phone=excluded.phone, email=excluded.email, language=excluded.language,
       country_code=excluded.country_code, profile_pic=excluded.profile_pic,
       lifecycle=excluded.lifecycle, status=excluded.status,
       assignee_id=excluded.assignee_id, assignee_name=excluded.assignee_name,
       tags_json=excluded.tags_json, fields_json=excluded.fields_json,
       synced_at=datetime('now')`,
    [
      c.id, c.firstName ?? null, c.lastName ?? null, c.phone ?? null, c.email ?? null,
      c.language ?? null, c.countryCode ?? null, c.profilePic ?? null,
      c.lifecycle ?? null, c.status ?? null,
      c.assignee?.id ?? null,
      c.assignee ? [c.assignee.firstName, c.assignee.lastName].filter(Boolean).join(' ') : null,
      J(c.tags ?? []), J(c.custom_fields ?? []), c.created_at ?? null,
    ],
  );
}

export function upsertContactChannel(contactId, ch) {
  run(
    `INSERT INTO respondio_contact_channels
       (id, contact_id, name, source, meta_json, last_message_time,
        last_incoming_message_time, created_at, synced_at)
     VALUES (?,?,?,?,?,?,?,?, datetime('now'))
     ON CONFLICT(id) DO UPDATE SET
       name=excluded.name, source=excluded.source, meta_json=excluded.meta_json,
       last_message_time=excluded.last_message_time,
       last_incoming_message_time=excluded.last_incoming_message_time,
       synced_at=datetime('now')`,
    [
      ch.id, contactId, ch.name ?? null, ch.source ?? null, J(ch.meta ?? null),
      ch.lastMessageTime ?? null, ch.lastIncomingMessageTime ?? null, ch.created_at ?? null,
    ],
  );
}

/** ดึงข้อความล่าสุดออกมาเป็นตัวหนังสือ เพื่อค้นหาได้ง่าย */
export function messageText(m) {
  const msg = m.message ?? m;
  if (typeof msg?.text === 'string') return msg.text;
  if (msg?.type === 'attachment') return `[${msg.attachment?.type ?? 'attachment'}] ${msg.attachment?.url ?? ''}`.trim();
  if (msg?.type === 'quick_reply') return msg.title ?? '';
  return null;
}

export function latestStatus(m) {
  const list = m.status;
  if (!Array.isArray(list) || list.length === 0) return null;
  return list.reduce((a, b) => ((b.timestamp ?? 0) >= (a.timestamp ?? 0) ? b : a)).value ?? null;
}

export function upsertMessage(contactId, m) {
  const msg = m.message ?? m;
  run(
    `INSERT INTO respondio_messages
       (id, contact_id, channel_id, traffic, type, text, payload_json, status, timestamp, synced_at)
     VALUES (?,?,?,?,?,?,?,?,?, datetime('now'))
     ON CONFLICT(id) DO UPDATE SET
       channel_id=excluded.channel_id, traffic=excluded.traffic, type=excluded.type,
       text=excluded.text, payload_json=excluded.payload_json, status=excluded.status,
       timestamp=excluded.timestamp, synced_at=datetime('now')`,
    [
      m.messageId ?? m.id, contactId, m.channelId ?? null, m.traffic ?? null,
      msg?.type ?? null, messageText(m), J(m), latestStatus(m), m.timestamp ?? null,
    ],
  );
}

// ── ตัว sync แต่ละชนิด ────────────────────────────────────────

export async function syncWorkspace(client = createClient()) {
  const out = [];

  out.push(await tracked('space.channel', async () => {
    const rows = await client.listChannels();
    tx(() => rows.forEach((c) => run(
      `INSERT INTO respondio_channels (id, name, source, meta_json, synced_at)
       VALUES (?,?,?,?, datetime('now'))
       ON CONFLICT(id) DO UPDATE SET name=excluded.name, source=excluded.source,
         meta_json=excluded.meta_json, synced_at=datetime('now')`,
      [c.id, c.name ?? null, c.source ?? null, J(c.meta ?? null)],
    )));
    return rows.length;
  }));

  out.push(await tracked('space.user', async () => {
    const rows = await client.listUsers();
    tx(() => rows.forEach((u) => run(
      `INSERT INTO respondio_users (id, first_name, last_name, email, synced_at)
       VALUES (?,?,?,?, datetime('now'))
       ON CONFLICT(id) DO UPDATE SET first_name=excluded.first_name,
         last_name=excluded.last_name, email=excluded.email, synced_at=datetime('now')`,
      [u.id, u.firstName ?? null, u.lastName ?? null, u.email ?? null],
    )));
    return rows.length;
  }));

  out.push(await tracked('space.custom_field', async () => {
    const rows = await client.listCustomFields();
    tx(() => rows.forEach((f) => run(
      `INSERT INTO respondio_custom_fields (id, name, type, meta_json, synced_at)
       VALUES (?,?,?,?, datetime('now'))
       ON CONFLICT(id) DO UPDATE SET name=excluded.name, type=excluded.type,
         meta_json=excluded.meta_json, synced_at=datetime('now')`,
      [f.id, f.name ?? null, f.type ?? null, J(f)],
    )));
    return rows.length;
  }));

  out.push(await tracked('space.closing_notes', async () => {
    const rows = await client.listClosingNotes();
    tx(() => rows.forEach((n) => run(
      `INSERT INTO respondio_closing_notes (id, name, meta_json, synced_at)
       VALUES (?,?,?, datetime('now'))
       ON CONFLICT(id) DO UPDATE SET name=excluded.name, meta_json=excluded.meta_json,
         synced_at=datetime('now')`,
      [n.id, n.name ?? null, J(n)],
    )));
    return rows.length;
  }));

  return out;
}

export async function syncContacts(client = createClient(), { max } = {}) {
  return tracked('contacts', async () => {
    const rows = await client.listContacts({ max });
    tx(() => {
      rows.forEach(upsertContact);
      for (const c of rows) {
        for (const t of c.tags ?? []) {
          run(`INSERT INTO respondio_tags (name) VALUES (?) ON CONFLICT(name) DO NOTHING`, [t]);
        }
      }
    });
    return rows.length;
  });
}

export async function syncContactDetails(client = createClient(), { messagesPerContact, contactIds } = {}) {
  const ids = contactIds ?? all('SELECT id FROM respondio_contacts ORDER BY id').map((r) => r.id);
  const perContact = messagesPerContact ?? config.respondio.messagesPerContact;

  const channels = await tracked('contact.channels', async () => {
    let n = 0;
    for (const id of ids) {
      const rows = await client.listContactChannels(id);
      tx(() => rows.forEach((ch) => upsertContactChannel(id, ch)));
      n += rows.length;
    }
    return n;
  });

  const messages = await tracked('contact.messages', async () => {
    let n = 0;
    for (const id of ids) {
      const rows = await client.listMessages(id, { max: perContact });
      tx(() => rows.forEach((m) => upsertMessage(id, m)));
      n += rows.length;
    }
    return n;
  });

  return [channels, messages];
}

/** ดึงทุกอย่าง — เรียงลำดับให้ workspace มาก่อน แล้วค่อย contact และข้อความ */
export async function syncAll(client = createClient(), opts = {}) {
  const results = [];
  results.push(...await syncWorkspace(client));
  const contacts = await syncContacts(client, opts);
  results.push(contacts);
  if (contacts.ok) results.push(...await syncContactDetails(client, opts));
  return results;
}

export function syncSummary() {
  return {
    contacts: get('SELECT COUNT(*) n FROM respondio_contacts').n,
    contactChannels: get('SELECT COUNT(*) n FROM respondio_contact_channels').n,
    messages: get('SELECT COUNT(*) n FROM respondio_messages').n,
    users: get('SELECT COUNT(*) n FROM respondio_users').n,
    channels: get('SELECT COUNT(*) n FROM respondio_channels').n,
    customFields: get('SELECT COUNT(*) n FROM respondio_custom_fields').n,
    tags: get('SELECT COUNT(*) n FROM respondio_tags').n,
    closingNotes: get('SELECT COUNT(*) n FROM respondio_closing_notes').n,
    linked: get('SELECT COUNT(*) n FROM respondio_contact_links').n,
  };
}
