# -*- coding: utf-8 -*-
"""Deal.dc.html -- Sold Deal detail, five separate statuses, lifecycle"""
from tokens import *
from shell import *

W, H = 1600, 1620

head = f'''<div class="row" style="gap:16px;align-items:flex-start">
  <div class="col grow" style="gap:5px">
    <span class="cap mut">Sales &nbsp;›&nbsp; Sold Deals &nbsp;›&nbsp; SD-2026-000123</span>
    <div class="row" style="gap:11px"><h2 class="h5">SD-2026-000123</h2>{flow_chip("Active")}</div>
    <span class="cap mut">Marina Golden Bay · A2508 · David Wong</span>
  </div>
  <button class="btn out sm">Edit Deal</button>
</div>
{kpi_strip([("3.50M", "Sale Price", TXT), ("650K", "Paid", SUCCESS),
            ("2.85M", "Outstanding", WARNING), ("200K", "Overdue", ERROR),
            ("18 Sep 2026", "Contract", TXT2), ("30 Jun 2027", "Transfer", TXT2)])}'''

left = f'''<div class="col grow" style="gap:18px;min-width:0">
  {tabs(["Overview", "Payment", "Commission", "Documents", "Activity"], "Overview")}
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:18px 24px">
    {sect("DEAL INFORMATION", kv([("Project", "Marina Golden Bay"), ("Unit", "A2508"),
        ("Sale Price", "3,500,000 THB"), ("Quota", "Foreign Quota"),
        ("Contract Date", "18 Sep 2026"), ("Contract No.", "CT-2026-000213")]))}
    {sect("CUSTOMER", kv([("Name", "David Wong"), ("Phone", "+66 81 234 5678"),
        ("Nationality", "Singapore"), ("Email", "david.w@example.com")]))}
    {sect("SALES TEAM", kv([("Seller", "John Smith"), ("Closer", "Sarah Lee")]))}
    {sect("AGENCY", kv([("Agency", "ABC Property"), ("Agent", "John Tan")]))}
    {sect("PAYMENT PLAN", kv([("Plan", "Plan A – Standard"), ("Installment", "18 months")]),
      right=f'<span class="chip" style="color:{SECOND};background:rgba(167,139,250,.16)">snapshot</span>')}
    {sect("SPECIAL REQUEST", f'<span class="b2" style="color:{TXT2}">Furniture upgrade package</span>')}
  </div>
  {note_box("info", "Sections, not tabs. Eight to ten tabs makes the information harder to find, not easier.")}
</div>'''

right = f'''<div class="col" style="gap:14px;width:320px;flex-shrink:0">
  <div class="card pad col" style="gap:11px;border-color:{WARNING}55">
    <h4 class="sec" style="color:{WARNING}">NEXT ACTION</h4>
    {kv([("Payment due", "30 Sep 2026"), ("Amount", "200,000 THB"),
         ("Assigned", "Sales Support")], cols=1)}
    <button class="btn out sm" style="align-self:flex-start">Open task</button>
  </div>
  <div class="card pad col" style="gap:12px">
    <h4 class="sec">ACTIVITY</h4>
    {timeline([
      ("Today 14:30", "Payment received", "200,000 THB · by Finance", SUCCESS),
      ("Today 11:15", "Visit recorded", "by John Smith", SECOND),
      ("Yesterday 16:40", "Status changed", "Holding → Reservation · by Sarah Lee", WARNING),
      ("18 Sep 09:02", "Sold deal created", "by Sarah Lee", PRIMARY),
    ])}
  </div>
</div>'''

detail = panel("SOLD DEAL DETAIL",
  body=f'{head}<div class="row" style="gap:22px;align-items:flex-start;margin-top:4px">{left}{right}</div>',
  grow=False)

