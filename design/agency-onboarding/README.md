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
| `Permissions.dc.html` | ตารางสิทธิ์ 13 พื้นที่ × 6 role |
| `AuditLog.dc.html` | Audit log + การ์ด Verified By / Verified At |
| `Mandatory.dc.html` | นิยามรายการบังคับ + กฎสถานะ Waiting Agency |

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

## สิทธิ์และร่องรอย

`Permissions.dc.html` กำหนดสิทธิ์ 13 พื้นที่ × 6 role ด้วย 5 ระดับ
(Full / Edit / Verify / View / ไม่มีสิทธิ์) กติกาที่ตารางบังคับ:

1. **Bank Information** แก้ได้เฉพาะ System Admin — Agency Support ยืนยันได้แต่แก้เลขบัญชีไม่ได้
2. **คนอัปโหลดเอกสารกับคนกด Verified ต้องคนละคน** — Seller อัปได้ แต่ยืนยันเองไม่ได้
3. **Complete Onboarding** กดได้เฉพาะ Manager ขึ้นไป และต่อเมื่อรายการบังคับครบ
4. ตัดสินสิทธิ์จาก `activeRole` ไม่ใช่ role ในโปรไฟล์ — ตรงกับโมดูลอื่นในระบบ

สี่จุดที่ต้องเก็บ Verified By / Verified At และ audit log เสมอ:
Document Verification · Bank Information · Agreement · Complete Onboarding

## รายการบังคับ — ใช้กฎเดิมของระบบ ไม่สร้างซ้ำ

ระบบมีกฎ mandatory ของ agency อยู่แล้ว และ**ใช้ร่วมกันสองที่**

| ไฟล์ | บทบาท |
| --- | --- |
| `api/src/agency/agency-profile.util.ts` → `missingAgencyProfile()` | ฝั่ง server — ตัวจริง |
| `web/src/components/AddAgencyDialog.tsx` → `missingProfile()` | ฝั่งหน้าเว็บ ต้องตรงกับข้างบน |

**Onboarding ต้องเรียกใช้ `missingAgencyProfile()` ไม่ใช่เขียนรายการใหม่ขึ้นมาซ้อน**
ไม่งั้นจะมีนิยามคำว่า "ข้อมูลครบ" สองชุดที่ค่อย ๆ เพี้ยนออกจากกัน

รวมทั้งหมด **34 ข้อบังคับเสมอ + 7 ข้อตามเงื่อนไข**

| เงื่อนไข | ผลต่อตัวหาร |
| --- | --- |
| ติ๊ก New Agency | ลด 3 ข้อ (Last Sale Date, Last Units Sold, Total Units Sold) |
| Office Type = Non-Physical | ลด 2 ข้อ (Address, Google Map Link) |
| Existing Relationship = No Have | ลด 1 ข้อ (รายละเอียดความสัมพันธ์) |
| บัญชีบริษัท ไม่ใช่บัญชีส่วนตัว | ลด 1 ข้อ (Authorization Letter) |

**ตัวหารจึงไม่คงที่** อยู่ระหว่าง 34 ถึง 41 ข้อ คำนวณต่อเอเจนซี่ตอนโหลด

## สถานะ Waiting Agency — ระบบตั้งให้เอง

```
In Progress ──(เงียบครบ 3 วัน)──> Waiting Agency ──(เงียบต่ออีก 4 วัน)──> Need Attention
```

### เหตุการณ์ที่รีเซ็ตตัวนับ — มีสองอย่างเท่านั้น

| รีเซ็ต | ไม่รีเซ็ต |
| --- | --- |
| อัปโหลดเอกสารเข้า onboarding | ข้อความในกลุ่ม LINE |
| ติ๊กหรือปลดติ๊ก checklist ข้อใดก็ได้ | เปิดดูหน้า onboarding |
| | แก้โน้ตภายในหรือข้อความในฟอร์ม |
| | เปลี่ยนผู้ดูแล |

เหตุผล: สองอย่างแรกเป็นร่องรอยที่พิสูจน์ได้ว่างานเดินจริง ส่วนการคุยกันเฉย ๆ
ไม่นับว่าคืบหน้า

- นับจากเหตุการณ์ล่าสุดในสองอย่างนั้น ไม่ใช่วันที่สร้าง onboarding
- เอเจนซี่ส่งเอกสารมาแล้วทีมเราอัปเข้าระบบหรือติ๊ก checklist ให้
  → ตัวนับรีเซ็ตและกลับเป็น In Progress เอง
- เอกสารที่ถูก Reject ก็นับว่าเป็นการอัปโหลด — ตัวนับรีเซ็ต เพราะมีคนทำงานกับมันจริง
- ผู้ใช้ตั้งสถานะนี้เองไม่ได้ เป็นค่าที่ระบบคำนวณเหมือนเปอร์เซ็นต์ความคืบหน้า
- Completed แล้วหยุดนับ — ย้ายไปอยู่ภายใต้กติกา Relationship Maintenance แทน

**หมายเหตุสำหรับตอนเขียนโค้ด** — สองเหตุการณ์นี้อยู่ใน audit log อยู่แล้ว
ตัวนับอ่านจาก log ได้เลย ไม่ต้องเพิ่มฟิลด์เก็บเวลาในตาราง onboarding
