import { all, get } from '../../db.js';

/**
 * คำนวณตัวเลขทั้งหมดของหน้า Omnichannel Overview จากตารางกระจกเงา respondio_*
 *
 * ทำงานบนข้อมูลในเครื่องล้วน ๆ ไม่เรียก respond.io เลย —
 * นี่คือแบบเดียวกับที่ระบบจริงต้องทำ: ดึงมาเก็บก่อน แล้วค่อยคำนวณ
 * ไม่ใช่เรียก API สดตอนผู้ใช้เปิดหน้า
 */

const day = (epochSec) =>
  epochSec ? new Date(epochSec * 1000).toISOString().slice(0, 10) : null;

/** ช่วงเวลาที่จะคิด — คืน epoch วินาที */
export function range(days) {
  const to = Math.floor(Date.now() / 1000);
  return { from: to - days * 86400, to, days };
}

// ── Audience ────────────────────────────────────────────────
export function audience() {
  const total = get(`SELECT COUNT(*) n FROM respondio_contacts`).n;
  const linked = get(`SELECT COUNT(*) n FROM respondio_contact_links`).n;
  const byLifecycle = all(
    `SELECT COALESCE(lifecycle,'(ไม่ระบุ)') k, COUNT(*) n
       FROM respondio_contacts GROUP BY lifecycle ORDER BY n DESC`);
  const open = get(`SELECT COUNT(*) n FROM respondio_contacts WHERE status='open'`).n;
  return { total, linked, unlinked: total - linked, openConversations: open, byLifecycle };
}

// ── ช่องทาง ─────────────────────────────────────────────────
export function channels({ from, to }) {
  return all(
    `SELECT COALESCE(cc.source,'(ไม่ระบุ)') AS channel,
            COUNT(DISTINCT cc.contact_id)   AS contacts,
            COUNT(DISTINCT CASE WHEN m.timestamp BETWEEN ? AND ?
                           THEN m.contact_id END) AS activeContacts,
            COUNT(CASE WHEN m.timestamp BETWEEN ? AND ? THEN 1 END) AS messages
       FROM respondio_contact_channels cc
       LEFT JOIN respondio_messages m ON m.contact_id = cc.contact_id
      GROUP BY cc.source
      ORDER BY contacts DESC`,
    [from, to, from, to]);
}

// ── เวลาตอบกลับ ─────────────────────────────────────────────
/**
 * First response = ข้อความ outgoing ตัวแรกหลังข้อความ incoming ที่เปิดรอบสนทนา
 * คิดต่อ contact แล้วเก็บ "ผลรวมกับจำนวน" ไม่ใช่ค่าเฉลี่ยสำเร็จรูป
 * เพื่อให้รวมข้ามวันแล้วยังถูก
 */
export function responseTimes({ from, to }) {
  const rows = all(
    `SELECT contact_id, traffic, timestamp
       FROM respondio_messages
      WHERE timestamp BETWEEN ? AND ? AND traffic IS NOT NULL
      ORDER BY contact_id, timestamp`, [from, to]);

  let firstSum = 0, firstCount = 0, allSum = 0, allCount = 0;
  let w5 = 0, w15 = 0, over30 = 0;
  let curContact = null, pendingIn = null, gotFirst = false;

  for (const r of rows) {
    if (r.contact_id !== curContact) {
      curContact = r.contact_id; pendingIn = null; gotFirst = false;
    }
    if (r.traffic === 'incoming') {
      if (pendingIn === null) pendingIn = r.timestamp;   // นับจากข้อความแรกที่รอ
    } else if (r.traffic === 'outgoing' && pendingIn !== null) {
      const delta = r.timestamp - pendingIn;
      if (delta >= 0) {
        allSum += delta; allCount++;
        if (!gotFirst) {
          firstSum += delta; firstCount++; gotFirst = true;
          if (delta <= 300) w5++;
          if (delta <= 900) w15++;
          if (delta > 1800) over30++;
        }
      }
      pendingIn = null;
    }
  }
  const pct = (n) => (firstCount ? Math.round(n / firstCount * 100) : 0);
  return {
    firstResponse: { sumSec: firstSum, count: firstCount,
                     avgSec: firstCount ? Math.round(firstSum / firstCount) : null },
    anyResponse:   { sumSec: allSum, count: allCount,
                     avgSec: allCount ? Math.round(allSum / allCount) : null },
    sla: { within5min: pct(w5), within15min: pct(w15), over30min: pct(over30),
           unanswered: get(
             `SELECT COUNT(DISTINCT contact_id) n FROM respondio_messages
               WHERE timestamp BETWEEN ? AND ? AND traffic='incoming'
                 AND contact_id NOT IN (SELECT contact_id FROM respondio_messages
                                         WHERE timestamp BETWEEN ? AND ? AND traffic='outgoing')`,
             [from, to, from, to]).n },
  };
}

// ── แนวโน้มรายวัน ───────────────────────────────────────────
export function trend({ from, to }) {
  const msgs = all(
    `SELECT timestamp, traffic, contact_id FROM respondio_messages
      WHERE timestamp BETWEEN ? AND ?`, [from, to]);
  const contacts = all(
    `SELECT created_at FROM respondio_contacts WHERE created_at BETWEEN ? AND ?`, [from, to]);

  const byDay = new Map();
  const touch = (d) => {
    if (!byDay.has(d)) byDay.set(d, { date: d, newContacts: 0, incoming: 0, outgoing: 0, activeContacts: new Set() });
    return byDay.get(d);
  };
  for (const c of contacts) { const d = day(c.created_at); if (d) touch(d).newContacts++; }
  for (const m of msgs) {
    const d = day(m.timestamp); if (!d) continue;
    const e = touch(d);
    if (m.traffic === 'incoming') e.incoming++; else if (m.traffic === 'outgoing') e.outgoing++;
    e.activeContacts.add(m.contact_id);
  }
  return [...byDay.values()]
    .sort((a, b) => a.date.localeCompare(b.date))
    .map(({ activeContacts, ...e }) => ({ ...e, activeContacts: activeContacts.size }));
}

// ── ป้ายกำกับและช่องว่าง ────────────────────────────────────
export function tags() {
  return all(`SELECT name FROM respondio_tags ORDER BY name`).map((r) => r.name);
}

export function gaps() {
  return {
    contactsWithoutChannel: get(
      `SELECT COUNT(*) n FROM respondio_contacts c
        WHERE NOT EXISTS (SELECT 1 FROM respondio_contact_channels cc
                           WHERE cc.contact_id = c.id)`).n,
    contactsWithoutMessages: get(
      `SELECT COUNT(*) n FROM respondio_contacts c
        WHERE NOT EXISTS (SELECT 1 FROM respondio_messages m
                           WHERE m.contact_id = c.id)`).n,
    contactsWithoutPhoneOrEmail: get(
      `SELECT COUNT(*) n FROM respondio_contacts
        WHERE (phone IS NULL OR phone='') AND (email IS NULL OR email='')`).n,
    lastSync: get(
      `SELECT resource, finished_at, ok, fetched FROM respondio_sync_runs
        ORDER BY id DESC LIMIT 1`) ?? null,
  };
}

/** รวมทุกอย่างเป็นก้อนเดียว — ไม่มีชื่อ เบอร์ หรืออีเมลของใครเลย */
export function overview(days = 7) {
  const r = range(days);
  return {
    generatedAt: new Date().toISOString(),
    rangeDays: days,
    audience: audience(),
    channels: channels(r),
    responseTimes: responseTimes(r),
    trend: trend(r),
    tags: tags(),
    gaps: gaps(),
  };
}
