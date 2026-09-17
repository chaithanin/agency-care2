# คำสั่งสำหรับตัวหลัก — Omnichannel Overview

> คัดลอกทั้งหน้านี้ไปวางได้เลย

---

เพิ่มแท็บใหม่ **Omnichannel Overview** ในหน้า `/reports` ของ Agency Care
ให้ **respond.io เป็นแหล่งข้อมูล** และ **Agency Care เป็นหน้าสรุปให้ผู้บริหาร**
รวม Customer + Agency + Sales + Channel + Performance + Conversion ไว้ในหน้าเดียว

## branch ที่ต้องใช้ — อ่านก่อนเริ่ม

แตกงานจาก **`feat/all-appointments-clean-on-118a2e2`** เท่านั้น
คือสายที่ระบบจริงใช้อยู่ (= Cloud Run revision `agency-care-00886-nus`)

**ห้ามใช้ `feat/crm-modules-jul-2026`** เคย deploy จากสายนั้นแล้วเมนูในระบบจริงหายไป 8 ตัว

```bash
git branch --show-current     # ต้องเป็น feat/all-appointments-clean-on-118a2e2
```

## แบบที่ต้องทำตาม

Design canvas 5 หน้าจอ — https://claude.ai/artifact/M4U6kjxyytkpy4pncUA94E

ไฟล์ต้นฉบับอยู่ที่รีโป `chaithanin/agency-care2`
branch `claude/agency-care-test-project-zo163o` โฟลเดอร์ `design/omnichannel-overview/`

| อาร์ตบอร์ด | คือหน้าอะไร |
| --- | --- |
| `Main.dc.html` | Global Filter · KPI 8 ตัว · Audience · Omnichannel Performance · Trend |
| `Funnel.dc.html` | Lead Journey 7 ขั้น + Project Interest |
| `Performance.dc.html` | Conversation Performance · Customer vs Agency · Broadcast · Team |
| `Attention.dc.html` | Needs Your Attention + ตัวอย่าง drill-down |
| `DataSources.dc.html` | **ตัวเลขแต่ละตัวมาจากไหน + สถาปัตยกรรม — อ่านแผ่นนี้ก่อนเขียนโค้ด** |

---

## การเพิ่มแท็บ — งานเล็กมาก

`web/src/pages/ReportsHub.tsx` เป็นลิสต์ 3 บรรทัด เพิ่มอีกบรรทัดเดียว

```tsx
{ key: 'omnichannel', label: 'Omnichannel Overview',
  render: () => <OmnichannelOverviewPage /> },
```

`HubTabs` ซิงก์กับ `?section=` ใน URL อยู่แล้ว ไม่ต้องแตะ
**ห้ามแก้หรือสลับลำดับแท็บเดิม** (CRM 360° / Reports / KPI) เพิ่มต่อท้ายอย่างเดียว

---

## สถาปัตยกรรม — ข้อนี้สำคัญที่สุด

```
respond.io API  →  ตาราง mirror (respondio_*)  →  ตารางสรุปรายวัน  →  หน้า Dashboard
```

**ห้ามเรียก respond.io สดตอนผู้ใช้เปิดหน้า**

Avg. First Response ต้องไล่ข้อความของ contact หมื่นกว่าคน เรียกสดจะช้าและชน rate limit ทันที
ให้คำนวณล่วงหน้าเก็บเป็นตารางสรุปรายวัน แล้ว dashboard query จากตารางนั้นอย่างเดียว

**เปิดหน้าต้องเสร็จภายใน 1 วินาที**

### ตารางสรุปที่ต้องมี

```
omnichannel_daily_stats
  id
  stat_date          Date
  channel            String?   // line | facebook | instagram | whatsapp | website | null = รวม
  contact_type       String?   // customer | agency | sales | null = รวม

  new_contacts               Int
  conversations_opened       Int
  conversations_resolved     Int
  first_response_sum_sec     Int   // เก็บผลรวมกับจำนวน ไม่ใช่ค่าเฉลี่ย
  first_response_count       Int   // จะได้รวมข้ามวันแล้วยังถูก
  response_sum_sec           Int
  response_count             Int
  resolution_sum_sec         Int
  resolution_count           Int
  within_5min                Int
  within_15min               Int
  over_30min                 Int

  computed_at        DateTime
  @@unique([stat_date, channel, contact_type])
```

