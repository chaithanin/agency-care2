import { all, get, run, tx } from '../../db.js';
import { LIFECYCLE_STAGES } from '../../config.js';

/**
 * แปลงข้อมูลที่ดึงมาจาก respond.io (ตาราง respondio_*) เข้าตารางหลักของระบบ
 *
 * หลักการ:
 *   - จับคู่ด้วยเบอร์โทรก่อน ถ้าไม่เจอค่อยใช้อีเมล ถ้าไม่เจอทั้งคู่จึงสร้างใหม่
 *   - ของที่จับคู่แล้วบันทึกไว้ใน respondio_contact_links กันสร้างซ้ำรอบหน้า
 *   - ไม่ลบ ไม่ทับข้อมูลเดิมที่มีค่าอยู่แล้ว เติมเฉพาะช่องที่ยังว่าง
 */

/** ชื่อ lifecycle ของ respond.io → ขั้นตอนในระบบ ปรับได้ตามที่ตั้งไว้จริง */
export const LIFECYCLE_MAP = {
  lead: 'new_lead',
  'new lead': 'new_lead',
  prospect: 'hot_lead',
  'hot lead': 'hot_lead',
  opportunity: 'hot_lead',
  negotiation: 'payment',
  payment: 'payment',
  won: 'customer',
  customer: 'customer',
  lost: 'lost',
  churned: 'lost',
};

export function mapLifecycle(name) {
  if (!name) return 'new_lead';
  const key = String(name).trim().toLowerCase();
  if (LIFECYCLE_MAP[key]) return LIFECYCLE_MAP[key];
  return LIFECYCLE_STAGES.includes(key) ? key : 'new_lead';
}

/** เบอร์โทรเทียบกันแบบตัดอักขระที่ไม่ใช่ตัวเลขออก */
export function normPhone(p) {
  if (!p) return null;
  const digits = String(p).replace(/\D/g, '');
  return digits ? digits.slice(-9) : null; // เทียบ 9 หลักท้าย ครอบคลุม +66 / 0 นำหน้า
}

export function displayName(c) {
  const name = [c.first_name, c.last_name].filter(Boolean).join(' ').trim();
  return name || c.phone || c.email || `respond.io #${c.id}`;
}

function findLocalContact(rc) {
  const linked = get(
    'SELECT contact_id FROM respondio_contact_links WHERE respondio_contact_id = ?',
    [rc.id],
  );
  if (linked) return { id: linked.contact_id, matchedBy: 'link' };

  const phone = normPhone(rc.phone);
  if (phone) {
    const hit = all('SELECT id, phone FROM contacts WHERE phone IS NOT NULL')
      .find((r) => normPhone(r.phone) === phone);
    if (hit) return { id: hit.id, matchedBy: 'phone' };
  }
  if (rc.email) {
    const hit = get('SELECT id FROM contacts WHERE lower(email) = lower(?)', [rc.email]);
    if (hit) return { id: hit.id, matchedBy: 'email' };
  }
  return null;
}

/**
 * แปลง contact ทั้งหมดที่ดึงมา
 * @param {{ dryRun?: boolean, overwrite?: boolean }} opts
 *   dryRun    = คำนวณอย่างเดียว ไม่เขียนฐานข้อมูล
 *   overwrite = ทับค่าที่มีอยู่เดิมด้วยค่าจาก respond.io (ปกติเติมเฉพาะช่องว่าง)
 */