STATES = [
  ("Deal Status", ["Draft", "Confirmed", "Contracted", "Payment In Progress",
                   "Transfer Pending", "Completed"], "Payment In Progress",
   "Cancelled", "Overall progress of the deal"),
  ("Payment Status", ["Unpaid", "Partially Paid", "Paid"], "Partially Paid",
   "Refunded", "Computed from the schedule. Nobody sets it by hand."),
  ("Contract Status", ["Unsigned", "Signed"], "Signed", None, "Follows the attached contract"),
  ("Commission Status", ["Calculated", "Pending Approval", "Approved", "Paid"],
   "Pending Approval", "Rejected", "Per entry, not for the whole deal"),
  ("Transfer Status", ["Not Ready", "Transfer Pending", "Completed"], "Not Ready",
   None, "Ready once payment completes"),
]
srows = []
for name, stages, active, rej, note in STATES:
    srows.append((f'<b>{name}</b>', flow_line(stages, active, rej),
                  f'<span class="cap mut">{note}</span>'))
state_panel = panel("FIVE STATUSES THAT MUST STAY SEPARATE — never one field with twenty values",
  body=table(["Status", "Possible values", "Note"], srows, [190, None, 230]),
  note="A sold deal is one entity, and Completed is a status on it. Never make the funnel carry two stages "
       "called Sold and Sold Completed — that mixes the sale with the fulfilment.",
  grow=False)

trigger = f'''<div class="card pad col grow" style="gap:12px;min-width:0">
  <h3 class="sec">WHEN A SOLD DEAL IS CREATED</h3>
  {flow_line(["Reservation", "Confirm Sale", "Sold Deal"], "Sold Deal")}
  <div class="col" style="gap:8px">
    <span class="b2" style="color:{TXT2}"><b style="color:{TXT}">Trigger:</b>
      an authorised approver confirms the sale <b>and</b> the mandatory data from the wizard is complete.</span>
    <span class="b2" style="color:{TXT2}"><b style="color:{TXT}">It does not mean</b>
      everything is paid. It means a commercial sale has been confirmed and a formal record now exists.</span>
  </div>
  {note_box("error", "Never use the deposit as the only trigger. A customer who has signed but not yet paid "
                     "would have nowhere to hold the contract, the schedule or the commission — "
                     "a circular dependency.")}
</div>'''

perm = f'''<div class="card pad col" style="gap:12px;width:520px;flex-shrink:0">
  <h3 class="sec">WHO CAN DO WHAT</h3>
  {table(["Action", "Sales", "Manager", "Support", "Finance"], [
    ("Create sold deal", "Request", f'<span style="color:{SUCCESS}">Approve</span>', "View", "View"),
    ("Edit sale price", "No", f'<span style="color:{SUCCESS}">Yes</span>', "No", "No"),
    ("Record payment", "View", "View", f'<span style="color:{SUCCESS}">Yes</span>', f'<span style="color:{SUCCESS}">Yes</span>'),
    ("Delete deal", f'<span style="color:{ERROR}">No</span>', f'<span style="color:{ERROR}">No</span>',
     f'<span style="color:{ERROR}">No</span>', f'<span style="color:{ERROR}">No</span>'),
  ], [170, 80, 90, 80, 80])}
  {note_box("error", "Financial records are never deleted. Use Void, Cancelled or Reversed, and record "
                     "who, when, the old value, the new value and the reason every time.")}
  <span class="cap mut">Permission checks run on the server against <code>user.role</code> only —
  not <code>activeRole</code>, and not by hiding a button.</span>
</div>'''

body = f'''<div class="col" style="gap:16px">
  {detail}
  {state_panel}
  <div class="row" style="gap:16px;align-items:stretch">{trigger}{perm}</div>
</div>'''

open("Deal.dc.html", "w", encoding="utf-8").write(sheet(
    "4 · Sold Deal",
    "The most important page in the system · five separate statuses · the creation trigger · permissions",
    body, W, H, badge="Phase 1"))
print("Deal.dc.html")
