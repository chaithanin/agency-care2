# -*- coding: utf-8 -*-
"""Convert.dc.html -- the five-step Sold Deal conversion wizard, plus the error UX"""
from tokens import *
from shell import *

W, H = 1600, 1760
STEPS = ["Customer & Unit", "Sales Information", "Contract", "Payment Plan", "Review"]

def wizard(active, inner, w=520, foot=None):
    foot = foot or ('<button class="btn out sm">Back</button><button class="btn sm">Next</button>')
    return f'''<div class="card col" style="width:{w}px;flex-shrink:0;gap:0;overflow:hidden">
  <div class="col pad" style="gap:13px;border-bottom:1px solid {DIVIDER};padding-bottom:15px">
    <h3 class="h6">Convert to Sold Deal</h3>
    {steps(STEPS, active)}
  </div>
  <div class="col pad" style="gap:13px">{inner}</div>
  <div class="row pad" style="gap:10px;justify-content:flex-end;border-top:1px solid {DIVIDER};padding-top:14px">{foot}</div>
</div>'''

ok = lambda t: (f'<div class="row" style="gap:8px">{icon(I_CHECK,14,SUCCESS)}'
                f'<span class="b2" style="color:{TXT2}">{t}</span></div>')

s1 = wizard(0, f'''
  {field("Customer", "David Wong", required=True)}
  {field("Project", "Marina Golden Bay", required=True)}
  {field("Unit", "A2508", required=True)}
  {field("Selling Price (THB)", "3,500,000", required=True)}
  <div class="col" style="gap:6px;background:{SURFACE};border:1px solid {DIVIDER};
       border-radius:13px;padding:11px 13px">
    <span class="cap mut">Carried over from the lead. Editable, but the edit is recorded.</span>
    {ok("Unit A2508 is already in reserved status")}
    {ok("Price matches the price list of 12 Sep 2026")}
  </div>
  {note_box("warn", "If the unit is held by another deal, block it on the server — "
                    "not by hiding the option in the UI.")}''',
  foot='<button class="btn out sm">Cancel</button><button class="btn sm">Next</button>')

s2 = wizard(1, f'''
  <div class="col" style="gap:0">
    <p class="lbl">Lead Source<span style="color:{ERROR}">&nbsp;*</span></p>
    <div class="row" style="gap:22px;background:{SURFACE};border:1px solid {DIVIDER};
         border-radius:12px;padding:9px 13px">
      {radio("Direct", False)}{radio("Agency", True)}
    </div>
  </div>
  <div class="row" style="gap:12px">{field("Seller", "John Smith", required=True)}{field("Closer", "Sarah Lee", required=True)}</div>
  {field("Agency Company", "ABC Property", required=True)}
  {field("Agent", "John Tan", required=True)}
  <div class="col" style="gap:5px;background:{SURFACE};border:1px solid {DIVIDER};
       border-radius:13px;padding:11px 13px">
    <span class="cap mut">Selectable agents — filtered to Agency = ABC Property</span>
    {"".join(f'<div class="row" style="gap:8px"><span style="color:{TXT3}">·</span>'
             f'<span class="b2" style="color:{TXT2}">{n}</span></div>'
             for n in ["John Tan", "Linda Wong", "Peter Chen"])}
  </div>
  {note_box("error", "Choosing Direct must disable and clear Agency and Agent. "
                     "These two are conditionally required — never required at all times.")}''')

s3 = wizard(2, f'''
  <div class="row" style="gap:12px">{field("Contract Date", "18 Sep 2026", required=True)}{field("Contract No.", "CT-2026-000213")}</div>
  <div class="col" style="gap:0">
    <p class="lbl">Quota<span style="color:{ERROR}">&nbsp;*</span></p>
    <div class="col" style="gap:0;background:{SURFACE};border:1px solid {DIVIDER};border-radius:12px;padding:8px 12px">
      {radio("Thai Quota")}{radio("Thai Company")}{radio("Foreign Quota", True)}
      {radio("Sub-Ing-Sis")}{radio("Lease-hold")}
    </div>
  </div>
  {field("Special Request", "Furniture upgrade package")}
  <div class="row" style="gap:10px;background:{SURFACE};border:1px dashed {DIVIDER};
       border-radius:13px;padding:13px 15px">
    {icon(I_UP,17,PRIMARY_L)}<span class="b2 grow" style="color:{TXT2}">Attach Contract</span>
    <button class="btn out sm">Upload</button>
  </div>
  {note_box("ok", "These five quota values are already what production stores in "
                  "bookings.quota_category. Reuse them as they are — no new list, and old reports stay correct.")}''')

