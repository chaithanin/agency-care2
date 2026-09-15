import path from 'node:path';
import http from 'node:http';
import { rmSync, existsSync, mkdtempSync } from 'node:fs';
import os from 'node:os';

/**
 * เตรียมฐานข้อมูลเปล่าแล้วค่อย import โมดูล (ต้องตั้ง env ก่อน import เสมอ)
 * node --test แยกโปรเซสให้ไฟล์ทดสอบละหนึ่งอัน จึงเรียกได้ไฟล์ละครั้ง
 */
export async function freshApp({ lineSecret = 'test-line-secret' } = {}) {
  const dir = mkdtempSync(path.join(os.tmpdir(), 'gtg-chat-test-'));
  process.env.DB_FILE = path.join(dir, 'test.db');
  process.env.LINE_CHANNEL_SECRET = lineSecret;
  process.env.LINE_DRY_RUN = 'true';

  const db = await import('../src/db.js');
  const { createServer } = await import('../src/server.js');
  const inbox = await import('../src/services/inbox.js');
  const apiKeys = await import('../src/services/apiKeys.js');
  const automations = await import('../src/services/automations.js');

  db.run("INSERT INTO users (email, name, role) VALUES ('a@t.local','Admin','admin')");
  db.run("INSERT INTO users (email, name, role) VALUES ('p@t.local','Ploy','agent')");
  db.run("INSERT INTO users (email, name, role) VALUES ('i@t.local','Ivan','agent')");
  db.run("INSERT INTO channels (provider, name, external_id, config_json) VALUES ('line','LINE','line-1',?)",
    [JSON.stringify({ channelSecret: lineSecret })]);
  db.run("INSERT INTO channels (provider, name, external_id) VALUES ('mock','Mock','mock-1')");
  db.run("INSERT INTO custom_field_defs (key, label, type) VALUES ('budget','งบประมาณ','number')");

  const server = createServer();
  await new Promise((r) => server.listen(0, r));
  const base = `http://localhost:${server.address().port}`;

  return {
    base, db, inbox, apiKeys, automations,
    async close() {
      await new Promise((r) => server.close(r));
      db.closeDb();
      for (const s of ['', '-wal', '-shm']) { const f = process.env.DB_FILE + s; if (existsSync(f)) rmSync(f); }
    },
  };
}

export async function req(base, method, url, { body, headers = {} } = {}) {
  const res = await fetch(base + url, {
    method,
    headers: { 'content-type': 'application/json', ...headers },
    body: body === undefined ? undefined : JSON.stringify(body),
  });
  const text = await res.text();
  let json = null;
  try { json = JSON.parse(text); } catch { /* ไม่ใช่ JSON เช่นไฟล์ static */ }
  return { status: res.status, json, text, headers: res.headers };
}

/** ตัวรับ webhook สำหรับทดสอบ — เก็บ request ที่เข้ามาไว้ตรวจ */
export async function webhookSink() {
  const requests = [];
  const server = http.createServer((rq, rs) => {
    const chunks = [];
    rq.on('data', (c) => chunks.push(c));
    rq.on('end', () => {
      requests.push({ headers: rq.headers, raw: Buffer.concat(chunks).toString('utf8') });
      rs.writeHead(200, { 'content-type': 'application/json' }).end('{"ok":true}');
    });
  });
  await new Promise((r) => server.listen(0, r));
  return {
    requests,
    url: `http://localhost:${server.address().port}/hooks`,
    close: () => new Promise((r) => server.close(r)),
  };
}
