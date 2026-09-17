# คำสั่งสำหรับตัวหลัก — Requirement Baseline v1.0 (17 กันยายน)

> คัดลอกทั้งหน้านี้ไปวางได้เลย

---

Requirement ชุดนี้เปลี่ยน Agency Care จากระบบ CRUD ธรรมดา **เป็นระบบ workflow**
มี 8 เรื่อง แบ่งเป็น 4 โมดูลใหม่ และ 4 โมดูลที่ต่อยอดจากของเดิม

## branch ที่ต้องใช้

แตกจาก **`feat/all-appointments-clean-on-118a2e2`** เท่านั้น
**ห้ามใช้ `feat/crm-modules-jul-2026`**

```bash
git branch --show-current
```

## แบบที่ต้องทำตาม

Design canvas 9 แผ่น — https://claude.ai/artifact/2K6QoysNKhuVpBCScMh9xS

ไฟล์ต้นฉบับ: รีโป `chaithanin/agency-care2`
branch `claude/agency-care-test-project-zo163o` โฟลเดอร์ `design/requirements-sep17/`

**เริ่มที่ `Main.dc.html`** — แผ่นนั้นมีตารางฐานข้อมูลทั้งหมด ลำดับการทำ และกฎ 8 ข้อ

---

## ลำดับการทำ — เจ้าของงานกำหนดเอง ห้ามสลับ

```
1 Database Schema → 2 Workflow → 3 Permission → 4 API
→ 5 Notification → 6 UI → 7 QA Test Cases
```

**ห้ามเริ่มจากหน้า UI** เจ้าของงานระบุเองว่าจะลดการรื้อระบบภายหลัง

เสนอให้แยกเป็น **PR ละโมดูล** ไม่ใช่ PR เดียว 8 เรื่อง — งานนี้ใหญ่เกินกว่าจะ review รอบเดียวไหว

---

## ของเดิมที่มีอยู่แล้ว — สำรวจก่อน อย่าเขียนซ้ำ

| ตาราง / โมดูล | สภาพ | ต้องทำอะไร |
| --- | --- | --- |
| `PurchaseRequest` + `PrItem` + `PrComment` + `PrActivity` + `PrAttachment` | **ครบแล้ว** มี status `draft / submitted / waiting_approval / approved / purchasing / ordered / received / completed / cancelled` และ `approverId` `approvedAt` | เชื่อมกับสต็อกและการแจ้งเตือน ไม่ต้องสร้างใหม่ |
| `Unit` | มี `status` = `available / reserved / booked / sold` และผูก `project` | ใช้เป็นฐานของ Selling Quota |
| `PosmItem` + `PosmTransaction` | เป็น **สต็อกรวม** (`stockQty` ตัวเดียว) | ต้องแยกตามที่เก็บ — ดูข้อ 3 |
| `TrainingRecord` | เป็นบันทึกการเข้าอบรม ไม่ใช่ระบบคอร์สที่มีข้อสอบ | เพิ่มตารางใหม่ **ห้ามแตะของเดิม** มีข้อมูลย้อนหลังอยู่ |
| `NotificationSetting` / `Template` / `Log` | ค่ากลางตัวเดียวต่อประเภท | เพิ่มตารางค่าของแต่ละคน **ห้ามแตะของเดิม** |
| `Promotion` (3265) | โปรโมชันของบริษัท — คนละตัวกับ `AgencyPromotion` | อย่าสับสนสองตัวนี้ |
| Construction | **ไม่มีเลย** | ของใหม่ทั้งหมด |

---

## 1 · Construction Schedule Update

**ของใหม่ทั้งหมด**

Admin ตั้งได้เอง: Project · ความถี่ · วันครบกำหนดของแต่ละรอบ · เวลา deadline ·
ผู้รับผิดชอบ · ผู้อนุมัติ · เตือนก่อนถึงกำหนด · เตือนเมื่อเกินกำหนด

**ห้ามฮาร์ดโค้ดวันที่ 1 และ 16** — ระบบสร้างรอบถัดไปตามความถี่ แต่แก้วันของแต่ละรอบทีหลังได้

```
Upcoming → Due → Submitted → Under Review → Approved
                                    ↘ Overdue
```

- **Overdue เป็นสถานะที่คำนวณ ไม่ใช่เก็บเป็นคอลัมน์** — เลย deadline แล้วยังไม่ส่ง
- **เกินกำหนดแล้วยังต้องส่งได้** ห้ามล็อก แต่ต้องบันทึกว่าส่งช้ากี่วัน

ตาราง: `construction_schedules` · `construction_rounds` · `construction_round_items`

---

## 2 · Inventory Purchase Request

**ต่อยอดของเดิม — ตาราง `PurchaseRequest` มีครบแล้ว**

