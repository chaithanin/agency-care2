from shell import *

# ══════════ 3. CONTACT DETAIL — จัดบทบาท ══════════
profile = f"""<div class="card pad row" style="gap:16px;align-items:flex-start">
  <div style="width:64px;height:64px;border-radius:999px;background:{SURFACE};
       border:1px solid {DIVIDER};flex-shrink:0"></div>
  <div class="col grow" style="gap:6px">
    <div class="row" style="gap:10px">
      <span class="h6" style="font-size:19px;font-weight:700">Chatchai Pongsakorn</span>
      {role_chip("Agency")}{role_chip("Customer")}
    </div>
    <div class="row" style="gap:20px;flex-wrap:wrap">
      <span class="cap"><span class="mut">LINE</span> &nbsp;@chatchai</span>
      <span class="cap"><span class="mut">User ID</span> &nbsp;U4af49…8d2c</span>
      <span class="cap"><span class="mut">Followed</span> &nbsp;12 Sep 2026</span>
      <span class="cap"><span class="mut">Last activity</span> &nbsp;2 days ago</span>
      <span class="cap">{status_dot("Active")}</span>
    </div>
  </div>
  <button class="btn sm out">Send Message</button>
</div>"""

def role_card(kind, lines, seller=None):
    chip = role_chip(kind)
    rows = "".join(
        f'<div class="row" style="gap:10px"><span class="cap mut" style="width:120px;flex-shrink:0">{k}</span>'
        f'<span class="b2" style="color:{TXT2}">{v}</span></div>' for k, v in lines)
    return f"""<div class="col" style="gap:11px;background:{SURFACE};border:1px solid {DIVIDER};
     border-radius:16px;padding:15px 17px">
  <div class="row" style="gap:10px">{chip}<span class="grow"></span>
    <button class="btn sm out">Edit</button>
    <button class="btn sm out" style="color:{ERROR};border-color:rgba(239,68,68,.4)">Remove</button></div>
  <div class="col" style="gap:7px">{rows}</div>
</div>"""

roles_body = f"""<div class="col" style="gap:12px">
  {role_card("Agency", [("Agency","ABC Property Pattaya"),("Position","Owner"),
                        ("Assigned Seller","K. Somchai"),("Classified by","K. Pim · 12 Sep 2026 16:04")])}
  {role_card("Customer", [("CRM Lead","CUS-004182 — Chatchai Pongsakorn"),
                          ("Interested Project","LOVE IT Wongamat"),
                          ("Assigned Seller","K. May"),("Classified by","K. May · 14 Sep 2026 10:22")])}
  <div class="row" style="gap:10px">
    <button class="btn sm out">{icon(I_PLUS,13,TXT2)} &nbsp;Add role</button>
    <span class="cap mut" style="align-self:center">ลบบทบาทสุดท้ายออก contact จะกลับไปเป็น Unclassified เอง</span>
  </div>
</div>"""

match = f"""<div class="col" style="gap:12px">
  <div class="row" style="gap:14px;background:rgba(34,197,94,.07);border:1px solid rgba(34,197,94,.30);
       border-radius:16px;padding:14px 16px;align-items:center">
    <div class="col grow" style="gap:3px">
      <span class="b2" style="font-weight:700;color:{SUCCESS}">Possible match พบใน CRM</span>
      <span class="cap mut">Somchai Prasert · 081-234-5678 · เบอร์ตรงกับโปรไฟล์ LINE</span>
    </div>
    <button class="btn sm out">Not a match</button>
    <button class="btn sm">Link Customer</button>
  </div>
  <div class="row" style="gap:14px">
    {field("Phone","+66 81 234 5678", w=210)}
    {field("Email","chatchai@abcprop.co.th")}
    {field("Language","Thai", w=150)}
    {field("Nationality","Thai", w=160)}
  </div>
  <div class="col" style="gap:0">
    <p class="lbl">Tags</p>
    <div class="row" style="gap:8px;flex-wrap:wrap">
      <span class="chip" style="background:rgba(59,130,246,.16);color:{PRIMARY_L}">VIP</span>
      <span class="chip" style="background:rgba(59,130,246,.16);color:{PRIMARY_L}">Wongamat</span>
      <span class="chip" style="border:1px solid {DIVIDER};color:{TXT3}">+ Add tag</span>
    </div>
  </div>
</div>"""

