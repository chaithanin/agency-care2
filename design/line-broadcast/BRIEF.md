# คำสั่งสำหรับตัวหลัก — LINE Contacts & Audience Management

> คัดลอกทั้งหน้านี้ไปวางได้เลย

---

ต่อยอด **LINE Broadcast Center** ที่มีอยู่ ให้มีระบบจัดการผู้ติดตาม LINE OA แบบรวมศูนย์
ทุกคนที่ Add Friend ต้องถูกเก็บเป็น contact และจัดประเภทเป็น
**Sales / Customer / Agency / Unclassified**
ตอนสร้าง broadcast ต้องเลือกกลุ่มเป้าหมายได้ พร้อมดูรายชื่อผู้รับก่อนส่ง และเก็บประวัติว่าส่งหาใครบ้าง

## branch ที่ต้องใช้ — อ่านก่อนเริ่ม

แตกงานจาก **`feat/all-appointments-clean-on-118a2e2`** เท่านั้น
คือสายที่ระบบจริงใช้อยู่ (= Cloud Run revision `agency-care-00886-nus`)

**ห้ามใช้ `feat/crm-modules-jul-2026`** เป็นคนละสายพัฒนาที่ตัดเมนูไปหลายตัว
เคย deploy จากสายนั้นแล้วเมนูในระบบจริงหายไป 8 ตัว

```bash
git branch --show-current     # ต้องเป็น feat/all-appointments-clean-on-118a2e2
```

---

## แบบที่ต้องทำตาม

Design canvas 10 หน้าจอ — https://claude.ai/artifact/PhCT772zZs3T9AAyFx4W6H

ไฟล์ต้นฉบับอยู่ที่รีโป `chaithanin/agency-care2`
branch `claude/agency-care-test-project-zo163o` โฟลเดอร์ `design/line-broadcast/`
อ่าน `README.md` ในโฟลเดอร์นั้นก่อน

| อาร์ตบอร์ด | คือหน้าอะไร |
| --- | --- |
| `Main.dc.html` | Overview — audience counter, แจ้งเตือน unclassified, โควตา |
| `Contacts.dc.html` | แท็บ Contacts |
| `ContactDetail.dc.html` | จัดบทบาทและผูกกับ CRM |
| `Step1Audience.dc.html` / `CustomSelection.dc.html` | ขั้นที่ 1 |
| `Step2Message.dc.html` / `Step3Preview.dc.html` / `Step4Send.dc.html` | ขั้นที่ 2–4 |
| `History.dc.html` | Send History |
| `DataModel.dc.html` | โครงสร้างฐานข้อมูลและกฎ 8 ข้อ |

สี ขนาด และฟอนต์ในแบบ ดึงจาก `web/src/theme/ThemeContext.tsx` โหมด dark ของรีโปนี้อยู่แล้ว
ใช้ค่าตามนั้นได้เลย ไม่ต้องปัดเลข

---

## สำรวจก่อน — ของหลายอย่างมีอยู่แล้ว อย่าเขียนซ้ำ

| มีอยู่แล้ว | ไฟล์ | ต้องทำอะไรต่อ |
| --- | --- | --- |
| รับ `follow` event | `api/src/notification/line-webhook.controller.ts:77` | ตอนนี้แค่ log กับตอบข้อความ — ต้องสร้าง contact record ด้วย |
| รับ `unfollow` event | บรรทัด 84 | ตอนนี้ล้าง `employee.lineUserId` — ต้องตั้ง contact เป็น `inactive` **ห้ามลบแถว** |
| ดึงโปรไฟล์ผู้ใช้ | `line.service.ts:43` `getProfile()` | ใช้ได้เลย ไม่ต้องเขียนใหม่ |
| ส่งข้อความ | `line.service.ts` `pushText()` / `pushFlex()` | ใช้ได้เลย |
| เช็กโควตาส่ง | `line.service.ts:75` `quota()` | เอามาโชว์ในหน้า Overview ได้ |
| ผูก LINE ของเอเจนซี่ | `agency.service.ts:1116` ส่งโค้ด `AG-XXXXXX` หาบอท | ใช้กลไกเดิม ให้ contact อ้าง `agency_id` ที่ผูกไว้แล้ว |
| ผูก LINE ของพนักงาน | `auth.service.ts` LIFF + `employee.lineUserId` | ใช้กลไกเดิม |
| ตาราง Broadcast | `schema.prisma:1738` | ขยาย ไม่ใช่สร้างใหม่ |
| หน้า Broadcast | `web/src/pages/BroadcastPage.tsx:310` | มี 4 แท็บแล้ว: Overview / Send History / Templates / Analytics |

