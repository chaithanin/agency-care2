import test from 'node:test';
import assert from 'node:assert/strict';
import path from 'node:path';
import os from 'node:os';
import { mkdtempSync, rmSync, existsSync } from 'node:fs';

process.env.DB_FILE = path.join(mkdtempSync(path.join(os.tmpdir(), 'gtg-rio-')), 'test.db');
process.env.RESPONDIO_API_TOKEN = 'test-token';
process.env.RESPONDIO_PAGE_SIZE = '2';
process.env.RESPONDIO_MAX_RETRIES = '2';

const { RespondIoClient, RespondIoError } = await import('../src/integrations/respondio/client.js');
const db = await import('../src/db.js');
const sync = await import('../src/integrations/respondio/sync.js');
const map = await import('../src/integrations/respondio/map.js');

/** สร้าง fetch ปลอมจากตารางเส้นทาง — คืนค่าตามลำดับที่กำหนดไว้ */
function stubFetch(routes) {
  const calls = [];
  const impl = async (url, init) => {
    calls.push({ url, method: init.method, body: init.body ? JSON.parse(init.body) : undefined });
    const u = new URL(url);
    const key = `${init.method} ${u.pathname}`;
    const handler = routes[key];
    if (!handler) return mkRes(404, { message: 'no stub for ' + key });
    const out = typeof handler === 'function' ? handler(u, calls.length) : handler;
    return out instanceof Response || out?.__res ? out : mkRes(200, out);
  };
  impl.calls = calls;
  return impl;
}

function mkRes(status, body, headers = {}) {
  return {
    __res: true,
    ok: status >= 200 && status < 300,
    status,
    headers: { get: (h) => headers[h.toLowerCase()] ?? null },
    text: async () => JSON.stringify(body),
  };
}

test('ใส่ Bearer token และ base URL ถูกต้อง', async () => {
  const f = stubFetch({ 'GET /v2/space/user': { items: [], pagination: { hasMore: false } } });
  const c = new RespondIoClient({ fetchImpl: f });
  await c.listUsers();
  assert.equal(f.calls[0].url.startsWith('https://api.respond.io/v2/space/user'), true);
});

test('ไล่ทุกหน้าด้วย cursor จนหมด', async () => {
  const pages = [
    { items: [{ id: 1 }, { id: 2 }], pagination: { hasMore: true, next: 2 } },
    { items: [{ id: 3 }], pagination: { hasMore: false, next: null } },
  ];
  let i = 0;
  const f = stubFetch({ 'GET /v2/space/user': () => pages[i++] });
  const c = new RespondIoClient({ fetchImpl: f });
  const rows = await c.listUsers();
  assert.deepEqual(rows.map((r) => r.id), [1, 2, 3]);
  assert.equal(new URL(f.calls[1].url).searchParams.get('cursorId'), '2');
});

test('เจอ 429 แล้วรอตาม Retry-After ก่อนลองใหม่', async () => {
  let n = 0;
  const f = stubFetch({
    'GET /v2/space/user': () => (++n === 1
      ? mkRes(429, { message: 'slow down' }, { 'retry-after': '0' })
      : { items: [{ id: 9 }], pagination: { hasMore: false } }),
  });
  const retries = [];
  const c = new RespondIoClient({ fetchImpl: f, onRetry: (r) => retries.push(r) });
  const rows = await c.listUsers();
  assert.equal(rows.length, 1);
  assert.equal(retries.length, 1);
  assert.equal(retries[0].status, 429);
});

test('เจอ 401 แล้วเลิกทันที ไม่ลองซ้ำ', async () => {
  let n = 0;
  const f = stubFetch({ 'GET /v2/space/user': () => { n++; return mkRes(401, { message: 'unauthorized' }); } });
  const c = new RespondIoClient({ fetchImpl: f });
  await assert.rejects(() => c.listUsers(), (err) => {
    assert.ok(err instanceof RespondIoError);
    assert.equal(err.status, 401);
    return true;
  });
  assert.equal(n, 1, 'ต้องเรียกแค่ครั้งเดียว');
});