> **เก็บผลรวมกับจำนวน ห้ามเก็บค่าเฉลี่ยสำเร็จรูป** — ค่าเฉลี่ยของค่าเฉลี่ยไม่เท่ากับ
> ค่าเฉลี่ยจริง พอผู้ใช้เลือกช่วง 7 วันหรือ This Month ตัวเลขจะเพี้ยนทันที

---

## ตัวเลขแต่ละตัวมาจากไหน

| Metric | แหล่ง | คิดจาก | อัปเดต |
| --- | --- | --- | --- |
| Total / New Contacts | respond.io | ตาราง mirror | 15 นาที |
| Audience 4 กลุ่ม | ต้อง join | type จาก `line_contact_roles` · ตัวคนจาก respond.io | 15 นาที |
| Active Conversations | respond.io | contact ที่ `status = open` | 5 นาที |
| Conversations by channel | respond.io | group ตาม source | 15 นาที |
| Avg. First / Avg. Response | respond.io | timestamp ข้อความ — **precompute** | 1 ชม. |
| Resolution Rate / Avg. Resolution | respond.io | เวลาที่เปลี่ยนเป็น close | 1 ชม. |
| SLA 5 / 15 / 30 นาที | respond.io | แจกแจงจาก first response | 1 ชม. |
| New Leads | Agency Care | `CustomerLead` ที่สร้างในช่วงนั้น | ทันที |
| Lead Journey 7 ขั้น | Agency Care | `dealStages` / `reportStatus` | ทันที |
| Project Interest | Agency Care | `interestedProjects` | ทันที |
| Reservations / Closed | Agency Care | `Booking` และ `Deal` เดิม | ทันที |
| Customer vs Agency | ต้อง join | นับคนจาก respond.io แยกด้วย role | 15 นาที |
| Broadcast | Agency Care | `Broadcast` / `BroadcastRecipient` | ทันที |
| Team Performance | ต้อง join | assignee จาก respond.io แม็ปด้วย `employee.lineUserId` | 1 ชม. |
| Needs Your Attention | ต้อง join | รวมเงื่อนไขสองฝั่ง | 5 นาที |

---

## กฎที่ห้ามทำผิด

### 1. ห้ามแสดงศูนย์เมื่อซิงก์ล้มเหลว

ถ้าการซิงก์ล่าสุดพัง ให้แสดง**ข้อมูลเก่าพร้อมป้ายเตือน**
ศูนย์ที่ไม่ใช่ศูนย์จริงทำให้ผู้บริหารตัดสินใจผิด

### 2. ทุกตัวเลขต้องบอกเวลาที่ซิงก์ล่าสุด

มุมบนของหน้าแสดง "ข้อมูล ณ ... · ซิงก์จาก respond.io ล่าสุด ... นาทีที่แล้ว"
ผู้บริหารต้องรู้ว่ากำลังดูข้อมูลสดหรือข้อมูลเมื่อชั่วโมงที่แล้ว

### 3. contact ที่ยังไม่จับคู่ ต้องบอกให้เห็น

Lead Journey และ Project Interest ใช้ข้อมูลของ Agency Care เท่านั้น
contact จาก respond.io ที่ยังไม่ผูกกับ `CustomerLead` **จะไม่ปรากฏใน funnel**
ต้องแสดงจำนวนที่หลุดออกไป ไม่ใช่ซ่อนเงียบ ๆ

### 4. Needs Your Attention ทุกแถวต้องกดไปทำงานต่อได้

