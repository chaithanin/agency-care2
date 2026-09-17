# คำสั่งสำหรับตัวหลัก — สร้างโมดูล Agency Onboarding

> คัดลอกทั้งหน้านี้ไปวางได้เลย

---

ทำโมดูล **Agency Onboarding** แบบ 7 เฟส ในโปรเจกต์ `chaithanin/agency-care`
แทนหน้า Onboarding เดิมที่เป็นตารางกับ drawer เช็กบ็อกซ์

## branch ที่ต้องใช้ — อ่านก่อนเริ่ม

แตกงานจาก **`feat/all-appointments-clean-on-118a2e2`** เท่านั้น
นี่คือสายที่ระบบจริงใช้อยู่ (= Cloud Run revision `agency-care-00886-nus`)

**ห้ามใช้ `feat/crm-modules-jul-2026`** เป็นคนละสายพัฒนา ที่เปลี่ยนชื่อและตัดเมนู
ไปหลายตัว เคย deploy จากสายนั้นแล้วเมนูในระบบจริงหายไป 8 ตัว
(Lead Status, Closed Deals, Registration Report, Advertising Requests,
LINE Checker, Staff Calendar, Social Media, Call Log)

ตรวจก่อนเริ่มทุกครั้ง

```bash
git branch --show-current     # ต้องเป็น feat/all-appointments-clean-on-118a2e2
```

## แบบที่ต้องทำตาม

Design canvas 12 หน้าจอ — https://claude.ai/artifact/PnXe4coE7J9wNhB25UP9f6

ไฟล์ต้นฉบับอยู่ที่รีโป `chaithanin/agency-care2`
branch `claude/agency-care-test-project-zo163o` โฟลเดอร์ `design/agency-onboarding/`
อ่าน `README.md` ในโฟลเดอร์นั้นก่อน มีรายละเอียดครบ

| อาร์ตบอร์ด | คือหน้าอะไร |
| --- | --- |
| `Main.dc.html` | Dashboard — stat card 5 ตัว, filter, search, การ์ดเอเจนซี่ |
| `Detail.dc.html` | Phase 1a — Agency Profile |
| `Phase1Docs.dc.html` | Phase 1b — Documents, Bank, Contacts, Social |
| `Phase2..7.dc.html` | เฟส 2 ถึง 7 |
| `Permissions.dc.html` | ตารางสิทธิ์ 13 พื้นที่ × 6 role |
| `AuditLog.dc.html` | Audit log + การ์ด Verified By / Verified At |
| `Mandatory.dc.html` | นิยามรายการบังคับ + กฎสถานะอัตโนมัติ |

สี ขนาด รัศมี และฟอนต์ในแบบ ดึงมาจาก `web/src/theme/ThemeContext.tsx` โหมด dark
ของรีโปนี้อยู่แล้ว ใช้ค่าตามนั้นได้เลย ไม่ต้องปัดเลข

## กฎที่ห้ามทำผิด

### 1. รายการบังคับ — เรียกใช้ของเดิม ห้ามเขียนใหม่

ระบบมีกฎ mandatory ของ agency อยู่แล้ว และใช้ร่วมกันสองที่

- `api/src/agency/agency-profile.util.ts` → `missingAgencyProfile()` — ตัวจริง
- `web/src/components/AddAgencyDialog.tsx` → `missingProfile()` — ต้องตรงกับข้างบน

ในโค้ดเขียนกำกับไว้เองว่า "แก้ที่นี่ที่เดียว ไม่งั้นสองที่จะเริ่มไม่ตรงกัน"

**Onboarding ต้องเรียก `missingAgencyProfile()` ไม่ใช่สร้างรายการใหม่ซ้อน**
ไม่งั้นจะมีนิยามคำว่า "ข้อมูลครบ" สองชุดที่ค่อย ๆ เพี้ยนออกจากกัน

รวม **34 ข้อบังคับเสมอ + 7 ข้อตามเงื่อนไข** ตัวหารไม่คงที่ อยู่ระหว่าง 34 ถึง 41
คำนวณต่อเอเจนซี่

| เงื่อนไข | ผลต่อตัวหาร |
| --- | --- |
| ติ๊ก New Agency | ลด 3 (Last Sale Date, Last Units Sold, Total Units Sold) |
| Office Type = Non-Physical | ลด 2 (Address, Google Map Link) |
| Existing Relationship = No Have | ลด 1 |
| บัญชีบริษัท ไม่ใช่บัญชีส่วนตัว | ลด 1 (Authorization Letter) |

### 2. สถานะที่ระบบคำนวณเอง — ผู้ใช้ตั้งไม่ได้

```
New → In Progress → Waiting Agency → Need Attention → Completed
```

