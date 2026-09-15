import { DatabaseSync } from 'node:sqlite';
import { readFileSync, mkdirSync } from 'node:fs';
import path from 'node:path';
import { config, ROOT } from './config.js';

let db;

export function getDb() {
  if (db) return db;
  mkdirSync(path.dirname(config.dbFile), { recursive: true });
  db = new DatabaseSync(config.dbFile);
  db.exec(readFileSync(path.join(ROOT, 'db', 'schema.sql'), 'utf8'));
  return db;
}

export function closeDb() {
  if (db) { db.close(); db = undefined; }
}

/** SELECT หลายแถว — ใช้ positional parameter (?) เท่านั้น กัน SQL injection */
export function all(sql, params = []) {
  return getDb().prepare(sql).all(...params);
}

/** SELECT แถวเดียว */
export function get(sql, params = []) {
  return getDb().prepare(sql).get(...params);
}

/** INSERT/UPDATE/DELETE — คืน { changes, lastInsertRowid } */
export function run(sql, params = []) {
  return getDb().prepare(sql).run(...params);
}

export function tx(fn) {
  const d = getDb();
  d.exec('BEGIN');
  try {
    const out = fn();
    d.exec('COMMIT');
    return out;
  } catch (err) {
    d.exec('ROLLBACK');
    throw err;
  }
}

export const nowIso = () => new Date().toISOString().replace('T', ' ').slice(0, 19);