ไม่ใช่แค่แสดงตัวเลข ทุกแถวลิงก์ไปหน้าที่แก้ปัญหานั้นได้จริง
นี่คือจุดที่ทำให้หน้านี้เป็นเครื่องมือบริหาร ไม่ใช่แค่รายงาน

### 5. Global Filter คุมทุกกล่องพร้อมกัน

เปลี่ยนช่วงเวลาหรือ channel แล้วทุกกล่องต้องเปลี่ยนตาม
ไม่ใช่บางกล่องเปลี่ยนบางกล่องไม่เปลี่ยน

### 6. ห้ามใส่ metric เชิงเทคนิคในหน้าแรก

ผู้บริหารไม่ได้อยากรู้ว่า "วันนี้ทีมส่ง 8,932 ข้อความ"
อยากรู้ว่า "ได้ lead กี่คน ทีมตอบทันไหม สนใจโครงการไหน ปิดได้กี่ราย"
**KPI แถวแรกห้ามเกิน 8 ตัว**

---

## เรื่องกราฟ

สีของ series **ตรวจด้วย validator แล้ว** บนพื้นการ์ดจริงของแอป (`#111827`) โหมด dark
ผ่านทุกข้อ — ใช้ตามลำดับนี้ ห้ามวนใช้ซ้ำและห้ามสลับ

```
slot 1  #3987e5  น้ำเงิน
slot 2  #d95926  ส้ม
slot 3  #199e70  เขียวอมฟ้า
slot 4  #c98500  เหลือง
slot 5  #d55181  ชมพู
```

worst adjacent CVD ΔE 8.4 · normal-vision ΔE 19.3 — คนตาบอดสีแยกออก

สีสถานะสงวนไว้ ห้ามเอาไปใช้เป็นสีของ series

```
good #0ca30c · warning #fab219 · serious #ec835a · critical #d03b3b
```

กฎที่ต้องทำตาม

- **ห้ามใช้กราฟสองแกน y** เด็ดขาด — ถ้าหน่วยต่างกันให้แยกเป็นสองกราฟ
- กราฟตั้งแต่ 2 series ขึ้นไป **ต้องมี legend เสมอ** และมีป้ายกำกับตรงจุด
  ไม่ให้แยกกันได้ด้วยสีอย่างเดียว
- สีติดกับ entity ไม่ใช่ลำดับ — กรองแล้ว series ที่เหลือต้องไม่เปลี่ยนสี
- ตัวหนังสือใช้สีตัวอักษรปกติ ไม่ใช่สีของ series
- เส้นหนา 2px · จุดอย่างน้อย 8px · ปลายแท่งมน 4px · กริดจาง ๆ ถอยหลัง
- ต้องมี tooltip ตอน hover ทุกกราฟ

---

## สิทธิ์

หน้านี้เป็นข้อมูลภาพรวมทั้งบริษัท **จำกัดเฉพาะ Admin กับ Manager**
Seller เห็นได้เฉพาะแถวของตัวเองในตาราง Team Performance
ตรวจฝั่ง server

⚠️ **ใช้ `user.role` ไม่ใช่ `user.activeRole`** — `api/src/common/current-user.decorator.ts`
เขียนกำกับไว้เองว่า `role` = permanent role (for permission guards) และ
`activeRole` = current active role (for data scoping)
แอดมินมักทำงานโดยสลับเป็น sales อยู่ ถ้าตัดสินสิทธิ์จาก `activeRole` จะล็อกตัวเองออก

---

## ต้องมีก่อนเริ่ม

| ของ | สถานะ |
| --- | --- |
| respond.io API token | **มีแล้ว** ในโปรเจกต์หลัก |
| ตัวเชื่อม respond.io | มีต้นแบบให้ยกไปใช้ — `apps/chat-inbox/src/integrations/respondio/` |
| ตัวคำนวณสถิติ | มีต้นแบบให้ยกไปใช้ — `apps/chat-inbox/src/integrations/respondio/stats.js` |
| โมดูล LINE Contacts | **ยังต้องทำก่อน** — `design/line-broadcast/BRIEF.md` |

