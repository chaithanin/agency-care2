# -*- coding: utf-8 -*-
"""Dashboard.dc.html -- operational dashboard, permission matrix, standard page structure"""
from tokens import *
from shell import *

W, H = 1620, 1620

def stat_card(title, rows, color, note=None):
    body = "".join(
      f'''<div class="row" style="gap:12px;padding:7px 0;border-bottom:1px solid {DIVIDER}">
        <span class="b2 grow" style="color:{TXT2}">{k}</span>
        <span style="font-size:17px;font-weight:700;color:{c or TXT}">{v}</span></div>'''
      for k, v, c in rows)
    n = f'<span class="cap mut">{note}</span>' if note else ""
    return f'''<div class="card pad col grow" style="gap:11px;min-width:0">
      <h3 class="sec" style="color:{color}">{title}</h3>{body}{n}</div>'''

funnel = stat_card("SALES FUNNEL", [
    ("New", "124", TXT), ("Contacted", "83", TXT), ("Visit", "41", TXT),
    ("Holding / Reservation", "22", WARNING), ("Sold Deal", "11", SUCCESS)],
    PRIMARY_L, "Clicking a number must open the filtered list — not a chart you cannot click")

pay = stat_card("PAYMENT ATTENTION", [
    ("Overdue deals", "7", ERROR), ("Amount overdue", "1.8M THB", ERROR),
    ("Due this week", "12", WARNING), ("Awaiting payment entry", "3", WARNING)],
    ERROR, "Read from the payment schedule, never a figure someone types in")

ag = stat_card("AGENCY FOLLOW-UP", [
    ("No visit in over 30 days", "28", WARNING), ("Follow-up due today", "6", PRIMARY_L),
    ("New agency leads", "14", SUCCESS)],
    SECOND, "Uses the computed Last Visit")

conv = stat_card("CONVERSION", [
    ("Visit → Holding", "34%", PRIMARY_L), ("Holding → Reservation", "57%", SUCCESS),
    ("Reservation → Sold", "62%", SUCCESS), ("Holding → Lost", "29%", ERROR)],
    SUCCESS, "Still splits by sub status even though the board merged the columns")

sub = f'''<div class="card pad col" style="gap:11px;width:330px;flex-shrink:0">
  <h3 class="sec" style="color:{WARNING}">HOLDING / RESERVATION SPLIT</h3>
  <div class="row" style="gap:14px;align-items:flex-end">
    <div class="col grow" style="gap:6px">
      <div class="row" style="gap:9px">{flow_chip("Holding")}
        <span class="grow"></span><span style="font-size:19px;font-weight:700">14</span></div>
      {bar(64, WARNING)}
    </div>
  </div>
  <div class="row" style="gap:14px;align-items:flex-end">
    <div class="col grow" style="gap:6px">
      <div class="row" style="gap:9px">{flow_chip("Reservation")}
        <span class="grow"></span><span style="font-size:19px;font-weight:700">8</span></div>
      {bar(36, SUCCESS)}
    </div>
  </div>
  {note_box("ok", "The board shows one column while the reports still split cleanly — "
                  "because sub_status is on every row in the database.")}
</div>'''

dash = panel("DASHBOARD — it must answer operational questions, not just look good",
  body=(f'<div class="row" style="gap:16px;align-items:stretch">{funnel}{pay}{ag}</div>'
        f'<div class="row" style="gap:16px;align-items:stretch">{conv}{sub}</div>'),
  note="Every number here must lead to the real records. If it cannot be clicked, it does not belong on this page.",
  grow=False)

ROLES = ["Sales", "Manager", "Support", "Finance", "Agency Support", "Management", "Admin"]
def cell(v):
    col = {"Edit": SUCCESS, "Approve": SUCCESS, "Request": WARNING, "Review": WARNING,
           "View": TXT2, "No": ERROR, "Override": SECOND}.get(v, TXT2)
    return f'<span style="color:{col};font-weight:600">{v}</span>'
PERM = [
  ("Lead", ["Edit", "Edit", "View", "View", "View", "View", "Override"]),
  ("Change sub status", ["Edit", "Edit", "View", "View", "View", "View", "Override"]),
  ("Create sold deal", ["Request", "Approve", "View", "View", "No", "View", "Override"]),
  ("Edit sale price", ["No", "Edit", "No", "No", "No", "View", "Override"]),
  ("Record payment", ["View", "View", "Edit", "Edit", "No", "View", "Override"]),
  ("Commission", ["View", "Review", "View", "Approve", "No", "View", "Override"]),
  ("Visit", ["Edit", "Edit", "Edit", "View", "Edit", "View", "Override"]),
  ("Agency", ["View", "Edit", "View", "View", "Edit", "View", "Override"]),
  ("Delete deal / financial record", ["No", "No", "No", "No", "No", "No", "No"]),
]
prows = [(f'<b>{n}</b>', *[cell(v) for v in vs]) for n, vs in PERM]
perm = panel("PERMISSION MATRIX",
  body=(table(["Action"] + ROLES, prows, [190] + [110] * 7) +
        note_box("error", "The last row is No for everyone. Financial records use Void, Cancelled or "
                          "Reversed instead of deletion, always.") +
        note_box("warn", "The real roles in the system are manager · super_admin · admin · closer · sales · "
                         "hr · marketing · staff · read_only · agency_user. The seven above must be mapped "
                         "onto that set — <b>no new values in the enum</b> — and permissions are checked "
                         "with <code>user.role</code>, not <code>activeRole</code>.")),
  grow=False)

