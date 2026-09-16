#!/usr/bin/env node
/**
 * คำนวณตัวเลขของหน้า Omnichannel Overview จากข้อมูลที่ดึงมาแล้ว
 *
 *   npm run respondio:stats              ช่วง 7 วันล่าสุด
 *   npm run respondio:stats -- --days 30
 *   npm run respondio:stats -- --json    พิมพ์ JSON ก้อนเดียว เอาไปวางต่อได้
 *
 * ไม่เรียก respond.io เลย อ่านจากตารางในเครื่องล้วน ๆ
 * ต้องรัน `npm run respondio:pull` มาก่อน
 */
import { overview } from '../src/integrations/respondio/stats.js';
import { closeDb, get } from '../src/db.js';

const argv = process.argv.slice(2);
const val = (f, d) => { const i = argv.indexOf(f); return i === -1 ? d : argv[i + 1]; };
const days = Number(val('--days', 7));
const asJson = argv.includes('--json');

const fmt = (sec) => {
  if (sec == null) return '—';
  const m = Math.floor(sec / 60), s = sec % 60;
  return m >= 60 ? `${Math.floor(m / 60)}h ${m % 60}m` : `${m}m ${String(s).padStart(2, '0')}s`;
};
const n = (x) => Number(x ?? 0).toLocaleString('en-US');

try {
  if (!get(`SELECT COUNT(*) c FROM respondio_contacts`).c) {
    console.error('ยังไม่มีข้อมูล — รัน `npm run respondio:pull` ก่อน');
    process.exit(1);
  }

  const o = overview(days);
  if (asJson) { console.log(JSON.stringify(o, null, 2)); process.exit(0); }

  const { audience: a, channels: ch, responseTimes: rt, trend: tr, gaps: g } = o;

  console.log(`\n── AUDIENCE ─────────────────────────────`);
  console.log(`  ${n(a.total).padStart(7)}  contacts ทั้งหมด`);
  console.log(`  ${n(a.openConversations).padStart(7)}  บทสนทนาที่ยังเปิดอยู่`);
  console.log(`  ${n(a.linked).padStart(7)}  จับคู่กับผู้ติดต่อในระบบแล้ว`);
  console.log(`  ${n(a.unlinked).padStart(7)}  ยังไม่จับคู่  ← กลุ่มนี้จะไม่อยู่ใน funnel`);
  if (a.byLifecycle.length) {
    console.log(`\n  lifecycle ที่ workspace ใช้จริง:`);
    for (const r of a.byLifecycle) console.log(`    ${String(r.n).padStart(6)}  ${r.k}`);
  }

  console.log(`\n── CHANNELS (${days} วันล่าสุด) ─────────────`);
  console.log(`  ${'channel'.padEnd(22)}${'contacts'.padStart(10)}${'active'.padStart(9)}${'messages'.padStart(10)}`);
  for (const c of ch) {
    console.log(`  ${String(c.channel).padEnd(22)}${n(c.contacts).padStart(10)}` +
                `${n(c.activeContacts).padStart(9)}${n(c.messages).padStart(10)}`);
  }

  console.log(`\n── RESPONSE TIME ────────────────────────`);
  console.log(`  first response  ${fmt(rt.firstResponse.avgSec).padStart(10)}   จาก ${n(rt.firstResponse.count)} รอบสนทนา`);
  console.log(`  ทุกข้อความ       ${fmt(rt.anyResponse.avgSec).padStart(10)}   จาก ${n(rt.anyResponse.count)} ครั้ง`);
  console.log(`  ภายใน 5 นาที     ${String(rt.sla.within5min).padStart(9)}%`);
  console.log(`  ภายใน 15 นาที    ${String(rt.sla.within15min).padStart(9)}%`);
  console.log(`  เกิน 30 นาที      ${String(rt.sla.over30min).padStart(9)}%`);
  console.log(`  ยังไม่ได้ตอบเลย    ${String(rt.sla.unanswered).padStart(9)} contacts`);

  console.log(`\n── TREND ────────────────────────────────`);
  console.log(`  ${'วันที่'.padEnd(14)}${'ใหม่'.padStart(7)}${'เข้า'.padStart(8)}${'ออก'.padStart(8)}${'active'.padStart(9)}`);
  for (const d of tr.slice(-14)) {
    console.log(`  ${d.date.padEnd(12)}${String(d.newContacts).padStart(7)}` +
                `${String(d.incoming).padStart(8)}${String(d.outgoing).padStart(8)}` +
                `${String(d.activeContacts).padStart(9)}`);
  }
  if (!tr.length) console.log('  (ไม่มีข้อมูลในช่วงนี้)');

  console.log(`\n── ช่องว่างที่ต้องรู้ ─────────────────────`);
  console.log(`  ${n(g.contactsWithoutChannel).padStart(7)}  ไม่มีข้อมูลช่องทาง`);
  console.log(`  ${n(g.contactsWithoutMessages).padStart(7)}  ไม่มีข้อความเลย`);
  console.log(`  ${n(g.contactsWithoutPhoneOrEmail).padStart(7)}  ไม่มีทั้งเบอร์และอีเมล ← จับคู่กับ CRM ไม่ได้`);
  if (g.lastSync) {
    console.log(`\n  ซิงก์ล่าสุด: ${g.lastSync.resource} · ${g.lastSync.finished_at}` +
                ` · ${g.lastSync.ok ? 'สำเร็จ' : 'ล้มเหลว'} · ${n(g.lastSync.fetched)} รายการ`);
  }
  console.log(`\n  ป้ายกำกับที่ใช้อยู่: ${o.tags.length ? o.tags.join(', ') : '(ไม่มี)'}\n`);
} finally {
  closeDb();
}
