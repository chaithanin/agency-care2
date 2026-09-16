import { readFileSync, existsSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

export const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');

// อ่าน .env แบบง่าย ๆ (ไม่พึ่ง dependency) — ค่าใน environment จริงชนะไฟล์เสมอ
function loadEnvFile(file) {
  if (!existsSync(file)) return;
  for (const raw of readFileSync(file, 'utf8').split('\n')) {
    const line = raw.trim();
    if (!line || line.startsWith('#')) continue;
    const eq = line.indexOf('=');
    if (eq === -1) continue;
    const key = line.slice(0, eq).trim();
    let value = line.slice(eq + 1).trim();
    if ((value.startsWith('"') && value.endsWith('"')) || (value.startsWith("'") && value.endsWith("'"))) {
      value = value.slice(1, -1);
    }
    if (process.env[key] === undefined) process.env[key] = value;
  }
}
loadEnvFile(path.join(ROOT, '.env'));

export const config = {
  port: Number(process.env.PORT || 4000),
  dbFile: process.env.DB_FILE || path.join(ROOT, 'data', 'chat-inbox.db'),
  line: {
    channelSecret: process.env.LINE_CHANNEL_SECRET || '',
    accessToken: process.env.LINE_CHANNEL_ACCESS_TOKEN || '',
    apiBase: process.env.LINE_API_BASE || 'https://api.line.me',
    // dryRun = ไม่ยิงออก LINE จริง ใช้ตอนทดสอบในเครื่อง
    dryRun: (process.env.LINE_DRY_RUN || 'true') === 'true',
  },
  respondio: {
    // token สร้างที่ respond.io → Settings → Integrations → Developer API → Add Access Token
    // ห้าม commit ค่านี้ ใส่ใน .env หรือ environment เท่านั้น
    apiToken: process.env.RESPONDIO_API_TOKEN || '',
    apiBase: process.env.RESPONDIO_API_BASE || 'https://api.respond.io/v2',
    timeoutMs: Number(process.env.RESPONDIO_TIMEOUT_MS || 20000),
    maxRetries: Number(process.env.RESPONDIO_MAX_RETRIES || 4),
    // จำนวนแถวต่อหนึ่งหน้า — respond.io จำกัดไว้ที่ 100
    pageSize: Number(process.env.RESPONDIO_PAGE_SIZE || 100),
    // timezone ที่ใช้กับ POST /contact/list
    timezone: process.env.RESPONDIO_TIMEZONE || 'Asia/Bangkok',
    // ดึงข้อความย้อนหลังกี่ข้อความต่อ contact ตอน sync
    messagesPerContact: Number(process.env.RESPONDIO_MESSAGES_PER_CONTACT || 50),
  },
  // ผู้ใช้ปลอมสำหรับ prototype — ของจริงต้องต่อ Auth.js ตาม roadmap สัปดาห์ 4-6
  devUserHeader: 'x-dev-user',
  webhookTimeoutMs: Number(process.env.WEBHOOK_TIMEOUT_MS || 5000),
};

export const LIFECYCLE_STAGES = ['new_lead', 'hot_lead', 'payment', 'customer', 'lost'];