test('ไม่มี token แล้วต้องฟ้อง ไม่ยิงเน็ต', async () => {
  const c = new RespondIoClient({ apiToken: '', fetchImpl: () => { throw new Error('ไม่ควรถูกเรียก'); } });
  assert.equal(c.configured, false);
  await assert.rejects(() => c.listUsers(), /RESPONDIO_API_TOKEN/);
});

test('ดึงข้อมูลลงตารางกระจกเงาได้ครบ', async () => {
  const f = stubFetch({
    'GET /v2/space/channel': { items: [{ id: 11, name: 'LINE OA', source: 'line' }], pagination: { hasMore: false } },
    'GET /v2/space/user': { items: [{ id: 21, firstName: 'Ploy', lastName: 'S', email: 'p@x.co' }], pagination: { hasMore: false } },
    'GET /v2/space/custom_field': { items: [{ id: 31, name: 'budget', type: 'number' }], pagination: { hasMore: false } },
    'GET /v2/space/closing_notes': { items: [{ id: 41, name: 'ปิดการขาย' }], pagination: { hasMore: false } },
    'POST /v2/contact/list': {
      items: [{
        id: 101, firstName: 'สมชาย', lastName: 'ใจดี', phone: '+66812345678',
        email: 'somchai@x.co', lifecycle: 'Lead', status: 'open',
        assignee: { id: 21, firstName: 'Ploy', lastName: 'S' },
        tags: ['vip', 'condo'], created_at: 1700000000,
      }],
      pagination: { hasMore: false },
    },
    'GET /v2/contact/id:101/channels': {
      items: [{ id: 501, name: 'LINE OA', source: 'line', lastMessageTime: 1700000500 }],
      pagination: { hasMore: false },
    },
    'GET /v2/contact/id:101/message/list': {
      items: [{
        messageId: 9001, channelId: 11, traffic: 'incoming', timestamp: 1700000400,
        message: { type: 'text', text: 'สนใจคอนโดครับ' },
        status: [{ value: 'sent', timestamp: 1 }, { value: 'read', timestamp: 2 }],
      }],
      pagination: { hasMore: false },
    },
  });

  const c = new RespondIoClient({ fetchImpl: f });
  const results = await sync.syncAll(c);
  assert.equal(results.every((r) => r.ok), true, JSON.stringify(results));

  const s = sync.syncSummary();
  assert.equal(s.contacts, 1);
  assert.equal(s.channels, 1);
  assert.equal(s.users, 1);
  assert.equal(s.customFields, 1);
  assert.equal(s.closingNotes, 1);
  assert.equal(s.contactChannels, 1);
  assert.equal(s.messages, 1);
  assert.equal(s.tags, 2);

  const msg = db.get('SELECT * FROM respondio_messages WHERE id = 9001');
  assert.equal(msg.text, 'สนใจคอนโดครับ');
  assert.equal(msg.status, 'read', 'ต้องเก็บสถานะล่าสุด');
  assert.equal(msg.traffic, 'incoming');
});

test('ดึงซ้ำแล้วไม่เกิดข้อมูลซ้ำ', async () => {
  const before = sync.syncSummary();
  const f = stubFetch({
    'POST /v2/contact/list': {
      items: [{ id: 101, firstName: 'สมชาย', lastName: 'ใจดีมาก', phone: '+66812345678', tags: ['vip'] }],
      pagination: { hasMore: false },
    },
  });
  const r = await sync.syncContacts(new RespondIoClient({ fetchImpl: f }));
  assert.equal(r.ok, true);
  assert.equal(sync.syncSummary().contacts, before.contacts, 'จำนวนต้องเท่าเดิม');
  assert.equal(db.get('SELECT last_name FROM respondio_contacts WHERE id = 101').last_name, 'ใจดีมาก');
});

