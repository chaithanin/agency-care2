# -*- coding: utf-8 -*-
"""Agency.dc.html + Visit.dc.html"""
from tokens import *
from shell import *

# ===================== Agency =====================
W, H = 1540, 1300

head = f'''<div class="row" style="gap:16px;align-items:flex-start">
  <div class="col grow" style="gap:5px">
    <span class="cap mut">Agency &nbsp;›&nbsp; Agencies &nbsp;›&nbsp; ABC Property</span>
    <div class="row" style="gap:11px"><h2 class="h5">ABC PROPERTY</h2>{flow_chip("Active")}</div>
    <span class="cap mut">Pattaya · Relationship Owner: Sarah Lee</span>
  </div>
  <button class="btn sm">+ Add Visit</button>
</div>
{kpi_strip([("20", "Agents", TXT), ("43", "Leads", PRIMARY_L), ("18", "Reservations", WARNING),
            ("12", "Sold Deals", SUCCESS), ("9", "Visits", SECOND)])}'''

lastvisit = f'''<div class="col" style="gap:9px;background:{SURFACE};border:1px solid {SUCCESS}44;
     border-radius:14px;padding:13px 15px">
  <div class="row" style="gap:9px">
    <span class="sec grow" style="color:{SUCCESS}">LAST VISIT</span>
    {icon(I_LOCK,14,SUCCESS)}
    <span class="cap" style="color:{SUCCESS}">computed · not editable</span>
  </div>
  {kv([("Date", "17 Sep 2026"), ("Visited by", "John Smith"),
       ("Discussed", "Marina Golden Bay promotion"),
       ("Agency feedback", "Clients interested in sea view units"),
       ("Next action", "Send the latest price list"), ("Follow-up", "24 Sep 2026")])}
  <span class="cap mut">Last Visit = MAX(office_visits.visit_at, visit_checkins.checkin_at) —
  there must be no field to type it into.</span>
</div>'''

a_left = f'''<div class="col grow" style="gap:18px;min-width:0">
  {tabs(["Overview", "Agents", "Visits", "Leads", "Sold Deals", "Activity"], "Overview")}
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:18px 24px">
    {sect("AGENCY INFORMATION", kv([("Company", "ABC Property"), ("Primary Contact", "John Tan"),
        ("Phone", "+66 38 123 456"), ("Email", "contact@abcproperty.co.th"),
        ("Address", "Pattaya Klang Rd."), ("Relationship Owner", "Sarah Lee")]))}
    {sect("SALES PERFORMANCE", kv([("Leads", "43"), ("Reservations", "18"),
        ("Sold Deals", "12"), ("Conversion", "28%")]))}
  </div>
  {lastvisit}
  {note_box("error", "No separate tabs for Site Visit Report, Visit Summary or Follow-up. "
                     "All of it reads from the same visit records.")}
</div>'''

a_right = f'''<div class="col" style="gap:14px;width:320px;flex-shrink:0">
  <div class="card pad col" style="gap:12px">
    <h4 class="sec">ACTIVITY</h4>
    {timeline([
      ("17 Sep", "Agency visit", "by John Smith · 3 photos", SECOND),
      ("12 Sep", "Sold deal created", "SD-2026-000118 · 2.9M", SUCCESS),
      ("05 Sep", "Leads assigned", "5 new leads", PRIMARY),
      ("28 Aug", "Agency visit", "by Sarah Lee", SECOND),
    ])}
  </div>
  {note_box("info", "The existing <code>agencies</code> and <code>agency_staff</code> tables are complete. "
                    "This phase reorganises the page; it does not change the data model.")}
</div>'''

agency_body = f'''<div class="col" style="gap:16px">
  {panel("AGENCY DETAIL",
         body=f'{head}<div class="row" style="gap:22px;align-items:flex-start;margin-top:4px">{a_left}{a_right}</div>',
         grow=False)}
</div>'''

open("Agency.dc.html", "w", encoding="utf-8").write(sheet(
    "7 · Agency", "A new agency page · computed Last Visit · no change to the existing data model",
    agency_body, W, H, badge="Phase 4"))
print("Agency.dc.html")

# ===================== Visit =====================
W2, H2 = 1620, 1700

