from shell import *

# ══════════ 1. OVERVIEW ══════════
counters = f"""<div class="col" style="gap:10px">
  <div class="row" style="gap:12px;flex-wrap:wrap">
    {stat("1,284","ALL CONTACTS",TXT)}
    {stat("42","SALES",INFO)}
    {stat("873","CUSTOMERS",SUCCESS)}
    {stat("291","AGENCIES",SECOND)}
    {stat("78","UNCLASSIFIED",WARNING,warn=True)}
  </div>
  <p class="cap mut" style="margin:0">นับเฉพาะผู้ติดตามที่ยัง active —
    คนหนึ่งอาจอยู่ได้มากกว่าหนึ่งกลุ่ม ผลรวมรายกลุ่มจึงมากกว่า All Contacts ได้</p>
</div>"""

alert = f"""<div class="card pad row" style="gap:12px;border-color:rgba(251,191,36,.35);
     background:rgba(251,191,36,.07)">
  {icon(I_WARN,18,WARNING)}
  <span class="b2 grow" style="color:{WARNING};font-weight:600">
    78 new followers need classification — ยังไม่รู้ว่าเป็นลูกค้า เอเจนซี่ หรือทีมขาย</span>
  <button class="btn sm out">Review now</button>
</div>"""

quota = f"""<div class="card pad col" style="gap:12px;width:330px;flex-shrink:0">
  <h3 class="sec">LINE Message Quota</h3>
  <div class="row" style="gap:10px;align-items:baseline">
    <span style="font-size:26px;font-weight:700;color:{TXT}">7,312</span>
    <span class="cap mut">เหลือจาก 10,000 ข้อความเดือนนี้</span>
  </div>
  {bar(73, PRIMARY)}
  <p class="cap mut" style="margin:0">ระบบเช็กโควตาก่อนส่งกลุ่มใหญ่ ถ้าไม่พอจะเตือนก่อน
    ไม่ปล่อยให้ส่งแล้วพังกลางทาง</p>
</div>"""

def hist_row(title, badge, badge_c, badge_bg, recips, delivered, failed, read, by, when):
    return f"""<div class="row" style="gap:14px;padding:13px 0;border-bottom:1px solid {DIVIDER}">
  <div class="col grow" style="gap:4px">
    <div class="row" style="gap:10px">
      <span class="b2" style="font-weight:700">{title}</span>
      <span class="chip" style="color:{badge_c};background:{badge_bg}">{badge}</span>
    </div>
    <span class="cap mut">Recipients {recips} · Delivered {delivered} · Failed {failed} · Read {read}</span>
  </div>
  <div class="col" style="gap:2px;align-items:flex-end">
    <span class="cap" style="color:{TXT2}">{by}</span>
    <span class="cap mut">{when}</span>
  </div>
</div>"""

recent = f"""<div class="card pad col grow" style="gap:10px">
  <div class="row"><h3 class="sec grow">Recent Broadcasts</h3>
    <button class="btn sm out">View all</button></div>
  {hist_row("MARINA SEPTEMBER UPDATE","Agencies",SECOND,"rgba(167,139,250,.16)",
            "284","278","6","64%","SystemAdmin","16/09/2026 14:30")}
  {hist_row("LOVE IT Wongamat — new price list","Customers",SUCCESS,"rgba(34,197,94,.14)",
            "721","715","6","51%","K. May","15/09/2026 09:12")}
  {hist_row("Weekly sales meeting moved to 10:00","Sales",INFO,"rgba(56,189,248,.14)",
            "42","42","0","93%","K. Warun","15/09/2026 08:00")}
</div>"""

body = f"""{counters}
{alert}
<div class="row" style="gap:18px;align-items:stretch">{recent}{quota}</div>"""

actions = '<button class="btn out">Export contacts</button><button class="btn">+ New Announcement</button>'
open("Main.dc.html","w").write(page_shell("OVERVIEW", body, 1440, 900, actions=actions))
print("Main.dc.html")

