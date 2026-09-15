# GTG Chat Inbox — prototype โมดูลแชทสำหรับ Agency Care

โปรเจกต์ย่อยสำหรับ **ทดสอบในเครื่องก่อน** ตามแผนใน *GTG Chat Backend Roadmap*
ตัดเอาเฉพาะเส้นทางที่แคบที่สุดแต่ครบวง แล้วทำให้เห็นผลจริงตั้งแต่วันแรก:

```
ลูกค้าส่งข้อความ ─► Channel adapter ─► contacts / conversations / messages
                                             │
                        กฎอัตโนมัติ (ทักทาย / มอบหมาย / แท็ก)
                                             │
              Inbox UI (เซลส์ตอบ)      Agency Care API + webhook ◄── ระบบ Agency Care
```

จุดเชื่อมกับ Agency Care คือสองอย่างตามที่ roadmap กำหนดไว้ในสัปดาห์ 15–16

| ทิศทาง | ช่องทาง | ใช้ทำอะไร |
| --- | --- | --- |
| Agency Care → ระบบแชท | REST API + API key | ดึง contacts / conversations / messages / สถิติ, เปลี่ยน lifecycle stage, ส่งข้อความหาลูกค้า |
| ระบบแชท → Agency Care | Outgoing webhook (ลงลายเซ็น HMAC) | แจ้งทันทีที่ lifecycle stage เปลี่ยน |

## ข้อกำหนด

Node.js 22.5 ขึ้นไป **เท่านั้น** — ไม่มี dependency ให้ติดตั้ง ไม่ต้องใช้ Docker หรือ PostgreSQL
ฐานข้อมูลใช้ SQLite ที่มากับ Node (`node:sqlite`) เก็บไฟล์ไว้ที่ `data/chat-inbox.db`

## เริ่มใช้ใน 3 คำสั่ง

```bash
cd apps/chat-inbox
npm run demo    # เดโม่ครบวงจรในเทอร์มินัล ไม่ต้องเปิดเบราว์เซอร์
npm run seed    # ใส่ข้อมูลตั้งต้น + ออก API key ให้ Agency Care (แสดงครั้งเดียว)
npm start       # เปิด http://localhost:4000/
```

ส่งข้อความทดสอบเข้าระบบ (ยังไม่ต้องมี LINE OA):

```bash
npm run simulate -- --user U-001 --name "คุณสมชาย" --text "สนใจพูลวิลล่าครับ ราคาเท่าไหร่"
```

รันชุดทดสอบ (29 เคส ครอบคลุมลายเซ็น, การกันข้อความซ้ำ, สิทธิ์ API key, SQL injection, webhook):

```bash
npm test
```

## หน้า Inbox

คอลัมน์ซ้ายรายการบทสนทนาพร้อมแท็บ ทั้งหมด / ยังไม่มีคนรับ / มอบหมายแล้ว / ของฉัน / ปิดแล้ว
กลางคือข้อความและกล่องพิมพ์ตอบ ขวาคือข้อมูลผู้ติดต่อ — เปลี่ยน lifecycle stage, ใส่แท็ก, กรอก custom fields
ข้อความใหม่เด้งขึ้นเองผ่าน Server-Sent Events ไม่ต้องกด refresh

prototype นี้ยังไม่มีระบบ login จริง — ใช้กล่องเลือกผู้ใช้มุมขวาบนแทน (ส่ง header `x-dev-user`)
ของจริงต้องเปลี่ยนเป็น session ตาม roadmap สัปดาห์ 4–6 **ก่อน** เอาขึ้นเครื่องจริง

## Agency Care API

ทุก endpoint ต้องมี header `X-API-Key: gtg_xxx` (หรือ `Authorization: Bearer gtg_xxx`)
ยกเว้น `/api/v1/health` — คีย์เก็บใน DB เป็น SHA-256 เท่านั้น ออกใบใหม่ด้วย `npm run reset`

