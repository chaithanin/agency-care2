/**
 * ใส่ข้อมูลตั้งต้นสำหรับทดสอบ: ผู้ใช้, ช่องทาง, custom fields, กฎอัตโนมัติ, API key
 * รัน:  npm run seed          (เพิ่มทับของเดิมแบบปลอดภัย)
 *       npm run reset         (ลบไฟล์ฐานข้อมูลแล้วสร้างใหม่)
 */
import { existsSync, rmSync } from 'node:fs';
import { config } from '../src/config.js';

if (process.argv.includes('--reset')) {
  for (const suffix of ['', '-wal', '-shm']) {
    const f = config.dbFile + suffix;
    if (existsSync(f)) rmSync(f);
  }
  console.log('ลบฐานข้อมูลเดิมแล้ว:', config.dbFile);
}

const { run, get, all } = await import('../src/db.js');
const { createApiKey } = await import('../src/services/apiKeys.js');

const upsert = (sql, params) => run(sql, params);

// ผู้ใช้
upsert("INSERT OR IGNORE INTO users (email, name, role) VALUES (?, ?, 'admin')", ['admin@gtg.local', 'Admin GTG']);
upsert("INSERT OR IGNORE INTO users (email, name, role) VALUES (?, ?, 'agent')", ['ploy@gtg.local', 'Ploy (Sales)']);
upsert("INSERT OR IGNORE INTO users (email, name, role) VALUES (?, ?, 'agent')", ['ivan@gtg.local', 'Ivan (Sales RU)']);

// ช่องทาง
upsert(
  "INSERT OR IGNORE INTO channels (provider, name, external_id, config_json) VALUES ('line', ?, ?, ?)",
  ['GTG LINE OA', 'gtg-line-oa', JSON.stringify({ channelSecret: config.line.channelSecret || '', accessToken: config.line.accessToken || '' })],
);
upsert("INSERT OR IGNORE INTO channels (provider, name, external_id) VALUES ('mock', ?, ?)", ['ช่องทางทดสอบ', 'mock-1']);

// custom fields ที่เซลส์ GTG ใช้จริง
const fields = [
  ['project_interest', 'โครงการที่สนใจ', 'select', JSON.stringify(['Marina Golden Bay', 'The Panora', 'Copacabana', 'อื่น ๆ'])],
  ['budget', 'งบประมาณ (บาท)', 'number', '[]'],
  ['nationality', 'สัญชาติ', 'text', '[]'],
  ['purpose', 'วัตถุประสงค์', 'select', JSON.stringify(['อยู่เอง', 'ลงทุน/ปล่อยเช่า', 'ยังไม่แน่ใจ'])],
];
for (const [key, label, type, options] of fields) {
  upsert('INSERT OR IGNORE INTO custom_field_defs (key, label, type, options_json) VALUES (?, ?, ?, ?)', [key, label, type, options]);
}

// กฎอัตโนมัติ — แก้ปัญหา Unassigned ค้างที่เห็นใน dashboard ปัจจุบัน
const rules = [
  ['ทักทายข้อความแรกตามภาษา', 'conversation.created', 'send_greeting', '{}', 10],
  ['มอบหมายเซลส์แบบวนรอบ', 'conversation.created', 'assign_round_robin', '{}', 20],
  ['แท็กจากคีย์เวิร์ด', 'message.received', 'add_tag_by_keyword', JSON.stringify({
    keywords: {
      villa: 'villa', พูลวิลล่า: 'villa', คอนโด: 'condo', condo: 'condo',
      ลงทุน: 'investment', invest: 'investment', เช่า: 'rental', rent: 'rental',
      ราคา: 'pricing', price: 'pricing',
    },
  }), 30],
];
for (const [name, trigger, action, cfg, order] of rules) {
  if (!get('SELECT id FROM automation_rules WHERE name = ?', [name])) {
    run('INSERT INTO automation_rules (name, trigger, action, config_json, sort_order) VALUES (?, ?, ?, ?, ?)',
      [name, trigger, action, cfg, order]);
  }
}

// API key สำหรับ Agency Care (แสดงครั้งเดียว — ใน DB เก็บแค่ hash)
let issuedKey = null;
if (!get("SELECT id FROM api_keys WHERE name = 'Agency Care'")) {
  issuedKey = createApiKey('Agency Care', 'read,write');
}

console.log('\nseed เรียบร้อย');
console.log('ผู้ใช้:', all('SELECT id, name, role FROM users').map((u) => `${u.id}:${u.name}(${u.role})`).join(', '));
console.log('ช่องทาง:', all('SELECT provider, name FROM channels').map((c) => `${c.provider}`).join(', '));
console.log('กฎอัตโนมัติ:', all('SELECT COUNT(*) AS n FROM automation_rules')[0].n, 'ข้อ');
if (issuedKey) {
  console.log('\n  API KEY ของ Agency Care (เก็บไว้เลย จะไม่แสดงอีก):');
  console.log(`  ${issuedKey}\n`);
  console.log(`  ทดสอบ: curl -H "X-API-Key: ${issuedKey}" http://localhost:${config.port}/api/v1/contacts\n`);
} else {
  console.log('\n  มี API key ของ Agency Care อยู่แล้ว — ถ้าทำหาย ให้ npm run reset เพื่อออกใบใหม่\n');
}