box = lambda t, h, c=None, d=None: (
  f'<div style="background:{SURFACE};border:1px {"dashed" if d else "solid"} {c or DIVIDER};'
  f'border-radius:11px;padding:9px 12px;height:{h}px;display:flex;align-items:center;'
  f'justify-content:center"><span class="cap" style="color:{c or TXT3}">{t}</span></div>')

layout = f'''<div class="card pad col" style="gap:12px;width:500px;flex-shrink:0">
  <h3 class="sec">THE DETAIL PAGE STRUCTURE EVERY ENTITY SHARES</h3>
  <div class="col" style="gap:8px">
    {box("Breadcrumb", 34)}
    {box("Page Title &nbsp;·&nbsp; Primary Action", 40, PRIMARY_L)}
    {box("Summary / KPI", 44, SUCCESS)}
    {box("Primary Navigation (at most 5 tabs)", 36, WARNING)}
    <div class="row" style="gap:8px">
      <div class="grow">{box("Main Content", 130)}</div>
      <div style="width:150px;flex-shrink:0">{box("Context Panel", 130, SECOND)}</div>
    </div>
    {box("Activity Timeline", 40, SECOND, d=True)}
  </div>
  <div class="row" style="gap:9px;flex-wrap:wrap">
    {"".join(f'<span class="chip" style="color:{TXT2};background:{SURFACE}">{t}</span>'
             for t in ["Desktop-first 1440px", "Sidebar 240", "Right panel 320–360",
                       "Spacing 4/8/12/16/24/32"])}
  </div>
</div>'''

comp = f'''<div class="card pad col grow" style="gap:12px;min-width:0">
  <h3 class="sec">COMPONENTS REUSED ACROSS THE SYSTEM — built once</h3>
  {table(["Component", "Used on", "Already exists?"], [
    ("Activity Timeline", "Lead · Sold Deal · Agency · Visit · Customer",
     f'<span style="color:{SUCCESS}">Yes — deal_timeline</span>'),
    ("Status Badge", "Everywhere", f'<span style="color:{SUCCESS}">Yes — deal_stages carries colours</span>'),
    ("Task Pill", "Lead · Deal · Payment · Agency", f'<span style="color:{SUCCESS}">Yes — tasks</span>'),
    ("Photo Pill + Lightbox", "Visit", f'<span style="color:{WARNING}">Photos yes, lightbox no</span>'),
    ("Financial Summary", "Sold Deal · Payment · Commission",
     f'<span style="color:{ERROR}">No — new</span>'),
    ("Filter Bar", "Every list page", f'<span style="color:{SUCCESS}">Yes</span>'),
  ], [200, 300, None])}
  {note_box("info", "Colour alone never carries meaning. Every status needs a label beside it, so it "
                    "reads the same for someone who is colour blind.")}
  <div style="height:1px;background:{DIVIDER}"></div>
  <h3 class="sec">FILTERS EVERY LIST PAGE ACTUALLY NEEDS</h3>
  {table(["Page", "Filters"], [
    ("Leads", "Stage · Sub Status · Project · Sales Owner · Agency · Lead Source · Created · Next Follow-up"),
    ("Sold Deals", "Project · Unit · Customer · Seller · Closer · Agency · Deal Status · Payment Status · Contract · Transfer"),
    ("Agencies", "Sales Owner · Last Visit · Sold Deals · Active / Inactive"),
    ("Visits", "Visit Type · Sales Person · Agency · Project · Date range"),
  ], [130, None])}
</div>'''

body = f'''<div class="col" style="gap:16px">
  {dash}
  {perm}
  <div class="row" style="gap:16px;align-items:stretch">{layout}{comp}</div>
</div>'''

open("Dashboard.dc.html", "w", encoding="utf-8").write(sheet(
    "9 · Dashboard · Permissions · Design System",
    "Numbers you can click · a matrix mapped onto the real roles · the shared page structure and components",
    body, W, H, badge="All phases"))
print("Dashboard.dc.html")
