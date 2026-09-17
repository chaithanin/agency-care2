# กฎของโปรเจกต์หลัก — อ่านก่อนเขียนโค้ดและก่อน deploy ทุกครั้ง

สรุปจากเอกสารของ `chaithanin/agency-care` เอง
branch `feat/all-appointments-clean-on-118a2e2` (= Cloud Run revision `agency-care-00886-nus`)

| ที่มา | เนื้อหา |
| --- | --- |
| `CONTRIBUTING.md` | แนวทางการเขียนโค้ด + PR checklist |
| `DEPLOYMENT.md` | โครงสร้าง production + กับดักตัวแปร |
| `DEPLOY.md` | ขั้นตอนตั้งค่าครั้งแรก |
| `deploy.ps1` | สคริปต์ deploy จริง มีคำเตือนเขียนไว้ในหัวไฟล์ |

**รีโปนี้ไม่มี `CLAUDE.md`** — `CONTRIBUTING.md` ทำหน้าที่แทน

---

## 1 · PR checklist ของโปรเจกต์ — 6 ข้อ

ลอกมาจาก `CONTRIBUTING.md` ตรง ๆ

- [ ] แก้ schema → ต้องมี inline migration คู่กัน และขึ้นไปพร้อมกัน
- [ ] มีตัวแปรใหม่ → ต้องบันทึกไว้ · คั่นด้วยจุลภาค · ห้าม commit ข้อความ placeholder
- [ ] `nest build` และ `vite build` แบบล้าง cache แล้วต้องผ่าน
- [ ] mutation ต้องเรียก `emitChange(...)` ถ้ามีหน้าจอที่ดูข้อมูลนั้นอยู่
- [ ] `@Roles(...)` ใช้ค่า enum เท่านั้น · สิทธิ์ระดับรายการต้องบังคับจริง
- [ ] **ห้ามฮาร์ดโค้ดภาษาไทยใน UI หรือรายงาน**

---

## 2 · เขียนโค้ด

### สิทธิ์

> **ใช้ `user.role` สำหรับตรวจสิทธิ์ ไม่ใช่ `activeRole`**
> — `CONTRIBUTING.md`

`api/src/common/current-user.decorator.ts` เขียนกำกับไว้เองว่า

```ts
role: UserRole;       // permanent role (for permission guards)
activeRole: UserRole; // current active role (for data scoping)
```

แอดมินมักทำงานโดยสลับเป็น sales ถ้าตัดสินสิทธิ์จาก `activeRole` จะล็อกตัวเองออก

- `@Roles(...)` **รับเฉพาะค่าใน enum `UserRole`**
- สิทธิ์ตามตำแหน่งงาน (เช่น Agency Support) ใช้ `userGrants(...)` ใน service
  ไม่ใช่ `@Roles` — "Agency Support" เป็น `Employee.position` ไม่ใช่ role

### ภาษา

**UI และรายงานเป็นภาษาอังกฤษล้วน** i18n บังคับอังกฤษเป็นฐาน ที่เหลือใช้ Google Translate
**ห้ามฮาร์ดโค้ดภาษาไทยลง UI**

> คอมเมนต์ในโค้ดเป็นภาษาไทยได้ และควรคงไว้ตรงที่มีอยู่แล้ว — เขียนให้กลมกลืนกับโค้ดรอบข้าง
> แต่ **ข้อความที่ผู้ใช้เห็น ต้องเป็นอังกฤษ**

Mockup ในโฟลเดอร์ `design/` เขียนเป็นไทยเพื่อสื่อสารกันเท่านั้น
**ตอนทำจริงให้แปลงป้ายทุกอันเป็นอังกฤษ**

### Migration

**ไม่ใช้ `prisma migrate` ใน production** เป็น inline SQL ใน
`api/src/prisma/prisma.service.ts` → `applyPendingMigrations()` รันทุกครั้งที่บูต

เพิ่มคอลัมน์ต้องทำสองที่ **และขึ้นไปพร้อมกัน**

