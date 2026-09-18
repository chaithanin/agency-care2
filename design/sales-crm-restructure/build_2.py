# -*- coding: utf-8 -*-
"""Lead.dc.html -- Pipeline View, Lead Detail, Change Status modal"""
from tokens import *
from shell import *

W, H = 1560, 1900

sub_hold = f'<div class="row" style="gap:6px">{flow_chip("Holding")}</div>'
sub_resv = f'<div class="row" style="gap:6px">{flow_chip("Reservation")}</div>'

cols = "".join([
  kanban_col("NEW", 32, [
    lead_card("Lead A", "Marina Golden Bay", "Today", owner="John S."),
    lead_card("Lead B", "LOVEIT @ Pattaya", "Today", owner="May P."),
    lead_card("Lead C", "HARMONIA", "1 day", owner="John S."),
  ]),
  kanban_col("CONTACTED", 18, [
    lead_card("Lead D", "LOVEIT @ Pattaya", "2 days", owner="Sarah L."),
    lead_card("Lead E", "Marina Golden Bay", "3 days", owner="May P."),
  ]),
  kanban_col("VISIT", 12, [
    lead_card("Lead F", "HARMONIA", "18 Sep", owner="John S."),
    lead_card("Lead G", "Marina Golden Bay", "16 Sep", owner="Sarah L."),
  ]),
  kanban_col("HOLDING / RESERVATION", 22, [
    lead_card("David Wong", "Marina Golden Bay · A2508", "18 Sep", sub_resv, "John S."),
    lead_card("Anna Petrova", "HARMONIA · B1204", "17 Sep", sub_hold, "Sarah L."),
    lead_card("Lee Chen", "Marina Golden Bay · C0902", "15 Sep", sub_hold, "May P."),
  ], width=282, sub="Holding 14 · Reservation 8"),
  kanban_col("SOLD DEAL", 11, [
    lead_card("SD-2026-000123", "Marina Golden Bay · A2508", "3.50M THB",
              f'<div class="row" style="gap:6px">{flow_chip("Active")}</div>', "John S."),
  ], sub="Opens the Sold Deals page"),
])

filters = f'''<div class="row" style="gap:9px;flex-wrap:wrap">
  <div class="row fld" style="gap:8px;width:250px">{icon(I_SEARCH,15)}<span class="mut">Search lead / phone / unit</span></div>
  {"".join(f'<div class="row fld" style="gap:9px">{f}{icon(I_CHEV,14)}</div>' for f in
    ["Stage", "Sub Status", "Project", "Sales Owner", "Agency", "Lead Source", "Next Follow-up"])}
</div>'''

pipeline = panel(
    "LEADS — PIPELINE VIEW",
    right=(f'<div class="row" style="gap:8px">'
           f'<span class="chip" style="color:{TXT};background:{SURFACE}">Pipeline</span>'
           f'<span class="chip" style="color:{TXT3}">List</span>'
           f'<button class="btn sm">+ New Lead</button></div>'),
    body=(filters +
          f'<div class="row" style="gap:16px;align-items:flex-start;overflow:hidden">{cols}</div>' +
          note_box("info", "A card carries only what is needed to decide quickly — customer, project, owner, "
                           "lead age, next follow-up, sub status. Do not pack every field onto the card.")),
    note="Holding and Reservation share one board column, but the split is still counted under the column "
         "heading and stays separable in every report.",
    grow=False)

head = f'''<div class="row" style="gap:14px;align-items:flex-start">
  <div class="col grow" style="gap:4px">
    <span class="cap mut">Sales &nbsp;›&nbsp; Leads &nbsp;›&nbsp; David Wong</span>
    <div class="row" style="gap:11px"><h2 class="h5">David Wong</h2>{flow_chip("Holding / Reservation")}{flow_chip("Reservation")}</div>
    <span class="cap mut">Marina Golden Bay · A2508 · lead age 34 days</span>
  </div>
  <div class="row" style="gap:9px">
    <button class="btn out sm">Change Status</button>
    <button class="btn sm">Convert to Sold Deal</button>
  </div>
</div>'''

left = f'''<div class="col grow" style="gap:16px;min-width:0">
  {tabs(["Overview", "Activities", "Visits", "Documents"], "Overview")}
  {sect("CUSTOMER", kv([("Phone", "+66 81 234 5678"), ("Email", "david.w@example.com"),
                        ("Nationality", "Singapore"), ("Source", "Agency")]))}
  {sect("INTEREST", kv([("Project", "Marina Golden Bay"), ("Unit", "A2508"),
                        ("Budget", "3.0 – 3.8M THB"), ("Room Type", "1 Bedroom · Sea View")]))}
  {sect("SALES", kv([("Sales Owner", "John Smith"), ("Agency", "ABC Property"),
                     ("Agent", "John Tan"), ("Lead Source", "Agency")]))}
  {sect("RESERVATION", kv([("Unit", "A2508"), ("Reservation Date", "18 Sep 2026"),
                           ("Reservation Amount", "50,000 THB"), ("Reservation Expiry", "02 Oct 2026"),
                           ("Payment Plan", "Plan A – Standard"), ("Quota", "Foreign Quota")]))}
  {sect("NEXT ACTION",
        kv([("Follow-up Date", "24 Sep 2026"), ("Assigned To", "John Smith"),
            ("Task", "Confirm documents and book the signing")]),
        right=f'<span class="chip" style="color:{PRIMARY_L};background:rgba(59,130,246,.16)">created as a task automatically</span>')}
</div>'''

