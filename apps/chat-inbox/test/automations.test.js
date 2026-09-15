import test from 'node:test';
import assert from 'node:assert/strict';
import { freshApp, req } from './helpers.js';

const app = await freshApp();
test.after(() => app.close());

const { detectLanguage, runAutomations } = app.automations;
const mock = app.inbox.getChannel('mock');

app.db.run("INSERT INTO automation_rules (name, trigger, action, config_json, sort_order) VALUES ('greet','conversation.created','send_greeting','{}',10)");
app.db.run("INSERT INTO automation_rules (name, trigger, action, config_json, sort_order) VALUES ('assign','conversation.created','assign_round_robin','{}',20)");
app.db.run("INSERT INTO automation_rules (name, trigger, action, config_json, sort_order) VALUES ('tag','message.received','add_tag_by_keyword',?,30)",
  [JSON.stringify({ keywords: { villa: 'villa', คอนโด: 'condo', ลงทุน: 'investment' } })]);

const incoming = async (userId, text, messageId, displayName) => {
  const r = app.inbox.ingestIncoming(mock, { externalUserId: userId, externalMessageId: messageId, text, profile: { displayName } });
  const fired = await runAutomations({
    conversationId: r.conversationId, contactId: r.contactId, text, conversationCreated: r.conversationCreated,
  });
  return { ...r, fired };
};

test('เดาภาษาจากตัวอักษรได้', () => {
  assert.equal(detectLanguage('สวัสดีครับ'), 'th');
  assert.equal(detectLanguage('Hello there'), 'en');
  assert.equal(detectLanguage('Здравствуйте'), 'ru');
});

test('ข้อความแรกได้รับการทักทายในภาษาเดียวกัน', async () => {
  const r = await incoming('U-th', 'สวัสดีครับ สนใจคอนโด', 'a1', 'สมชาย');
  assert.ok(r.fired.some((f) => f.result === 'greeted:th'), JSON.stringify(r.fired));
  const reply = app.db.get("SELECT * FROM messages WHERE conversation_id = ? AND direction = 'out'", [r.conversationId]);
  assert.equal(reply.source, 'automation');
  assert.match(reply.text, /GTG/);
  assert.equal(app.db.get('SELECT language FROM contacts WHERE id = ?', [r.contactId]).language, 'th');
});

test('มอบหมายอัตโนมัติ ไม่มีเคสค้างแบบ unassigned', async () => {
  const r = await incoming('U-en', 'I want a villa', 'a2', 'Anna');
  const conv = app.db.get('SELECT * FROM conversations WHERE id = ?', [r.conversationId]);
  assert.ok(conv.assignee_user_id, 'ต้องถูกมอบหมายให้เซลส์คนใดคนหนึ่ง');
  assert.ok(r.fired.some((f) => f.result.startsWith('assigned:')));
});

test('กระจายงานวนรอบ — เซลส์คนที่ว่างกว่าได้เคสถัดไป', async () => {
  await incoming('U-3', 'hello', 'a3');
  await incoming('U-4', 'hello', 'a4');
  const loads = app.db.all(
    `SELECT u.name, COUNT(c.id) AS n FROM users u
       LEFT JOIN conversations c ON c.assignee_user_id = u.id AND c.status = 'open'
      WHERE u.role = 'agent' GROUP BY u.id`,
  );
  const counts = loads.map((r) => r.n);
  assert.ok(Math.max(...counts) - Math.min(...counts) <= 1, `งานต้องกระจายใกล้เคียงกัน: ${JSON.stringify(loads)}`);
});

test('แท็กจากคีย์เวิร์ดทั้งไทยและอังกฤษ', async () => {
  const r = await incoming('U-tag', 'สนใจคอนโดเพื่อลงทุน และ villa ด้วย', 'a5');
  const tags = app.inbox.contactTags(r.contactId);
  assert.deepEqual(tags.sort(), ['condo', 'investment', 'villa']);
});

test('ทุกครั้งที่กฎทำงานมีบันทึกไว้ debug ได้', () => {
  const runs = app.db.all('SELECT * FROM automation_runs ORDER BY id');
  assert.ok(runs.length >= 5);
  assert.ok(runs.every((r) => typeof r.result === 'string' && r.result.length));
});

test('ข้อความที่สองไม่ทักทายซ้ำ (กฎผูกกับ conversation.created)', async () => {
  const before = app.db.get("SELECT COUNT(*) AS n FROM messages WHERE source = 'automation'").n;
  await incoming('U-th', 'แล้วมีโปรโมชันไหมครับ', 'a6');
  const after = app.db.get("SELECT COUNT(*) AS n FROM messages WHERE source = 'automation'").n;
  assert.equal(after, before);
});

test('ตอบจากหน้า Inbox ต้องระบุผู้ใช้ และบันทึกเป็นข้อความขาออก', async () => {
  const conv = app.db.get('SELECT id FROM conversations ORDER BY id LIMIT 1');
  const noUser = await req(app.base, 'POST', `/internal/conversations/${conv.id}/reply`, { body: { text: 'สวัสดีครับ' } });
  assert.equal(noUser.status, 400);

  const agent = app.db.get("SELECT id FROM users WHERE role = 'agent' ORDER BY id LIMIT 1");
  const ok = await req(app.base, 'POST', `/internal/conversations/${conv.id}/reply`, {
    body: { text: 'โครงการอยู่ติดหาดครับ' }, headers: { 'x-dev-user': String(agent.id) },
  });
  assert.equal(ok.status, 201);
  const msg = app.db.get("SELECT * FROM messages WHERE conversation_id = ? AND source = 'human' ORDER BY id DESC LIMIT 1", [conv.id]);
  assert.equal(msg.sender_user_id, agent.id);
  assert.ok(app.db.get('SELECT first_reply_at FROM conversations WHERE id = ?', [conv.id]).first_reply_at);
});

test('ปิดเคสแล้วข้อความใหม่เปิดบทสนทนาใหม่ ไม่ต่อของเก่า', async () => {
  const r = await incoming('U-close', 'ทดสอบปิดเคส', 'a7');
  app.inbox.setConversationStatus(r.conversationId, 'closed');
  const again = await incoming('U-close', 'กลับมาถามอีกรอบ', 'a8');
  assert.notEqual(again.conversationId, r.conversationId);
  assert.equal(again.contactId, r.contactId, 'ต้องเป็นลูกค้าคนเดิม');
});