### ต้นแบบที่ยกไปใช้ได้เลย

อยู่ที่รีโป `chaithanin/agency-care2` branch `claude/agency-care-test-project-zo163o`

| ไฟล์ | ทำอะไร | ทดสอบแล้ว |
| --- | --- | --- |
| `respondio/client.js` | Bearer token · cursor pagination · retry 429 ตาม `Retry-After` · เลิกทันทีเมื่อ 401 | 14 เคส |
| `respondio/sync.js` | ดึงลงตารางกระจกเงา บันทึกทุกรอบที่ sync แม้ตอนพัง | 14 เคส |
| `respondio/map.js` | จับคู่ contact กับผู้ติดต่อในระบบด้วยเบอร์ 9 หลักท้าย แล้วอีเมล | 14 เคส |
| `respondio/stats.js` | **คำนวณตัวเลขทุกตัวของหน้านี้จากข้อมูลในเครื่อง** | 8 เคส |

`stats.js` คือตัวที่ตรงกับงานนี้ที่สุด — มี `audience()`, `channels()`,
`responseTimes()`, `trend()`, `gaps()` และ `overview()` เขียนเป็น JavaScript ธรรมดา
แปลงเป็น TypeScript + Prisma ได้ตรง ๆ

ตรรกะที่ทดสอบผ่านแล้วและควรลอกไป

- **First response นับจากข้อความแรกที่รอ ไม่ใช่ข้อความล่าสุด** —
  ลูกค้าพิมพ์ติดกันสามบรรทัด ต้องนับจากบรรทัดแรก ไม่ใช่บรรทัดที่สาม
- **เก็บผลรวมกับจำนวน ไม่ใช่ค่าเฉลี่ยสำเร็จรูป** — รวมข้ามวันแล้วยังถูก
- **นับคนที่ถามแล้วยังไม่มีใครตอบแยกต่างหาก** — ไม่ใช่ปล่อยให้หายไปจากค่าเฉลี่ย
- **ผลลัพธ์ไม่มีชื่อ เบอร์ หรืออีเมลติดออกมาเลย** มีเทสต์คุมข้อนี้ไว้

### สิ่งที่ยังขาด

โมดูล **LINE Contacts** (ตาราง `line_contacts` และ `line_contact_roles`)
ใช้แยก Customer / Agency / Sales

**ถ้ายังไม่มี** ให้ทำหน้านี้ได้ในส่วนที่ไม่ต้องใช้ type ก่อน —
KPI, Channels, Response Time, Trend, Lead Journey, Project Interest, Broadcast
ใช้ได้หมด ส่วน **Audience, Customer vs Agency และ Team Performance**
ให้แสดงว่า "รอโมดูล LINE Contacts" แทนที่จะแสดงศูนย์

---

## ห้ามกระทบของเดิม

- **เพิ่มบรรทัดใหม่เท่านั้น** ห้ามลบหรือแก้แท็บ เมนู route หรือฟังก์ชันที่มีอยู่
- ตารางใหม่สร้างตอนแอปบูตผ่าน `PrismaService` แบบ `CREATE TABLE IF NOT EXISTS`
  เหมือนโมดูลอื่นในรีโป ใส่ `this.logger.log(...)` บรรทัดสุดท้ายไว้ตรวจตอน deploy
- **อย่าพึ่ง `prisma migrate deploy`** — migration `delete_all_assignment_plans`
  ของรีโปนี้พังอยู่ก่อนแล้ว

## ต้องผ่านก่อน push

```bash
cd api && npx prisma validate && npx tsc --noEmit
cd ../web && npx tsc --noEmit && npx vite build
```

แล้ว **นับคำในไฟล์ที่ build ออกมา เพื่อพิสูจน์ว่าไม่มีเมนูเดิมหาย**

```bash
cd web && B=$(cat dist/assets/*.js)
for s in "Lead Status" "Closed Deals" "Registration Report" "Advertising Requests" \
         "LINE Checker" "Staff Calendar" "Social Media" "Call Log" \
         "CRM 360" "Omnichannel Overview"; do
  printf '%-24s %s\n' "$s" "$(printf '%s' "$B" | grep -c "$s")"
done
```

