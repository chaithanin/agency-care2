# เชื่อมต่อ respond.io เข้า Chat Inbox

ตัวเชื่อมกับ [respond.io Developer API v2](https://developers.respond.io/docs/api/)
สำหรับดึงข้อมูลบทสนทนา ผู้ติดต่อ และข้อมูล workspace เข้ามาใช้ในระบบ

## สิ่งที่ต้องมีก่อน

1. แผน respond.io ระดับ **Growth ขึ้นไป** (Developer API เปิดให้เฉพาะแผนนี้ขึ้นไป)
2. Access token — สร้างที่ **Settings → Integrations → Developer API → Add Access Token**

ใส่ token ลงไฟล์ `apps/chat-inbox/.env` (ไฟล์นี้อยู่ใน `.gitignore` อยู่แล้ว)

```
RESPONDIO_API_TOKEN=xxxxxxxxxxxxxxxx
```

> อย่าใส่ token ลงในโค้ดหรือ commit ขึ้น git เด็ดขาด
> ถ้าเผลอ push ขึ้นไปแล้ว ให้ไปเพิกถอน token เดิมที่หน้า Developer API แล้วสร้างใหม่

## ใช้งาน

```bash
cd apps/chat-inbox

npm run respondio:check                 # ตรวจว่า token ใช้ได้ และมองเห็นอะไรบ้าง
npm run respondio:pull -- --max 20      # ลองดึง contact 20 คนแรกก่อน
npm run respondio:pull                  # ดึงทั้งหมด
npm run respondio:pull -- --map         # ดึงแล้วแปลงเข้าตาราง contacts ของระบบ
npm run respondio:pull -- --map-only --dry-run   # ลองแปลงดูผล โดยไม่เขียนจริง
npm run respondio:stats                 # สรุปตัวเลขจากข้อมูลที่ดึงมาแล้ว
npm run respondio:stats -- --days 30    # เปลี่ยนช่วงเวลา
npm run respondio:stats -- --json       # พิมพ์ JSON ก้อนเดียว
```

## สรุปตัวเลข

`respondio:stats` คำนวณจากตารางในเครื่องล้วน ๆ **ไม่เรียก respond.io เลย**
ต้องรัน `respondio:pull` มาก่อน

| หัวข้อ | มีอะไร |
| --- | --- |
| Audience | จำนวน contact · บทสนทนาที่เปิดอยู่ · จับคู่แล้ว/ยังไม่จับคู่ · lifecycle ที่ใช้จริง |
| Channels | contact และข้อความแยกตามช่องทาง |
| Response time | first response · ทุกข้อความ · SLA 5/15/30 นาที · คนที่ยังไม่ได้ตอบ |
| Trend | รายวัน — contact ใหม่ · ข้อความเข้า/ออก · contact ที่ active |
| ช่องว่าง | ไม่มีช่องทาง · ไม่มีข้อความ · ไม่มีทั้งเบอร์และอีเมล |

**ผลลัพธ์ไม่มีชื่อ เบอร์ หรืออีเมลของใครติดออกมาเลย** มีเทสต์คุมไว้
เอาไปแปะให้คนอื่นดูได้โดยไม่หลุดข้อมูลส่วนบุคคล

ตรรกะสำคัญที่เขียนไว้ใน `stats.js`

- **First response นับจากข้อความแรกที่รอ ไม่ใช่ข้อความล่าสุด** —
  ลูกค้าพิมพ์ติดกันสามบรรทัด ต้องนับจากบรรทัดแรก
- **เก็บผลรวมกับจำนวน ไม่ใช่ค่าเฉลี่ยสำเร็จรูป** — รวมข้ามวันแล้วยังถูก
  (ค่าเฉลี่ยของค่าเฉลี่ยไม่เท่ากับค่าเฉลี่ยจริง)
- **คนที่ถามแล้วยังไม่มีใครตอบ นับแยกต่างหาก** ไม่ปล่อยให้หายไปจากค่าเฉลี่ย

ตัวเลือกอื่น

| ตัวเลือก | ความหมาย |
| --- | --- |
| `--workspace` | ดึงเฉพาะ channel / user / custom field / closing note |
| `--max N` | จำกัดจำนวน contact ที่ดึง |
| `--map` | แปลงเข้าตาราง `contacts` ของระบบหลังดึงเสร็จ |
| `--map-only` | ข้ามการดึง แปลงจากข้อมูลที่ดึงไว้แล้วอย่างเดียว |
| `--dry-run` | คำนวณผลการแปลงให้ดู แต่ไม่เขียนฐานข้อมูล |
| `--overwrite` | ให้ค่าจาก respond.io ทับค่าเดิมในระบบ (ปกติเติมเฉพาะช่องที่ว่าง) |

## ดึงอะไรมาได้บ้าง

| ข้อมูล | endpoint | ลงตาราง |
| --- | --- | --- |
| ผู้ติดต่อ | `POST /contact/list` | `respondio_contacts` |
| ช่องทางของผู้ติดต่อ | `GET /contact/{id}/channels` | `respondio_contact_channels` |
| ข้อความ | `GET /contact/{id}/message/list` | `respondio_messages` |
| สถานะบทสนทนา + ผู้ดูแล | มากับ contact (`status`, `assignee`) | `respondio_contacts` |
| channel ใน workspace | `GET /space/channel` | `respondio_channels` |
| ผู้ใช้ | `GET /space/user` | `respondio_users` |
| custom field | `GET /space/custom_field` | `respondio_custom_fields` |
| closing note | `GET /space/closing_notes` | `respondio_closing_notes` |
| tag | มากับ contact | `respondio_tags` |

ช่องทางที่ respond.io รองรับและจะเห็นในคอลัมน์ `source`: LINE, WhatsApp (หลายผู้ให้บริการ),
Facebook, Instagram, Telegram, Viber, WeChat, Twitter, Gmail, อีเมลอื่น, Twilio,
MessageBird, Vonage และ custom channel

## โครงสร้าง

```
src/integrations/respondio/
  client.js   ตัวเรียก API — Bearer token, ไล่หน้าแบบ cursor, ลองใหม่เมื่อ 429/5xx
  sync.js     ดึงข้อมูลลงตาราง respondio_* (ตารางกระจกเงา)
  map.js      แปลงจากตารางกระจกเงาเข้าตารางหลักของระบบ
scripts/
  respondio-check.js   ตรวจการเชื่อมต่อ
  respondio-pull.js    สั่งดึง / สั่งแปลง
```

**ทำไมต้องมีตารางกระจกเงา** — ข้อมูลที่ดึงมาถูกเก็บดิบ ๆ ไว้ในตาราง `respondio_*` ก่อน
แยกจากตารางหลักของระบบ การดึงข้อมูลจึงไม่มีทางทำข้อมูลเดิมเสียหาย และถ้าการแปลงผิด
ก็แก้แล้วแปลงใหม่ได้โดยไม่ต้องดึงจาก respond.io ซ้ำ

## การจับคู่ผู้ติดต่อ

เวลาแปลงเข้าตาราง `contacts` ของระบบ จะจับคู่ตามลำดับนี้

1. เคยจับคู่ไว้แล้ว (ตาราง `respondio_contact_links`)
2. เบอร์โทรตรงกัน — เทียบ 9 หลักท้าย จึงข้าม `+66` / `0` นำหน้าและขีดคั่นได้
3. อีเมลตรงกัน (ไม่สนตัวพิมพ์เล็กใหญ่)
4. ไม่เจอเลย → สร้างผู้ติดต่อใหม่

ค่าเริ่มต้นจะ **ไม่ทับข้อมูลเดิมที่มีอยู่** เติมเฉพาะช่องที่ยังว่าง ถ้าต้องการให้ทับใช้ `--overwrite`

### แปลง lifecycle

ชื่อ lifecycle ใน respond.io ถูกแปลงเป็นขั้นตอนในระบบตามตารางใน `map.js`

| respond.io | ระบบ |
| --- | --- |
| Lead / New Lead | `new_lead` |
| Prospect / Hot Lead / Opportunity | `hot_lead` |
| Negotiation / Payment | `payment` |
| Won / Customer | `customer` |
| Lost / Churned | `lost` |

ชื่ออื่นที่ไม่อยู่ในตารางจะกลายเป็น `new_lead` **ถ้า workspace ของจริงตั้งชื่อต่างจากนี้
ให้แก้ `LIFECYCLE_MAP` ใน `src/integrations/respondio/map.js` ก่อนแปลงจริง**

## ข้อจำกัดของ rate limit

respond.io ตอบ `429` พร้อม header `Retry-After` เมื่อยิงถี่เกินไป
ตัว client รอตามเวลาที่บอกแล้วลองใหม่ให้เอง สูงสุด 4 ครั้ง (ปรับที่ `RESPONDIO_MAX_RETRIES`)
ส่วน `5xx` ใช้การถอยแบบเพิ่มเวลาเป็นเท่าตัว — ส่วน `4xx` อื่น ๆ เช่น `401` จะเลิกทันที
เพราะลองไปก็ผิดเหมือนเดิม

ถ้า workspace มี contact เยอะมาก แนะนำให้ดึงครั้งแรกด้วย `--max` ก่อน เพื่อดูว่าข้อมูลหน้าตาเป็นอย่างไร

## ที่ยังไม่ได้ทำ

- **ยังไม่ได้ทดสอบกับ token จริง** — ทดสอบทั้งหมดใช้ HTTP ปลอมในเครื่อง (14 เคส ผ่านหมด)
  ต้องรัน `npm run respondio:check` กับ token จริงเพื่อยืนยันว่ารูปแบบข้อมูลตรงกับที่เขียนไว้
- **ยังไม่ได้ดึงข้อความเข้าตาราง `messages` ของระบบ** — ข้อความอยู่ในตาราง `respondio_messages`
  ครบแล้ว แต่ตาราง `channels` ของระบบจำกัด provider ไว้แค่ `line / facebook / whatsapp / mock`
  ถ้าจะรับช่องทางอื่นของ respond.io ต้องขยายข้อจำกัดนั้นก่อน ซึ่งกระทบตารางเดิม
  จึงยังไม่ทำจนกว่าจะตกลงกัน
- **ยังไม่ได้ทำ webhook รับเหตุการณ์แบบเรียลไทม์** — ตอนนี้เป็นการดึงตามสั่งเท่านั้น
  ของจริง respond.io ส่งออกผ่าน Workflow ได้ ต้องออกแบบเพิ่ม
- **ยังไม่ได้ต่อเข้า Agency Care** — ตัวเชื่อมนี้อยู่ในโปรเจกต์ทดสอบก่อนตามที่ตกลง