1. เพิ่มฟิลด์ใน `api/prisma/schema.prisma`
2. เพิ่ม `ALTER TABLE "<table>" ADD COLUMN IF NOT EXISTS "<col>" <type>` ใน `applyPendingMigrations()`

ค่า enum ใหม่ใช้ `ALTER TYPE "<Enum>" ADD VALUE IF NOT EXISTS '<value>'`

> ถ้าขึ้นแค่ schema แต่ลืม migration — `findMany` ที่ไม่มี `select` จะ 500 ทันที

### อื่น ๆ

- ไฟล์ใช้ `StorageService` เท่านั้น **ห้ามเขียนลงดิสก์ใน production**
- หลัง mutation เรียก `RealtimeGateway.emitChange('<resource>')` ให้ client รีเฟรช
  ฝั่ง client subscribe ด้วย `useRealtime`
- แตกงานจาก default branch · ไม่ commit หรือ push จนกว่าจะถูกสั่ง
- **ห้าม commit secret หรือ `.env`**

---

## 3 · ตรวจ build — กับดักที่พังบ่อยที่สุดของรีโปนี้

`nest build` ในเครื่องใช้ incremental cache แล้ว **มองไม่เห็น error** ที่ Docker build จะเจอ
(import หาย · ค่า enum ผิด) ส่วน `.vite` ที่ค้างจะทำให้ได้ bundle เก่า

**ต้องล้าง cache ก่อนถึงจะเชื่อผลได้**

```bash
rm -rf api/dist api/tsconfig.tsbuildinfo && (cd api && npx nest build)
rm -rf web/dist web/node_modules/.vite && (cd web && npx vite build)
```

`npx tsc --noEmit` อย่างเดียว **ไม่พอ**

---

## 4 · Deploy — ห้ามทำผิดขั้นตอน

### production เป็นอะไร

| | |
| --- | --- |
| Service | `agency-care` · region `asia-east2` · project `gtg-crm-499607` |
| DB | Cloud SQL Postgres `agency-care-db` (f1-micro) |
| Domain | `agency.chaithanin.com` |
| รูปแบบ | Docker container เดียว เสิร์ฟทั้ง NestJS API และ React bundle |

### ขั้นตอน

```powershell
.\deploy.ps1
```

สคริปต์จะ

1. **ตรวจว่า secret ครบทุกตัวก่อน** ขาดตัวไหนหยุดทันที ไม่ deploy ครึ่ง ๆ กลาง ๆ
2. deploy เป็น **canary ที่ 0% traffic** (`--no-traffic --tag canary`)
3. พิมพ์ชื่อ revision กับคำสั่งสลับทราฟฟิกให้

จากนั้น

```
1) อุ่นเครื่องก่อน — migration รันเป็น background หลัง startup
   revision ที่ 0% จะไม่มีวันรันถ้าไม่มีคนเรียก ยิงประมาณ 40 ครั้ง
   https://canary---agency-care-oohrdxzlwq-df.a.run.app/api/health

2) ยืนยันว่า migration รันแล้ว
   gcloud run services logs read agency-care --project gtg-crm-499607 \
     --region asia-east2 | grep "tables ready"

3) ค่อยสลับทราฟฟิก แบบปักหมุด revision
   gcloud run services update-traffic agency-care --project gtg-crm-499607 \
     --region asia-east2 --to-revisions <REV>=100 --remove-tags canary
```

ย้อนกลับ: คำสั่งเดิม แต่ใส่ชื่อ revision ก่อนหน้า

### 🚫 ห้ามใช้ `--to-latest`

หัวไฟล์ `deploy.ps1` เขียนไว้ว่า

> **Never use `update-traffic --to-latest` — that is what let the wrong build take production.**

เคยเกิดขึ้นจริงครั้งหนึ่งแล้ว เมนูในระบบจริงหายไป 8 ตัว เพราะทราฟฟิกถูกสลับไป build
ของอีก branch **ต้องปักหมุด revision ที่ตรวจแล้วเท่านั้น**

