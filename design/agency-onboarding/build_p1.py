from shell import *

# ── Phase 1a — Agency Profile (ใช้ฟิลด์จริงจากฟอร์ม Add Agency) ──
def req(label, value="", filled=True, w=None):
    """ฟิลด์บังคับ — ยังไม่กรอกจะขึ้นขอบแดง"""
    style = "flex-grow:1;min-width:0" if w is None else f"width:{w}px;flex-shrink:0"
    border = "" if filled else f"border-color:{ERROR}"
    shown = value if filled else f'<span style="color:{ERROR}">ยังไม่ได้กรอก</span>'
    star = f'<span style="color:{ERROR}">&nbsp;*</span>'
    return f"""<div class="col" style="gap:0;{style}">
  <p class="lbl">{label}{star}</p>
  <div class="fld" style="{border}">{shown}</div>
</div>"""

sec1 = f"""<div class="col" style="gap:14px">
  <div class="row" style="gap:14px">
    {field("Agency Code","AG-00238", w=150)}
    {req("Agency Name","ABC Property Pattaya Co., Ltd.")}
    {req("Contact Person","Mr. Chatchai Pongsakorn", w=250)}
  </div>
  <div class="row" style="gap:14px">
    {req("Phone","+66 81 234 5678", w=210)}
    {req("Email","chatchai@abcprop.co.th", w=260)}
    {field("Website","abcproperty-pattaya.com")}
    {field("Tax ID / National ID","0205561012345", w=190)}
  </div>
  <div class="row" style="gap:14px">
    {field("WhatsApp","+66 81 234 5678", w=190)}
    {field("LINE ID","@abcprop", w=170)}
    {field("LINE OA","@abcprop-oa", w=170)}
    {field("Preferred channel","LINE")}
    {field("Status","Active", w=150)}
  </div>
</div>"""

sec3 = f"""<div class="col" style="gap:14px">
  <div class="row" style="gap:20px;flex-wrap:wrap">
    {check("New Agency (no sales history yet)", False)}
    {check("Do They Sell Our Projects?")}
  </div>
  <div class="row" style="gap:14px">
    {req("Last Sale Date","28 Aug 2026", w=200)}
    {req("Last Units Sold","3", w=180)}
    {req("Total Units Sold","14", w=180)}
    <div class="col grow"></div>
  </div>
  <p class="cap mut" style="margin:0">ติ๊ก New Agency แล้วสามช่องนี้เลิกบังคับทันที
    ตามกฎเดิมของระบบ — ตัวหารของ progress จะลดลง 3 ข้อ</p>
</div>"""

sec4 = f"""<div class="col" style="gap:14px">
  <div class="row" style="gap:14px">
    <div class="col" style="gap:0;width:320px;flex-shrink:0">
      <p class="lbl">Office Type<span style="color:{ERROR}">&nbsp;*</span></p>
      <div class="row" style="gap:8px">
        <span class="chip" style="background:rgba(59,130,246,.16);color:{PRIMARY_L}">Physical Office</span>
        <span class="chip" style="border:1px solid {DIVIDER};color:{TXT3}">Booth</span>
        <span class="chip" style="border:1px solid {DIVIDER};color:{TXT3}">Non-Physical</span>
      </div>
    </div>
    {req("Province","Chonburi", w=200)}
    {req("Zone","Pattaya", w=200)}
    {req("Number of Sales Agents","6", w=200)}
  </div>
  <div class="row" style="gap:14px">
    {req("Address","199/12 Moo 9, Nong Prue, Bang Lamung, Chonburi 20150")}
    {req("Google Map Link","maps.app.goo.gl/x8Kq2", w=280)}
  </div>
  <div class="col" style="gap:0">
    <p class="lbl">Agency Photo — อย่างน้อย 1 รูป<span style="color:{ERROR}">&nbsp;*</span></p>
    <div class="row" style="gap:10px">
      <div style="width:78px;height:78px;border-radius:12px;background:{SURFACE};border:1px solid {DIVIDER}"></div>
      <div style="width:78px;height:78px;border-radius:12px;border:1.5px dashed {DIVIDER};
           display:grid;place-items:center">{icon(I_PLUS,18,TXT3)}</div>
    </div>
  </div>
  <p class="cap mut" style="margin:0">เลือก Non-Physical Office แล้ว Address และ Google Map Link
    เลิกบังคับ — ตัวหารลดลง 2 ข้อ</p>
</div>"""

