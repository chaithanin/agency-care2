from tokens import *

def std_page(title, subtitle, body, w, h):
    inner = f"""<div class="col" style="padding:26px 30px;gap:18px">
  <div class="col" style="gap:3px">
    <h1 class="h5">{title}</h1>
    <p class="cap mut" style="margin:0">{subtitle}</p>
  </div>
  {body}
</div>"""
    return page(inner, w, h)

# ════════════ ตารางสิทธิ์ 6 role ════════════
# ระดับสิทธิ์ — ใช้ทั้งสีและตัวอักษร ไม่พึ่งสีอย่างเดียว
LEVELS = {
    "full":   ("Full",    PRIMARY_L, "rgba(59,130,246,.16)"),
    "edit":   ("Edit",    SUCCESS,   "rgba(34,197,94,.14)"),
    "verify": ("Verify",  SECOND,    "rgba(167,139,250,.16)"),
    "view":   ("View",    TXT2,      "rgba(203,213,225,.10)"),
    "none":   ("—",       TXT3,      "transparent"),
}
ROLES = ["System Admin", "Manager", "Agency Support", "Assigned Seller", "Marketing", "Project Manager"]

# (พื้นที่ในระบบ, [สิทธิ์ของแต่ละ role ตามลำดับ ROLES], ต้องเก็บ audit ไหม)
AREAS = [
    ("Onboarding list &amp; reassign",   ["full","edit","view","view","none","none"], False),
    ("Agency Background (Phase 1)",      ["full","view","edit","edit","none","view"], False),
    ("Document Verification",            ["full","view","verify","edit","none","none"], True),
    ("Bank Information",                 ["full","view","verify","none","none","none"], True),
    ("Communication Setup (Phase 2)",    ["full","edit","view","edit","view","none"], False),
    ("Venio CRM Setup (Phase 3)",        ["full","view","edit","edit","none","none"], False),
    ("Agency Report &amp; Tasks",        ["full","view","view","edit","none","view"], False),
    ("Marketing Package (Phase 4)",      ["full","view","none","view","edit","edit"], False),
    ("Agreement (Phase 5)",              ["full","verify","edit","view","none","none"], True),
    ("Sales Materials (Phase 6)",        ["full","view","none","view","edit","edit"], False),
    ("Agency Visit",                     ["full","view","none","edit","view","view"], False),
    ("Activities &amp; Relationship",    ["full","view","view","edit","view","view"], False),
    ("Complete Onboarding",              ["full","edit","none","none","none","none"], True),
]

def cell(key):
    label, c, bgc = LEVELS[key]
    if key == "none":
        return f'<td style="text-align:center"><span class="mut" style="font-size:15px">—</span></td>'
    return (f'<td style="text-align:center"><span class="chip" '
            f'style="color:{c};background:{bgc}">{label}</span></td>')

rows = ""
for area, perms, audited in AREAS:
    mark = icon(I_WARN, 13, WARNING, extra='style="vertical-align:-2px"')
    lock = ('&nbsp;' + mark) if audited else ''
    rows += (f'<tr><td style="font-weight:600">{area}{lock}</td>'
             + "".join(cell(p) for p in perms) + "</tr>")

legend = "".join(
    f'<div class="row" style="gap:7px"><span class="chip" style="color:{c};background:{bgc}">{lab}</span>'
    f'<span class="cap mut">{desc}</span></div>'
    for (lab, c, bgc), desc in [
        (LEVELS["full"],   "ทำได้ทุกอย่าง รวมลบและย้อนสถานะ"),
        (LEVELS["edit"],   "แก้ไขและบันทึกได้"),
        (LEVELS["verify"], "ยืนยัน/อนุมัติได้ แต่แก้เนื้อหาไม่ได้"),
        (LEVELS["view"],   "ดูอย่างเดียว"),
    ])

matrix = f"""<div class="card pad col" style="gap:16px">
  <div class="row" style="gap:12px">
    <h3 class="sec grow">Onboarding Permission Matrix</h3>
    <span class="cap mut">ตรวจสิทธิ์ฝั่ง server ทุกครั้ง ไม่พึ่ง frontend</span>
  </div>
  <table>
    <thead><tr>
      <th style="width:260px">Area</th>
      {"".join(f'<th style="text-align:center;width:118px">{r}</th>' for r in ROLES)}
    </tr></thead>
    <tbody>{rows}</tbody>
  </table>
  <div class="row" style="gap:22px;flex-wrap:wrap">{legend}</div>
  <div class="row" style="gap:9px;background:rgba(251,191,36,.10);
       border:1px solid rgba(251,191,36,.35);border-radius:14px;padding:11px 14px">
    {icon(I_WARN,16,WARNING)}
    <span class="b2" style="color:{WARNING};font-weight:600">
      แถวที่มีเครื่องหมายนี้ต้องบันทึก Verified By, Verified At และ audit log ทุกครั้งที่เปลี่ยน</span>
  </div>
</div>"""