right_panel = f'''<div class="col" style="gap:14px;width:330px;flex-shrink:0">
  <div class="card pad col" style="gap:14px">
    <h4 class="sec">ACTIVITY TIMELINE</h4>
    {timeline([
      ("18 Sep · 14:30", "Reservation created", "by John Smith · 50,000 THB", SUCCESS),
      ("17 Sep · 11:15", "Site visit", "Marina Golden Bay · 3 photos", SECOND),
      ("15 Sep · 09:40", "WhatsApp contact", "by John Smith", PRIMARY),
      ("14 Sep · 16:02", "Status changed", "Visit → Holding / Reservation", WARNING),
      ("14 Sep · 10:00", "Lead created", "Source: ABC Property", TXT3),
    ])}
  </div>
  {note_box("info", "This timeline is a shared component reused on Lead, Sold Deal, Agency and Visit. "
                    "It reads deal_timeline, which already exists — no new table.")}
</div>'''

detail = panel("LEAD DETAIL",
               body=f'{head}<div class="row" style="gap:20px;align-items:flex-start">{left}{right_panel}</div>',
               note="One timeline that reads end to end matters more than a long row of tabs.",
               grow=False)

m_body = f'''
  {field("Funnel Stage", "Holding / Reservation")}
  <div class="col" style="gap:0">
    <p class="lbl">Sub Status<span style="color:{ERROR}">&nbsp;*</span></p>
    <div class="col" style="gap:0;background:{SURFACE};border:1px solid {DIVIDER};border-radius:12px;padding:8px 12px">
      {radio("Holding", False, "no money down yet")}
      {radio("Reservation", True, "reservation fee paid")}
    </div>
  </div>
  {field("Effective Date", "18 Sep 2026")}
  {field("Remark", "", placeholder="Why the status changed")}
  <div class="col" style="gap:9px;background:rgba(251,191,36,.08);border:1px solid {WARNING}44;
       border-radius:13px;padding:12px 14px">
    <div class="row" style="gap:8px">{icon(I_WARN,15,WARNING)}
      <span class="cap" style="color:{WARNING};font-weight:700">Choosing Reservation makes these mandatory</span></div>
    {field("Unit", "A2508", required=True)}
    {field("Reservation Date", "18 Sep 2026", required=True)}
    {field("Reservation Amount", "50,000")}
    {field("Reservation Expiry", "02 Oct 2026")}
    {field("Payment Plan", "Plan A – Standard")}
  </div>'''
m = modal("Update Lead Status", m_body,
          '<button class="btn out sm">Cancel</button><button class="btn sm">Update Status</button>', w=430)

conv = f'''<div class="card pad col grow" style="gap:14px">
  <h3 class="sec">CONVERSION THAT MUST STILL BE MEASURABLE AFTER THE MERGE</h3>
  {table(["Path", "Count", "Rate"], [
    ("Visit → Holding", "41 → 14", f'<b style="color:{PRIMARY_L}">34%</b>'),
    ("Holding → Reservation", "14 → 8", f'<b style="color:{SUCCESS}">57%</b>'),
    ("Holding → Lost", "14 → 4", f'<b style="color:{ERROR}">29%</b>'),
    ("Reservation → Sold", "8 → 5", f'<b style="color:{SUCCESS}">62%</b>'),
    ("Reservation → Cancelled", "8 → 1", f'<b style="color:{ERROR}">13%</b>'),
  ], [230, 130, 90])}
  {note_box("error", "This is why the data must never be merged past the point of separation. "
                     "The board may combine the columns; sub_status must stay on every row in the database.")}
  <div class="col" style="gap:7px">
    <span class="cap mut">Fields required to produce this table</span>
    <span class="b2" style="color:{TXT2}">
      <code>lead_status_history</code> holding old_stage · old_sub_status · new_stage · new_sub_status
      · changed_at · changed_by · reason — <b>insert only, never update a past row</b></span>
  </div>
</div>'''

body = f'''<div class="col" style="gap:16px">
  {pipeline}
  {detail}
  <div class="row" style="gap:16px;align-items:stretch">
    <div class="col" style="gap:0;flex-shrink:0">{m}</div>
    {conv}
  </div>
</div>'''

open("Lead.dc.html", "w", encoding="utf-8").write(sheet(
    "1 · Lead Management",
    "Pipeline view · lead detail · change status — funnel stage kept separate from sub status",
    body, W, H, badge="Phase 1"))
print("Lead.dc.html")
