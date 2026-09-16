from shell import *

# ══════════ 9. SEND HISTORY ══════════
BADGE = {"Agencies":(SECOND,"rgba(167,139,250,.16)"), "Customers":(SUCCESS,"rgba(34,197,94,.14)"),
         "Sales":(INFO,"rgba(56,189,248,.14)"), "All":(PRIMARY_L,"rgba(59,130,246,.16)"),
         "Custom":(TXT2,"rgba(203,213,225,.10)")}

def card(title, badge, recips, delivered, failed, read, by, when, status="Sent", note=None):
    c, bg = BADGE[badge]
    sc = {"Sent":SUCCESS, "Scheduled":WARNING, "Failed":ERROR}[status]
    sbg = {"Sent":"rgba(34,197,94,.14)","Scheduled":"rgba(251,191,36,.15)","Failed":"rgba(239,68,68,.15)"}[status]
    note_html = f'<p class="cap mut" style="margin:0">{note}</p>' if note else ""
    read_pct = int(read.rstrip('%')) if read.endswith('%') else 0
    return f"""<div class="card pad col" style="gap:13px">
  <div class="row" style="gap:10px;flex-wrap:wrap">
    <span class="b2" style="font-weight:700">{title}</span>
    <span class="chip" style="color:{c};background:{bg}">{badge}</span>
    <span class="grow"></span>
    <span class="chip" style="color:{sc};background:{sbg}">{status}</span>
  </div>
  <div class="row" style="gap:26px;flex-wrap:wrap">
    <div class="col" style="gap:1px"><span class="cap mut">Recipients</span>
      <span class="b2" style="font-weight:700">{recips}</span></div>
    <div class="col" style="gap:1px"><span class="cap mut">Delivered</span>
      <span class="b2" style="font-weight:700;color:{SUCCESS}">{delivered}</span></div>
    <div class="col" style="gap:1px"><span class="cap mut">Failed</span>
      <span class="b2" style="font-weight:700;color:{ERROR if failed!='0' else TXT3}">{failed}</span></div>
    <div class="col grow" style="gap:4px;min-width:170px">
      <div class="row"><span class="cap mut grow">Read</span>
        <span class="cap" style="font-weight:700;color:{TXT2}">{read}</span></div>
      {bar(read_pct, PRIMARY)}
    </div>
    <div class="col" style="gap:1px;align-items:flex-end"><span class="cap mut">{by}</span>
      <span class="cap mut">{when}</span></div>
  </div>
  {note_html}
  <div class="row" style="gap:10px">
    <button class="btn sm out">View recipient list</button>
    <button class="btn sm out">Duplicate</button>
  </div>
</div>"""

filters = f"""<div class="card" style="padding:14px 18px">
  <div class="row" style="gap:10px;flex-wrap:wrap">
    <div class="row fld grow" style="gap:9px;padding:8px 14px;border-radius:999px;min-width:260px">
      {icon(I_SEARCH,16,TXT3)}<span class="b2 mut">Search title...</span>
    </div>
    {pill("All Audiences")}{pill("Status")}{pill("Sent by")}{pill("Date range")}
  </div>
</div>"""

body = f"""{filters}
{card("MARINA SEPTEMBER UPDATE","Agencies","284","278","6","64%","SystemAdmin","16/09/2026 14:30")}
{card("LOVE IT Wongamat — new price list","Customers","721","715","6","51%","K. May","15/09/2026 09:12")}
{card("Weekly sales meeting moved to 10:00","Sales","42","42","0","93%","K. Warun","15/09/2026 08:00",
      note="ประเภท HR — ส่งได้เฉพาะกลุ่ม Sales เท่านั้นตามกฎของระบบ")}
{card("Golden week promotion","Custom","328","—","—","0%","K. May","18/09/2026 09:00",status="Scheduled",
      note="Custom Selection: Customer + Agency · LOVE IT Wongamat · Thai, English")}"""

open("History.dc.html","w").write(
    page_shell("SEND HISTORY", body, 1240, 1080,
               subtitle="ประวัติการส่ง — เก็บรายชื่อผู้รับไว้ทุกครั้ง"))
print("History.dc.html")

# ══════════ 10. DATA MODEL & RULES ══════════
def sql_card(title, note, lines):
    rows = "".join(
        f'<div class="row" style="gap:12px;padding:5px 0;border-bottom:1px solid {DIVIDER}">'
        f'<span class="b2" style="width:210px;flex-shrink:0;font-weight:600;font-family:ui-monospace,monospace;'
        f'font-size:13px">{k}</span><span class="cap" style="color:{TXT2}">{v}</span></div>'
        for k, v in lines)
    return f"""<div class="card pad col" style="gap:12px">
  <div class="row" style="gap:12px"><h3 class="sec grow">{title}</h3></div>
  <p class="cap mut" style="margin:0">{note}</p>
  <div class="col" style="gap:0">{rows}</div>
</div>"""

contacts_tbl = sql_card("line_contacts — ตัวคน", "หนึ่งแถวต่อหนึ่ง LINE User", [
  ("line_user_id","unique — ตัวระบุจาก LINE"),
  ("display_name / picture_url","ดึงจาก getProfile() ที่มีอยู่แล้วใน line.service.ts"),
  ("phone / email / language / nationality","เติมทีหลังตอนจัดบทบาทหรือผูกกับ CRM"),
  ("project_interest","string[] — โครงการที่สนใจ"),
  ("followed_at / unfollowed_at / last_interaction_at","จาก webhook"),
  ("status","active | blocked | inactive — นับเฉพาะ active"),
  ("tags","string[]"),
])