rules = f"""<div class="card pad col" style="gap:12px">
  <h3 class="sec">กติกาที่ตารางนี้บังคับ</h3>
  <div class="col" style="gap:9px">
    <div class="row" style="gap:10px"><span style="color:{PRIMARY_L};font-weight:700">1</span>
      <span class="b2" style="color:{TXT2}">Bank Information แก้ได้เฉพาะ System Admin — Agency Support
        ยืนยันได้แต่แก้เลขบัญชีไม่ได้ กันแก้ปลายทางการจ่ายเงิน</span></div>
    <div class="row" style="gap:10px"><span style="color:{PRIMARY_L};font-weight:700">2</span>
      <span class="b2" style="color:{TXT2}">คนที่อัปโหลดเอกสารกับคนที่กด Verified ต้องไม่ใช่คนเดียวกัน —
        Assigned Seller อัปได้ แต่ยืนยันเองไม่ได้</span></div>
    <div class="row" style="gap:10px"><span style="color:{PRIMARY_L};font-weight:700">3</span>
      <span class="b2" style="color:{TXT2}">Complete Onboarding กดได้เฉพาะ Manager ขึ้นไป และกดได้ต่อเมื่อ
        รายการบังคับครบแล้วเท่านั้น</span></div>
    <div class="row" style="gap:10px"><span style="color:{PRIMARY_L};font-weight:700">4</span>
      <span class="b2" style="color:{TXT2}">ตัดสินสิทธิ์จาก activeRole (role ที่ผู้ใช้สลับอยู่)
        ไม่ใช่ role ในโปรไฟล์ — ตรงกับที่โมดูลอื่นในระบบทำอยู่</span></div>
  </div>
</div>"""

open("Permissions.dc.html","w").write(
    std_page("Onboarding — Roles &amp; Permissions",
             "ใครทำอะไรได้บ้างในแต่ละส่วนของ onboarding", matrix + rules, 1240, 1120))
print("Permissions.dc.html")

# ════════════ Audit Log ════════════
ACT = {
    "verified":  (SUCCESS, "rgba(34,197,94,.14)",  "Verified"),
    "rejected":  (ERROR,   "rgba(239,68,68,.15)",  "Rejected"),
    "uploaded":  (INFO,    "rgba(56,189,248,.14)", "Uploaded"),
    "changed":   (PRIMARY_L,"rgba(59,130,246,.16)","Changed"),
    "assigned":  (SECOND,  "rgba(167,139,250,.16)","Assigned"),
    "completed": (SUCCESS, "rgba(34,197,94,.14)",  "Completed"),
}

ENTRIES = [
    ("16 Sep 2026", "10:42", "K. Somchai",   "Assigned Seller", "changed",
     "Phase 3 · Venio Agency ID", "—", "VEN-000283"),
    ("16 Sep 2026", "09:58", "K. Pim",       "Agency Support",  "verified",
     "Phase 1 · Bank Book", "Under Review", "Verified"),
    ("15 Sep 2026", "17:20", "K. Pim",       "Agency Support",  "rejected",
     "Phase 1 · Owner ID / Passport", "Uploaded", "Rejected — page cut off"),
    ("15 Sep 2026", "16:05", "K. Somchai",   "Assigned Seller", "uploaded",
     "Phase 1 · Owner ID / Passport", "Missing", "Uploaded"),
    ("15 Sep 2026", "14:32", "K. Pim",       "Agency Support",  "changed",
     "Phase 1 · Bank Account Type", "Company Account", "Owner Personal Account"),
    ("15 Sep 2026", "11:10", "K. Warun",     "Manager",         "assigned",
     "Assigned Seller", "—", "K. Somchai Rattana"),
    ("15 Sep 2026", "10:04", "K. Warun",     "Manager",         "changed",
     "Onboarding status", "New", "In Progress"),
]

arows = ""
for d, t, who, role, kind, field, before, after in ENTRIES:
    c, bgc, label = ACT[kind]
    arows += f"""<tr>
  <td style="white-space:nowrap"><div class="col" style="gap:1px">
    <span style="font-weight:600">{d}</span>
    <span class="cap mut">{t}</span></div></td>
  <td><div class="col" style="gap:1px">
    <span style="font-weight:600">{who}</span>
    <span class="cap mut">{role}</span></div></td>
  <td><span class="chip" style="color:{c};background:{bgc}">{label}</span></td>
  <td style="color:{TXT2}">{field}</td>
  <td class="mut" style="font-size:13px">{before}</td>
  <td style="font-weight:600">{after}</td>
</tr>"""

