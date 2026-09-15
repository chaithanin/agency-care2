import crypto from 'node:crypto';
import { get, run, nowIso } from '../db.js';
import { unauthorized } from '../http.js';

export const hashKey = (key) => crypto.createHash('sha256').update(key, 'utf8').digest('hex');

/** ออกคีย์ใหม่ — คืนคีย์เต็มครั้งเดียว ใน DB เก็บแค่ hash */
export function createApiKey(name, scopes = 'read') {
  const key = `gtg_${crypto.randomBytes(24).toString('hex')}`;
  run('INSERT INTO api_keys (name, prefix, key_hash, scopes) VALUES (?, ?, ?, ?)',
    [name, key.slice(0, 12), hashKey(key), scopes]);
  return key;
}

/** ตรวจ header X-API-Key — เทียบ hash แบบ timing-safe */
export function authenticate(req, requiredScope = 'read') {
  const provided = req.headers['x-api-key']
    || (String(req.headers.authorization || '').startsWith('Bearer ')
      ? String(req.headers.authorization).slice(7)
      : '');
  if (!provided) throw unauthorized('ต้องส่ง header X-API-Key');

  const hash = hashKey(provided);
  const row = get('SELECT * FROM api_keys WHERE active = 1 AND key_hash = ?', [hash]);
  if (!row) throw unauthorized();

  const a = Buffer.from(row.key_hash, 'utf8');
  const b = Buffer.from(hash, 'utf8');
  if (a.length !== b.length || !crypto.timingSafeEqual(a, b)) throw unauthorized();

  const scopes = row.scopes.split(',').map((s) => s.trim());
  if (!scopes.includes(requiredScope) && !scopes.includes('admin')) {
    throw unauthorized(`คีย์นี้ไม่มีสิทธิ์ ${requiredScope}`);
  }
  run('UPDATE api_keys SET last_used_at = ? WHERE id = ?', [nowIso(), row.id]);
  return { id: row.id, name: row.name, scopes };
}