sec6 = f"""<div class="col" style="gap:14px">
  <div class="col" style="gap:0">
    <p class="lbl">Existing Project / Relationship<span style="color:{ERROR}">&nbsp;*</span></p>
    <div class="row" style="gap:8px">
      <span class="chip" style="background:rgba(34,197,94,.15);color:{SUCCESS}">Have</span>
      <span class="chip" style="border:1px solid {DIVIDER};color:{TXT3}">No Have</span>
    </div>
  </div>
  <div class="row" style="gap:10px;background:rgba(34,197,94,.08);
       border:1px solid rgba(34,197,94,.30);border-radius:14px;padding:10px 14px">
    {icon(I_CHECK,16,SUCCESS)}
    <span class="b2" style="color:{SUCCESS};font-weight:600">
      เลือก Have แล้วต้องมีช่องทางอย่างน้อย 1 รายการ — กรอกแล้ว 4 รายการ</span>
  </div>
  <div class="row" style="gap:14px">
    {field("Facebook","fb.com/abcpropertypattaya")}
    {field("Instagram","@abcproperty.pattaya")}
  </div>
  <div class="row" style="gap:14px">
    {field("TikTok","", placeholder="—")}
    {field("LinkedIn","", placeholder="—")}
    {field("Other Social","LINE OA @abcprop")}
  </div>
</div>"""

body = f"""<div class="row" style="gap:12px">
  <h2 class="h6 grow">Phase 1 — Pre-Onboarding</h2>
  <span class="cap mut">Section 1 of 2 · Agency Profile</span>
</div>
<div class="card pad row" style="gap:12px;border-color:rgba(167,139,250,.35);background:rgba(167,139,250,.07)">
  {icon(I_WARN,18,SECOND)}
  <span class="b2 grow" style="color:{SECOND}">ส่วนนี้คือฟิลด์เดียวกับฟอร์ม Add Agency ที่ใช้อยู่จริง
    เงื่อนไขบังคับมาจาก <b>missingAgencyProfile()</b> ฝั่ง API — onboarding เรียกใช้กฎชุดเดิม
    ไม่สร้างรายการซ้ำ</span>
  <button class="btn sm out">Open in Agency form</button>
</div>
{panel("Section 1 — General", f'<span class="cap mut">4 ข้อบังคับ</span>', sec1)}
{panel("Section 3 — Sales Performance", f'<span class="cap mut">3 ข้อ · มีเงื่อนไข</span>', sec3)}
{panel("Section 4 — Office Information", f'<span class="cap mut">5 ข้อบังคับ + 2 ตามประเภทออฟฟิศ</span>', sec4)}
{panel("Section 6 — Existing Relationship", f'<span class="cap mut">1 ข้อบังคับ + 1 ตามคำตอบ</span>', sec6)}
<div class="row" style="gap:10px;justify-content:flex-end">
  <button class="btn out">Back</button>
  <button class="btn">Continue to Documents</button>
</div>"""

open("Detail.dc.html","w").write(detail_page(1, body, 1400, pct=7, status="NEW", done=3, total=41, outstanding=11))
print("Detail.dc.html")

# ── Phase 1b — Documents / Bank / Contacts / Social ──────────
DOCS = [
    ("Company Registration / DBD", "Verified",  "View",   "Agency Support"),
    ("Owner ID / Passport",        "Missing",   "Upload", "—"),
    ("Business Card",              "Optional",  "Upload", "—"),
    ("Bank Book",                  "Verified",  "View",   "Admin"),
    ("Commission Authorization",   "Under Review", "View", "Agency Support"),
]
SCOL = {"Verified":(SUCCESS,"rgba(34,197,94,.15)"), "Missing":(ERROR,"rgba(239,68,68,.15)"),
        "Optional":(TXT3,"rgba(107,114,128,.18)"), "Under Review":(WARNING,"rgba(251,191,36,.15)"),
        "Uploaded":(INFO,"rgba(56,189,248,.14)"), "Rejected":(ERROR,"rgba(239,68,68,.15)")}

rows = ""
for name, st, act, by in DOCS:
    c, bgc = SCOL[st]
    link = "out" if act == "Upload" else "out"
    rows += f"""<tr>
  <td style="font-weight:600">{name}</td>
  <td><span class="chip" style="color:{c};background:{bgc}">{st}</span></td>
  <td><button class="btn sm {link}">{act}</button></td>
  <td class="mut" style="font-size:13px">{by}</td>
</tr>"""

docs_body = f"""<table>
  <thead><tr><th>Document</th><th style="width:150px">Status</th>
    <th style="width:120px">File</th><th style="width:170px">Verified by</th></tr></thead>
  <tbody>{rows}</tbody>
</table>
<div class="row" style="gap:10px;justify-content:center;border:1.5px dashed {DIVIDER};
     border-radius:16px;padding:22px">
  {icon(I_UP,20,TXT3)}
  <span class="b2 mut">Drag &amp; drop PDF / JPG / PNG here, or <a href="#">browse files</a></span>
</div>"""