**แท็บ CONTACTS แทรกเป็นแท็บที่ 2** → `OVERVIEW | CONTACTS | SEND HISTORY | TEMPLATES | ANALYTICS`

---

## ฐานข้อมูล

### ตารางใหม่ — แยกสองตาราง

คนหนึ่งเป็นได้หลายบทบาท (เจ้าของเอเจนซี่ที่ซื้อห้องเองด้วย เป็นทั้ง Agency และ Customer)
จึงแยก "ตัวคน" ออกจาก "บทบาท" ตั้งแต่แรก — เปลี่ยนทีหลังแพงกว่ามาก

#### `line_contacts` — ตัวคน หนึ่งแถวต่อหนึ่ง LINE User

```
id                  String  @id @default(cuid())
lineUserId          String  @unique
displayName         String?
pictureUrl          String?

phone               String?
email               String?
language            String?
nationality         String?
projectInterest     String[] @default([])

followedAt          DateTime
unfollowedAt        DateTime?
lastInteractionAt   DateTime?
status              String  @default("active")   // active | blocked | inactive
tags                String[] @default([])
createdAt / updatedAt

roles               LineContactRole[]
```

index: `lineUserId` unique · `status`

#### `line_contact_roles` — บทบาท หนึ่งแถวต่อหนึ่งบทบาท

```
id                String  @id @default(cuid())
lineContactId     String   -> LineContact  (onDelete: Cascade)
contactType       String            // sales | customer | agency | partner | other

customerLeadId    String?  -> CustomerLead    (เมื่อ type = customer)
agencyId          String?  -> Agency          (เมื่อ type = agency)
employeeId        String?  -> Employee        (เมื่อ type = sales)
position          String?                     // ตำแหน่งในเอเจนซี่
assignedSellerId  String?  -> Employee

isPrimary         Boolean @default(false)
classifiedById    String?  -> User
classifiedAt      DateTime?
createdAt / updatedAt

@@unique([lineContactId, contactType])
```

index: `contactType` · `agencyId` · `customerLeadId` · `employeeId`

#### Unclassified คือ "ไม่มีบทบาท"

**ไม่ต้องมี `contactType = 'unclassified'`** — contact ที่ยังไม่มีแถวใน
`line_contact_roles` เลย คือ Unclassified โดยนิยาม

นับด้วย

```sql
SELECT COUNT(*) FROM line_contacts c
WHERE c.status = 'active'
  AND NOT EXISTS (SELECT 1 FROM line_contact_roles r WHERE r.line_contact_id = c.id);
```

ทำให้ไม่มีทางเกิดสถานะกำกวมแบบ "มีบทบาท Customer แต่ยังเป็น unclassified อยู่"

### ขยาย `Broadcast` (ตารางเดิม เพิ่มคอลัมน์ ห้ามแก้ของเดิม)

```
audienceType        String  @default("all")
                            // sales | customer | agency | all | custom
audienceFilter      Json?   // เก็บเงื่อนไขของ Custom Selection
includeUnclassified Boolean @default(false)
```

> `recipientType` เดิมยังอยู่ ใช้กับผู้รับที่เป็นพนักงานเหมือนเดิม
> `audienceType` เป็นตัวใหม่สำหรับกลุ่ม LINE — อย่าลบหรือเปลี่ยนความหมายของเดิม

### ขยาย `BroadcastRecipient`

ตอนนี้มี FK ไป `Employee` อย่างเดียว ในโค้ดเขียนกำกับไว้เองว่า

> "agency มี lineUserId ต่างหาก; ไม่มี BroadcastRecipient FK จึงไม่บันทึกรายตัว"
> — `broadcast.service.ts:23`

แก้โดย **เพิ่มคอลัมน์ ไม่ใช่เขียนตารางใหม่**