```
สต็อกถึง Minimum → แจ้งเตือน → สร้าง PR → Submit → Manager Review
→ Approve/Reject → Purchase → Receive → Update Stock
```

```
Draft → Pending Approval → Approved → Ordered → Received → Completed
              ↘ Rejected (ระบุเหตุผลบังคับ) → แก้ → Submit ใหม่
```

- **Manager เป็นผู้อนุมัติ** ตรวจฝั่ง server
- **Reject ต้องกรอกเหตุผล** ตรวจฝั่ง server ไม่ใช่แค่ required ในฟอร์ม
- **PR เดิมไม่ถูกลบตอนตีกลับ** เก็บประวัติทุกครั้งที่ส่ง
- **ตอนกด Received ต้องเพิ่มสต็อกเข้าที่เก็บที่ระบุในแต่ละรายการ**
  และสร้างธุรกรรม `receive` อัตโนมัติ ห้ามให้คนแก้ยอดเอง

เพิ่ม `stock_location_id` ใน `PrItem` ว่าของเข้าที่ไหน

---

## 3 · Inventory แยกสต็อกตามที่เก็บ

**เปลี่ยนโครงสร้างเดิม — ข้อนี้กระทบมากที่สุด**

```
Project → Location → Warehouse → Item
```

ของชิ้นเดียวกันอยู่ได้หลายที่

```
Marina Brochure (Marina Residence)
  Main Warehouse     500
  Marina Showroom    100
  Sales Office        50
  ──────────────────────
  รวม                650
```

ตารางใหม่: `stock_locations` · `stock_balances` (`@@unique(item_id, location_id)`) ·
`stock_transactions`

ธุรกรรม 6 ประเภท: `receive` · `issue` · `transfer` · `adjustment` · `distribution` · `return`

- **ห้ามลบ `PosmItem.stockQty`** ให้กลายเป็นค่าที่คำนวณจากผลรวมแทน
  หน้าจอเดิมที่อ่านฟิลด์นี้จะได้ไม่พัง
- **ห้าม UPDATE ยอดคงเหลือตรง ๆ** ทุกการเปลี่ยนต้องมีแถวใน `stock_transactions`
  ยอดคงเหลือคือผลรวมของธุรกรรม
- **Transfer สร้างสองแถว** ตัดจากต้นทาง เพิ่มที่ปลายทาง อยู่ใน transaction เดียวกัน
  ถ้าฝั่งใดฝั่งหนึ่งล้มเหลวต้อง rollback ทั้งคู่

---

## 4 · Brochure Distribution ต้องมีหลักฐาน

**ของใหม่**

บันทึก: Agency · Project · Item · จำนวน · วันที่ · ผู้ส่งมอบ · ผู้รับ · **ไฟล์หลักฐาน** · หมายเหตุ

รับ: รูปภาพ · PDF · ใบรับของ · เอกสารเซ็นรับ · รูปถ่ายตอนส่งของ

- **ต้องมีหลักฐานอย่างน้อย 1 ไฟล์ถึงจะบันทึกได้** ตรวจฝั่ง server
- **ไฟล์ลงถังส่วนตัวผ่าน `storage.savePrivate()` เท่านั้น** ไม่ใช่ถัง public
  และต้องมี `GCS_PRIVATE_BUCKET` ตอน deploy —
  ⚠️ **เคยหลุดมาแล้วและทำให้รูป Photo Evidence หายถาวร**
- บันทึกแล้วต้องตัดสต็อกจากที่เก็บที่ระบุ + สร้างธุรกรรม `distribution` + ผูกไฟล์กับธุรกรรมนั้น
- **ไฟล์หลักฐานลบไม่ได้** ไม่มี endpoint ลบ

ตาราง: `stock_distributions` · `stock_distribution_files`

---

## 5 · Promotion Selling Quota ผูกยูนิตจริง

**ต่อยอด — ใช้ตาราง `Unit` เดิม ห้ามสร้างตารางยูนิตใหม่**

โควตาคือ **รายชื่อยูนิต** ไม่ใช่ตัวเลข

```
Summer Campaign
  A101 Available · A102 Reserved · A103 Sold · A104 Available · A105 Sold
```

Dashboard คำนวณจากสถานะจริงของยูนิต

```
Total 20 · Available 8 · Reserved 4 · Sold 8 · Remaining 8
```

- **ห้ามเก็บโควตาเป็นตัวเลข** เช่น `quota: 20` ไม่งั้นตัวเลขจะไม่มีทางตรงกับความจริง
- **ห้ามเก็บสถานะยูนิตซ้ำในตารางโปรโมชัน** อ่านจาก `Unit.status` ตรง ๆ
- **ยูนิตหนึ่งอยู่ได้ทีละโปรโมชันเดียวในช่วงเวลาเดียวกัน** — `@@unique` ตอนที่ยัง active
- **ย้ายข้ามแคมเปญได้เฉพาะยูนิตที่ยัง Available** — Reserved หรือ Sold แล้วห้ามย้าย
  เพราะลูกค้าตกลงเงื่อนไขของแคมเปญเดิมไปแล้ว ตรวจฝั่ง server
