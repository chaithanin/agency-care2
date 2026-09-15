/**
 * เดโม่ครบวงจรในคำสั่งเดียว — ไม่ต้องมี LINE, ไม่ต้องเปิดเบราว์เซอร์
 *   npm run demo
 * ลำดับ: ลูกค้าทัก → บันทึก+กฎอัตโนมัติทำงาน → Agency Care ดึงข้อมูลผ่าน API
 *        → Agency Care เปลี่ยน stage → เรายิง webhook กลับไปให้ Agency Care
 */
import path from 'node:path';
import http from 'node:http';
import { rmSync, existsSync } from 'node:fs';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
process.env.DB_FILE = path.join(ROOT, 'data', 'demo.db');
process.env.PORT = process.env.DEMO_PORT || '4555';
process.env.LINE_DRY_RUN = 'true';
for (const s of ['', '-wal', '-shm']) if (existsSync(process.env.DB_FILE + s)) rmSync(process.env.DB_FILE + s);

await import('./seed.js');
const { createServer } = await import('../src/server.js');
const { createApiKey } = await import('../src/services/apiKeys.js');
const { run, all, get } = await import('../src/db.js');
const { verifySignature } = await import('../src/services/webhooks.js');

const PORT = Number(process.env.PORT);
const HOOK_PORT = PORT + 1;
const HOOK_SECRET = 'demo-agency-care-secret';
const base = `http://localhost:${PORT}`;
const line = (t) => console.log(`\n\x1b[36m${t}\x1b[0m`);

// ── ฝั่ง Agency Care (จำลอง): รับ webhook แล้วตรวจลายเซ็น ───────────────
const received = [];
const receiver = http.createServer((req, res) => {
  const chunks = [];
  req.on('data', (c) => chunks.push(c));
  req.on('end', () => {
    const raw = Buffer.concat(chunks).toString('utf8');
    const valid = verifySignature(HOOK_SECRET, req.headers['x-gtg-timestamp'], raw, req.headers['x-gtg-signature']);
    received.push({ event: req.headers['x-gtg-event'], valid, body: JSON.parse(raw) });
    res.writeHead(valid ? 200 : 401).end();
  });
});
await new Promise((r) => receiver.listen(HOOK_PORT, r));

run('INSERT INTO webhooks_out (name, url, secret, events) VALUES (?, ?, ?, ?)',
  ['Agency Care (demo)', `http://localhost:${HOOK_PORT}/hooks/gtg-chat`, HOOK_SECRET, 'contact.lifecycle_changed']);

const server = createServer();
await new Promise((r) => server.listen(PORT, r));
const apiKey = createApiKey('Demo Agency Care', 'read,write');

const api = async (method, url, body, headers = {}) => {
  const res = await fetch(base + url, {
    method,
    headers: { 'content-type': 'application/json', 'x-api-key': apiKey, ...headers },
    body: body ? JSON.stringify(body) : undefined,
  });
  return { status: res.status, json: await res.json().catch(() => null) };
};
const inbound = (userId, displayName, text, messageId) =>
  fetch(`${base}/webhook/mock`, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify({ userId, displayName, text, messageId }),
  }).then((r) => r.json());

// ── 1) ลูกค้าทักเข้ามา 3 คน ────────────────────────────────────────────
line('1) ลูกค้าทักเข้ามาทางช่องทางแชท');
const inbox1 = await inbound('U-somchai', 'คุณสมชาย', 'สวัสดีครับ สนใจพูลวิลล่า ราคาเท่าไหร่ครับ', 'm-1');
const inbox2 = await inbound('U-anna', 'Anna', 'Hello, I want to invest in a condo near the beach', 'm-2');
await inbound('U-ivan', 'Иван', 'Здравствуйте, интересует вилла', 'm-3');
console.log('  สมชาย  →', JSON.stringify(inbox1.handled[0].automations));
console.log('  Anna   →', JSON.stringify(inbox2.handled[0].automations));