```
lineContactId   String?   -> LineContact      (เพิ่มใหม่)
matchedRoles    String[] @default([])         (snapshot — role ที่ทำให้เข้าเกณฑ์ ตอนส่ง)
employeeId      String?                       (เปลี่ยนจากบังคับเป็นไม่บังคับ)
readAt          DateTime?

@@unique([broadcastId, lineContactId])        (กันส่งซ้ำที่ระดับฐานข้อมูล)
```

**สำคัญ — เก็บ snapshot ตอนส่ง** `matchedRoles` เก็บว่า ณ ตอนส่ง คนนี้เข้าเกณฑ์
เพราะ role อะไรบ้าง เช่น `["customer","agency"]` — ไม่ใช่เก็บแค่ `audienceType`
ระดับ broadcast เพราะบทบาทเปลี่ยนได้ แต่ประวัติต้องตอบได้เสมอว่า
"ครั้งนั้นส่งหาใครบ้าง และเขาเข้าเกณฑ์ด้วยบทบาทอะไร"

`@@unique` ตัวนี้เป็นตาข่ายกันพลาดของกฎข้อ 7 — ถ้าโค้ดเผลอวนส่งจาก role
ฐานข้อมูลจะปฏิเสธแถวที่สอง แทนที่จะปล่อยให้ลูกค้าได้ข้อความซ้ำ

---

## กฎที่ห้ามทำผิด

### 1. คนใหม่เข้า Unclassified เสมอ — ห้ามเดา

`follow` event เข้ามา → สร้างแถวใน `line_contacts` **โดยไม่สร้าง role เลย**
(= Unclassified) ห้ามเดาจากชื่อ รูป หรืออะไรก็ตาม

ยกเว้นกรณีเดียว: `lineUserId` ตรงกับ `employee.lineUserId` หรือ `agency.lineUserId`
ที่ผูกไว้แล้ว → สร้าง role `sales` / `agency` ให้เลย เพราะมีหลักฐานการผูกจากระบบ

### 2. Sales ต้องมาจากฐานพนักงานเท่านั้น

ห้ามให้คนนอกเลือกเองว่าเป็น Sales
role `sales` สร้างได้เฉพาะเมื่อ `employeeId` ไม่ว่าง
ตรวจฝั่ง server ด้วย ไม่ใช่แค่ซ่อนตัวเลือกในหน้าเว็บ

### 3. All ไม่รวม Unclassified

`audienceType = 'all'` = Sales + Customer + Agency **ไม่รวม Unclassified**
จะรวมต้องติ๊ก `includeUnclassified` และ **เฉพาะ Manager กับ Admin เท่านั้น**
ที่ติ๊กได้ — ตรวจฝั่ง server

### 4. ข้อความภายในห้ามหลุดออกนอก

`Broadcast.type` เดิมมี `hr` / `it` / `training` — พวกนี้เป็นเรื่องภายใน
**ถ้า `type` เป็นสามตัวนี้ ต้องส่งได้เฉพาะ `audienceType = 'sales'`**
ปฏิเสธที่ server ถ้าพยายามส่งหา customer หรือ agency

**เจ้าของงานยืนยันแล้วว่าเอากฎนี้** — ปฏิเสธที่ server ไม่ใช่แค่ซ่อนตัวเลือกในหน้าเว็บ

### 5. unfollow ห้ามลบข้อมูล

ตั้ง `status = 'inactive'` และ `unfollowedAt` เก็บแถวไว้
ประวัติการส่งต้องยังอ้างถึงคนนี้ได้

### 6. Agency เก็บเป็นหลายคน ไม่ใช่คนเดียว

เอเจนซี่หนึ่งรายมีได้หลาย contact (Owner, Sales Manager, Agent) ทุกคนมี role
`agency` ที่ชี้ `agencyId` เดียวกัน เก็บตำแหน่งไว้ใน `position`
เพื่อให้อนาคตเลือกส่งแบบ Selected Agency หรือ Agency Owner Only ได้

### 7. คนซ้ำต้องได้รับข้อความครั้งเดียว

คนที่มีทั้ง role `customer` และ `agency` พอเลือก All หรือเลือกสองกลุ่มพร้อมกัน
**ต้องได้ข้อความใบเดียว ไม่ใช่สองใบ**