body = f"""{profile}
{panel("Roles", f'<span class="cap mut">2 บทบาท</span>', roles_body,
       note="คนหนึ่งเป็นได้หลายบทบาท เก็บแยกแถวกัน แต่ละบทบาทผูกกับข้อมูลคนละชุด")}
{panel("Profile &amp; CRM Link", "", match)}"""
open("ContactDetail.dc.html","w").write(
    page_shell("CONTACTS", body, 1240, 1080, title="Contact — Chatchai Pongsakorn",
               subtitle="จัดบทบาทและผูกกับข้อมูลในระบบ"))
print("ContactDetail.dc.html")

# ══════════ 4. STEP 1 — AUDIENCE ══════════
def aud_opt(label, count, note, on=False, warn=False):
    dot = (f'<div style="width:19px;height:19px;border-radius:999px;border:2px solid {PRIMARY};'
           f'display:grid;place-items:center"><div style="width:9px;height:9px;border-radius:999px;'
           f'background:{PRIMARY}"></div></div>' if on else
           f'<div style="width:19px;height:19px;border-radius:999px;border:2px solid {DIVIDER}"></div>')
    bd = f"1px solid {PRIMARY}" if on else f"1px solid {DIVIDER}"
    bg = "rgba(59,130,246,.08)" if on else SURFACE
    return f"""<div class="row" style="gap:12px;border:{bd};background:{bg};border-radius:16px;
     padding:14px 16px;align-items:center;cursor:pointer">
  {dot}
  <div class="col grow" style="gap:2px">
    <span class="b2" style="font-weight:700">{label}</span>
    <span class="cap mut">{note}</span>
  </div>
  <span class="b2" style="font-weight:700;color:{WARNING if warn else TXT}">{count}</span>
</div>"""

aud = f"""<div class="col" style="gap:10px">
  {aud_opt("Sales","42 recipients","ทีมขายที่ผูก LINE แล้ว")}
  {aud_opt("Customers","873 recipients","ลูกค้าและผู้สนใจ")}
  {aud_opt("Agencies","291 recipients","ผู้ติดต่อของเอเจนซี่ทุกราย")}
  {aud_opt("All","1,206 eligible recipients","Sales + Customers + Agencies — ไม่รวม Unclassified", on=True)}
  {aud_opt("Custom Selection","กรองเอง","เลือกตามโครงการ ภาษา เอเจนซี่ หรือผู้ดูแล")}
</div>
<div class="col" style="gap:10px;background:rgba(251,191,36,.08);border:1px solid rgba(251,191,36,.35);
     border-radius:16px;padding:14px 16px">
  <div class="row" style="gap:10px">
    <div style="width:18px;height:18px;border-radius:5px;border:1.5px solid {WARNING}"></div>
    <span class="b2" style="color:{WARNING};font-weight:600">Include Unclassified Contacts (78)</span>
    <span class="grow"></span>
    <span class="chip" style="color:{WARNING};background:rgba(251,191,36,.15)">Manager / Admin only</span>
  </div>
  <p class="cap mut" style="margin:0">ปกติไม่รวม เพราะยังไม่รู้ว่าคนกลุ่มนี้เป็นลูกค้าหรือเอเจนซี่
    ส่งไปอาจผิดกลุ่ม</p>
</div>"""

warn_internal = f"""<div class="card pad row" style="gap:12px;border-color:rgba(239,68,68,.35);
     background:rgba(239,68,68,.07)">
  {icon(I_WARN,18,ERROR)}
  <div class="col grow" style="gap:2px">
    <span class="b2" style="color:{ERROR};font-weight:700">ประเภท HR / IT / Training ส่งได้เฉพาะ Sales</span>
    <span class="cap mut">ถ้าเลือกประเภทเหล่านี้ ตัวเลือก Customers · Agencies · All จะถูกปิด
      และ server ปฏิเสธถ้าพยายามส่ง</span>
  </div>
</div>"""

body4 = f"""{steps(1)}
{panel("Select Audience", f'<span class="cap mut">Who would you like to send this message to?</span>', aud)}
{warn_internal}
<div class="row" style="gap:10px;justify-content:flex-end">
  <button class="btn out">Cancel</button>
  <button class="btn">Next — Message</button>
</div>"""
open("Step1Audience.dc.html","w").write(
    page_shell("OVERVIEW", body4, 1240, 1080, title="New Announcement",
               subtitle="ขั้นที่ 1 จาก 4 — เลือกกลุ่มผู้รับ"))
print("Step1Audience.dc.html")
