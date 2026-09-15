/**
 * ChannelAdapter — สัญญากลางของทุกช่องทาง (roadmap สัปดาห์ 9-10)
 * เพิ่มช่องทางใหม่ = เขียนไฟล์ที่ทำครบ 3 อย่างนี้ โดยไม่ต้องแตะโค้ด Inbox
 *
 *   verifySignature(rawBody, headers, channel) -> boolean
 *   parseIncoming(body, channel)               -> NormalizedMessage[]
 *   sendMessage({ channel, to, text, replyToken }) -> { externalMessageId, dryRun }
 *
 * NormalizedMessage = {
 *   externalUserId, externalMessageId, text, replyToken, profile, raw
 * }
 */
const registry = new Map();

export function registerAdapter(provider, adapter) {
  registry.set(provider, adapter);
}

export function getAdapter(provider) {
  const adapter = registry.get(provider);
  if (!adapter) throw new Error(`ยังไม่มี adapter สำหรับช่องทาง: ${provider}`);
  return adapter;
}

export const listProviders = () => [...registry.keys()];
