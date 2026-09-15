import test from 'node:test';
import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import { freshApp, req } from './helpers.js';

const SECRET = 'line-secret-for-test';
const app = await freshApp({ lineSecret: SECRET });
test.after(() => app.close());

const lineBody = (userId, text, messageId) => JSON.stringify({
  events: [{
    type: 'message', replyToken: 'rt-1', source: { type: 'user', userId },
    message: { type: 'text', id: messageId, text },
  }],
});
const sign = (body) => crypto.createHmac('sha256', SECRET).update(body).digest('base64');

test('ปฏิเสธ webhook ที่ไม่มีลายเซ็น', async () => {
  const body = lineBody('U1', 'hi', 'm1');
  const res = await req(app.base, 'POST', '/webhook/line', { body: JSON.parse(body) });
  assert.equal(res.status, 401);
  assert.equal(res.json.error.code, 'invalid_signature');
});

test('ปฏิเสธ webhook ที่ลายเซ็นผิด', async () => {
  const body = lineBody('U1', 'hi', 'm1');
  const res = await fetch(`${app.base}/webhook/line`, {
    method: 'POST',
    headers: { 'content-type': 'application/json', 'x-line-signature': sign('ของปลอม') },
    body,
  });
  assert.equal(res.status, 401);
});

test('รับข้อความ LINE ที่ลายเซ็นถูกต้อง แล้วสร้าง contact/conversation/message', async () => {
  const body = lineBody('U-somchai', 'สนใจพูลวิลล่าครับ ราคาเท่าไหร่', 'm-100');
  const res = await fetch(`${app.base}/webhook/line`, {
    method: 'POST',
    headers: { 'content-type': 'application/json', 'x-line-signature': sign(body) },
    body,
  });
  assert.equal(res.status, 200);
  const json = await res.json();
  assert.equal(json.received, 1);

  const contact = app.db.get("SELECT * FROM contacts WHERE display_name LIKE 'LINE%'");
  assert.ok(contact, 'ต้องมี contact ใหม่');
  assert.equal(contact.lifecycle_stage, 'new_lead');
  assert.equal(app.db.get('SELECT COUNT(*) AS n FROM conversations').n, 1);
  assert.equal(app.db.get("SELECT COUNT(*) AS n FROM messages WHERE direction = 'in'").n, 1);
});

test('LINE ยิงซ้ำ (retry) ไม่บันทึกข้อความซ้ำ', async () => {
  const body = lineBody('U-somchai', 'สนใจพูลวิลล่าครับ ราคาเท่าไหร่', 'm-100');
  const res = await fetch(`${app.base}/webhook/line`, {
    method: 'POST',
    headers: { 'content-type': 'application/json', 'x-line-signature': sign(body) },
    body,
  });
  const json = await res.json();
  assert.equal(json.handled[0].duplicate, true);
  assert.equal(app.db.get("SELECT COUNT(*) AS n FROM messages WHERE external_message_id = 'm-100'").n, 1);
});

test('ข้อความจากคนเดิมไปลงบทสนทนาเดิมที่ยังเปิดอยู่', async () => {
  const body = lineBody('U-somchai', 'อยู่ตรงไหนครับ', 'm-101');
  await fetch(`${app.base}/webhook/line`, {
    method: 'POST', headers: { 'content-type': 'application/json', 'x-line-signature': sign(body) }, body,
  });
  assert.equal(app.db.get('SELECT COUNT(*) AS n FROM conversations').n, 1);
  assert.equal(app.db.get('SELECT COUNT(*) AS n FROM contacts').n, 1);
});

test('ช่องทางที่ยังไม่ได้ตั้งค่า ตอบ 404', async () => {
  const res = await req(app.base, 'POST', '/webhook/facebook', { body: {} });
  assert.equal(res.status, 404);
});

test('ไฟล์ static ออกนอก public/ ไม่ได้', async () => {
  const res = await fetch(`${app.base}/../src/config.js`);
  assert.ok([400, 404].includes(res.status), `ต้องไม่ยอมให้อ่านไฟล์นอก public (ได้ ${res.status})`);
});
