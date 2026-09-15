/**
 * ตัวรับ webhook ฝั่ง Agency Care (จำลอง) — ตรวจลายเซ็นก่อนเชื่อทุกครั้ง
 * ใช้: npm run receiver            (ฟังที่ port 4100)
 * แล้วลงทะเบียน endpoint นี้ในตาราง webhooks_out (scripts/demo.js ทำให้อัตโนมัติ)
 */
import http from 'node:http';
import { verifySignature } from '../src/services/webhooks.js';

const PORT = Number(process.env.RECEIVER_PORT || 4100);
const SECRET = process.env.RECEIVER_SECRET || 'agency-care-dev-secret';

http.createServer((req, res) => {
  const chunks = [];
  req.on('data', (c) => chunks.push(c));
  req.on('end', () => {
    const raw = Buffer.concat(chunks).toString('utf8');
    const ts = req.headers['x-gtg-timestamp'];
    const ok = verifySignature(SECRET, ts, raw, req.headers['x-gtg-signature']);
    const fresh = Math.abs(Date.now() - Number(ts)) < 5 * 60 * 1000;

    if (!ok || !fresh) {
      console.log('ปฏิเสธ: ', !ok ? 'ลายเซ็นไม่ถูกต้อง' : 'timestamp เก่าเกินไป (กัน replay)');
      res.writeHead(401).end('invalid signature');
      return;
    }
    console.log('[Agency Care] ได้รับ event:', req.headers['x-gtg-event']);
    console.log(JSON.stringify(JSON.parse(raw).data, null, 2));
    res.writeHead(200, { 'content-type': 'application/json' }).end('{"ok":true}');
  });
}).listen(PORT, () => console.log(`Agency Care receiver (จำลอง) ฟังอยู่ที่ http://localhost:${PORT}/hooks/gtg-chat`));
