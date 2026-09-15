import { randomUUID } from 'node:crypto';

export class HttpError extends Error {
  constructor(status, code, message) {
    super(message);
    this.status = status;
    this.code = code;
  }
}
export const badRequest = (m) => new HttpError(400, 'bad_request', m);
export const unauthorized = (m = 'API key ไม่ถูกต้อง') => new HttpError(401, 'unauthorized', m);
export const notFound = (m = 'ไม่พบข้อมูล') => new HttpError(404, 'not_found', m);

export function sendJson(res, status, body) {
  const payload = JSON.stringify(body);
  res.writeHead(status, {
    'content-type': 'application/json; charset=utf-8',
    'content-length': Buffer.byteLength(payload),
    'cache-control': 'no-store',
    'x-content-type-options': 'nosniff',
  });
  res.end(payload);
}

export function sendError(res, err) {
  const status = err instanceof HttpError ? err.status : 500;
  const code = err instanceof HttpError ? err.code : 'internal_error';
  if (status >= 500) console.error('[error]', err);
  sendJson(res, status, { error: { code, message: err.message || 'เกิดข้อผิดพลาด' } });
}

/** อ่าน body ดิบ เก็บทั้ง Buffer (ต้องใช้ตรวจลายเซ็น) และ JSON ที่ parse แล้ว */
export function readBody(req, limitBytes = 1_000_000) {
  return new Promise((resolve, reject) => {
    const chunks = [];
    let size = 0;
    req.on('data', (c) => {
      size += c.length;
      if (size > limitBytes) {
        reject(new HttpError(413, 'payload_too_large', 'body ใหญ่เกินกำหนด'));
        req.destroy();
        return;
      }
      chunks.push(c);
    });
    req.on('end', () => {
      const raw = Buffer.concat(chunks);
      let json = null;
      if (raw.length) {
        try { json = JSON.parse(raw.toString('utf8')); }
        catch { return reject(badRequest('body ไม่ใช่ JSON ที่ถูกต้อง')); }
      }
      resolve({ raw, json });
    });
    req.on('error', reject);
  });
}

export const requestId = () => randomUUID();

/** แปลง query string เป็น object พร้อมค่า default */
export function parseQuery(url) {
  return Object.fromEntries(url.searchParams.entries());
}

export function clampLimit(value, def = 25, max = 100) {
  const n = Number(value);
  if (!Number.isFinite(n) || n <= 0) return def;
  return Math.min(Math.floor(n), max);
}