line('2) ยิงข้อความเดิมซ้ำ (LINE retry) — ต้องไม่บันทึกซ้ำ');
const dup = await inbound('U-somchai', 'คุณสมชาย', 'สวัสดีครับ สนใจพูลวิลล่า ราคาเท่าไหร่ครับ', 'm-1');
console.log('  duplicate =', dup.handled[0].duplicate);

// ── 2) Agency Care ดึงข้อมูล ───────────────────────────────────────────
line('3) Agency Care เรียก GET /api/v1/contacts');
const contacts = await api('GET', '/api/v1/contacts');
for (const c of contacts.json.data) {
  console.log(`  #${c.id} ${c.displayName.padEnd(12)} stage=${c.lifecycleStage.padEnd(9)} lang=${c.language} tags=[${c.tags.join(',')}]`);
}

line('4) ไม่ส่ง API key → ต้องโดนปฏิเสธ');
const noKey = await fetch(`${base}/api/v1/contacts`).then(async (r) => ({ status: r.status, json: await r.json() }));
console.log(' ', noKey.status, noKey.json.error.message);

// ── 3) เปลี่ยน stage ผ่าน API แล้วดู webhook เด้งกลับ ───────────────────
const somchai = contacts.json.data.find((c) => c.displayName === 'คุณสมชาย');
line(`5) Agency Care เปลี่ยน stage ของ #${somchai.id} เป็น hot_lead`);
const changed = await api('POST', `/api/v1/contacts/${somchai.id}/lifecycle`, { stage: 'hot_lead' });
console.log(' ', changed.status, JSON.stringify(changed.json.data));

await new Promise((r) => setTimeout(r, 200));
line('6) webhook ที่ Agency Care ได้รับกลับไป');
console.log(' ', JSON.stringify(received[0] && { event: received[0].event, ลายเซ็นถูกต้อง: received[0].valid, data: received[0].body.data }, null, 2));

line('7) กรอง hot_lead อย่างเดียว (GET /api/v1/contacts?stage=hot_lead)');
const hot = await api('GET', '/api/v1/contacts?stage=hot_lead');
console.log(' ', hot.json.data.map((c) => `#${c.id} ${c.displayName}`).join(', ') || '(ไม่มี)');

line('8) Agency Care ส่งข้อความหาลูกค้าผ่าน API');
const conv = (await api('GET', `/api/v1/conversations?contact_id=${somchai.id}`)).json.data[0];
const sent = await api('POST', `/api/v1/conversations/${conv.id}/messages`, { text: 'ทีมงาน Agency Care นัดหมายเข้าชมโครงการวันเสาร์ 10:00 น. ครับ' });
console.log(' ', sent.status, JSON.stringify(sent.json.data));

line('9) Dashboard (GET /api/v1/stats/dashboard)');
const stats = (await api('GET', '/api/v1/stats/dashboard')).json.data;
console.log('  conversations:', JSON.stringify(stats.conversations));
console.log('  lifecycle:    ', JSON.stringify(stats.lifecycle));
console.log('  messages:     ', JSON.stringify(stats.messages));
console.log('  ภาระงานเซลส์:  ', stats.workload.map((w) => `${w.name}=${w.openConversations}`).join(', '));

line('สรุปสิ่งที่บันทึกลงฐานข้อมูล');
console.log('  contacts     ', get('SELECT COUNT(*) AS n FROM contacts').n);
console.log('  conversations', get('SELECT COUNT(*) AS n FROM conversations').n);
console.log('  messages     ', get('SELECT COUNT(*) AS n FROM messages').n);
console.log('  automation_runs ที่ทำงานจริง:',
  all("SELECT result FROM automation_runs WHERE result NOT IN ('skipped','no_keyword')").map((r) => r.result).join(', '));
console.log(`\nเดโม่จบ — เปิด UI ด้วย: npm start แล้วไปที่ http://localhost:4000/\n`);

server.close();
receiver.close();
