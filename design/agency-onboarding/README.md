# Mockup — Agency Onboarding (7-Phase Workflow)

Design canvas: https://claude.ai/artifact/PnXe4coE7J9wNhB25UP9f6

ออกแบบใหม่แทนหน้า Onboarding เดิมของ Agency Care ซึ่งเป็นตารางเปล่า ๆ
(`New Agency Onboarding — 0 open / 0 completed`) + drawer เช็กบ็อกซ์

**เป็น mockup นิ่ง ๆ ไม่ได้ต่อ API และไม่ได้แก้โค้ดของระบบจริง**

## หน้าจอ

| ไฟล์ | หน้าจอ |
| --- | --- |
| `Main.dc.html` | Dashboard — stat card 5 ตัว, filter, search, การ์ดเอเจนซี่ |
| `Detail.dc.html` | Phase 1a — Agency Background, Market Focus, Business Channel |
| `Phase1Docs.dc.html` | Phase 1b — Documents, Bank, Contacts, Social & Online |
| `Phase2.dc.html` | Phase 2 — LINE Group + Assigned Seller |
| `Phase3.dc.html` | Phase 3 — Venio CRM Setup + Initial Agency Report |
| `Phase4.dc.html` | Phase 4 — Welcome Communication + Marketing Package |
| `Phase5.dc.html` | Phase 5 — Agreement approval flow + checklist |
| `Phase6.dc.html` | Phase 6 — Sales Materials + Agency Visit |
| `Phase7.dc.html` | Phase 7 — Relationship Schedule + Activity + Completion |

## สถานะหลัก

```
New → In Progress → Waiting Agency → Need Attention → Completed
```

## ตรรกะที่ mockup ตั้งใจแสดงให้เห็น

1. **Phase 1b** — เลือก *Owner Personal Account* แล้ว Authorization Letter
   กลายเป็นฟิลด์บังคับทันที (ตาม requirement เรื่องจ่าย commission เข้าบัญชีส่วนตัว)
2. **Phase 7** — ปุ่ม *Complete Onboarding* ถูก disable ไว้ ระบบคำนวณ
   Onboarding Readiness เอง ผู้ใช้กดปิดงานเองไม่ได้
3. **Phase 7** — Relationship Schedule เป็นเป้าที่ระบบสร้างให้อัตโนมัติ
   (เยี่ยม 2 ครั้ง/เดือน · โทร 4 ครั้ง/เดือน · ส่ง material ทุกสัปดาห์)

## ค่าที่ลอกมาจากโปรเจกต์จริง

ดึงจาก `web/src/theme/ThemeContext.tsx` โหมด dark ของ `chaithanin/agency-care`
branch `feat/all-appointments-clean-on-118a2e2` = revision **agency-care-00886-nus**

| | |
| --- | --- |
| พื้นหลัง | `linear-gradient(135deg,#0F172A 0%,#111827 60%,#1F2937 100%)` |
| การ์ด / Paper | `#111827` · radius `20px` |
| เส้นแบ่ง | `#374151` |
| ตัวอักษร | `#F1F5F9` / `#CBD5E1` / `#6B7280` |
| primary / secondary | `#3B82F6` / `#A78BFA` |
| success / warning / error / info | `#22C55E` / `#FBBF24` / `#EF4444` / `#38BDF8` |
| ปุ่ม | radius `999` · ไม่ใช้ตัวพิมพ์ใหญ่ · น้ำหนัก 600 · padding ซ้ายขวา 18 |
| เมนูด้านข้าง | radius `14` · ขอบขวา `1px solid #374151` |
| ฟอนต์ | `"SF Pro Display", -apple-system, "Segoe UI", ...` |

## สร้างไฟล์ใหม่

```bash
cd design/agency-onboarding
python3 build_dashboard.py && python3 build_p1.py && python3 build_p23.py \
  && python3 build_p45.py && python3 build_p67.py
```

`tokens.py` เก็บสีและสไตล์ · `shell.py` เก็บ header กับ stepper 7 เฟส
ที่ทุกหน้ารายละเอียดใช้ร่วมกัน · `canvas.json` คุมตำแหน่งบนผืนผ้าใบ

## ยังไม่ได้ทำ

- ตารางสิทธิ์ตาม role 6 ตัว (System Admin / Manager / Agency Support /
  Assigned Seller / Marketing / Project Manager)
- หน้า Audit log ของ Agreement, Bank Information และ Document ที่ verified แล้ว
