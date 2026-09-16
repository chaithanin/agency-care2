# Mockup — LINE Broadcast Center (Contacts & Audience Management)

Design canvas: https://claude.ai/artifact/PhCT772zZs3T9AAyFx4W6H

คำสั่งสำหรับตัวหลัก: [`BRIEF.md`](./BRIEF.md) — copy ทั้งไฟล์ไปวางได้เลย

ต่อยอด LINE Broadcast ที่มีอยู่ ให้เก็บผู้ติดตาม LINE OA ทุกคนเป็น contact
จัดบทบาทได้ และเลือกกลุ่มผู้รับตอนส่งได้

**เป็น mockup นิ่ง ๆ ไม่ได้ต่อ API และไม่ได้แก้โค้ดของระบบจริง**

## หน้าจอ

| ไฟล์ | หน้าจอ |
| --- | --- |
| `Main.dc.html` | Overview — audience counter 5 ตัว, แจ้งเตือน unclassified, โควตา LINE |
| `Contacts.dc.html` | แท็บ Contacts — ตาราง ตัวกรอง และการเลือกหลายแถว |
| `ContactDetail.dc.html` | รายละเอียด contact — จัดบทบาทและผูกกับ CRM |
| `Step1Audience.dc.html` | New Announcement 1 — เลือกกลุ่มผู้รับ |
| `CustomSelection.dc.html` | New Announcement 1 — Custom Selection + นับผู้รับ real-time |
| `Step2Message.dc.html` | New Announcement 2 — เนื้อหาข้อความ |
| `Step3Preview.dc.html` | New Announcement 3 — ตัวอย่างใน LINE + สรุปผู้รับ |
| `Step4Send.dc.html` | New Announcement 4 — ส่งหรือตั้งเวลา |
| `History.dc.html` | Send History พร้อมป้ายกลุ่มผู้รับ |
| `DataModel.dc.html` | โครงสร้างฐานข้อมูลและกฎ 8 ข้อ |

## แท็บใหม่แทรกเป็นตัวที่สอง

```
OVERVIEW | CONTACTS | SEND HISTORY | TEMPLATES | ANALYTICS
```

## โครงสร้างข้อมูล — แยกสองตาราง

คนหนึ่งเป็นได้หลายบทบาท (เจ้าของเอเจนซี่ที่ซื้อห้องเองด้วย) จึงแยก
"ตัวคน" ออกจาก "บทบาท" ตั้งแต่แรก

```
line_contacts        ตัวคน — line_user_id, โปรไฟล์, status, followed_at
line_contact_roles   บทบาท — หนึ่งแถวต่อหนึ่งบทบาท
                     @@unique(line_contact_id, contact_type)
```

**Unclassified = contact ที่ยังไม่มีแถวใน `line_contact_roles` เลย**
ไม่ต้องมี contact_type ชื่อ unclassified

## กฎ 8 ข้อที่ต้องบังคับฝั่ง server

1. คนใหม่เข้า Unclassified เสมอ ห้ามเดา
2. role `sales` สร้างได้เฉพาะเมื่อมี `employee_id`
3. All ไม่รวม Unclassified — ติ๊กรวมได้เฉพาะ Manager กับ Admin
4. ประเภท hr / it / training ส่งได้เฉพาะกลุ่ม Sales
5. `unfollow` ห้ามลบแถว ตั้ง `inactive` เท่านั้น
6. เอเจนซี่หนึ่งรายมีได้หลาย contact ชี้ `agency_id` เดียวกัน
7. คนที่มีหลายบทบาทต้องได้ข้อความใบเดียว
8. `blocked` และ `inactive` ไม่นับใน counter และไม่ถูกส่ง

## ค่าที่ลอกมาจากโปรเจกต์จริง

ดึงจาก `web/src/theme/ThemeContext.tsx` โหมด dark ของ `chaithanin/agency-care`
branch `feat/all-appointments-clean-on-118a2e2` = revision **agency-care-00886-nus**
ค่าทั้งหมดอยู่ใน `tokens.py`

## สร้างไฟล์ใหม่

```bash
cd design/line-broadcast
python3 build_1.py && python3 build_2.py && python3 build_3.py \
  && python3 build_4.py && python3 build_5.py
```

`tokens.py` เก็บสี · `shell.py` เก็บแท็บ stepper และชิ้นส่วนที่ใช้ร่วมกัน ·
`canvas.json` คุมตำแหน่งบนผืนผ้าใบ

## ของที่มีอยู่แล้วในระบบ — อย่าเขียนซ้ำ

| มีแล้ว | ที่ไหน |
| --- | --- |
| รับ `follow` / `unfollow` event | `line-webhook.controller.ts:77` |
| `getProfile(lineUserId)` | `line.service.ts:43` |
| `pushText` / `pushFlex` / `quota()` | `line.service.ts` |
| ผูก LINE ของเอเจนซี่ด้วยโค้ด `AG-XXXXXX` | `agency.service.ts:1116` |
| ตาราง `Broadcast` / `BroadcastRecipient` / `BroadcastTemplate` | `schema.prisma:1738` |
| หน้า Broadcast 4 แท็บ | `BroadcastPage.tsx:310` |

รายละเอียดทั้งหมดอยู่ใน `BRIEF.md`