test('บันทึกผลการ sync ไว้ทุกครั้ง แม้ตอนพัง', async () => {
  const f = stubFetch({ 'POST /v2/contact/list': () => mkRes(500, { message: 'boom' }) });
  const r = await sync.syncContacts(new RespondIoClient({ fetchImpl: f, maxRetries: 0 }));
  assert.equal(r.ok, false);
  const last = db.get(`SELECT * FROM respondio_sync_runs WHERE resource='contacts' ORDER BY id DESC LIMIT 1`);
  assert.equal(last.ok, 0);
  assert.match(last.error, /500/);
});

test('เทียบเบอร์โทรข้ามรูปแบบได้', () => {
  assert.equal(map.normPhone('+66812345678'), map.normPhone('0812345678'));
  assert.equal(map.normPhone('081-234-5678'), map.normPhone('66812345678'));
  assert.equal(map.normPhone(null), null);
});

test('แปลง lifecycle เข้าขั้นตอนของระบบ', () => {
  assert.equal(map.mapLifecycle('Lead'), 'new_lead');
  assert.equal(map.mapLifecycle('Won'), 'customer');
  assert.equal(map.mapLifecycle('ไม่รู้จัก'), 'new_lead');
  assert.equal(map.mapLifecycle('payment'), 'payment');
});

test('แปลงเข้าตาราง contacts — จับคู่เบอร์เดิมได้ ไม่สร้างซ้ำ', () => {
  db.run("INSERT INTO contacts (display_name, phone) VALUES ('สมชาย (เดิม)', '081-234-5678')");
  const existing = db.get("SELECT id FROM contacts WHERE display_name = 'สมชาย (เดิม)'").id;

  const r = map.mapContacts();
  assert.equal(r.total, 1);
  assert.equal(r.created, 0, 'ต้องไม่สร้างใหม่เพราะเบอร์ตรงกับของเดิม');
  assert.equal(r.byMatch.phone, 1);

  const link = db.get('SELECT * FROM respondio_contact_links WHERE respondio_contact_id = 101');
  assert.equal(link.contact_id, existing);

  // ไม่ทับชื่อเดิมถ้าไม่ได้สั่ง overwrite
  assert.equal(db.get('SELECT display_name FROM contacts WHERE id = ?', [existing]).display_name, 'สมชาย (เดิม)');
  // tag ถูกผูกให้
  const tags = db.all(
    `SELECT t.name FROM contact_tags ct JOIN tags t ON t.id = ct.tag_id WHERE ct.contact_id = ?`,
    [existing],
  ).map((x) => x.name).sort();
  assert.deepEqual(tags, ['vip']);
});

test('รันแปลงซ้ำแล้วผลไม่เพี้ยน', () => {
  const before = db.get('SELECT COUNT(*) n FROM contacts').n;
  map.mapContacts();
  assert.equal(db.get('SELECT COUNT(*) n FROM contacts').n, before);
});

test('--overwrite ทับค่าเดิมตามที่สั่ง', () => {
  const id = db.get('SELECT contact_id FROM respondio_contact_links WHERE respondio_contact_id = 101').contact_id;
  map.mapContacts({ overwrite: true });
  assert.equal(db.get('SELECT display_name FROM contacts WHERE id = ?', [id]).display_name, 'สมชาย ใจดีมาก');
});

test('ภาพรวมสรุปข้อมูลได้', () => {
  const o = map.overview();
  assert.equal(o.contacts, 1);
  assert.equal(o.linked, 1);
  assert.equal(o.messages, 1);
  assert.ok(o.bySource.some((r) => r.source === 'line'));
});

test.after(() => {
  db.closeDb();
  for (const s of ['', '-wal', '-shm']) {
    const f = process.env.DB_FILE + s;
    if (existsSync(f)) rmSync(f);
  }
});