- ทุกการย้ายเก็บประวัติ: ใครย้าย เมื่อไหร่ จากไหนไปไหน ตอนนั้นยูนิตสถานะอะไร

ตาราง: `promotion_quota_units` · `promotion_quota_history`

---

## 6 · Internal / External Message

**ของใหม่ — ข้อนี้เป็นเรื่องความปลอดภัยของข้อมูล**

โปรโมชันหนึ่งมีข้อความสองชุด

| | Internal | External |
| --- | --- | --- |
| ใครเห็น | Sales · Agency Support · Management | ทุกคนที่เข้าระบบได้ |
| ใครเขียน | Sales · Agency Support · Manager · Admin | Marketing · Manager · Admin |
| ส่งออกภายนอก | **ไม่ได้ — ไม่มี endpoint** | Manager · Admin เท่านั้น |

External ส่งได้ทาง LINE · Email · Social Media และต้องมี **Preview ก่อนส่ง**

- **ห้ามมี endpoint ที่ส่งข้อความ `scope = internal` ออกช่องทางภายนอก**
  ไม่ใช่แค่ซ่อนปุ่ม ต้องไม่มีทางเรียกได้เลย
- **ห้ามมีปุ่มคัดลอกจาก Internal ไป External**
- ทุกครั้งที่ส่งออกบันทึก: ช่องทาง เวลา ใครสั่ง ส่งให้ใคร ผลเป็นอย่างไร

ตาราง: `promotion_messages` (มี `scope`) · `promotion_message_sends`

---

## 7 · SOP / JD / Rules → Training & Test

**ของใหม่ + ต่อยอด**

```
SOP/JD/Rules → Course → Learning Material → 5 Questions
→ Submit → Score → Pass/Fail → Training Record
```

- คำถาม 5 ข้อต่อคอร์ส ตัวเลือก 4 ข้อ
- **ตั้ง Passing Score ได้** เช่น 80%
- เก็บประวัติ: Employee · Course · **Version** · วันเริ่ม · วันจบ · คะแนน ·
  ผ่านไม่ผ่าน · จำนวนครั้ง · ครั้งล่าสุด · ใบรับรอง

- **ผลสอบต้องผูกกับ version ของคอร์ส** แก้ SOP แล้วออกเวอร์ชันใหม่
  ผลเก่าต้องยังอ้างเนื้อหาชุดเดิมได้ ไม่งั้นตอบไม่ได้ว่าคนนี้สอบผ่านเนื้อหาชุดไหน
- **ห้ามแตะ `TrainingRecord` เดิม** มีข้อมูลอบรมย้อนหลังอยู่
- **ห้ามส่งเฉลยไปฝั่ง frontend** ตรวจคำตอบที่ server เท่านั้น

ตาราง: `training_courses` · `training_questions` · `training_assignments` · `training_attempts`

---

## 8 · Notification

**ต่อยอด — System + LINE + Email · ไม่ใช้ Microsoft Teams**

Event ที่ต้องมี: Lead (3) · Task (4) · Inventory (6) · Construction (5) ·
Promotion (5) · Training (5) รวม **28 event**

- **ผู้ใช้เลือกได้ว่า event ไหนส่งช่องทางไหน**
- **แอดมินตั้งค่าเริ่มต้นต่อ role ได้** ค่าของคนชนะค่าของ role เสมอ
- **ห้ามส่งซ้ำ** ใส่ `@@unique(event, target_user_id, ref_id)` ที่ระดับฐานข้อมูล
  ไม่ใช่เช็กในโค้ดอย่างเดียว เพราะ scheduler ที่รันซ้อนกันจะยิงซ้ำทันที
- **LINE ส่งได้เฉพาะคนที่ผูก `lineUserId` แล้ว** คนที่ยังไม่ผูกต้องแสดงว่า
  "ยังผูก LINE ไม่ได้" ในหน้าตั้งค่า ไม่ใช่ปล่อยให้ติ๊กแล้วเงียบหาย
- **ห้ามแตะ `NotificationSetting` เดิม**

ตาราง: `notification_events` · `notification_role_defaults` ·
`notification_user_prefs` · `notification_outbox`

---

## สิทธิ์

ตรวจฝั่ง server ทุก endpoint

⚠️ **ใช้ `user.role` ไม่ใช่ `user.activeRole`** —
`api/src/common/current-user.decorator.ts` เขียนกำกับไว้เองว่า
`role` = permanent role (for permission guards) และ
`activeRole` = current active role (for data scoping)

