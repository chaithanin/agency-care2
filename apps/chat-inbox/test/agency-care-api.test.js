import test from 'node:test';
import assert from 'node:assert/strict';
import { freshApp, req, webhookSink } from './helpers.js';

const app = await freshApp();
const sink = await webhookSink();
test.after(async () => { await sink.close(); await app.close(); });

const { verifySignature } = await import('../src/services/webhooks.js');

const readKey = app.apiKeys.createApiKey('Agency Care (read)', 'read');
const writeKey = app.apiKeys.createApiKey('Agency Care (rw)', 'read,write');
const auth = (key) => ({ 'x-api-key': key });

const mock = app.inbox.getChannel('mock');
app.inbox.ingestIncoming(mock, { externalUserId: 'U-a', externalMessageId: 'x1', text: 'สนใจคอนโด', profile: { displayName: 'สมชาย' } });
app.inbox.ingestIncoming(mock, { externalUserId: 'U-b', externalMessageId: 'x2', text: 'villa please', profile: { displayName: 'Anna' } });

test('ไม่ส่ง API key → 401', async () => {
  const res = await req(app.base, 'GET', '/api/v1/contacts');
  assert.equal(res.status, 401);
  assert.equal(res.json.error.code, 'unauthorized');
});

test('API key ปลอม → 401 (header ต้องเป็น ASCII เท่านั้น)', async () => {
  const res = await req(app.base, 'GET', '/api/v1/contacts', { headers: auth('gtg_not_a_real_key_0000') });
  assert.equal(res.status, 401);
});

test('health เรียกได้โดยไม่ต้องมีคีย์', async () => {
  const res = await req(app.base, 'GET', '/api/v1/health');
  assert.equal(res.status, 200);
  assert.equal(res.json.ok, true);
});

test('GET /contacts คืนรายชื่อพร้อมแท็กและ pagination', async () => {
  const res = await req(app.base, 'GET', '/api/v1/contacts', { headers: auth(readKey) });
  assert.equal(res.status, 200);
  assert.equal(res.json.data.length, 2);
  assert.equal(res.json.pagination.total, 2);
  assert.equal(res.json.pagination.hasMore, false);
  assert.ok(Array.isArray(res.json.data[0].tags));
  assert.ok(res.headers.get('x-ratelimit-remaining'));
});

test('คีย์สิทธิ์ read เขียนไม่ได้', async () => {
  const contactId = app.db.get('SELECT id FROM contacts ORDER BY id LIMIT 1').id;
  const res = await req(app.base, 'POST', `/api/v1/contacts/${contactId}/lifecycle`, {
    headers: auth(readKey), body: { stage: 'hot_lead' },
  });
  assert.equal(res.status, 401);
});

test('stage ที่ไม่มีอยู่จริง → 400 ไม่ใช่ 500', async () => {
  const res = await req(app.base, 'GET', '/api/v1/contacts?stage=vip', { headers: auth(readKey) });
  assert.equal(res.status, 400);
});

test('ค่าที่ผู้เรียกส่งมาถูกใส่เป็น parameter — ยิง SQL injection ไม่ทะลุ', async () => {
  const res = await req(app.base, 'GET', "/api/v1/contacts?q=' OR 1=1; DROP TABLE contacts;--", { headers: auth(readKey) });
  assert.equal(res.status, 200);
  assert.equal(res.json.data.length, 0);
  assert.equal(app.db.get('SELECT COUNT(*) AS n FROM contacts').n, 2, 'ตาราง contacts ต้องยังอยู่');
});