| Method | Endpoint | สิทธิ์ | หมายเหตุ |
| --- | --- | --- | --- |
| GET | `/api/v1/health` | — | เช็กว่าเซิร์ฟเวอร์ยังอยู่ |
| GET | `/api/v1/contacts` | read | กรอง `stage`, `tag`, `channel`, `q`, `updated_since` + `limit`/`offset` |
| GET | `/api/v1/contacts/:id` | read | รวมแท็ก, custom fields, ช่องทาง, ประวัติ stage, บทสนทนา |
| POST | `/api/v1/contacts/:id/lifecycle` | write | `{ "stage": "hot_lead" }` — ยิง webhook กลับไปด้วย |
| GET | `/api/v1/conversations` | read | กรอง `status`, `contact_id`, `assignee_id`, `unassigned` |
| GET | `/api/v1/conversations/:id/messages` | read | เรียงเก่า→ใหม่ |
| POST | `/api/v1/conversations/:id/messages` | write | `{ "text": "..." }` ส่งออกช่องทางเดิมของลูกค้า |
| GET | `/api/v1/stats/dashboard` | read | ยอด lifecycle, open/assigned/unassigned, เวลาตอบเฉลี่ย, ภาระงานต่อเซลส์ |

ตัวอย่างที่ roadmap ระบุไว้เป็นเกณฑ์ผ่านของสัปดาห์ 16:

```bash
curl -H "X-API-Key: $GTG_API_KEY" "http://localhost:4000/api/v1/contacts?stage=hot_lead"
```

```json
{
  "data": [
    { "id": 1, "displayName": "คุณสมชาย", "lifecycleStage": "hot_lead",
      "language": "th", "tags": ["pricing", "villa"] }
  ],
  "pagination": { "total": 1, "limit": 25, "offset": 0, "hasMore": false }
}
```

ข้อผิดพลาดคืนรูปแบบเดียวกันเสมอ: `{ "error": { "code": "unauthorized", "message": "..." } }`
และมี rate limit 120 ครั้ง/นาที ต่อหนึ่ง API key (ดูจำนวนคงเหลือได้ที่ header `x-ratelimit-remaining`)

## Webhook ที่ Agency Care ต้องรับ

เมื่อ lifecycle stage เปลี่ยน (ไม่ว่าจะเปลี่ยนจากหน้า Inbox หรือจาก API) ระบบจะ POST ไปที่ URL ที่ลงทะเบียนไว้ในตาราง `webhooks_out`

```
POST /hooks/gtg-chat
x-gtg-event: contact.lifecycle_changed
x-gtg-timestamp: 1757925757000
x-gtg-signature: sha256=<hex>

{"event":"contact.lifecycle_changed","data":{"contactId":1,"displayName":"คุณสมชาย",
 "fromStage":"new_lead","toStage":"hot_lead","changedBy":"agency-care:Agency Care",
 "changedAt":"2026-09-15T08:22:37.766Z"},"sentAt":"..."}
```

ฝั่งรับต้องตรวจ 2 อย่างก่อนเชื่อ:

1. `signature === "sha256=" + HMAC_SHA256(secret, timestamp + "." + rawBody)` — เทียบแบบ timing-safe
2. `timestamp` ห่างจากเวลาปัจจุบันไม่เกิน 5 นาที (กันคนดักจับแล้วยิงซ้ำ)

ตัวรับตัวอย่างพร้อมโค้ดตรวจลายเซ็นอยู่ที่ `scripts/agency-care-receiver.js` (`npm run receiver`)
ทุกครั้งที่ส่งจะบันทึกผลไว้ในตาราง `webhook_deliveries` ดูย้อนหลังได้ว่าอันไหนล้มเหลวเพราะอะไร

## ต่อ LINE ของจริง