ให้ query ระดับ `line_contacts` แล้วใช้ `DISTINCT` หรือ `EXISTS` เสมอ
ห้าม query จาก `line_contact_roles` ตรง ๆ แล้ววนส่ง — จะส่งซ้ำทันที

ใน `broadcast_recipients` ก็เก็บแถวเดียวต่อหนึ่งคนต่อหนึ่ง broadcast
ใส่ `@@unique([broadcastId, lineContactId])` กันพลาดที่ระดับฐานข้อมูลด้วย
ส่วน role ที่ทำให้เขาเข้าเกณฑ์ ให้เก็บเป็น array ใน snapshot

### 8. blocked และ inactive ไม่นับและไม่ส่ง

ทุก counter และทุก audience นับเฉพาะ `status = 'active'`
คนที่บล็อก OA หรือเลิกติดตามแล้ว **ไม่นับใน Audience counter และไม่ถูกส่ง**

หน้า Preview ขั้นที่ 3 ยังต้องบอกจำนวนที่ถูกตัดออกให้เห็น
(blocked กี่คน · inactive กี่คน · unclassified กี่คน) เพื่อให้คนส่งรู้ว่าหายไปไหน

---

## สิ่งที่ต้องทำ

### แท็บ CONTACTS

ตาราง: Profile (รูป + ชื่อ) · Type · Company · Status · Followed Since · Last Activity

คอลัมน์ **Type แสดงได้หลายป้ายในแถวเดียว** เช่นคนที่เป็นทั้งสองอย่างขึ้น
`Agency` `Customer` เรียงกัน — ไม่ใช่เลือกมาแสดงอันเดียว
คอลัมน์ Company แสดงชื่อเอเจนซี่จาก role `agency` ถ้ามี
ตัวกรอง: Search / All Types / Status / Project / Agency / Assigned Seller
เลือกหลายแถวแล้วทำพร้อมกัน: Change Type · Add Tag · Send Message
แถว Unclassified ขึ้นป้ายเตือน **⚠ Review**

### การจัดประเภท

กดที่ contact → **เพิ่มบทบาท** ได้หลายอัน และลบทีละอันได้
(ไม่ใช่เปลี่ยนค่าเดียว) → ตอนเพิ่มบทบาท

- **Customer** → ค้นหา `CustomerLead` ที่เบอร์หรืออีเมลตรงกัน เสนอเป็น Possible Match ให้กด Link
- **Agency** → เลือก Agency + ตำแหน่ง + Assigned Seller
- **Sales** → เลือกจากรายชื่อพนักงานเท่านั้น

บันทึก `classifiedById` และ `classifiedAt` ในแถว role ทุกครั้งที่เพิ่มหรือแก้

ลบบทบาทสุดท้ายออก → contact กลับไปเป็น Unclassified เอง ไม่ต้องตั้งค่าอะไรเพิ่ม

### Overview — Audience counter

`ALL CONTACTS / SALES / CUSTOMERS / AGENCIES / UNCLASSIFIED`
กดแล้วเข้าแท็บ Contacts พร้อม filter · Unclassified ใช้สีเตือน

นับเฉพาะ `status = 'active'` ทุกช่อง

**ระวัง — ตัวเลขทับซ้อนกันได้** คนหนึ่งมีได้หลาย role ดังนั้น
SALES + CUSTOMERS + AGENCIES + UNCLASSIFIED **อาจมากกว่า** ALL CONTACTS

- `ALL CONTACTS` = จำนวน**คน** ที่ active (นับหัวไม่ซ้ำ)
- ช่องอื่น = จำนวนคนที่มี role นั้น

ใส่คำอธิบายสั้น ๆ ใต้แถวการ์ดว่า "คนหนึ่งอาจอยู่ได้มากกว่าหนึ่งกลุ่ม"
ไม่งั้นคนใช้จะคิดว่าตัวเลขผิด

### New Announcement — 4 ขั้น

```
1 Audience → 2 Message → 3 Preview → 4 Send / Schedule
```

- **ขั้น 1** เลือก Sales / Customers / Agencies / All / Custom Selection
  แสดงจำนวนผู้รับทันทีที่เลือก