roles_tbl = sql_card("line_contact_roles — บทบาท", "หนึ่งแถวต่อหนึ่งบทบาท คนหนึ่งมีได้หลายแถว", [
  ("line_contact_id","-> line_contacts (cascade)"),
  ("contact_type","sales | customer | agency | partner | other"),
  ("customer_lead_id","-> CustomerLead (เมื่อเป็น customer)"),
  ("agency_id","-> Agency (เมื่อเป็น agency)"),
  ("employee_id","-> Employee (เมื่อเป็น sales — บังคับ)"),
  ("position","ตำแหน่งในเอเจนซี่ เช่น Owner, Sales Manager"),
  ("assigned_seller_id","-> Employee"),
  ("classified_by_id / classified_at","ใครจัดบทบาทนี้ เมื่อไหร่"),
  ("@@unique","(line_contact_id, contact_type)"),
])

unclass = f"""<div class="card pad col" style="gap:12px;border-color:rgba(251,191,36,.35);
     background:rgba(251,191,36,.07)">
  <h3 class="sec" style="color:{WARNING}">Unclassified คือ "ไม่มีบทบาท"</h3>
  <p class="b2" style="margin:0;color:{TXT2}">ไม่ต้องมี contact_type ชื่อ unclassified —
    contact ที่ยังไม่มีแถวใน line_contact_roles เลย คือ Unclassified โดยนิยาม</p>
  <div class="fld" style="font-family:ui-monospace,monospace;font-size:12.5px;color:{TXT2};line-height:1.7">
SELECT COUNT(*) FROM line_contacts c<br>
WHERE c.status = 'active'<br>
&nbsp;&nbsp;AND NOT EXISTS (SELECT 1 FROM line_contact_roles r<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;WHERE r.line_contact_id = c.id);
  </div>
  <p class="cap mut" style="margin:0">หมดปัญหาสถานะกำกวมแบบ "มีบทบาท Customer แล้ว
    แต่ยังเป็น unclassified อยู่"</p>
</div>"""

RULES = [
 ("1","คนใหม่เข้า Unclassified เสมอ",
  "follow event เข้ามา สร้างแถวใน line_contacts โดยไม่สร้าง role เลย ห้ามเดาจากชื่อหรือรูป "
  "ยกเว้น lineUserId ตรงกับ employee.lineUserId หรือ agency.lineUserId ที่ผูกไว้แล้ว"),
 ("2","Sales มาจากฐานพนักงานเท่านั้น",
  "role sales สร้างได้เฉพาะเมื่อ employee_id ไม่ว่าง คนนอกเลือกเองไม่ได้ ตรวจฝั่ง server"),
 ("3","All ไม่รวม Unclassified",
  "All = Sales + Customer + Agency จะรวม Unclassified ต้องติ๊กเพิ่ม และเฉพาะ Manager กับ Admin"),
 ("4","ข้อความภายในห้ามหลุดออกนอก",
  "type hr / it / training ส่งได้เฉพาะกลุ่ม Sales — ปฏิเสธที่ server ไม่ใช่แค่ซ่อนตัวเลือก"),
 ("5","unfollow ห้ามลบข้อมูล",
  "ตั้ง status = inactive และ unfollowed_at เก็บแถวไว้ ประวัติการส่งต้องยังอ้างถึงได้"),
 ("6","Agency เก็บเป็นหลายคน",
  "เอเจนซี่หนึ่งรายมีได้หลาย contact ทุกคนมี role agency ที่ชี้ agency_id เดียวกัน เก็บตำแหน่งใน position"),
 ("7","คนซ้ำต้องได้ข้อความครั้งเดียว",
  "query ที่ระดับ line_contacts ด้วย DISTINCT หรือ EXISTS เสมอ ห้าม query จาก roles แล้ววนส่ง "
  "และใส่ @@unique(broadcast_id, line_contact_id) เป็นตาข่ายกันพลาด"),
 ("8","blocked และ inactive ไม่นับไม่ส่ง",
  "ทุก counter และ audience นับเฉพาะ status = active แต่หน้า Preview ต้องบอกจำนวนที่ถูกตัดออกให้เห็น"),
]
rules = "".join(
  f'<div class="row" style="gap:14px;padding:11px 0;border-bottom:1px solid {DIVIDER}">'
  f'<span style="width:26px;flex-shrink:0;font-weight:700;color:{PRIMARY_L}">{n}</span>'
  f'<div class="col grow" style="gap:3px"><span class="b2" style="font-weight:700">{t}</span>'
  f'<span class="cap" style="color:{TXT2}">{d}</span></div></div>' for n, t, d in RULES)

body2 = f"""<div class="row" style="gap:18px;align-items:flex-start">
  <div class="col grow" style="gap:18px">{contacts_tbl}{roles_tbl}</div>
  <div class="col" style="gap:18px;width:430px;flex-shrink:0">{unclass}
    {panel("กฎที่ห้ามทำผิด","", f'<div class="col" style="gap:0">{rules}</div>')}</div>
</div>"""

open("DataModel.dc.html","w").write(
    page_shell("CONTACTS", body2, 1560, 1560, title="Data Model &amp; Rules",
               subtitle="โครงสร้างฐานข้อมูลและกฎที่ต้องบังคับฝั่ง server"))
print("DataModel.dc.html")
