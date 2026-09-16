from shell import *

# ── Phase 1a — Agency Background ─────────────────────────────
bg_body = f"""<div class="col" style="gap:14px">
  <div class="row" style="gap:14px">
    {field("Agency Full Name — English","ABC Property Pattaya Co., Ltd.")}
    {field("Agency Full Name — Thai","บริษัท เอบีซี พร็อพเพอร์ตี้ พัทยา จำกัด")}
  </div>
  <div class="row" style="gap:14px">
    {field("Full Address","199/12 Moo 9, Nong Prue, Bang Lamung, Chonburi 20150")}
    {field("Owner Full Name","Mr. Chatchai Pongsakorn")}
  </div>
  <div class="col" style="gap:0">
    <p class="lbl">Company History / Background</p>
    <div class="fld" style="min-height:74px;color:{TXT2}">Founded 2018 in Pattaya. Focused on
      foreign buyers from Europe and CIS. 6 full-time agents, office on Second Road.</div>
  </div>
  <div class="row" style="gap:14px">
    {field("Units Sold / Rented for GTG","14")}
    {field("Number of Agents","6")}
    <div class="col" style="gap:0;flex-grow:1">
      <p class="lbl">Agency Size</p>
      <div class="row" style="gap:8px">
        <span class="chip" style="border:1px solid {DIVIDER};color:{TXT3}">Small</span>
        <span class="chip" style="background:rgba(59,130,246,.16);color:{PRIMARY_L}">Medium</span>
        <span class="chip" style="border:1px solid {DIVIDER};color:{TXT3}">Large</span>
      </div>
    </div>
  </div>
</div>"""

focus_body = f"""<div class="col" style="gap:16px">
  {multiselect("Market Focus", ["Buyer","Investor","Foreign Market"], ["Rental","Thai Market"])}
  {multiselect("Nationality / Market", ["Russian","German","British"], ["Chinese","Indian","Thai","Other"])}
  {multiselect("Business Channel", ["Online","Offline","Exhibition"], ["Booth","Freelancer","Others"])}
  <div style="height:1px;background:{DIVIDER}"></div>
  <div class="row" style="gap:16px">
    <span class="b2 grow">Has the agency seen or known our projects before?</span>
    <div class="row" style="gap:8px">
      <span class="chip" style="background:rgba(34,197,94,.15);color:{SUCCESS}">Yes</span>
      <span class="chip" style="border:1px solid {DIVIDER};color:{TXT3}">No</span>
    </div>
  </div>
</div>"""

body = f"""<div class="row" style="gap:12px">
  <h2 class="h6 grow">Phase 1 — Pre-Onboarding</h2>
  <span class="cap mut">Section 1 of 2 · Background &amp; Profile</span>
</div>
{panel("Agency Background", f'<span class="cap mut">Required</span>', bg_body)}
{panel("Market Focus &amp; Channels", "", focus_body)}
<div class="row" style="gap:10px;justify-content:flex-end">
  <button class="btn out">Back</button>
  <button class="btn">Continue to Documents</button>
</div>"""

open("Detail.dc.html","w").write(detail_page(1, body, 1400, pct=8, status="NEW", done=3, total=39, outstanding=9))
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

open("Phase1Docs.dc.html","w").write(detail_page(1, body2, 2080, pct=13, status="NEW", done=5, total=39, outstanding=7))
print("Phase1Docs.dc.html")
