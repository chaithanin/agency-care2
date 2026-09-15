import crypto from 'node:crypto';
import { config } from '../config.js';
import { registerAdapter } from './adapter.js';

/** ตรวจ X-Line-Signature = base64(HMAC-SHA256(channelSecret, rawBody)) */
export function verifyLineSignature(rawBody, signature, secret) {
  if (!secret || !signature) return false;
  const expected = crypto.createHmac('sha256', secret).update(rawBody).digest();
  let given;
  try { given = Buffer.from(String(signature), 'base64'); } catch { return false; }
  // ความยาวต้องเท่ากันก่อน timingSafeEqual ไม่งั้นมันโยน error
  if (given.length !== expected.length) return false;
  return crypto.timingSafeEqual(given, expected);
}

const lineAdapter = {
  provider: 'line',

  verifySignature(rawBody, headers, channel) {
    const secret = channel?.config?.channelSecret || config.line.channelSecret;
    return verifyLineSignature(rawBody, headers['x-line-signature'], secret);
  },

  parseIncoming(body) {
    const events = Array.isArray(body?.events) ? body.events : [];
    return events
      .filter((e) => e.type === 'message' && e.message?.type === 'text')
      .map((e) => ({
        externalUserId: e.source?.userId || e.source?.groupId || 'unknown',
        externalMessageId: e.message.id,
        text: e.message.text || '',
        replyToken: e.replyToken || null,
        profile: { sourceType: e.source?.type || 'user' },
        raw: e,
      }));
  },

  async sendMessage({ channel, to, text, replyToken }) {
    const token = channel?.config?.accessToken || config.line.accessToken;
    if (config.line.dryRun || !token) {
      // โหมดทดสอบในเครื่อง: ไม่ยิงออกไปจริง แต่ยังบันทึกข้อความขาออกลง DB
      return { externalMessageId: `dry-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`, dryRun: true };
    }
    const useReply = Boolean(replyToken);
    const url = `${config.line.apiBase}/v2/bot/message/${useReply ? 'reply' : 'push'}`;
    const payload = useReply
      ? { replyToken, messages: [{ type: 'text', text }] }
      : { to, messages: [{ type: 'text', text }] };

    const res = await fetch(url, {
      method: 'POST',
      headers: { authorization: `Bearer ${token}`, 'content-type': 'application/json' },
      body: JSON.stringify(payload),
      signal: AbortSignal.timeout(10_000),
    });
    if (!res.ok) {
      throw new Error(`LINE API ${res.status}: ${(await res.text()).slice(0, 300)}`);
    }
    const data = await res.json().catch(() => ({}));
    return { externalMessageId: data.sentMessages?.[0]?.id || null, dryRun: false };
  },
};

registerAdapter('line', lineAdapter);
export default lineAdapter;