แอดมินมักทำงานโดยสลับเป็น sales อยู่ ถ้าตัดสินสิทธิ์จาก `activeRole` จะล็อกตัวเองออก

"Agency Support" ไม่ใช่ role แต่เป็น `Employee.position`
(`agency_support` / `agency_support_manager` / `businessman`)
แก้แบบเดียวกับที่ `management.service.ts` ทำอยู่

---

## ห้ามกระทบของเดิม

- **เพิ่มบรรทัดใหม่เท่านั้น** ห้ามลบหรือแก้เมนู route หรือฟังก์ชันที่มีอยู่
- ตารางใหม่สร้างตอนบูตผ่าน `PrismaService` แบบ `CREATE TABLE IF NOT EXISTS`
  ปิดท้ายด้วย `this.logger.log(...)` ไว้ตรวจตอน deploy
- **อย่าพึ่ง `prisma migrate deploy`** — migration `delete_all_assignment_plans` พังอยู่ก่อนแล้ว

## ต้องผ่านก่อน push (ทุก PR)

```bash
cd api && npx prisma validate && npx tsc --noEmit
cd ../web && npx tsc --noEmit && npx vite build
```

นับเมนูในไฟล์ที่ build ออกมา ทุกตัวต้องมากกว่า 0

```bash
cd web && B=$(cat dist/assets/*.js)
for s in "Lead Status" "Closed Deals" "Registration Report" "Advertising Requests" \
         "LINE Checker" "Staff Calendar" "Social Media" "Call Log"; do
  printf '%-24s %s\n' "$s" "$(printf '%s' "$B" | grep -c "$s")"
done
```

**และเขียน QA test case ของทุกเส้นทางสถานะ รวมเส้นที่ผิดพลาด** เช่น

- ย้ายยูนิตที่ Sold แล้ว → ต้องถูกปฏิเสธที่ server
- ส่ง internal message ออก LINE → ต้องไม่มี endpoint ให้เรียก
- โอนสต็อกมากกว่ายอดคงเหลือ → ต้องถูกปฏิเสธ ไม่ใช่ติดลบ
- บันทึก distribution โดยไม่แนบไฟล์ → ต้องถูกปฏิเสธ
- ส่ง notification ซ้ำ event เดิม → ฐานข้อมูลต้องปฏิเสธแถวที่สอง

## เรื่อง deploy

**ใช้ `.\deploy.ps1` ของ branch นี้เท่านั้น** อย่าประกอบคำสั่ง `gcloud run deploy` เอง

ตรวจว่ามี `GCS_PRIVATE_BUCKET` ก่อน deploy — โมดูล Distribution พึ่งตัวนี้

```bash
gcloud run services describe agency-care --region asia-east2 --format=json \
 | python3 -c "import sys,json
c=json.load(sys.stdin)['spec']['template']['spec']['containers'][0]
print([e['name'] for e in c.get('env',[]) if 'GCS' in e['name']])"
```

หลัง deploy สลับทราฟฟิกเอง

```bash
gcloud run services update-traffic agency-care --region asia-east2 --to-latest
```

## สิ่งที่ต้องส่งมอบ

1. **PR แยกต่อโมดูล** ไม่ใช่ PR เดียว 8 เรื่อง
2. ทุก PR แตกจาก `feat/all-appointments-clean-on-118a2e2`
3. ทุก PR มีตารางสรุปว่าแตะไฟล์เดิมกี่บรรทัด และผลการตรวจทั้งหมด
4. **อย่าเพิ่ง deploy** รอเจ้าของงานสั่ง

## เรื่องที่ยังต้องถามเจ้าของงาน

1. **Location กับ Warehouse เป็นคนละระดับ หรือระดับเดียวกัน** — แบบร่างทำเป็นระดับเดียว
   (`stock_locations` มีฟิลด์ `type`) ถ้าต้องแยกสองชั้นจริง ๆ ต้องเพิ่มตาราง
2. **ของที่อยู่ในสต็อกตอนนี้ (`PosmItem.stockQty`) จะย้ายเข้าที่เก็บไหน** — ต้องมีขั้นตอน
   ย้ายข้อมูลครั้งแรก ไม่งั้นยอดเดิมจะหายไปจากระบบใหม่
3. **Social Media ส่งออกยังไง** — ยังไม่มีการเชื่อมต่อในระบบ ถ้าจะส่งจริงต้องตั้งค่าเพิ่ม
   หรือทำเป็น "คัดลอกข้อความไปโพสต์เอง" ก่อน
4. **ใบรับรอง (Certificate) ออกยังไง** — ไฟล์ที่อัปเอง หรือระบบสร้าง PDF ให้
