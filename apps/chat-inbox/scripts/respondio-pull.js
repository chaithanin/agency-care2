#!/usr/bin/env node
/**
 * ดึงข้อมูลจาก respond.io ลงตารางกระจกเงา respondio_*
 *
 *   npm run respondio:pull                 ดึงทุกอย่าง
 *   npm run respondio:pull -- --max 50     จำกัดจำนวน contact (ไว้ลองก่อน)
 *   npm run respondio:pull -- --workspace  ดึงเฉพาะ channel/user/field/note
 *   npm run respondio:pull -- --map        ดึงเสร็จแล้วแปลงเข้าตาราง contacts ของระบบ
 *   npm run respondio:pull -- --map-only --dry-run   ลองแปลงดูผลโดยไม่เขียนจริง
 */
import { createClient } from '../src/integrations/respondio/client.js';
import { syncAll, syncWorkspace, syncSummary } from '../src/integrations/respondio/sync.js';
import { mapContacts, overview } from '../src/integrations/respondio/map.js';
import { closeDb } from '../src/db.js';

const argv = process.argv.slice(2);
const has = (f) => argv.includes(f);
const val = (f, d) => {
  const i = argv.indexOf(f);
  return i === -1 ? d : argv[i + 1];
};

const max = val('--max') ? Number(val('--max')) : undefined;
const dryRun = has('--dry-run');

const client = createClient({
  onRetry: ({ attempt, delay, status }) =>
    console.log(`  ลองใหม่ครั้งที่ ${attempt + 1} (${status ?? 'network'}) รอ ${delay}ms`),
});

if (!client.configured && !has('--map-only')) {
  console.error('ยังไม่ได้ตั้ง RESPONDIO_API_TOKEN — ดูวิธีที่ docs/RESPOND_IO.md');
  process.exit(1);
}

try {
  if (!has('--map-only')) {
    console.log('กำลังดึงข้อมูลจาก respond.io ...');
    const results = has('--workspace')
      ? await syncWorkspace(client)
      : await syncAll(client, { max });

    for (const r of results) {
      console.log(r.ok
        ? `  ${String(r.fetched).padStart(5)}  ${r.resource}`
        : `      ✗  ${r.resource} — ${r.error}`);
    }
    const bad = results.filter((r) => !r.ok);
    console.log('\nรวมในฐานข้อมูล:', JSON.stringify(syncSummary(), null, 2));
    if (bad.length) process.exitCode = 1;
  }

  if (has('--map') || has('--map-only')) {
    console.log(`\n${dryRun ? 'ลองแปลง (ไม่เขียนจริง)' : 'แปลงเข้าตาราง contacts ของระบบ'} ...`);
    console.log(JSON.stringify(mapContacts({ dryRun, overwrite: has('--overwrite') }), null, 2));
  }

  console.log('\nภาพรวม:', JSON.stringify(overview(), null, 2));
} finally {
  closeDb();
}
