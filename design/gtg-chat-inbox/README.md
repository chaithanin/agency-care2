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

จาก `agency-care/web/src/theme/ThemeContext.tsx` (โหมดมืด) และ `components/Layout.tsx`
บน branch `feat/crm-modules-jul-2026` ซึ่งเป็นโค้ดของเว็บที่ใช้งานอยู่จริง

- primary `#3B82F6` (light `#60A5FA`, dark `#1E40AF`), success `#22C55E`, warning `#FBBF24`, error `#EF4444`
- พื้นหลัง `linear-gradient(135deg, #0F172A 0%, #111827 60%, #1F2937 100%)`
- Drawer `#111827` ขอบขวา `#374151` กว้าง 264px · AppBar `#1F2937`
- การ์ด `#111827` ขอบ `#374151` มุม 20px · ปุ่มทรงแคปซูล (radius 999) ตัวหนา 600
- อินพุตมุม 12px · เมนูมุม 14px · ชิปทรงแคปซูล
- ตัวอักษร `#F1F5F9` / รอง `#CBD5E1` ฟอนต์ `SF Pro Display` → fallback `IBM Plex Sans Thai`

สีกราฟใน Dashboard ใช้ `#3B82F6 / #D97706 / #0E9F8E` ซึ่งผ่านการตรวจคอนทราสต์และการแยกสี
สำหรับตาบอดสีบนพื้นหลัง `#111827` ของแอปจริง

## แก้ไขและ deploy ใหม่

```bash
cd design/gtg-chat-inbox
python3 build1.py && python3 build2.py && python3 build3.py \
  && python3 build4.py && python3 build5.py && python3 build6.py && python3 build7.py
```

`gen.py` เก็บโทเคนและส่วนประกอบกลาง (sidebar, ปุ่ม, การ์ด, ชิป) — แก้ที่เดียวแล้วสะท้อนทุกหน้าจอ
