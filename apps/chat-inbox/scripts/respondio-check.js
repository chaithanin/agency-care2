#!/usr/bin/env node
/**
 * ตรวจว่า token ใช้ได้จริงและมองเห็นอะไรบ้าง — ไม่เขียนฐานข้อมูล
 *   npm run respondio:check
 */
import { createClient, RespondIoError } from '../src/integrations/respondio/client.js';

const client = createClient({
  onRetry: ({ attempt, delay, status }) =>
    console.log(`  ลองใหม่ครั้งที่ ${attempt + 1} (${status ?? 'network'}) รอ ${delay}ms`),
});

if (!client.configured) {
  console.error('ยังไม่ได้ตั้ง RESPONDIO_API_TOKEN');
  console.error('สร้าง token ที่ respond.io → Settings → Integrations → Developer API → Add Access Token');
  console.error('แล้วใส่ใน apps/chat-inbox/.env  →  RESPONDIO_API_TOKEN=xxxxx');
  process.exit(1);
}

console.log(`base URL: ${client.apiBase}`);

const checks = [
  ['channel ใน workspace', () => client.listChannels()],
  ['ผู้ใช้', () => client.listUsers()],
  ['custom field', () => client.listCustomFields()],
  ['closing note', () => client.listClosingNotes()],
  ['contact (ดู 5 คนแรก)', () => client.listContacts({ max: 5 })],
];

let failed = 0;
for (const [label, fn] of checks) {
  try {
    const rows = await fn();
    console.log(`  ${String(rows.length).padStart(4)}  ${label}`);
  } catch (err) {
    failed++;
    const extra = err instanceof RespondIoError && err.status ? ` (HTTP ${err.status})` : '';
    console.log(`     ✗  ${label}${extra} — ${err.message}`);
  }
}

if (failed) {
  console.error(`\nมี ${failed} รายการที่เรียกไม่สำเร็จ`);
  console.error('401 = token ผิดหรือหมดอายุ · 403 = แผนไม่รองรับ (ต้อง Growth ขึ้นไป) หรือ token ไม่มีสิทธิ์');
  process.exit(1);
}
console.log('\nเชื่อมต่อได้ครบทุกรายการ');