```
In Progress ──(เงียบครบ 3 วัน)──> Waiting Agency ──(เงียบต่ออีก 4 วัน)──> Need Attention
```

เหตุการณ์ที่รีเซ็ตตัวนับ **มีสองอย่างเท่านั้น**

| รีเซ็ต | ไม่รีเซ็ต |
| --- | --- |
| อัปโหลดเอกสารเข้า onboarding | ข้อความในกลุ่ม LINE |
| ติ๊ก/ปลดติ๊ก checklist ข้อใดก็ได้ | เปิดดูหน้า onboarding |
| | แก้โน้ตภายในหรือข้อความในฟอร์ม |
| | เปลี่ยนผู้ดูแล |

- เอกสารที่ถูก Reject ก็นับว่าอัปโหลด ตัวนับรีเซ็ต เพราะมีคนทำงานกับมันจริง
- Completed แล้วหยุดนับ ย้ายไปอยู่ใต้กติกา Relationship Maintenance
- **สองเหตุการณ์นี้อยู่ใน audit log อยู่แล้ว อ่านจาก log ได้**
  ไม่ต้องเพิ่มฟิลด์เก็บเวลาในตาราง onboarding

### 3. ปุ่ม Complete Onboarding

ผู้ใช้กดปิดงานเองไม่ได้ ระบบคำนวณความพร้อมเอง ปุ่ม disable จนกว่ารายการบังคับครบทุกข้อ
กดได้เฉพาะ Manager ขึ้นไป **ตรวจฝั่ง server ด้วย ไม่ใช่แค่ disable ปุ่ม**

### 4. สิทธิ์

ตรวจสิทธิ์ฝั่ง server ทุก endpoint

⚠️ **ใช้ `user.role` ไม่ใช่ `user.activeRole`** — `api/src/common/current-user.decorator.ts`
เขียนกำกับไว้เองว่า `role` = permanent role (for permission guards) และ
`activeRole` = current active role (for data scoping)
แอดมินมักทำงานโดยสลับเป็น sales อยู่ ถ้าตัดสินสิทธิ์จาก `activeRole` จะล็อกตัวเองออก

กติกาที่ตารางสิทธิ์บังคับ

1. **Bank Information** แก้ได้เฉพาะ System Admin — Agency Support ยืนยันได้แต่แก้เลขบัญชีไม่ได้
2. **คนอัปโหลดเอกสารกับคนกด Verified ต้องคนละคน** — Seller อัปได้ แต่ยืนยันเองไม่ได้
3. **Complete Onboarding** เฉพาะ Manager ขึ้นไป และต่อเมื่อรายการบังคับครบ

### 5. Audit log

สี่จุดนี้ต้องบันทึก Verified By, Verified At และ audit log ทุกครั้งที่เปลี่ยน
**ห้ามมี endpoint สำหรับลบหรือแก้รายการเก่า**

- Document Verification
- Bank Information
- Agreement
- Complete Onboarding

### 6. ห้ามกระทบของเดิม

- เพิ่มบรรทัดใหม่เท่านั้น **ห้ามลบหรือแก้เมนู route หรือฟังก์ชันที่มีอยู่**
- ตารางใหม่สร้างตอนแอปบูตผ่าน `PrismaService` แบบ `CREATE TABLE IF NOT EXISTS`
  เหมือนโมดูลอื่นในรีโป ใส่ `this.logger.log(...)` บรรทัดสุดท้ายไว้ตรวจตอน deploy
  **อย่าพึ่ง `prisma migrate deploy`** — migration `delete_all_assignment_plans`
  ของรีโปนี้พังอยู่ก่อนแล้ว รันกับฐานข้อมูลใหม่ไม่ผ่าน

---

## กฎของโปรเจกต์ที่ต้องทำตาม

**อ่าน [`design/PROJECT_RULES.md`](../PROJECT_RULES.md) ให้จบก่อนเขียนโค้ด** — สรุปจาก
`CONTRIBUTING.md` และ `DEPLOYMENT.md` ของโปรเจกต์หลักเอง สรุปย่อ

| กฎ | รายละเอียด |
| --- | --- |
| **UI เป็นอังกฤษล้วน** | ห้ามฮาร์ดโค้ดภาษาไทยลง UI หรือรายงาน — mockup ในโฟลเดอร์นี้เขียนไทยไว้เพื่อสื่อสารเท่านั้น ตอนทำจริงแปลงป้ายเป็นอังกฤษทั้งหมด |
| **`user.role` ไม่ใช่ `activeRole`** | `CONTRIBUTING.md` ระบุตรง ๆ · `@Roles()` รับเฉพาะค่า enum · สิทธิ์ตามตำแหน่งใช้ `userGrants(...)` ใน service |
| **`emitChange('<resource>')`** | ทุก mutation ที่มีหน้าจอดูข้อมูลนั้นอยู่ ต้องเรียก ไม่งั้นหน้าไม่รีเฟรช |
| **schema + migration ขึ้นพร้อมกัน** | inline SQL ใน `applyPendingMigrations()` ถ้าขึ้นแค่ schema จะ 500 ทันที |
| **ไฟล์ใช้ `StorageService`** | ห้ามเขียนลงดิสก์ใน production |
| **ชื่อไฟล์ห้ามเป็นภาษาไทย** | ทำ Docker build พัง — ต้องอยู่ใน `.dockerignore` |

