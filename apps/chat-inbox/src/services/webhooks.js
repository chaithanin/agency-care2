import crypto from 'node:crypto';
import { all, run } from '../db.js';
import { config } from '../config.js';

/**
 * Webhook ขาออกไปหา Agency Care
 * ฝั่งรับต้องตรวจ header:
 *   x-gtg-timestamp  = unix ms
 *   x-gtg-signature  = sha256=HEX( HMAC-SHA256(secret, `${timestamp}.${rawBody}`) )
 * การใส่ timestamp เข้าไปในสิ่งที่เซ็น ทำให้ replay ของเก่ายิงซ้ำไม่ได้ถ้าฝั่งรับเช็กอายุ
 */
export function signPayload(secret, timestamp, rawBody) {
  return 'sha256=' + crypto.createHmac('sha256', secret).update(`${timestamp}.${rawBody}`).digest('hex');
}

export function verifySignature(secret, timestamp, rawBody, signature) {
  const expected = Buffer.from(signPayload(secret, timestamp, rawBody), 'utf8');
  const given = Buffer.from(String(signature || ''), 'utf8');
  return given.length === expected.length && crypto.timingSafeEqual(given, expected);
}

/** ส่ง event ให้ทุก endpoint ที่สมัครฟัง event นั้น และบันทึกผลลง webhook_deliveries */
export async function dispatchWebhook(event, data) {
  const hooks = all('SELECT * FROM webhooks_out WHERE active = 1').filter((h) =>
    h.events.split(',').map((e) => e.trim()).includes(event));
  if (!hooks.length) return [];

  const body = JSON.stringify({ event, data, sentAt: new Date().toISOString() });
  const results = [];

  for (const hook of hooks) {
    const deliveryId = run(
      "INSERT INTO webhook_deliveries (webhook_id, event, payload_json, status, attempts) VALUES (?, ?, ?, 'pending', 1)",
      [hook.id, event, body],
    ).lastInsertRowid;

    const ts = Date.now();
    try {
      const res = await fetch(hook.url, {
        method: 'POST',
        headers: {
          'content-type': 'application/json',
          'x-gtg-event': event,
          'x-gtg-timestamp': String(ts),
          'x-gtg-signature': signPayload(hook.secret, ts, body),
        },
        body,
        signal: AbortSignal.timeout(config.webhookTimeoutMs),
      });
      run('UPDATE webhook_deliveries SET status = ?, response_code = ? WHERE id = ?',
        [res.ok ? 'ok' : 'failed', res.status, deliveryId]);
      results.push({ hook: hook.name, ok: res.ok, status: res.status });
    } catch (err) {
      run('UPDATE webhook_deliveries SET status = ?, error = ? WHERE id = ?',
        ['failed', String(err.message).slice(0, 300), deliveryId]);
      results.push({ hook: hook.name, ok: false, error: String(err.message) });
      console.error(`[webhook] ส่งไป ${hook.url} ไม่สำเร็จ:`, err.message);
    }
  }
  return results;
}