# ══════════ 2. CONTACTS ══════════
def contact_row(name, line_id, roles, company, status, followed, last, warn=False):
    chips = "".join(role_chip(r) for r in roles) if roles else UNCLASSIFIED_CHIP
    review = (f'&nbsp;<span class="chip" style="color:{WARNING};background:rgba(251,191,36,.15)">⚠ Review</span>'
              if warn else "")
    return f"""<tr>
  <td style="width:44px"><div style="width:18px;height:18px;border-radius:5px;
      border:1.5px solid {DIVIDER}"></div></td>
  <td><div class="row" style="gap:10px">
    <div style="width:34px;height:34px;border-radius:999px;background:{SURFACE};
         border:1px solid {DIVIDER};flex-shrink:0"></div>
    <div class="col" style="gap:1px">
      <span style="font-weight:600">{name}</span>
      <span class="cap mut">{line_id}</span>
    </div></div></td>
  <td><div class="row" style="gap:6px;flex-wrap:wrap">{chips}{review}</div></td>
  <td style="color:{TXT2}">{company}</td>
  <td>{status_dot(status)}</td>
  <td class="mut" style="font-size:13px">{followed}</td>
  <td class="mut" style="font-size:13px">{last}</td>
</tr>"""

rows = (
  contact_row("Anna K.","@annak_prop",["Agency"],"ABC Property","Active","15 Sep 2026","Yesterday")
+ contact_row("Somchai P.","@somchai.p",["Customer"],"— · LOVE IT Wongamat","Active","16 Sep 2026","Today")
+ contact_row("John M.","@johnm",["Sales"],"Global Top Group","Active","10 Sep 2026","Today")
+ contact_row("Chatchai P.","@chatchai",["Agency","Customer"],"ABC Property","Active","12 Sep 2026","2 days ago")
+ contact_row("Peter T.","@peter_t",[],"—","New","16 Sep 2026","—",warn=True)
+ contact_row("Nadia R.","@nadia",[],"—","New","16 Sep 2026","—",warn=True)
+ contact_row("Wichai S.","@wichai",["Customer"],"—","Blocked","02 Aug 2026","18 Aug 2026")
)

filters = f"""<div class="card" style="padding:14px 18px">
  <div class="row" style="gap:10px;flex-wrap:wrap">
    <div class="row fld grow" style="gap:9px;padding:8px 14px;border-radius:999px;min-width:300px">
      {icon(I_SEARCH,16,TXT3)}<span class="b2 mut">Search LINE name, phone, agency...</span>
    </div>
    {pill("All Types")}{pill("Status")}{pill("Project")}{pill("Agency")}{pill("Assigned Seller")}
  </div>
</div>"""

bulk = f"""<div class="card pad row" style="gap:12px;border-color:rgba(59,130,246,.35);
     background:rgba(59,130,246,.08)">
  <span class="b2" style="color:{PRIMARY_L};font-weight:700">3 selected</span>
  <span class="grow"></span>
  <button class="btn sm out">Change Type</button>
  <button class="btn sm out">Add Tag</button>
  <button class="btn sm">Send Message</button>
</div>"""

table = f"""<div class="card pad col" style="gap:12px">
  <div class="row"><h3 class="sec grow">LINE Contacts</h3>
    <span class="cap mut">1,284 คน · แสดง 7 แถวแรก</span></div>
  <table>
    <thead><tr>
      <th style="width:44px"></th><th style="width:230px">Profile</th>
      <th style="width:210px">Type</th><th style="width:210px">Company / Project</th>
      <th style="width:120px">Status</th><th style="width:140px">Followed Since</th>
      <th>Last Activity</th>
    </tr></thead>
    <tbody>{rows}</tbody>
  </table>
  <p class="cap mut" style="margin:0">คนหนึ่งมีได้หลายบทบาท — Chatchai P. เป็นทั้งเจ้าของเอเจนซี่
    และซื้อห้องเอง จึงขึ้นทั้ง Agency และ Customer</p>
</div>"""

body2 = f"{filters}{bulk}{table}"
open("Contacts.dc.html","w").write(page_shell("CONTACTS", body2, 1440, 900))
print("Contacts.dc.html")
