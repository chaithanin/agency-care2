import test from 'node:test';
import assert from 'node:assert/strict';
import path from 'node:path';
import os from 'node:os';
import { mkdtempSync, rmSync, existsSync } from 'node:fs';

process.env.DB_FILE = path.join(mkdtempSync(path.join(os.tmpdir(), 'gtg-stats-')), 'test.db');

const db = await import('../src/db.js');
const stats = await import('../src/integrations/respondio/stats.js');

const NOW = Math.floor(Date.now() / 1000);
const ago = (min) => NOW - min * 60;

function seed() {
  const c = (id, status, lifecycle, phone) => db.run(
    `INSERT INTO respondio_contacts (id, first_name, status, lifecycle, phone, created_at)
     VALUES (?,?,?,?,?,?)`, [id, `C${id}`, status, lifecycle, phone, ago(60 * 24)]);
  c(1, 'open',  'Lead',     '0812345678');
  c(2, 'close', 'Customer', null);
  c(3, 'open',  'Lead',     '0899999999');

  const ch = (id, contact, source) => db.run(
    `INSERT INTO respondio_contact_channels (id, contact_id, source) VALUES (?,?,?)`,
    [id, contact, source]);
  ch(11, 1, 'line'); ch(12, 2, 'line'); ch(13, 3, 'facebook');

  let mid = 100;
  const m = (contact, traffic, minutesAgo) => db.run(
    `INSERT INTO respondio_messages (id, contact_id, traffic, timestamp) VALUES (?,?,?,?)`,
    [mid++, contact, traffic, ago(minutesAgo)]);

  // contact 1 — ลูกค้าถาม 100 นาทีที่แล้ว ตอบหลังจากนั้น 2 นาที
  m(1, 'incoming', 100); m(1, 'outgoing', 98);
  // ถามอีกรอบ ตอบช้า 40 นาที
  m(1, 'incoming', 90);  m(1, 'outgoing', 50);
  // contact 2 — ตอบใน 20 นาที (เกิน 15 ไม่เกิน 30)
  m(2, 'incoming', 80);  m(2, 'outgoing', 60);
  // contact 3 — ถามแล้วยังไม่มีใครตอบ
  m(3, 'incoming', 30);
}

test('audience นับได้ถูก', () => {
  seed();
  const a = stats.audience();
  assert.equal(a.total, 3);
  assert.equal(a.openConversations, 2);
  assert.equal(a.unlinked, 3, 'ยังไม่จับคู่กับใครเลย');
  assert.deepEqual(a.byLifecycle.map((r) => [r.k, r.n]).sort(),
                   [['Customer', 1], ['Lead', 2]]);
});

test('แยกตามช่องทางได้', () => {
  const rows = stats.channels(stats.range(7));
  const line = rows.find((r) => r.channel === 'line');
  const fb = rows.find((r) => r.channel === 'facebook');
  assert.equal(line.contacts, 2);
  assert.equal(fb.contacts, 1);
  assert.equal(line.messages, 6, 'contact 1 มี 4 ข้อความ contact 2 มี 2');
});

test('first response คิดจากข้อความแรกที่รอ ไม่ใช่ข้อความล่าสุด', () => {
  const rt = stats.responseTimes(stats.range(7));
  // contact1 รอบแรก 2 นาที · contact2 20 นาที → เฉลี่ย 11 นาที = 660 วินาที
  assert.equal(rt.firstResponse.count, 2);
  assert.equal(rt.firstResponse.avgSec, 660);
  // เก็บผลรวมกับจำนวนไว้ ไม่ใช่ค่าเฉลี่ยสำเร็จรูป — รวมข้ามวันแล้วยังถูก
  assert.equal(rt.firstResponse.sumSec, 120 + 1200);
});

test('นับทุกครั้งที่ตอบ ไม่ใช่แค่ครั้งแรก', () => {
  const rt = stats.responseTimes(stats.range(7));
  assert.equal(rt.anyResponse.count, 3, 'contact1 ตอบ 2 ครั้ง contact2 อีก 1');
  assert.equal(rt.anyResponse.sumSec, 120 + 2400 + 1200);
});

test('SLA แบ่งช่วงถูก และนับคนที่ยังไม่ได้ตอบ', () => {
  const rt = stats.responseTimes(stats.range(7));
  assert.equal(rt.sla.within5min, 50, 'contact1 ตอบใน 2 นาที = 1 จาก 2');
  assert.equal(rt.sla.within15min, 50, 'contact2 ใช้ 20 นาที ไม่เข้าเกณฑ์');
  assert.equal(rt.sla.over30min, 0, 'first response ทั้งสองไม่เกิน 30 นาที');
  assert.equal(rt.sla.unanswered, 1, 'contact 3 ถามแล้วเงียบ');
});

test('trend แยกวันและนับ contact ที่ active ไม่ซ้ำ', () => {
  const tr = stats.trend(stats.range(7));
  assert.ok(tr.length >= 1);
  const total = tr.reduce((s, d) => s + d.incoming + d.outgoing, 0);
  assert.equal(total, 7, 'ข้อความทั้งหมดที่ seed ไว้');
});

test('ช่องว่างที่จับคู่กับ CRM ไม่ได้', () => {
  const g = stats.gaps();
  assert.equal(g.contactsWithoutPhoneOrEmail, 1, 'contact 2 ไม่มีทั้งเบอร์และอีเมล');
  assert.equal(g.contactsWithoutChannel, 0);
  assert.equal(g.contactsWithoutMessages, 0);
});

test('overview รวมทุกอย่างและไม่มีข้อมูลส่วนบุคคลติดออกมา', () => {
  const o = stats.overview(7);
  const json = JSON.stringify(o);
  assert.ok(o.audience && o.channels && o.responseTimes && o.trend && o.gaps);
  assert.equal(json.includes('0812345678'), false, 'ห้ามมีเบอร์โทรใน output');
  assert.equal(json.includes('C1'), false, 'ห้ามมีชื่อใน output');
});

test.after(() => {
  db.closeDb();
  for (const s of ['', '-wal', '-shm']) {
    const f = process.env.DB_FILE + s;
    if (existsSync(f)) rmSync(f);
  }
});