test('เปลี่ยน stage ผ่าน API แล้วยิง webhook ที่ลายเซ็นตรวจสอบได้ไปหา Agency Care', async () => {
  app.db.run('INSERT INTO webhooks_out (name, url, secret, events) VALUES (?, ?, ?, ?)',
    ['Agency Care', sink.url, 'hook-secret', 'contact.lifecycle_changed']);

  const contactId = app.db.get("SELECT id FROM contacts WHERE display_name = 'สมชาย'").id;
  const res = await req(app.base, 'POST', `/api/v1/contacts/${contactId}/lifecycle`, {
    headers: auth(writeKey), body: { stage: 'hot_lead' },
  });
  assert.equal(res.status, 200);
  assert.equal(res.json.data.lifecycleStage, 'hot_lead');

  assert.equal(sink.requests.length, 1, 'ต้องมี webhook ออกไป 1 ครั้ง');
  const hit = sink.requests[0];
  assert.equal(hit.headers['x-gtg-event'], 'contact.lifecycle_changed');
  assert.ok(verifySignature('hook-secret', hit.headers['x-gtg-timestamp'], hit.raw, hit.headers['x-gtg-signature']),
    'ลายเซ็นต้องตรวจผ่านด้วย secret ที่ถูกต้อง');
  assert.equal(verifySignature('secret-ผิด', hit.headers['x-gtg-timestamp'], hit.raw, hit.headers['x-gtg-signature']), false);

  const payload = JSON.parse(hit.raw);
  assert.equal(payload.data.fromStage, 'new_lead');
  assert.equal(payload.data.toStage, 'hot_lead');
  assert.match(payload.data.changedBy, /agency-care/);

  const delivery = app.db.get('SELECT * FROM webhook_deliveries ORDER BY id DESC LIMIT 1');
  assert.equal(delivery.status, 'ok');
  assert.equal(delivery.response_code, 200);
});

test('กรองด้วย stage และ tag ได้', async () => {
  const hot = await req(app.base, 'GET', '/api/v1/contacts?stage=hot_lead', { headers: auth(readKey) });
  assert.equal(hot.json.data.length, 1);
  assert.equal(hot.json.data[0].displayName, 'สมชาย');

  const anna = app.db.get("SELECT id FROM contacts WHERE display_name = 'Anna'").id;
  app.inbox.addTag(anna, 'villa');
  const tagged = await req(app.base, 'GET', '/api/v1/contacts?tag=villa', { headers: auth(readKey) });
  assert.equal(tagged.json.data.length, 1);
  assert.equal(tagged.json.data[0].displayName, 'Anna');
});

test('ดูรายละเอียดผู้ติดต่อพร้อมประวัติ stage และช่องทาง', async () => {
  const id = app.db.get("SELECT id FROM contacts WHERE display_name = 'สมชาย'").id;
  const res = await req(app.base, 'GET', `/api/v1/contacts/${id}`, { headers: auth(readKey) });
  assert.equal(res.status, 200);
  assert.equal(res.json.data.lifecycleHistory[0].toStage, 'hot_lead');
  assert.equal(res.json.data.channels[0].provider, 'mock');
  assert.ok(res.json.data.customFields.some((f) => f.key === 'budget'));
});

test('ผู้ติดต่อที่ไม่มีอยู่ → 404', async () => {
  const res = await req(app.base, 'GET', '/api/v1/contacts/99999', { headers: auth(readKey) });
  assert.equal(res.status, 404);
});

test('อ่านและส่งข้อความในบทสนทนาผ่าน API ได้', async () => {
  const conv = app.db.get('SELECT id FROM conversations ORDER BY id LIMIT 1');
  const sent = await req(app.base, 'POST', `/api/v1/conversations/${conv.id}/messages`, {
    headers: auth(writeKey), body: { text: 'นัดชมโครงการวันเสาร์ 10:00 น.' },
  });
  assert.equal(sent.status, 201);

  const msgs = await req(app.base, 'GET', `/api/v1/conversations/${conv.id}/messages`, { headers: auth(readKey) });
  assert.equal(msgs.status, 200);
  const last = msgs.json.data.at(-1);
  assert.equal(last.direction, 'out');
  assert.equal(last.source, 'api');
});

test('dashboard รวมตัวเลขให้ Agency Care', async () => {
  const res = await req(app.base, 'GET', '/api/v1/stats/dashboard', { headers: auth(readKey) });
  assert.equal(res.status, 200);
  const d = res.json.data;
  assert.equal(d.contactsTotal, 2);
  assert.equal(d.lifecycle.hot_lead, 1);
  assert.equal(d.lifecycle.new_lead, 1);
  assert.equal(d.conversations.open, 2);
  assert.ok(d.messages.inbound >= 2);
  assert.ok(Array.isArray(d.workload));
});