### 🚫 `--set-env-vars` และ `--set-secrets` เขียนทับทั้งชุด

หัวไฟล์ `deploy.ps1` เขียนไว้ว่า

> Anything not on those lines is dropped from the new revision. This is how
> `GCS_PRIVATE_BUCKET` was lost once before: uploads then went to container disk
> and were destroyed for good on the next revision.

- **อย่าประกอบคำสั่ง `gcloud run deploy` เอง** ใช้ `deploy.ps1` ที่มี preflight
- แก้ตัวแปรทีละตัวใช้ `--update-env-vars` / `--update-secrets` (เติม ไม่ทับ)
- คั่นด้วย **จุลภาค** ไม่ใช่เว้นวรรค — เว้นวรรคทำให้ทุกอย่างยัดเข้าตัวแรก
- **ห้ามบันทึกข้อความ placeholder** อย่าง `<token>` ลงไปจริง

### instance ต้องเป็น min = max = 1

```bash
gcloud run services update agency-care --region asia-east2 --project gtg-crm-499607 \
  --min-instances=1 --max-instances=1
```

- **`max=1`** — socket.io ไม่มี Redis adapter มากกว่า 1 instance แล้ว emit ข้ามเครื่องไม่ถึง
- **`min=1`** — งานตามเวลาเป็น `@Cron` ในโปรเซส ถ้า scale to zero
  **รายงาน LINE และ broadcast จะไม่ยิงเลยโดยไม่มีใครรู้**

### deploy ทีเดียว อย่ายิงรัว

f1-micro มี connection น้อย ตอน revision เก่ากับใหม่ทับกันจะรั่ว
("Too many database connections" — หายเอง แต่ผู้ใช้เจอ error จริง)

### ตรวจหลัง deploy

```bash
curl -s -o /dev/null -w "%{http_code}\n" https://agency-care-oohrdxzlwq-df.a.run.app/api/health

gcloud logging read 'resource.type="cloud_run_revision"
  AND resource.labels.service_name="agency-care"
  AND (severity>=ERROR OR textPayload:"Nest application successfully started")' \
  --project gtg-crm-499607 --limit 5 --freshness=5m --format="value(textPayload)"

JS=$(curl -s https://agency-care-oohrdxzlwq-df.a.run.app/ \
     | grep -oE '/assets/index-[A-Za-z0-9_]+\.js' | head -1)
curl -s "https://agency-care-oohrdxzlwq-df.a.run.app$JS" | grep -c 'STRING_ที่เพิ่งเพิ่ม'
```

### ชื่อไฟล์ภาษาไทยทำ build พัง

ชื่อไฟล์ที่ไม่ใช่ ASCII ใน Docker build context ทำให้ Cloud Run
`ContainerImageImportFailed` — เอกสารที่ชื่อเป็นไทยต้องอยู่ใน `.dockerignore`

`deploy.ps1` เองก็ต้องเป็น ASCII ล้วน เพราะ PowerShell 5.1 อ่านไฟล์ที่ไม่มี BOM
เป็น ANSI แล้ว parse พัง

---

## 5 · เรื่องที่ยังค้างอยู่ในระบบจริง

| เรื่อง | สภาพ |
| --- | --- |
| `LINE_CHANNEL_SECRET` | **ยังไม่มีใน production** และ webhook เป็น fail-open (`if (secret && signature)`) รับ request ที่ไม่มีลายเซ็นได้ ตอนนี้เส้นทางนั้นเขียนข้อมูลลงฐานข้อมูลได้แล้ว |
| migration ที่พัง | `api/prisma/migrations/delete_all_assignment_plans/migration.sql` อ้างตารางที่ไม่มี — `prisma migrate deploy` รันไม่ผ่านกับฐานข้อมูลใหม่ (ไม่กระทบ เพราะใช้ inline migration) |
| `Layout.tsx` | ประกาศ `/agency-transfers` ซ้ำสองครั้ง ทำให้ React ขึ้น warning เรื่อง key ซ้ำ |
