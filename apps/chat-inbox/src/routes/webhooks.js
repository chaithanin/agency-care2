import { getAdapter } from '../channels/adapter.js';
import { getChannel, ingestIncoming } from '../services/inbox.js';
import { runAutomations } from '../services/automations.js';
import { sendJson, notFound, HttpError } from '../http.js';

/**
 * POST /webhook/:provider   (line | mock)
 * ขั้นตอน: ตรวจลายเซ็น → normalize → บันทึก → รันกฎอัตโนมัติ
 * ตอบ 200 เสมอเมื่อลายเซ็นผ่าน เพราะ LINE จะ retry ถ้าเราตอบ error
 */
export async function handleChannelWebhook(req, res, url) {
  const provider = url.pathname.split('/').filter(Boolean)[1];
  const channel = getChannel(provider);
  if (!channel) throw notFound(`ยังไม่ได้ตั้งค่าช่องทาง: ${provider}`);

  const adapter = getAdapter(provider);
  if (!adapter.verifySignature(req.rawBody, req.headers, channel)) {
    throw new HttpError(401, 'invalid_signature', 'ลายเซ็นไม่ถูกต้อง');
  }

  const incoming = adapter.parseIncoming(req.body || {}, channel);
  const handled = [];

  for (const msg of incoming) {
    const result = ingestIncoming(channel, msg);
    if (result.duplicate) {
      handled.push({ messageId: result.messageId, duplicate: true });
      continue;
    }
    const fired = await runAutomations({
      conversationId: result.conversationId,
      contactId: result.contactId,
      text: msg.text,
      conversationCreated: result.conversationCreated,
    });
    handled.push({
      messageId: result.messageId,
      conversationId: result.conversationId,
      contactId: result.contactId,
      automations: fired,
    });
  }

  return sendJson(res, 200, { ok: true, received: incoming.length, handled });
}
