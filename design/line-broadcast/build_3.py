from shell import *

def check(label, on=True, muted=False):
    mark = (f'<div style="width:18px;height:18px;border-radius:5px;background:{SUCCESS};'
            f'display:grid;place-items:center;flex-shrink:0">{icon(I_CHECK,12,"#0F172A")}</div>' if on else
            f'<div style="width:18px;height:18px;border-radius:5px;border:1.5px solid {DIVIDER};flex-shrink:0"></div>')
    col = TXT if on else (TXT3 if muted else TXT2)
    return f'<div class="row" style="gap:10px;padding:5px 0">{mark}<span class="b2" style="color:{col}">{label}</span></div>'

# ══════════ 5. CUSTOM SELECTION ══════════
def grp(title, items):
    return (f'<div class="col" style="gap:4px"><p class="lbl">{title}</p>'
            + "".join(check(l, o) for l, o in items) + '</div>')

filters = f"""<div class="col" style="gap:16px">
  {grp("CONTACT TYPE", [("Customer",True),("Agency",True),("Sales",False),("Partner",False)])}
  {grp("PROJECT INTEREST", [("LOVE IT Wongamat",True),("Marina Golden Bay",False),
                            ("Harmonia",False),("LUMINA",False)])}
  {grp("LANGUAGE", [("Thai",True),("English",True),("Russian",False),("Chinese",False)])}
  <div class="row" style="gap:14px">
    {field("Agency","All Agencies")}
    {field("Assigned Seller","All Sellers")}
  </div>
</div>"""

preview = f"""<div class="col" style="gap:14px;width:330px;flex-shrink:0">
  <div class="col" style="gap:12px;background:{SURFACE};border:1px solid {DIVIDER};
       border-radius:16px;padding:16px 18px">
    <h4 class="sec">Audience Preview</h4>
    <div class="col" style="gap:1px">
      <span style="font-size:32px;font-weight:700;letter-spacing:-0.02em;color:{PRIMARY_L}">328</span>
      <span class="cap mut">recipients · นับหัวไม่ซ้ำ</span>
    </div>
    <div style="height:1px;background:{DIVIDER}"></div>
    <div class="col" style="gap:7px">
      <div class="row"><span class="b2 grow" style="color:{TXT2}">Customers</span>
        <span class="b2" style="font-weight:700">289</span></div>
      <div class="row"><span class="b2 grow" style="color:{TXT2}">Agency Contacts</span>
        <span class="b2" style="font-weight:700">39</span></div>
      <div class="row"><span class="b2 grow" style="color:{TXT3}">อยู่ทั้งสองกลุ่ม</span>
        <span class="b2" style="color:{TXT3}">4</span></div>
    </div>
    <p class="cap mut" style="margin:0">289 + 39 = 328 หลังหักคนที่ซ้ำ 4 คนออกแล้ว
      แต่ละคนได้ข้อความใบเดียว</p>
    <button class="btn sm out">View Recipient List</button>
  </div>
</div>"""

body = f"""{steps(1)}
{panel("Custom Selection", f'<span class="cap mut">นับผู้รับใหม่ทันทีที่เปลี่ยนตัวกรอง</span>',
  f'<div class="row" style="gap:28px;align-items:flex-start">'
  f'<div class="grow">{filters}</div>'
  f'<div style="width:1px;align-self:stretch;background:{DIVIDER}"></div>{preview}</div>')}
<div class="row" style="gap:10px;justify-content:flex-end">
  <button class="btn out">Back</button>
  <button class="btn">Next — Message</button>
</div>"""
open("CustomSelection.dc.html","w").write(
    page_shell("OVERVIEW", body, 1240, 1000, title="New Announcement",
               subtitle="ขั้นที่ 1 จาก 4 — Custom Selection"))
print("CustomSelection.dc.html")

# ══════════ 6. STEP 2 — MESSAGE ══════════
msg = f"""<div class="col" style="gap:14px">
  <div class="row" style="gap:14px">
    {field("Title","MARINA SEPTEMBER UPDATE")}
    {field("Category","Promotion", w=210)}
    {field("Priority","Normal", w=180)}
  </div>
  <div class="col" style="gap:0">
    <p class="lbl">Message</p>
    <div class="fld" style="min-height:120px;color:{TXT2}">อัปเดตความคืบหน้า Marina Golden Bay
เดือนกันยายน — งานโครงสร้างชั้น 24 เสร็จแล้ว พร้อมราคาและยูนิตคงเหลือล่าสุด

ดูรายละเอียดและ price list ได้ที่ลิงก์ด้านล่าง</div>
  </div>
  <div class="row" style="gap:12px;flex-wrap:wrap">
    <button class="btn sm out">{icon(I_UP,13,TXT2)} &nbsp;Image</button>
    <button class="btn sm out">{icon(I_UP,13,TXT2)} &nbsp;Video</button>
    <button class="btn sm out">{icon(I_UP,13,TXT2)} &nbsp;PDF</button>
    <button class="btn sm out">{icon(I_PLUS,13,TXT2)} &nbsp;Link button</button>
    <span class="grow"></span>
    <button class="btn sm out">Load from template</button>
  </div>
  <div class="row" style="gap:12px">
    <div style="width:120px;height:120px;border-radius:14px;background:{SURFACE};
         border:1px solid {DIVIDER}"></div>
    <div class="col" style="gap:8px;align-self:center">
      <span class="b2" style="font-weight:600">marina-sept-update.jpg</span>
      <span class="cap mut">1440 × 960 · 412 KB</span>
    </div>
  </div>
</div>"""

body2 = f"""{steps(2)}
<div class="card pad row" style="gap:12px;border-color:rgba(167,139,250,.35);background:rgba(167,139,250,.07)">
  {icon(I_CHECK,18,SECOND)}
  <span class="b2 grow" style="color:{SECOND}">Audience: <b>Agencies</b> · 291 recipients</span>
  <button class="btn sm out">เปลี่ยนกลุ่มผู้รับ</button>
</div>
{panel("Message", "", msg)}
<div class="row" style="gap:10px;justify-content:flex-end">
  <button class="btn out">Back</button>
  <button class="btn">Next — Preview</button>
</div>"""
open("Step2Message.dc.html","w").write(
    page_shell("OVERVIEW", body2, 1240, 1000, title="New Announcement",
               subtitle="ขั้นที่ 2 จาก 4 — เนื้อหาข้อความ"))
print("Step2Message.dc.html")
