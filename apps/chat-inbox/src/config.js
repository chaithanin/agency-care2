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
  // ผู้ใช้ปลอมสำหรับ prototype — ของจริงต้องต่อ Auth.js ตาม roadmap สัปดาห์ 4-6
  devUserHeader: 'x-dev-user',
  webhookTimeoutMs: Number(process.env.WEBHOOK_TIMEOUT_MS || 5000),
};

export const LIFECYCLE_STAGES = ['new_lead', 'hot_lead', 'payment', 'customer', 'lost'];
