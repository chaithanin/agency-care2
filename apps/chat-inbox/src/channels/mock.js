import crypto from 'node:crypto';
import { registerAdapter } from './adapter.js';

/**
 * ช่องทางจำลองสำหรับทดสอบในเครื่อง — รูปแบบ payload ของเราเอง
 * ใช้ตอนยังไม่มี LINE OA หรือยังไม่ได้เปิด ngrok
 * body: { userId, displayName, text, messageId? }
 */
const mockAdapter = {
  provider: 'mock',

  verifySignature(rawBody, headers, channel) {
    const secret = channel?.config?.channelSecret;
    if (!secret) return true; // ช่องทางทดสอบที่ไม่ตั้ง secret = เปิดให้ยิงได้เลย
    const expected = crypto.createHmac('sha256', secret).update(rawBody).digest('hex');
    const given = Buffer.from(String(headers['x-mock-signature'] || ''), 'utf8');
    const exp = Buffer.from(expected, 'utf8');
    return given.length === exp.length && crypto.timingSafeEqual(given, exp);
  },

  parseIncoming(body) {
    if (!body?.userId || typeof body.text !== 'string') return [];
    return [{
      externalUserId: String(body.userId),
      externalMessageId: body.messageId || `mock-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`,
      text: body.text,
      replyToken: null,
      profile: { displayName: body.displayName || null },
      raw: body,
    }];
  },

  async sendMessage() {
    return { externalMessageId: `mock-out-${Date.now()}`, dryRun: true };
  },
};

registerAdapter('mock', mockAdapter);
export default mockAdapter;