filters = f"""<div class="card" style="padding:14px 18px">
  <div class="row" style="gap:10px;flex-wrap:wrap">
    <div class="row fld grow" style="gap:9px;padding:8px 14px;border-radius:999px;min-width:260px">
      {icon(I_SEARCH,16,TXT3)}<span class="b2 mut">Search field / value / person...</span>
    </div>
    <div class="row fld" style="gap:8px;padding:8px 12px;border-radius:999px">
      <span class="b2">All Agencies</span>{icon(I_CHEV,14,TXT3)}</div>
    <div class="row fld" style="gap:8px;padding:8px 12px;border-radius:999px">
      <span class="b2">Action</span>{icon(I_CHEV,14,TXT3)}</div>
    <div class="row fld" style="gap:8px;padding:8px 12px;border-radius:999px">
      <span class="b2">Role</span>{icon(I_CHEV,14,TXT3)}</div>
    <div class="row fld" style="gap:8px;padding:8px 12px;border-radius:999px">
      <span class="b2">Date range</span>{icon(I_CHEV,14,TXT3)}</div>
    <button class="btn out">Export CSV</button>
  </div>
</div>"""

table = f"""<div class="card pad col" style="gap:14px">
  <div class="row" style="gap:12px">
    <h3 class="sec grow">Activity — ABC Property Pattaya</h3>
    <span class="cap mut">7 entries · เก็บถาวร แก้ไขและลบไม่ได้</span>
  </div>
  <table>
    <thead><tr>
      <th style="width:130px">When</th><th style="width:170px">Who</th>
      <th style="width:120px">Action</th><th style="width:250px">Field</th>
      <th style="width:190px">Before</th><th>After</th>
    </tr></thead>
    <tbody>{arows}</tbody>
  </table>
</div>"""

verified_card = f"""<div class="card pad col" style="gap:14px">
  <div class="row" style="gap:12px">
    <h3 class="sec grow">Verification record</h3>
    <span class="cap mut">แสดงคู่กับทุกเอกสารและทุกสถานะที่ต้องยืนยัน</span>
  </div>
  <div style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px">
    <div class="col" style="gap:9px;background:{SURFACE};border:1px solid {DIVIDER};
         border-radius:16px;padding:14px 16px">
      <span class="cap mut" style="font-weight:600">Bank Book</span>
      <span class="chip" style="color:{SUCCESS};background:rgba(34,197,94,.14);align-self:flex-start">Verified</span>
      <span class="cap" style="color:{TXT2}">Verified by K. Pim · Agency Support</span>
      <span class="cap mut">16 Sep 2026, 09:58</span>
    </div>
    <div class="col" style="gap:9px;background:{SURFACE};border:1px solid {DIVIDER};
         border-radius:16px;padding:14px 16px">
      <span class="cap mut" style="font-weight:600">Owner ID / Passport</span>
      <span class="chip" style="color:{ERROR};background:rgba(239,68,68,.15);align-self:flex-start">Rejected</span>
      <span class="cap" style="color:{TXT2}">Rejected by K. Pim · Agency Support</span>
      <span class="cap mut">15 Sep 2026, 17:20 — page cut off</span>
    </div>
    <div class="col" style="gap:9px;background:{SURFACE};border:1px solid {DIVIDER};
         border-radius:16px;padding:14px 16px">
      <span class="cap mut" style="font-weight:600">Signed Agency Agreement</span>
      <span class="chip" style="color:{WARNING};background:rgba(251,191,36,.15);align-self:flex-start">Waiting Signature</span>
      <span class="cap" style="color:{TXT2}">Prepared by K. Pim · Agency Support</span>
      <span class="cap mut">14 Sep 2026, 15:02</span>
    </div>
  </div>
  <div class="row" style="gap:9px;background:rgba(59,130,246,.10);
       border:1px solid rgba(59,130,246,.30);border-radius:14px;padding:11px 14px">
    {icon(I_WARN,16,PRIMARY_L)}
    <span class="b2" style="color:{PRIMARY_L};font-weight:600">
      ทุกการเปลี่ยนสถานะเขียนลง audit log ทันที ไม่มี endpoint สำหรับลบหรือแก้รายการเก่า</span>
  </div>
</div>"""

open("AuditLog.dc.html","w").write(
    std_page("Onboarding — Audit Log",
             "ใครทำอะไร เมื่อไหร่ ค่าเดิมเป็นอะไร เปลี่ยนเป็นอะไร",
             filters + verified_card + table, 1480, 1160))
print("AuditLog.dc.html")
