# -*- coding: utf-8 -*-
"""Commission.dc.html -- per-deal commission entries, workflow, approval, audit"""
from tokens import *
from shell import *

W, H = 1560, 1900

summ = kpi_strip([("193,000", "Total Commission", TXT), ("105,000", "Approved", SUCCESS),
                  ("67,000", "Pending", WARNING), ("21,000", "On Hold", TXT2)])

CROWS = [
  ("ABC Property", "Agency", "Sale Price", "3%", "105,000", "Approved"),
  ("John Smith", "Seller", "Net Price", "1%", "33,500", "Pending Approval"),
  ("Sarah Lee", "Closer", "Net Price", "1%", "33,500", "Pending Approval"),
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
  note="Basis is stated per entry — Sale Price, Net Price or Agency Commission. Net Price is now locked: "
       "see the formula panel below.",
  grow=False)


net = f'''<div class="card pad col grow" style="gap:13px;min-width:0;border-color:{SUCCESS}66;
     background:linear-gradient(135deg,rgba(34,197,94,.08),{PAPER} 65%)">
  <div class="row" style="gap:10px">{icon(I_CHECK,17,SUCCESS)}
    <h3 class="h6 grow">NET PRICE — locked by the owner</h3>
    <span class="chip" style="color:{SUCCESS};background:rgba(34,197,94,.14)">decided</span></div>
  <div class="row" style="gap:10px;flex-wrap:wrap;align-items:center;background:{SURFACE};
       border:1px solid {DIVIDER};border-radius:13px;padding:13px 15px">
    <span class="b2" style="font-weight:700">Net Price</span>
    <span style="color:{TXT3}">=</span>
    <span class="b2" style="color:{TXT2}">Sale Price</span>
    <span style="color:{ERROR};font-weight:700">−</span>
    <span class="b2" style="color:{TXT2}">Discount</span>
    <span style="color:{ERROR};font-weight:700">−</span>
    <span class="b2" style="color:{TXT2}">Promotion value</span>
  </div>
  <div class="row" style="gap:12px;align-items:stretch;flex-wrap:wrap">
    <div class="col" style="gap:5px;flex:1;min-width:210px">
      <span class="cap mut">Worked example</span>
      {table(["Line", "THB"], [
        ("Sale Price", "3,500,000"),
        ("less Discount", f'<span style="color:{ERROR}">− 50,000</span>'),
        ("less Promotion value", f'<span style="color:{ERROR}">− 100,000</span>'),
        ("<b>Net Price</b>", f'<b style="color:{SUCCESS}">3,350,000</b>'),
      ], [180, None])}
    </div>
    <div class="col" style="gap:5px;flex:1;min-width:210px">
      <span class="cap mut">What each entry is calculated on</span>
      {table(["Entry", "Basis"], [
        ("Agency", "Sale Price · 3% → 105,000"),
        ("Seller", "Net Price · 1% → 33,500"),
        ("Closer", "Net Price · 1% → 33,500"),
        ("Agent", "Agency commission · 20% → 21,000"),
      ], [110, None])}
    </div>
  </div>
  {note_box("warn", "<b>Tax is not deducted.</b> The owner named discount and promotion only. "
                    "If VAT or withholding should come out of the basis, it has to be stated "
                    "before Phase 3 is coded.")}
</div>'''

cols_panel = f'''<div class="card pad col" style="gap:12px;width:520px;flex-shrink:0;border-color:{WARNING}66">
  <div class="row" style="gap:10px">{icon(I_WARN,17,WARNING)}
    <h3 class="h6 grow">THE FORMULA NEEDS ONE NEW COLUMN</h3></div>
  {table(["Field", "Today", "Action"], [
    ("<code>bookings.selling_price</code>", "Float — the sale price",
     f'<span style="color:{SUCCESS}">use as is</span>'),
    ("<code>bookings.discount</code>", "Float, <b>already a baht amount</b>",
     f'<span style="color:{SUCCESS}">use as is</span>'),
    ("<code>bookings.promotion</code>", f'<b style="color:{ERROR}">String — free text</b>',
     f'<span style="color:{WARNING}">keep, do not touch</span>'),
    ("<code>bookings.promotion_value</code>", f'<b style="color:{ERROR}">does not exist</b>',
     f'<span style="color:{SECOND}">add: Float, nullable</span>'),
  ], [230, 170, None])}
  <div class="col" style="gap:6px">
    <span class="cap mut">Why discount can be trusted as an amount</span>
    <span class="cap" style="color:{TXT2}"><code>deals.service.ts</code> already computes
    <code>value = sellingPrice − discount</code> in five places. The deal value on the board is
    that subtraction today, so the meaning is settled.</span>
  </div>
  {note_box("error", "A null promotion_value counts as 0, never as “skip the deal”. "
                     "Backfill the existing rows to 0 and record which ones were assumed, "
                     "so nobody reads an old deal as having had no promotion when nobody checked.")}
</div>'''

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
    ("Sale Price 3,500,000 · rate 3%", f'<b style="color:{SUCCESS}">105,000</b>'),
    ("3,500,000 − 50,000 − 100,000 · rate 1%", f'Net <b>3,350,000</b> → <b style="color:{SUCCESS}">33,500</b>'),
    ("promotion_value is null", f'Treated as <b>0</b>, never as skip'),
    ("Due 500,000 · paid 300,000", f'Outstanding <b>200,000</b> · {flow_chip("Partially Paid")}'),
    ("Deal cancelled after commission approved", f'Issue a {flow_chip("Reversed")} entry; never delete the original'),
  ], [250, None])}
  {note_box("info", "Agree the rounding before writing code: round to two decimals per entry, "
                    "then sum — not sum then round.")}
</div>'''

body = f'''<div class="col" style="gap:16px">
  {tbl}
  <div class="row" style="gap:16px;align-items:stretch">{net}{cols_panel}</div>
  <div class="row" style="gap:16px;align-items:stretch">{wf}{perm}</div>
  <div class="row" style="gap:16px;align-items:stretch">{audit}{calc}</div>
</div>'''

open("Commission.dc.html", "w", encoding="utf-8").write(sheet(
    "6 · Commission",
    "Net Price locked · per-deal entries · workflow · approval rights · audit",
    body, W, H, badge="Phase 3"))
print("Commission.dc.html")