- **Custom Selection** กรองด้วย Contact Type, Project Interest, Language, Agency,
  Assigned Seller — นับผู้รับแบบ real-time พร้อมปุ่ม View Recipient List
- **ขั้น 3 Preview** แสดงตัวอย่างข้อความ + สรุปผู้รับ แยกจำนวนตาม type
  และบอกจำนวนที่ถูกตัดออก (blocked / inactive / unclassified)

### Send History

เปลี่ยนจาก `Sent to 1 recipient` เป็น

```
MARINA SEPTEMBER UPDATE                    [Agencies]
Audience: Agencies · Recipients 284
Delivered 278 · Failed 6 · Read 64%
By SystemAdmin · 16/09/2026 14:30
```

### Welcome Message — จัดประเภทอัตโนมัติ

ตอบ `follow` ด้วยปุ่มให้เลือก

| ปุ่ม | ตั้ง contactType เป็น |
| --- | --- |
| I'm looking for a property | `customer` |
| I'm a property agent / agency | `agency` (ยังไม่ผูก agencyId รอคนยืนยัน) |
| Other | `unclassified` |

**ไม่มีปุ่ม Sales** — ตามกฎข้อ 2

---

## ข้อจำกัดของ LINE ที่ต้องเช็กก่อนเขียน

| เรื่อง | ข้อเท็จจริง |
| --- | --- |
| `GET /v2/bot/profile/{userId}` | ใช้ได้เฉพาะคนที่เป็นเพื่อนกับ OA อยู่ — คนที่ block แล้วดึงไม่ได้ ต้องรับ error ให้ได้ |
| ดึงรายชื่อ follower ทั้งหมด | endpoint นี้จำกัดเฉพาะบัญชีบางประเภท (verified / premium) **อย่าออกแบบให้ระบบพึ่งมัน** |
| วิธีที่ปลอดภัยที่สุด | เริ่มบันทึกตั้งแต่ `follow` webhook เข้ามา แล้วค่อยเพิ่ม sync ทีหลังถ้าบัญชีรองรับ |
| โควตาส่ง | มี `quota()` อยู่แล้ว — เช็กก่อนส่งกลุ่มใหญ่ ถ้าไม่พอให้เตือนก่อน ไม่ใช่ส่งแล้วพังกลางทาง |
| จำนวนต่อครั้ง | โค้ดเดิมแบ่ง batch อยู่แล้วใน `broadcast.service.ts` ใช้แบบเดิม |

**ข้อมูลส่วนบุคคล** — contact ที่เป็นลูกค้าคือข้อมูลส่วนบุคคล
เก็บเท่าที่ใช้จริง และอย่า log เบอร์ อีเมล หรือชื่อลงใน Cloud Logging

---

## สิทธิ์

ตรวจฝั่ง server ทุก endpoint ตัดสินจาก `req.user.activeRole` (role ที่สลับอยู่)
ไม่ใช่ role ในโปรไฟล์ — ตรงกับที่โมดูลอื่นในรีโปทำอยู่

| การกระทำ | ใครทำได้ |
| --- | --- |
| ดูรายชื่อ contact | Admin, Manager, Agency Support, Seller |
| จัดประเภท / ผูกกับ Lead หรือ Agency | Admin, Manager, Agency Support |
| ตั้ง contactType = sales | Admin, Manager |
| ติ๊ก Include Unclassified | Admin, Manager |
| ส่ง broadcast หา customer หรือ agency | Admin, Manager |

---

## ห้ามกระทบของเดิม

- **เพิ่มบรรทัดใหม่เท่านั้น** ห้ามลบหรือแก้เมนู route หรือฟังก์ชันที่มีอยู่
- `recipientType` เดิมของ Broadcast ต้องยังทำงานเหมือนเดิมทุกประการ
- ตารางใหม่สร้างตอนแอปบูตผ่าน `PrismaService` แบบ `CREATE TABLE IF NOT EXISTS`
  เหมือนโมดูลอื่นในรีโป ใส่ `this.logger.log(...)` บรรทัดสุดท้ายไว้ตรวจตอน deploy