bank_body = f"""<div class="col" style="gap:14px">
  <div class="col" style="gap:0">
    <p class="lbl">Bank Account Type</p>
    <div class="row" style="gap:8px">
      <span class="chip" style="border:1px solid {DIVIDER};color:{TXT3}">Company Account</span>
      <span class="chip" style="background:rgba(167,139,250,.16);color:{SECOND}">Owner Personal Account</span>
    </div>
  </div>
  <div class="row" style="gap:14px">
    {field("Bank","Kasikorn Bank")}
    {field("Account Name","Mr. Chatchai Pongsakorn")}
    {field("Account Number","012-3-45678-9")}
  </div>
  <div class="col" style="gap:10px;background:rgba(167,139,250,.08);
       border:1px solid rgba(167,139,250,.35);border-radius:16px;padding:14px 16px">
    <div class="row" style="gap:9px">
      {icon(I_WARN,16,SECOND)}
      <span class="b2" style="font-weight:600;color:{SECOND}">
        Personal account selected — Authorization Letter is now mandatory</span>
    </div>
    <p class="cap mut" style="margin:0">Commission may only be paid into an owner's personal
      account with a signed letter authorising it.</p>
    <div class="row" style="gap:10px">
      <button class="btn sm out">Upload signed authorization letter</button>
      <span class="chip" style="color:{ERROR};background:rgba(239,68,68,.15)">Missing</span>
    </div>
  </div>
</div>"""

CONTACTS = [("Mr. Chatchai P.","Owner","+66 81 234 5678","chatchai@abcprop.co.th",True),
            ("Ms. Bua S.","Sales","+66 92 111 2233","bua@abcprop.co.th",False),
            ("Mr. Chai R.","Sales","+66 88 555 7788","chai@abcprop.co.th",False)]
crows = ""
for n, role, ph, em, primary in CONTACTS:
    mark = (f'<div style="width:19px;height:19px;border-radius:999px;background:{SUCCESS};'
            f'display:grid;place-items:center">{icon(I_CHECK,12,"#0F172A")}</div>'
            if primary else f'<div style="width:19px;height:19px;border-radius:999px;border:1.5px solid {DIVIDER}"></div>')
    crows += (f'<tr><td style="font-weight:600">{n}</td><td class="mut">{role}</td>'
              f'<td>{ph}</td><td>{em}</td><td>{mark}</td></tr>')

contacts_body = f"""<table>
  <thead><tr><th>Name</th><th style="width:110px">Role</th><th style="width:170px">Phone</th>
    <th>Email</th><th style="width:80px">Primary</th></tr></thead>
  <tbody>{crows}</tbody>
</table>
<div><button class="btn sm out">{icon(I_PLUS,14,TXT2)} &nbsp;Add Contact</button></div>"""

SOCIAL = [("Website","abcproperty-pattaya.com",True),("Facebook","fb.com/abcpropertypattaya",True),
          ("Instagram","@abcproperty.pattaya",True),("TikTok","",False),
          ("YouTube","",False),("LINE Official","@abcprop",True),
          ("Google Business Profile","",False)]
srows = ""
for name, val, has in SOCIAL:
    right = (f'<button class="btn sm out">{icon(I_EXT,13,TXT2)} &nbsp;Open Link</button>'
             if has else f'<span class="cap mut">Not provided</span>')
    shown = val if has else '<span class="mut">—</span>'
    srows += f"""<div class="row" style="gap:14px;padding:9px 0;border-bottom:1px solid {DIVIDER}">
  <span class="b2" style="width:190px;flex-shrink:0;font-weight:600">{name}</span>
  <span class="b2 grow" style="color:{TXT2}">{shown}</span>{right}</div>"""

body2 = f"""<div class="row" style="gap:12px">
  <h2 class="h6 grow">Phase 1 — Pre-Onboarding</h2>
  <span class="cap mut">Section 2 of 2 · Documents, Bank, Contacts &amp; Online</span>
</div>
{panel("Document Verification",
       f'<span class="chip" style="color:{WARNING};background:rgba(251,191,36,.15)">2 outstanding</span>',
       docs_body)}
{panel("Bank Information", "", bank_body)}
{panel("Contacts", "", contacts_body)}
{panel("Social &amp; Online Presence", "", f'<div class="col" style="gap:0">{srows}</div>')}
<div class="row" style="gap:10px;justify-content:flex-end">
  <button class="btn out">Back</button>
  <button class="btn">Continue to Phase 2</button>
</div>"""

open("Phase1Docs.dc.html","w").write(detail_page(1, body2, 2080, pct=12, status="NEW", done=5, total=41, outstanding=9))
print("Phase1Docs.dc.html")
