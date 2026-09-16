# Mockup — Omnichannel Overview (แท็บใหม่ในหน้า Reports)

Design canvas: https://claude.ai/artifact/M4U6kjxyytkpy4pncUA94E

คำสั่งสำหรับตัวหลัก: [`BRIEF.md`](./BRIEF.md) — copy ทั้งไฟล์ไปวางได้เลย

แท็บใหม่ใน `/reports` ที่ให้ **respond.io เป็นแหล่งข้อมูล** และ
**Agency Care เป็นหน้าสรุปให้ผู้บริหาร** รวมทุกอย่างไว้ในหน้าเดียว

**เป็น mockup นิ่ง ๆ ตัวเลขทั้งหมดเป็นตัวอย่างสมมติ ไม่ได้ต่อ API และไม่ได้แก้โค้ดของระบบจริง**

## หน้าจอ

| ไฟล์ | หน้าจอ |
| --- | --- |
| `Main.dc.html` | Global Filter · KPI 8 ตัว · Audience · Omnichannel Performance · Trend |
| `Funnel.dc.html` | Lead Journey 7 ขั้น + Project Interest |
| `Performance.dc.html` | Conversation Performance · Customer vs Agency · Broadcast · Team |
| `Attention.dc.html` | Needs Your Attention + ตัวอย่าง drill-down |
| `DataSources.dc.html` | ตัวเลขแต่ละตัวมาจากไหน + สถาปัตยกรรม + ช่องว่างที่ต้องรู้ |

## 7 คำถามที่หน้านี้ต้องตอบให้ครบ

1. วันนี้มีคนเข้ามาเท่าไร
2. มาจาก channel ไหน
3. เป็น Customer หรือ Agency
4. สนใจโครงการอะไร
5. ทีมตอบเร็วหรือช้า
6. Lead เดินไปถึง Viewing / Reservation / Closing เท่าไร
7. ตอนนี้มีอะไรที่ต้องเข้าไปจัดการทันที

## การเพิ่มแท็บ — งานเล็กมาก

`web/src/pages/ReportsHub.tsx` เป็นลิสต์ 3 บรรทัด เพิ่มอีกบรรทัดเดียว
`HubTabs` ซิงก์กับ `?section=` ใน URL ให้อยู่แล้ว

## สถาปัตยกรรม — ข้อสำคัญที่สุด

```
respond.io API  →  ตาราง mirror  →  ตารางสรุปรายวัน  →  หน้า Dashboard
```

**ห้ามเรียก respond.io สดตอนเปิดหน้า** — Avg. First Response ต้องไล่ข้อความของ
contact หมื่นกว่าคน เรียกสดจะช้าและชน rate limit

ตารางสรุป **เก็บผลรวมกับจำนวน ห้ามเก็บค่าเฉลี่ยสำเร็จรูป** —
ค่าเฉลี่ยของค่าเฉลี่ยไม่เท่ากับค่าเฉลี่ยจริง พอเลือกช่วง 7 วันตัวเลขจะเพี้ยน

## สีของกราฟ — ตรวจแล้ว ไม่ได้เลือกด้วยตา

ตรวจด้วย `scripts/validate_palette.js` ของ dataviz บนพื้นการ์ดจริงของแอป
(`#111827`) โหมด dark ผ่านทุกข้อ

| ชุด | ผลตรวจ |
| --- | --- |
| ช่องทาง 5 สี | CVD ΔE 8.4 (protan) · normal 19.3 |
| กลุ่มผู้ติดต่อ 4 สี | CVD ΔE 8.4 · normal 19.8 |
| เส้นแนวโน้ม 3 สี | CVD ΔE 9.4 · normal 26.5 |

```
#3987e5  #d95926  #199e70  #c98500  #d55181
```

ค่าทั้งหมดอยู่ใน `tokens.py` · สีสถานะ (good/warning/serious/critical) สงวนไว้
ห้ามเอาไปใช้เป็นสีของ series

## ต้องมีก่อนทำหน้านี้

1. ตัวเชื่อม respond.io — `apps/chat-inbox/src/integrations/respondio/`
2. โมดูล LINE Contacts — `design/line-broadcast/BRIEF.md`

ถ้ายังไม่มีสองอย่างนี้ Audience, Customer vs Agency และ Team Performance
จะไม่มีข้อมูล

## ค่าที่ลอกมาจากโปรเจกต์จริง

ธีมดึงจาก `web/src/theme/ThemeContext.tsx` โหมด dark ของ `chaithanin/agency-care`
branch `feat/all-appointments-clean-on-118a2e2` = revision **agency-care-00886-nus**

## สร้างไฟล์ใหม่

```bash
cd design/omnichannel-overview
python3 build_1.py && python3 build_2.py && python3 build_3.py \
  && python3 build_4.py && python3 build_5.py
```

`tokens.py` เก็บสีและชุดสีกราฟ · `shell.py` เก็บแท็บ การ์ด KPI donut และกราฟเส้น ·
`canvas.json` คุมตำแหน่ง
