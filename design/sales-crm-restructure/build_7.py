# -*- coding: utf-8 -*-
"""Commission.dc.html -- per-deal commission entries, workflow, approval, audit"""
from tokens import *
from shell import *

W, H = 1560, 1420

summ = kpi_strip([("175,000", "Total Commission", TXT), ("105,000", "Approved", SUCCESS),
                  ("70,000", "Pending", WARNING), ("0", "Paid", TXT2)])

CROWS = [
  ("ABC Property", "Agency", "Sale Price", "3%", "105,000", "Approved"),
  ("John Smith", "Seller", "Net Price", "1%", "35,000", "Pending Approval"),
  ("Sarah Lee", "Closer", "Net Price", "1%", "35,000", "Pending Approval"),
  ("John Tan", "Agent", "Agency Commission", "20%", "21,000", "On Hold"),
]
rows = [(f'<b>{a}</b>', b, c, d, f'<b>{e}</b>', flow_chip(f)) for a, b, c, d, e, f in CROWS]
tbl = panel("COMMISSION ENTRIES — one deal can carry several",
  right='<button class="btn out sm">+ Add Entry</button>',
  body=(summ + table(["Recipient", "Type", "Basis", "Rate", "Amount", "Status"], rows,
                     [190, 130, 180, 90, 130, 180]) +
        note_box("error", "Commission must never be a free-text field, and "
                          "<code>bookings.commission_pct</code> must not carry on as the single value "
                          "per deal. Keep the old column for compatibility; the real entries live here.")),
  note="Basis is stated per entry (Sale Price / Net Price / Agency Commission). This is the one question "
       "still open: what exactly Net Price is calculated from.",
  grow=False)

wf = f'''<div class="card pad col grow" style="gap:13px;min-width:0">
  <h3 class="sec">WORKFLOW</h3>
  {flow_line(["Calculated", "Pending Approval", "Approved", "Ready for Payment", "Paid"],
             "Pending Approval", "Rejected")}
  <div class="row" style="gap:9px;flex-wrap:wrap;align-items:center">
    <span class="cap mut">Extra states real operations need</span>
    {flow_chip("On Hold")}{flow_chip("Cancelled")}{flow_chip("Rejected")}
  </div>
  <div style="height:1px;background:{DIVIDER}"></div>
  <span class="cap mut">Where it starts</span>
  {flow_line(["Sold Deal", "Payment In Progress", "Calculated"], "Calculated")}
  <span class="b2" style="color:{TXT2}">Commission is calculated when the
  <b style="color:{TXT}">payment condition is met</b>, not the moment the deal is created.
  The threshold is config per project, never hard-coded.</span>
</div>'''

perm = f'''<div class="card pad col" style="gap:12px;width:500px;flex-shrink:0">
  <h3 class="sec">PERMISSIONS — checked on the server against user.role</h3>
  {table(["Role", "Rights"], [
    ("Sales", "View only"),
    ("Sales Manager", "Review"),
    ("Finance", f'<span style="color:{SUCCESS}">Approve / record payment</span>'),
    ("Admin", "Override, with a mandatory reason"),
  ], [190, None])}
  {note_box("error", "Once approved, Sales cannot edit. Block it in the API, not by disabling a button.")}
  <div class="col" style="gap:7px">
    <span class="cap mut">Every action writes all five to <code>audit_logs</code></span>
    <div class="row" style="gap:7px;flex-wrap:wrap">
      {"".join(f'<span class="chip" style="color:{TXT2};background:{SURFACE}">{t}</span>'
               for t in ["Who", "When", "Old value", "New value", "Reason"])}
    </div>
  </div>
</div>'''

audit = f'''<div class="card pad col grow" style="gap:12px;min-width:0">
  <h3 class="sec">AUDIT — uses the existing audit_logs table, nothing new</h3>
  {timeline([
    ("18 Sep 2026 · 15:22", "Sarah Lee changed the sale price",
     "3,450,000 → 3,500,000 · reason: customer upgraded unit", WARNING),
    ("18 Sep 2026 · 15:23", "System recalculated commission",
     "ABC Property 103,500 → 105,000", PRIMARY),
    ("18 Sep 2026 · 16:05", "Finance approved",
     "ABC Property · 105,000 THB", SUCCESS),
  ])}
  {note_box("warn", "Changing the sale price recalculates any commission still unapproved. "
                    "Entries already approved must not change by themselves — issue an adjustment instead.")}
</div>'''

calc = f'''<div class="card pad col" style="gap:12px;width:480px;flex-shrink:0">
  <h3 class="sec">ACCEPTANCE — the arithmetic must hold in every case</h3>
  {table(["Case", "Required result"], [
    ("basis 3,500,000 · rate 3%", f'<b style="color:{SUCCESS}">105,000</b>'),
    ("Due 500,000 · paid 300,000", f'Outstanding <b>200,000</b> · {flow_chip("Partially Paid")}'),
    ("Deal cancelled after commission approved", f'Issue a {flow_chip("Reversed")} entry; never delete the original'),
  ], [250, None])}
  {note_box("info", "Agree the rounding before writing code: round to two decimals per entry, "
                    "then sum — not sum then round.")}
</div>'''

body = f'''<div class="col" style="gap:16px">
  {tbl}
  <div class="row" style="gap:16px;align-items:stretch">{wf}{perm}</div>
  <div class="row" style="gap:16px;align-items:stretch">{audit}{calc}</div>
</div>'''

open("Commission.dc.html", "w", encoding="utf-8").write(sheet(
    "6 · Commission",
    "Per-deal entries · a workflow with the states real operations need · approval rights · audit",
    body, W, H, badge="Phase 3"))
print("Commission.dc.html")
