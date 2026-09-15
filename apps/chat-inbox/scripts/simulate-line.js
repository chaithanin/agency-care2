/**
 * จำลอง LINE ยิง webhook เข้ามา (เซ็นลายเซ็นให้ถูกต้องด้วย LINE_CHANNEL_SECRET)
 * ใช้: npm run simulate -- --user U123 --name "คุณสมชาย" --text "สนใจพูลวิลล่าครับ ราคาเท่าไหร่"
 */
import crypto from 'node:crypto';
import { config } from '../src/config.js';

const args = process.argv.slice(2);
const arg = (name, def) => {
  const i = args.indexOf(`--${name}`);
  return i !== -1 && args[i + 1] ? args[i + 1] : def;
};

const userId = arg('user', 'U-demo-0001');
const text = arg('text', 'สวัสดีครับ สนใจคอนโดวิวทะเล ราคาเท่าไหร่ครับ');
const port = arg('port', String(config.port));
const secret = config.line.channelSecret;

const body = JSON.stringify({
  destination: 'gtg-line-oa',
  events: [{
    type: 'message',
    replyToken: `rt-${crypto.randomBytes(6).toString('hex')}`,
    source: { type: 'user', userId },
    timestamp: Date.now(),
    message: { type: 'text', id: `m-${crypto.randomBytes(6).toString('hex')}`, text },
  }],
});

if (!secret) {
  console.error('ยังไม่ได้ตั้ง LINE_CHANNEL_SECRET ใน .env — จะส่งเข้าช่องทาง mock แทน');
}

const target = secret ? 'line' : 'mock';
const headers = { 'content-type': 'application/json' };
let payload = body;

if (secret) {
  headers['x-line-signature'] = crypto.createHmac('sha256', secret).update(body).digest('base64');
} else {
  payload = JSON.stringify({ userId, displayName: arg('name', 'ลูกค้าทดสอบ'), text });
}

const res = await fetch(`http://localhost:${port}/webhook/${target}`, { method: 'POST', headers, body: payload });
console.log(res.status, JSON.stringify(await res.json(), null, 2));