s4 = wizard(3, f'''
  {field("Project", "Marina Golden Bay")}
  <div class="row fld" style="gap:10px;align-items:center">
    <span class="grow">Plan A – Standard</span>{icon(I_CHEV,15)}
  </div>
  {table(["Milestone", "Amount", "Due"], [
    ("Booking", "50,000", "On contract date"),
    ("Contract", "100,000", "+7 days"),
    ("Down Payment", "500,000", "+30 days"),
    ("Installment", "100,000 × 18", "Monthly"),
    ("Transfer", "Remaining balance", "On transfer"),
  ], [150, 170, None])}
  {note_box("error", "Selecting from the master must <b>copy a snapshot</b> onto the deal. "
                     "If marketing edits the master plan in six months, an existing customer's "
                     "contract must not change with it.")}''')

s5 = wizard(4, f'''
  {kv([("Customer", "David Wong"), ("Project / Unit", "Marina Golden Bay / A2508"),
       ("Sale Price", "3,500,000 THB"), ("Quota", "Foreign Quota"),
       ("Seller", "John Smith"), ("Closer", "Sarah Lee"),
       ("Agency", "ABC Property"), ("Agent", "John Tan"),
       ("Contract Date", "18 Sep 2026"), ("Payment Plan", "Plan A – Standard")])}
  <div style="height:1px;background:{DIVIDER}"></div>
  {check("I confirm the above information.", True)}
  {note_box("info", "Create Sold Deal must do all of it in one transaction — build the payment schedule "
                    "from the snapshot, set the unit to sold, write the timeline entry, create the first "
                    "payment task. If any part fails, the whole thing rolls back.")}''',
  foot='<button class="btn out sm">Back</button><button class="btn sm">Create Sold Deal</button>')

done = f'''<div class="card pad col" style="width:380px;flex-shrink:0;gap:14px;align-items:center;
     text-align:center;border-color:{SUCCESS}66">
  <div style="width:46px;height:46px;border-radius:999px;background:rgba(34,197,94,.16);
       display:grid;place-items:center">{icon(I_CHECK,24,SUCCESS)}</div>
  <div class="col" style="gap:4px">
    <h3 class="h6">Sold Deal Created Successfully</h3>
    <span style="font-size:22px;font-weight:700;letter-spacing:-.02em;color:{SUCCESS}">SD-2026-000123</span>
  </div>
  <button class="btn sm">View Sold Deal</button>
  <span class="cap mut">The deal number continues the existing bookingNo sequence the system already
  issues. Do not start a second counter.</span>
</div>'''

err = f'''<div class="card pad col" style="width:400px;flex-shrink:0;gap:13px;border-color:{ERROR}66">
  <div class="row" style="gap:10px">{icon(I_WARN,18,ERROR)}
    <h3 class="h6 grow" style="color:{ERROR}">Cannot create Sold Deal</h3></div>
  <span class="b2" style="color:{TXT2}">Please complete the following:</span>
  <div class="col" style="gap:7px">
    {"".join(f"""<div class="row" style="gap:9px;background:rgba(239,68,68,.08);
      border:1px solid {ERROR}44;border-radius:11px;padding:9px 12px">
      <span style="color:{ERROR}">•</span>
      <span class="b2 grow" style="color:{TXT2}">{t}</span>
      <span class="cap" style="color:{PRIMARY_L}">Go to step {s}</span></div>"""
      for t, s in [("Payment Plan", 4), ("Contract Date", 3), ("Seller", 2)])}
  </div>
  <button class="btn out sm" style="align-self:flex-start">Return to Details</button>
  {note_box("info", "Never show a generic “Something went wrong”. Say what is missing and "
                    "give a way to go and fix it.")}
</div>'''

auto = f'''<div class="card pad col grow" style="gap:12px;min-width:0">
  <h3 class="sec">SAVE AS DRAFT + AUTOSAVE</h3>
  <div class="row" style="gap:10px;background:{SURFACE};border:1px solid {DIVIDER};
       border-radius:13px;padding:11px 14px">
    {icon(I_CLOCK,15,TXT3)}<span class="cap grow" style="color:{TXT2}">Last saved 15:24</span>
    <button class="btn out sm">Save as Draft</button>
  </div>
  <span class="b2" style="color:{TXT2}">This form has thirty fields. Nobody should have to fill all of
  them and submit once — the system holds a draft they can come back to.</span>
  {note_box("warn", "A draft must not count as a sale in any report until Create Sold Deal succeeds.")}
</div>'''

body = f'''<div class="col" style="gap:16px">
  {note_box("info", "Never let someone change a dropdown from Reservation to Sold and be done. "
                    "A sale is created one way only — through this wizard — so the mandatory data "
                    "is complete from day one.")}
  <div class="row" style="gap:16px;align-items:flex-start;flex-wrap:wrap">{s1}{s2}{s3}</div>
  <div class="row" style="gap:16px;align-items:flex-start;flex-wrap:wrap">{s4}{s5}{done}</div>
  <div class="row" style="gap:16px;align-items:stretch">{err}{auto}</div>
</div>'''

open("Convert.dc.html", "w", encoding="utf-8").write(sheet(
    "3 · Convert to Sold Deal",
    "Five-step wizard · conditional Direct / Agency · payment plan snapshot · an error state that points at the fix",
    body, W, H, badge="Phase 1"))
print("Convert.dc.html")
