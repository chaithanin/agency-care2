from shell import *

NEW  = f'<span class="chip" style="color:{SUCCESS};background:rgba(34,197,94,.14)">ใหม่</span>'
EXT  = f'<span class="chip" style="color:{PRIMARY_L};background:rgba(59,130,246,.16)">ต่อยอด</span>'
KEEP = f'<span class="chip" style="color:{TXT3};background:rgba(107,114,128,.18)">ใช้ของเดิม</span>'

TABLES = [
 ("1 · Construction", [
   ("construction_schedules", NEW, "โครงการ · ความถี่ · เวลา deadline · ผู้รับผิดชอบ · ผู้อนุมัติ · ตั้งค่าเตือน"),
   ("construction_rounds", NEW, "รอบละแถว · วันครบกำหนด · สถานะคำนวณเอง · ส่งเมื่อไหร่ ใครอนุมัติ"),
   ("construction_round_items", NEW, "เนื้อหาที่ส่ง · รูป · ความคืบหน้าเป็นเปอร์เซ็นต์"),
 ]),
 ("2-3 · Inventory", [
   ("PosmItem", KEEP, "ข้อมูลของ · เก็บไว้ แต่ stockQty กลายเป็นค่าที่คำนวณจากผลรวม"),
   ("stock_locations", NEW, "ที่เก็บ · ผูก project · ประเภท warehouse / showroom / sales office"),
   ("stock_balances", NEW, "ยอดคงเหลือต่อ (item, location) · @@unique กันซ้ำ"),
   ("stock_transactions", NEW, "receive · issue · transfer · adjustment · distribution · return"),
   ("PurchaseRequest", KEEP, "มี status ครบแล้ว ใช้ของเดิม"),
   ("PrItem", EXT, "เพิ่ม stock_location_id ว่ารับของเข้าที่ไหน"),
 ]),
 ("4 · Distribution", [
   ("stock_distributions", NEW, "แจกให้ agency ไหน ของอะไร กี่ชิ้น ใครส่ง ใครรับ"),
   ("stock_distribution_files", NEW, "หลักฐานการรับของ เก็บใน private bucket ลบไม่ได้"),
 ]),
 ("5 · Promotion Quota", [
   ("Unit", KEEP, "มี status available / reserved / booked / sold อยู่แล้ว"),
   ("promotion_quota_units", NEW, "โควตาผูกยูนิตจริงรายตัว · @@unique(unit_id) ตอนที่ยัง active"),
   ("promotion_quota_history", NEW, "ย้ายยูนิตข้ามแคมเปญ · ใครย้าย เมื่อไหร่ ตอนนั้นสถานะอะไร"),
 ]),
 ("6 · Message", [
   ("promotion_messages", NEW, "scope = internal | external · ผูกกับโปรโมชัน"),
   ("promotion_message_sends", NEW, "ส่งออกช่องทางไหน เมื่อไหร่ ใครสั่ง ผลเป็นยังไง"),
 ]),
 ("7 · Training", [
   ("TrainingRecord", KEEP, "บันทึกการเข้าอบรมเดิม ห้ามแตะ มีข้อมูลย้อนหลังอยู่"),
   ("training_courses", NEW, "ผูกกับ SOP / JD / Rules · version · passing score"),
   ("training_questions", NEW, "5 ข้อต่อคอร์ส · ตัวเลือก 4 ข้อ · เฉลย"),
   ("training_assignments", NEW, "มอบหมายให้ใคร กำหนดส่งเมื่อไหร่"),
   ("training_attempts", NEW, "ทุกครั้งที่สอบ · คะแนน · ผ่านไม่ผ่าน · ผูกกับ version ของคอร์ส"),
 ]),
 ("8 · Notification", [
   ("NotificationSetting", KEEP, "ค่ากลางเดิม ห้ามแตะ"),
   ("notification_events", NEW, "รายชื่อ event ทั้งหมด · กลุ่ม · คำอธิบาย"),
   ("notification_role_defaults", NEW, "ค่าเริ่มต้นต่อ role ต่อ event"),
   ("notification_user_prefs", NEW, "ค่าของแต่ละคน ชนะค่าของ role"),
   ("notification_outbox", NEW, "คิวส่ง · @@unique(event, target, ref_id) กันส่งซ้ำ"),
 ]),
]
rows = ""
for grp, items in TABLES:
    rows += (f'<tr><td colspan="3" style="padding-top:15px;border-bottom:0">'
             f'<span class="sec">{grp}</span></td></tr>')
    for name, tag, desc in items:
        rows += (f'<tr><td style="font-family:ui-monospace,monospace;font-size:13px;font-weight:600">{name}</td>'
                 f'<td style="width:120px">{tag}</td><td style="color:{TXT2}">{desc}</td></tr>')