export function mapContacts({ dryRun = false, overwrite = false } = {}) {
  const rows = all('SELECT * FROM respondio_contacts ORDER BY id');
  const result = { total: rows.length, linked: 0, created: 0, updated: 0, byMatch: {} };

  const apply = () => {
    for (const rc of rows) {
      const found = findLocalContact(rc);
      let contactId;
      let matchedBy;

      if (found) {
        contactId = found.id;
        matchedBy = found.matchedBy;
        const cur = get('SELECT * FROM contacts WHERE id = ?', [contactId]);
        if (cur) {
          const next = {
            display_name: overwrite ? displayName(rc) : (cur.display_name || displayName(rc)),
            phone: overwrite ? (rc.phone ?? cur.phone) : (cur.phone || rc.phone),
            email: overwrite ? (rc.email ?? cur.email) : (cur.email || rc.email),
            language: overwrite ? (rc.language ?? cur.language) : (cur.language || rc.language || 'th'),
            lifecycle_stage: overwrite ? mapLifecycle(rc.lifecycle) : cur.lifecycle_stage,
          };
          const changed = Object.entries(next).some(([k, v]) => cur[k] !== v);
          if (changed) {
            run(
              `UPDATE contacts SET display_name=?, phone=?, email=?, language=?,
                      lifecycle_stage=?, updated_at=datetime('now') WHERE id=?`,
              [next.display_name, next.phone, next.email, next.language, next.lifecycle_stage, contactId],
            );
            result.updated++;
          }
        }
      } else {
        const r = run(
          `INSERT INTO contacts (display_name, language, lifecycle_stage, phone, email)
           VALUES (?,?,?,?,?)`,
          [displayName(rc), rc.language || 'th', mapLifecycle(rc.lifecycle), rc.phone, rc.email],
        );
        contactId = Number(r.lastInsertRowid);
        matchedBy = 'created';
        result.created++;
      }

      run(
        `INSERT INTO respondio_contact_links (respondio_contact_id, contact_id, matched_by)
         VALUES (?,?,?)
         ON CONFLICT(respondio_contact_id) DO UPDATE SET
           contact_id=excluded.contact_id, matched_by=excluded.matched_by,
           linked_at=datetime('now')`,
        [rc.id, contactId, matchedBy],
      );
      result.linked++;
      result.byMatch[matchedBy] = (result.byMatch[matchedBy] ?? 0) + 1;

      // tag
      for (const t of JSON.parse(rc.tags_json || '[]')) {
        run('INSERT INTO tags (name) VALUES (?) ON CONFLICT(name) DO NOTHING', [t]);
        const tag = get('SELECT id FROM tags WHERE name = ?', [t]);
        if (tag) {
          run(
            'INSERT INTO contact_tags (contact_id, tag_id) VALUES (?,?) ON CONFLICT DO NOTHING',
            [contactId, tag.id],
          );
        }
      }
    }
  };

  if (dryRun) {
    // นับอย่างเดียว ไม่แตะฐานข้อมูล — ใช้ transaction แล้ว rollback
    const d = all('SELECT 1').length; // บังคับเปิด db
    void d;
    try {
      tx(() => { apply(); throw new Error('__dry_run__'); });
    } catch (err) {
      if (err.message !== '__dry_run__') throw err;
    }
    return { ...result, dryRun: true };
  }

  tx(apply);
  return result;
}

/** สรุปข้อมูลที่ดึงมา ไว้แสดงผลหลังรัน */
export function overview() {
  return {
    contacts: get('SELECT COUNT(*) n FROM respondio_contacts').n,
    linked: get('SELECT COUNT(*) n FROM respondio_contact_links').n,
    bySource: all(
      `SELECT source, COUNT(*) n FROM respondio_contact_channels
        GROUP BY source ORDER BY n DESC`,
    ),
    byLifecycle: all(
      `SELECT COALESCE(lifecycle,'(ไม่ระบุ)') lifecycle, COUNT(*) n
         FROM respondio_contacts GROUP BY lifecycle ORDER BY n DESC`,
    ),
    messages: get('SELECT COUNT(*) n FROM respondio_messages').n,
    messagesByTraffic: all(
      `SELECT COALESCE(traffic,'(ไม่ระบุ)') traffic, COUNT(*) n
         FROM respondio_messages GROUP BY traffic`,
    ),
    openConversations: get(
      `SELECT COUNT(*) n FROM respondio_contacts WHERE status = 'open'`,
    ).n,
  };
}