- **อย่าพึ่ง `prisma migrate deploy`** — migration `delete_all_assignment_plans`
  ของรีโปนี้พังอยู่ก่อนแล้ว รันกับฐานข้อมูลใหม่ไม่ผ่าน
- การเปลี่ยน `BroadcastRecipient.employeeId` จากบังคับเป็นไม่บังคับ
  เป็นการผ่อนเงื่อนไข ข้อมูลเดิมไม่เสีย แต่ต้องเขียนเป็น `ALTER COLUMN ... DROP NOT NULL`
  ในตัว bootstrap ด้วย ไม่ใช่แค่แก้ schema.prisma

---

## ต้องผ่านก่อน push

```bash
cd api && npx prisma validate && npx tsc --noEmit
cd ../web && npx tsc --noEmit && npx vite build
```

แล้ว **นับคำในไฟล์ที่ build ออกมา เพื่อพิสูจน์ว่าไม่มีเมนูเดิมหาย**

```bash
cd web && B=$(cat dist/assets/*.js)
for s in "Lead Status" "Closed Deals" "Registration Report" "Advertising Requests" \
         "LINE Checker" "Staff Calendar" "Social Media" "Call Log" "LINE Broadcast"; do
  printf '%-24s %s\n' "$s" "$(printf '%s' "$B" | grep -c "$s")"
done
```

ทุกตัวต้องมากกว่า 0

**ทดสอบ follow webhook โดยไม่ต้องรอคนจริง**

```bash
curl -X POST http://localhost:3000/api/line/webhook \
  -H 'Content-Type: application/json' \
  -d '{"events":[{"type":"follow","source":{"userId":"Utest123"},"replyToken":"x"}]}'
```

(ต้องใส่ header ลายเซ็นให้ถูกตามที่ `line-webhook.controller.ts:38` ตรวจ
หรือทดสอบผ่าน unit test ของ controller แทน)

---

## เรื่อง deploy

**ใช้ `.\deploy.ps1` ของ branch นี้เท่านั้น** อย่าประกอบคำสั่ง `gcloud run deploy` เอง —
`--set-env-vars` และ `--set-secrets` เขียนทับตัวแปรทั้งชุด ตกตัวไหนตัวนั้นหลุด
เคยเกิดกับ `GCS_PRIVATE_BUCKET` แล้วรูปที่อัปโหลดหายถาวร

โมดูลนี้ต้องมี secret สองตัว ตรวจว่ามีครบก่อน deploy

```bash
gcloud run services describe agency-care --region asia-east2 --format=json \
 | python3 -c "import sys,json
c=json.load(sys.stdin)['spec']['template']['spec']['containers'][0]
print([e['name'] for e in c.get('env',[]) if 'LINE' in e['name']])"
```

ต้องเห็น `LINE_CHANNEL_ACCESS_TOKEN` (ส่งข้อความ) และ `LINE_CHANNEL_SECRET`
(ตรวจลายเซ็น webhook — ขาดตัวนี้ follow event จะถูกปฏิเสธหมด)

หลัง deploy ต้องสลับทราฟฟิกเอง

```bash
gcloud run services update-traffic agency-care --region asia-east2 --to-latest
```

---

## สิ่งที่ต้องส่งมอบ

1. branch ใหม่แตกจาก `feat/all-appointments-clean-on-118a2e2`
2. PR เข้า branch เดิมนั้น พร้อมตารางสรุปว่าแตะไฟล์เดิมกี่บรรทัด เพิ่ม/ลบเท่าไหร่
3. ผลการตรวจทั้งหมดข้างบน ใส่ไว้ในเนื้อ PR
4. **อย่าเพิ่ง deploy** รอให้เจ้าของงานสั่ง

## เจ้าของงานตัดสินใจแล้ว — ไม่ต้องถามซ้ำ

| เรื่อง | คำตอบ |
| --- | --- |
| ห้ามส่ง hr / it / training ออกนอก | **เอา** — ปฏิเสธที่ server |
| contact ที่ blocked นับใน counter ไหม | **ไม่นับ** และไม่ส่ง |
| คนหนึ่งเป็นได้หลาย type ไหม | **ได้** — จึงแยกเป็นตาราง `line_contact_roles` ตั้งแต่แรก |