ORDER = [
 ("1","Database Schema","ตารางทั้งหมด + สร้างตอนบูตแบบ IF NOT EXISTS + ห้ามแตะตารางเดิม"),
 ("2","Workflow","สถานะและกฎการเปลี่ยนสถานะของทั้ง 5 โมดูล เขียนเป็นฟังก์ชันล้วน ทดสอบได้โดยไม่ต้องมีฐานข้อมูล"),
 ("3","Permission","ใครทำอะไรได้ ตรวจฝั่ง server ทุกเส้น โดยเฉพาะ internal / external"),
 ("4","API","endpoint ตาม workflow ที่เขียนไว้แล้ว"),
 ("5","Notification","ต่อ event ของทุกโมดูลเข้า outbox เดียวกัน"),
 ("6","UI","ค่อยทำหน้าจอ"),
 ("7","QA Test Cases","ไล่ทุกเส้นทางสถานะ รวมเส้นที่ผิดพลาด"),
]
order_rows = "".join(
    f'<div class="row" style="gap:16px;padding:11px 0;border-bottom:1px solid {DIVIDER}">'
    f'<span style="width:30px;flex-shrink:0;font-size:18px;font-weight:700;color:{PRIMARY_L}">{n}</span>'
    f'<span class="b2" style="width:190px;flex-shrink:0;font-weight:700">{t}</span>'
    f'<span class="b2 grow" style="color:{TXT2}">{d}</span></div>' for n, t, d in ORDER)

RULES = [
 ("ห้ามเริ่มจาก UI","เจ้าของงานระบุเอง — เริ่มจาก schema แล้วไล่ลงมา ลดการรื้อทีหลัง"),
 ("ห้ามแก้ตารางเดิม","PosmItem · PurchaseRequest · Unit · TrainingRecord · NotificationSetting "
  "ใช้ของเดิมหรือเพิ่มคอลัมน์เท่านั้น ห้ามลบหรือเปลี่ยนความหมาย"),
 ("สถานะทุกตัวคำนวณ ไม่ใช่ตั้ง","Overdue · Remaining · Total stock — เก็บเป็นคอลัมน์เมื่อไหร่ ค่าจะเพี้ยนจากความจริงเมื่อนั้น"),
 ("ทุกการเปลี่ยนสต็อกต้องมีธุรกรรม","ห้าม UPDATE ยอดตรง ๆ — ยอดคงเหลือคือผลรวมของธุรกรรม"),
 ("Internal ห้ามมี endpoint ส่งออก","ไม่ใช่แค่ซ่อนปุ่ม ต้องไม่มีทางเรียกได้เลย"),
 ("ผลสอบผูกกับ version ของคอร์ส","แก้ SOP แล้วผลเก่าต้องยังอ้างเนื้อหาชุดเดิมได้"),
 ("แจ้งเตือนห้ามส่งซ้ำ","unique key ที่ระดับฐานข้อมูล ไม่ใช่เช็กในโค้ด"),
 ("ไฟล์หลักฐานลงถังส่วนตัว","savePrivate() เท่านั้น และต้องมี GCS_PRIVATE_BUCKET ตอน deploy"),
]
rule_rows = "".join(
    f'<div class="row" style="gap:14px;padding:10px 0;border-bottom:1px solid {DIVIDER}">'
    f'{icon(I_WARN,16,WARNING)}<div class="col grow" style="gap:2px">'
    f'<span class="b2" style="font-weight:700">{t}</span>'
    f'<span class="cap" style="color:{TXT2}">{d}</span></div></div>' for t, d in RULES)

body = f"""{note_box("info","เจ้าของงานกำหนดลำดับไว้เอง — Database Schema → Workflow → Permission "
          "→ API → Notification → UI → QA ห้ามเริ่มจากหน้า UI")}
<div class="row" style="gap:18px;align-items:flex-start">
  {panel("ตารางที่ต้องมี", f'<div class="row" style="gap:8px">{NEW}{EXT}{KEEP}</div>',
    f'<table><tbody>{rows}</tbody></table>')}
  <div class="col" style="gap:18px;width:480px;flex-shrink:0">
    {panel("ลำดับการทำ", "", f'<div class="col" style="gap:0">{order_rows}</div>', grow=False)}
    {panel("กฎที่ห้ามทำผิด", "", f'<div class="col" style="gap:0">{rule_rows}</div>', grow=False)}
  </div>
</div>"""

open("Main.dc.html","w").write(
    sheet("Baseline v1.0 — Schema &amp; ลำดับการทำ",
          "ตารางทั้งหมด อันไหนใหม่ อันไหนต่อยอด อันไหนใช้ของเดิม",
          body, 1720, 1720))
print("Main.dc.html")