## ต้องผ่านก่อน push

**อ่าน [`design/PROJECT_RULES.md`](../PROJECT_RULES.md) หัวข้อ "ตรวจ build" ก่อน**

`nest build` ในเครื่องใช้ incremental cache แล้ว **มองไม่เห็น error** ที่ Docker build จะเจอ
`.vite` ที่ค้างจะทำให้ได้ bundle เก่า — **ต้องล้าง cache ก่อนถึงจะเชื่อผลได้**

```bash
cd api && npx prisma validate
rm -rf api/dist api/tsconfig.tsbuildinfo && (cd api && npx nest build)
rm -rf web/dist web/node_modules/.vite && (cd web && npx vite build)
```

แล้ว **นับคำในไฟล์ที่ build ออกมา เพื่อพิสูจน์ว่าไม่มีเมนูเดิมหาย**

```bash
cd web && B=$(cat dist/assets/*.js)
for s in "Lead Status" "Closed Deals" "Registration Report" "Advertising Requests" \
         "LINE Checker" "Staff Calendar" "Social Media" "Call Log"; do
  printf '%-24s %s\n' "$s" "$(printf '%s' "$B" | grep -c "$s")"
done
```

ทุกตัวต้องมากกว่า 0

## เรื่อง deploy

**อ่าน [`design/PROJECT_RULES.md`](../PROJECT_RULES.md) ให้จบก่อน deploy** —
สรุปกฎจากเอกสารของโปรเจกต์หลักเอง

```powershell
.\deploy.ps1
```

สคริปต์ตรวจว่า secret ครบก่อน แล้ว deploy เป็น **canary ที่ 0% traffic**

1. **อุ่นเครื่องก่อน** ยิง `https://canary---agency-care-oohrdxzlwq-df.a.run.app/api/health`
   ประมาณ 40 ครั้ง — migration รันเป็น background หลัง startup
   revision ที่ 0% จะไม่มีวันรันถ้าไม่มีใครเรียก
2. ยืนยันว่า migration รันแล้ว — หา `tables ready` ใน log
3. ค่อยสลับทราฟฟิก **แบบปักหมุด revision**

```bash
gcloud run services update-traffic agency-care --project gtg-crm-499607 \
  --region asia-east2 --to-revisions <REV>=100 --remove-tags canary
```

### 🚫 ห้ามใช้ `--to-latest`

หัวไฟล์ `deploy.ps1` เขียนไว้เองว่า *"Never use `update-traffic --to-latest` —
that is what let the wrong build take production."*
เคยเกิดขึ้นจริงแล้วครั้งหนึ่ง เมนูในระบบจริงหายไป 8 ตัว

### 🚫 อย่าประกอบคำสั่ง `gcloud run deploy` เอง

`--set-env-vars` และ `--set-secrets` **เขียนทับตัวแปรทั้งชุด** ตกตัวไหนตัวนั้นหลุด
เคยทำให้ `GCS_PRIVATE_BUCKET` หายและรูปที่อัปโหลดถูกทำลายถาวรมาแล้ว
`deploy.ps1` มี preflight ตรวจ secret ก่อน ใช้ตัวนั้น

แก้ตัวแปรทีละตัวใช้ `--update-env-vars` / `--update-secrets` (เติม ไม่ทับ)

### instance ต้องเป็น min = max = 1

`max=1` เพราะ socket.io ไม่มี Redis adapter · `min=1` เพราะงานตามเวลาเป็น `@Cron`
ในโปรเซส ถ้า scale to zero รายงาน LINE จะไม่ยิงเลยโดยไม่มีใครรู้

## สิ่งที่ต้องส่งมอบ

1. branch ใหม่แตกจาก `feat/all-appointments-clean-on-118a2e2`
2. PR เข้า branch เดิมนั้น พร้อมตารางสรุปว่าแตะไฟล์เดิมกี่บรรทัด เพิ่ม/ลบเท่าไหร่
3. ผลการตรวจทั้ง 5 อย่างข้างบน ใส่ไว้ในเนื้อ PR
4. **อย่าเพิ่ง deploy** รอให้เจ้าของงานสั่ง