1. คัดลอก `.env.example` เป็น `.env` ใส่ `LINE_CHANNEL_SECRET` กับ `LINE_CHANNEL_ACCESS_TOKEN`
2. ตั้ง `LINE_DRY_RUN=false` เมื่อพร้อมให้ส่งข้อความออกจริง
3. `npm run seed` อีกครั้งเพื่อเขียน token ลงตาราง `channels` แล้ว `npm start`
4. เปิด ngrok: `ngrok http 4000` แล้วตั้ง Webhook URL ใน LINE Console เป็น `https://xxxx.ngrok.io/webhook/line`

ระบบตรวจ `X-Line-Signature` ทุกครั้ง — ลายเซ็นไม่ตรงจะตอบ 401 และไม่บันทึกอะไรลงฐานข้อมูล

## โครงไฟล์

```
db/schema.sql              ตารางทั้งหมด (ย้ายไป PostgreSQL ได้โดยแก้ชนิดคอลัมน์)
src/channels/adapter.js    สัญญากลางของทุกช่องทาง — เพิ่ม Facebook/WhatsApp ที่นี่
src/channels/line.js       ตรวจลายเซ็น + แปลง event + ส่งข้อความ (reply/push)
src/channels/mock.js       ช่องทางจำลองสำหรับทดสอบโดยไม่ต้องมี LINE
src/services/inbox.js      หัวใจ: หา/สร้าง contact, conversation, บันทึกข้อความ, เปลี่ยน stage
src/services/automations.js กฎ: ทักทายตามภาษา, มอบหมายวนรอบ, แท็กจากคีย์เวิร์ด
src/services/webhooks.js   ลงลายเซ็นและส่ง webhook ออก + บันทึกผล
src/services/apiKeys.js    ออก/ตรวจ API key (เก็บเฉพาะ hash)
src/routes/agencyCare.js   API ที่ Agency Care เรียก
src/routes/internal.js     API ของหน้า Inbox เอง + SSE
public/index.html          หน้า Inbox 3 คอลัมน์ (vanilla JS ไฟล์เดียว)
```

## สิ่งที่ทำแล้วในต้นแบบนี้ เทียบกับ roadmap

| สัปดาห์ | หัวข้อ | สถานะในต้นแบบ |
| --- | --- | --- |
| 1 | ออกแบบฐานข้อมูล | ครบทุกตารางหลัก (SQLite) |
| 2–3 | รับ/ตอบ LINE | ครบ รวมการตรวจลายเซ็นและกันข้อความซ้ำ |
| 4–6 | Inbox UI | ครบแบบย่อ — **ยังไม่มี login จริง** |
| 7–8 | Contacts, แท็ก, lifecycle | ครบแบบย่อ (custom fields 4 ช่อง) |
| 9–10 | Channel adapter | โครงพร้อม มี LINE + mock ยังไม่มี Facebook |
| 11–12 | Automations | 3 กฎ + บันทึก automation_runs ยังไม่มี UI สร้างกฎ |
| 13 | Broadcast | ยังไม่ทำ |
| 14 | Dashboard | มีเป็น API (`/stats/dashboard`) ยังไม่มีหน้ากราฟ |
| 15–16 | Deploy + Agency Care API | API + webhook ครบ ยังไม่ได้ทำ Dockerfile/Cloud Run |

## ก่อนเอาขึ้นใช้จริง ต้องทำเพิ่ม

- **login จริง** แทน header `x-dev-user` (ตอนนี้ใครยิง header นี้ก็เป็นใครก็ได้)
- ย้ายจาก SQLite ไป PostgreSQL (Cloud SQL) และเก็บ secret ใน Secret Manager แทน `.env`
- คิวงาน (BullMQ/Redis) สำหรับ webhook ที่ล้มเหลว — ตอนนี้ยิงครั้งเดียว ไม่ retry
- rate limit แบบแชร์ข้ามหลาย instance (ตอนนี้นับในหน่วยความจำของ process เดียว)
- HTTPS + โดเมนจริง และ log ที่ไม่บันทึกข้อความลูกค้าทั้งก้อนลง stdout
