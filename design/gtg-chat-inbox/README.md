# Mockup โมดูลแชทใน Agency Care

Design canvas: https://claude.ai/artifact/3HMeXnFFLv6niuxhtYRFXr

ไฟล์ `.dc.html` หนึ่งไฟล์ = หนึ่งหน้าจอ (artboard) — `canvas.json` คุมตำแหน่งบนผืนผ้าใบ

| ไฟล์ | หน้าจอ |
| --- | --- |
| `Login.dc.html` | เข้าสู่ระบบ |
| `Main.dc.html` | Chat Inbox (3 คอลัมน์) |
| `Contacts.dc.html` / `ContactDetail.dc.html` | รายชื่อผู้ติดต่อ และหน้ารายละเอียด |
| `Automations.dc.html` | ตัวสร้างกฎอัตโนมัติ |
| `Broadcast.dc.html` | ส่งข้อความเป็นชุด |
| `Dashboard.dc.html` | Chat Insight |
| `SettingsChannels.dc.html` | ตั้งค่า › ช่องทาง |
| `SettingsIntegrations.dc.html` | ตั้งค่า › Integrations (API key + webhook ของ Agency Care) |
| `MobileInbox.dc.html` / `MobileChat.dc.html` | มือถือ |

## ค่าที่ลอกมาจากโปรเจกต์จริง

จาก `agency-care/web/src/theme.ts` และ `components/Layout.tsx`

- primary `#7c6ff0` (light `#9d93f5`, dark `#5b4fd6`), พื้นหลัง `#0a0913` + radial gradient
- การ์ด `rgba(26,23,43,0.66)` ขอบ `rgba(255,255,255,0.06)` มุม 16px
- ปุ่ม primary `linear-gradient(135deg,#8b7ff5,#6a5be0)` เงา `0 8px 22px -8px rgba(124,111,240,0.7)` มุม 12px
- ตัวอักษร `#ECEBF5` / รอง `#9B99B8` ฟอนต์ Sarabun
- Drawer 252px พื้น `#100e1c` เมนู active `linear-gradient(90deg, rgba(124,111,240,0.30), rgba(124,111,240,0.04))`

สีกราฟใน Dashboard ใช้ `#7c6ff0 / #b8800f / #2f9fd0` ซึ่งผ่านการตรวจ contrast และการแยกสีสำหรับตาบอดสี
บนพื้นหลังมืดจริงของแอป

## แก้ไขและ deploy ใหม่

```bash
cd design/gtg-chat-inbox
python3 build1.py && python3 build2.py && python3 build3.py \
  && python3 build4.py && python3 build5.py && python3 build6.py && python3 build7.py
```

`gen.py` เก็บโทเคนและส่วนประกอบกลาง (sidebar, ปุ่ม, การ์ด, ชิป) — แก้ที่เดียวแล้วสะท้อนทุกหน้าจอ