ทุกตัวต้องมากกว่า 0

**และวัดเวลาโหลดหน้าจริง** — เปิดแท็บนี้ด้วยข้อมูลเต็ม ต้องไม่เกิน 1 วินาที
ถ้าเกิน แปลว่ายัง query ผิดที่ ให้กลับไปดูสถาปัตยกรรมด้านบน

## เรื่อง deploy

**ใช้ `.\deploy.ps1` ของ branch นี้เท่านั้น** อย่าประกอบคำสั่ง `gcloud run deploy` เอง —
`--set-env-vars` และ `--set-secrets` เขียนทับตัวแปรทั้งชุด ตกตัวไหนตัวนั้นหลุด

หลัง deploy ต้องสลับทราฟฟิกเอง

```bash
gcloud run services update-traffic agency-care --region asia-east2 --to-latest
```

## สิ่งที่ต้องส่งมอบ

1. branch ใหม่แตกจาก `feat/all-appointments-clean-on-118a2e2`
2. PR เข้า branch เดิมนั้น พร้อมตารางสรุปว่าแตะไฟล์เดิมกี่บรรทัด เพิ่ม/ลบเท่าไหร่
3. ผลการตรวจทั้งหมดข้างบน รวมเวลาโหลดหน้า ใส่ไว้ในเนื้อ PR
4. **อย่าเพิ่ง deploy** รอให้เจ้าของงานสั่ง

## ขั้นแรกที่ควรทำ — ดูข้อมูลจริงก่อนออกแบบตาราง

ก่อนเขียน schema ให้ดึงข้อมูลจริงมาดูก่อนว่าหน้าตาเป็นยังไง
workspace ตั้งชื่อ lifecycle ว่าอะไร มีช่องทางอะไรต่อไว้แล้วบ้าง

```bash
# ในต้นแบบ — ใส่ RESPONDIO_API_TOKEN ใน .env ก่อน
cd apps/chat-inbox
npm run respondio:check              # token ใช้ได้ไหม เห็นอะไรบ้าง
npm run respondio:pull -- --max 200  # ดึงมา 200 คนแรก
npm run respondio:stats              # ตัวเลขจริงของหน้านี้ทั้งหมด
npm run respondio:stats -- --json    # เอา JSON ไปใช้ต่อ
```

`respondio:stats` จะบอกสามอย่างที่ตัดสินใจไม่ได้ถ้าไม่เห็นข้อมูลจริง

1. **lifecycle ที่ workspace ใช้จริงชื่ออะไร** — กระทบการแม็ปเข้า Lead Journey
2. **ช่องทางไหนต่อเข้า respond.io แล้วบ้าง** — ช่องที่ยังไม่ต่อจะไม่มีข้อมูลเลย
3. **มี contact กี่คนที่ไม่มีทั้งเบอร์และอีเมล** — กลุ่มนี้จับคู่กับ CRM ไม่ได้
   จะไม่ปรากฏใน funnel ต้องรู้จำนวนก่อนจะได้ตัดสินใจว่าจะแสดงยังไง

**อย่าเดาตัวเลขพวกนี้** ตัวเลขใน mockup เป็นตัวอย่างสมมติทั้งหมด

---

## เรื่องที่ยังต้องถามเจ้าของงาน

1. ช่องทางที่ยังไม่ได้ต่อเข้า respond.io จะตัดแถวออก หรือแสดงว่า "ยังไม่ได้เชื่อม"
   (รู้ได้เองว่ามีช่องทางไหนบ้างจาก `npm run respondio:stats`)
2. เก็บข้อมูลสรุปย้อนหลังกี่เดือน — กระทบขนาดตารางและความเร็ว
3. ให้ Seller เห็นภาพรวมทั้งบริษัทได้ไหม หรือเห็นเฉพาะของตัวเอง