VROWS = [
  ("17 Sep 2026", "Agency Visit", "John Smith", "ABC Property", "Marina Golden Bay",
   f'<span class="chip" style="color:{SECOND};background:rgba(167,139,250,.16)">3 photos</span>'),
  ("16 Sep 2026", "Site Visit", "Sarah Lee", "—", "HARMONIA",
   f'<span class="chip" style="color:{SECOND};background:rgba(167,139,250,.16)">5 photos</span>'),
  ("15 Sep 2026", "Customer Visit", "May P.", "XYZ Realty", "Marina Golden Bay",
   f'<span class="chip" style="color:{TXT3};background:{SURFACE}">no photos</span>'),
]
vrows = [(a, f'<span class="chip" style="color:{PRIMARY_L};background:rgba(59,130,246,.16)">{b}</span>',
          c, d, e, f) for a, b, c, d, e, f in VROWS]

vlist = panel("VISITS — one record set for the whole system",
  right='<button class="btn sm">+ Add Visit</button>',
  body=(f'<div class="row" style="gap:9px;flex-wrap:wrap">'
        f'<div class="row fld" style="gap:8px;width:230px">{icon(I_SEARCH,15)}'
        f'<span class="mut">Search agency / customer / project</span></div>'
        + "".join(f'<div class="row fld" style="gap:9px">{f}{icon(I_CHEV,14)}</div>'
                  for f in ["Visit Type", "Sales Person", "Agency", "Project", "Date range"])
        + '</div>'
        + table(["Date", "Type", "Visited by", "Agency", "Project", "Photos"],
                vrows, [140, 160, 150, 170, 200, 130])
        + note_box("ok", "Site Visit Report and Visit Summary Report become <b>preset filtered views</b> "
                         "of this table. Both old routes keep working — they are not deleted.")),
  note="This reads office_visits as its primary source and folds in planned visits from visit_plans. "
       "visit_plans keeps behaving exactly as before — nothing merged, nothing moved.",
  grow=False)

add = modal("Add Visit", f'''
  <div class="col" style="gap:0">
    <p class="lbl">Visit Type<span style="color:{ERROR}">&nbsp;*</span></p>
    <div class="col" style="gap:0;background:{SURFACE};border:1px solid {DIVIDER};border-radius:12px;padding:8px 12px">
      {radio("Agency Visit", True)}{radio("Site Visit")}{radio("Customer Visit")}{radio("Other")}
    </div>
  </div>
  {field("Date & Time", "18 Sep 2026 14:00", required=True)}
  {field("Sales Person", "John Smith", required=True)}
  <div class="col" style="gap:9px;background:rgba(59,130,246,.08);border:1px solid {PRIMARY}44;
       border-radius:13px;padding:12px 14px">
    <span class="cap" style="color:{PRIMARY_L};font-weight:700">
      Agency Visit reveals only these two</span>
    {field("Agency", "ABC Property", required=True)}
    {field("Agent", "John Tan")}
  </div>
  {field("Discussion Topic", "Marina Golden Bay promotion", required=True)}
  {field("Discussion Details", "")}
  {field("Agency / Customer Feedback", "")}
  {field("Next Action", "")}
  {field("Follow-up Date", "24 Sep 2026")}
  <div class="row" style="gap:10px">
    <div class="row grow" style="gap:9px;background:{SURFACE};border:1px dashed {DIVIDER};
         border-radius:13px;padding:11px 13px">{icon(I_CAM,16,PRIMARY_L)}
      <span class="b2 grow" style="color:{TXT2}">+ Add Photos</span></div>
    <div class="row grow" style="gap:9px;background:{SURFACE};border:1px dashed {DIVIDER};
         border-radius:13px;padding:11px 13px">{icon(I_UP,16,PRIMARY_L)}
      <span class="b2 grow" style="color:{TXT2}">+ Add File</span></div>
  </div>''',
  '<button class="btn out sm">Cancel</button><button class="btn sm">Save Visit</button>', w=450)

cond = f'''<div class="card pad col grow" style="gap:12px;min-width:0">
  <h3 class="sec">FIELDS FOLLOW THE TYPE — not every field, all the time</h3>
  {table(["Type", "Required", "Hidden"], [
    ("Agency Visit", "Agency", "Customer · Unit"),
    ("Site Visit", "Customer · Project", "Agent"),
    ("Customer Visit", "Customer", "Unit"),
    ("Other", "Discussion topic", "Agency · Customer · Project"),
  ], [170, 260, None])}
  {note_box("info", "Progressive disclosure keeps the cognitive load down — but a hidden field must "
                    "also be cleared, not merely hidden.")}
  <div style="height:1px;background:{DIVIDER}"></div>
  <h3 class="sec">EXTENDING office_visits — new columns only</h3>
  {table(["New column", "Why"], [
    ("<code>visit_type</code>", "Separates Agency / Site / Customer / Other (today there is only purpose)"),
    ("<code>project_id</code>", "Today only interested_projects exists, which means something else"),
    ("<code>unit_no</code>", "A site visit needs the unit that was shown"),
    ("<code>agency_staff_id</code>", "Identifies the agent who was met"),
    ("<code>feedback</code>", "There is a result field, but it does not separate the other side's view"),
    ("<code>booking_id</code>", "Links the visit to a deal"),
  ], [220, None])}
  {note_box("ok", "photos, discussionTopics, nextAction, nextVisitDate and soft delete already exist. "
                  "Nothing to add there.")}
</div>'''

