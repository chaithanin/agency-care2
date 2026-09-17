# Requirement Baseline v1.0 — 17 กันยายน

Design canvas: https://claude.ai/artifact/2K6QoysNKhuVpBCScMh9xS

คำสั่งสำหรับตัวหลัก: [`BRIEF.md`](./BRIEF.md) — copy ทั้งไฟล์ไปวางได้เลย

Requirement ชุดนี้เปลี่ยน Agency Care **จากระบบ CRUD ธรรมดาเป็นระบบ workflow**

**เป็น mockup นิ่ง ๆ ตัวเลขเป็นตัวอย่างสมมติ ไม่ได้ต่อ API และไม่ได้แก้โค้ดของระบบจริง**

## แผ่นทั้งหมด

| ไฟล์ | เรื่อง |
| --- | --- |
| `Main.dc.html` | **อ่านก่อน** — ตารางฐานข้อมูลทั้งหมด ลำดับการทำ และกฎ 8 ข้อ |
| `Construction.dc.html` | 1 · Construction Schedule Update |
| `Purchase.dc.html` | 2 · Inventory Purchase Request |
| `Inventory.dc.html` | 3 · Multi-Location Inventory |
| `Distribution.dc.html` | 4 · Brochure Distribution + หลักฐาน |
| `Quota.dc.html` | 5 · Promotion Selling Quota ผูกยูนิตจริง |
| `Message.dc.html` | 6 · Internal / External Message |
| `Training.dc.html` | 7 · SOP → Training & Test |
| `Notification.dc.html` | 8 · Notification (System + LINE + Email) |

## ลำดับการทำ — ห้ามสลับ

```
Database Schema → Workflow → Permission → API → Notification → UI → QA
```

เจ้าของงานกำหนดเองว่า **ห้ามเริ่มจากหน้า UI** เพื่อลดการรื้อระบบภายหลัง

## ของเดิมที่มีอยู่แล้ว — สำรวจแล้ว อย่าเขียนซ้ำ

| ตาราง | สภาพ |
| --- | --- |
| `PurchaseRequest` + 5 ตารางลูก | **ครบแล้ว** status ตรงกับ requirement เกือบทั้งหมด |
| `Unit` | มี `status` = available / reserved / booked / sold + ผูก project |
| `PosmItem` + `PosmTransaction` | สต็อกรวม ต้องแยกตามที่เก็บ |
| `TrainingRecord` | บันทึกการเข้าอบรม ไม่ใช่ระบบข้อสอบ — ห้ามแตะ |
| `NotificationSetting` / `Template` / `Log` | ค่ากลาง ต้องเพิ่มค่าของแต่ละคน — ห้ามแตะของเดิม |
| Construction | **ไม่มีเลย** ของใหม่ทั้งหมด |

## 8 กฎที่ห้ามทำผิด

1. ห้ามเริ่มจาก UI
2. ห้ามแก้ตารางเดิม — เพิ่มคอลัมน์ได้ ลบหรือเปลี่ยนความหมายไม่ได้
3. สถานะทุกตัวคำนวณ ไม่ใช่เก็บเป็นคอลัมน์ (Overdue · Remaining · Total stock)
4. ทุกการเปลี่ยนสต็อกต้องมีธุรกรรม ห้าม UPDATE ยอดตรง ๆ
5. Internal message ห้ามมี endpoint ส่งออกภายนอก
6. ผลสอบผูกกับ version ของคอร์ส
7. แจ้งเตือนห้ามส่งซ้ำ — unique key ที่ระดับฐานข้อมูล
8. ไฟล์หลักฐานลงถังส่วนตัวผ่าน `savePrivate()` เท่านั้น

## ค่าที่ลอกมาจากโปรเจกต์จริง

ธีมจาก `web/src/theme/ThemeContext.tsx` โหมด dark ของ `chaithanin/agency-care`
branch `feat/all-appointments-clean-on-118a2e2` = revision **agency-care-00886-nus**

## สร้างไฟล์ใหม่

```bash
cd design/requirements-sep17
for i in 1 2 3 4 5 6; do python3 build_$i.py; done
```