lb = f'''<div class="card col" style="width:430px;flex-shrink:0;gap:0;overflow:hidden;
     box-shadow:0 24px 64px rgba(0,0,0,.45)">
  <div class="row pad" style="gap:12px;border-bottom:1px solid {DIVIDER};padding-bottom:13px">
    <h3 class="h6 grow">Site Visit Photos</h3>
    <span class="cap mut">2 / 5</span>{icon(I_X,17,TXT3)}
  </div>
  <div class="row" style="gap:12px;align-items:center;padding:16px 18px">
    <div style="width:34px;height:34px;border-radius:999px;border:1px solid {DIVIDER};
         display:grid;place-items:center;flex-shrink:0;transform:rotate(180deg)">{icon(I_ARROW,15,TXT2)}</div>
    <div class="grow" style="height:210px;border-radius:14px;background:{SURFACE};
         border:1px solid {DIVIDER};display:grid;place-items:center">{icon(I_CAM,34,TXT3)}</div>
    <div style="width:34px;height:34px;border-radius:999px;border:1px solid {DIVIDER};
         display:grid;place-items:center;flex-shrink:0">{icon(I_ARROW,15,TXT2)}</div>
  </div>
  <div class="row" style="gap:8px;padding:0 18px 12px">
    {"".join(f'<div style="width:52px;height:38px;border-radius:9px;background:{SURFACE};'
             f'border:{"2px solid "+PRIMARY if i==1 else "1px solid "+DIVIDER}"></div>' for i in range(5))}
  </div>
  <div class="col pad" style="gap:10px;border-top:1px solid {DIVIDER};padding-top:13px">
    <div class="col" style="gap:2px">
      <span class="b2">Marina Golden Bay showroom</span>
      <span class="cap mut">18 Sep 2026 · 14:33 · by John Smith</span>
    </div>
    <div class="row" style="gap:9px;flex-wrap:wrap">
      {"".join(f'<span class="chip" style="color:{TXT2};background:{SURFACE}">{t}</span>'
               for t in ["← → to move", "ESC to close", "Zoom", "Swipe on mobile"])}
    </div>
    <button class="btn out sm" style="align-self:flex-start">Download</button>
  </div>
</div>'''

visit_body = f'''<div class="col" style="gap:16px">
  {vlist}
  <div class="row" style="gap:16px;align-items:flex-start">
    <div class="col" style="gap:0;flex-shrink:0">{add}</div>
    <div class="col grow" style="gap:16px;min-width:0">{cond}</div>
  </div>
  <div class="row" style="gap:16px;align-items:flex-start">
    {lb}
    <div class="card pad col grow" style="gap:12px;min-width:0">
      <h3 class="sec">PHOTO AND ATTACHMENT ACCESS</h3>
      {table(["Topic", "Rule"], [
        ("Storage", "Private bucket through <code>StorageService.savePrivate()</code> only"),
        ("URLs", "Short-lived signed URLs. Never a permanent directly-reachable URL."),
        ("Download button", "Shown by permission and checked on the server, not merely hidden"),
        ("File names", "ASCII only — non-ASCII names have broken the Cloud Run build before"),
      ], [170, None])}
      {note_box("error", "If GCS_PRIVATE_BUCKET is missing from a revision, the service writes files to the "
                         "container disk and they are destroyed for good on the next deploy. "
                         "This already happened to Photo Evidence. Check the variable before every "
                         "traffic switch.")}
    </div>
  </div>
</div>'''

open("Visit.dc.html", "w", encoding="utf-8").write(sheet(
    "8 · Visit",
    "One visit record · fields that follow the type · photo lightbox · extending office_visits",
    visit_body, W2, H2, badge="Phase 4"))
print("Visit.dc.html")
