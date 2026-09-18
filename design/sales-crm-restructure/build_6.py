# -*- coding: utf-8 -*-
"""Payment.dc.html -- payment plan master + snapshot, schedule, record payment, reminders"""
from tokens import *
from shell import *

W, H = 1620, 1760

summary = f'''<div class="col" style="gap:13px">
  {kpi_strip([("3,500,000", "Total Contract Value", TXT), ("650,000", "Paid", SUCCESS),
              ("2,850,000", "Outstanding", WARNING), ("200,000", "Overdue", ERROR)])}
  {progress(19, SUCCESS, "19% of contract value")}
</div>'''

ROWS = [
  ("Booking", "18 Sep 2026", "50,000", "50,000", "Paid"),
  ("Contract", "20 Sep 2026", "100,000", "100,000", "Paid"),
  ("Down Payment", "30 Sep 2026", "500,000", "300,000", "Partial"),
  ("Installment #1", "30 Oct 2026", "100,000", "—", "Upcoming"),
  ("Installment #2", "30 Nov 2026", "100,000", "—", "Upcoming"),
  ("Transfer", "30 Jun 2027", "2,650,000", "—", "Future"),
]
prows = [(f'<b>{a}</b>', b, c, d, flow_chip(e)) for a, b, c, d, e in ROWS]
sched = panel("PAYMENT SCHEDULE",
  right='<button class="btn sm">Record Payment</button>',
  body=(table(["Payment", "Due Date", "Amount", "Paid", "Status"], prows, [180, 150, 150, 150, 150]) +
        f'<div class="row" style="gap:9px;flex-wrap:wrap;padding-top:4px">'
        f'{"".join(flow_chip(s) for s in ["Paid","Partial","Pending","Upcoming","Overdue","Cancelled","Refunded"])}</div>' +
        note_box("info", "The requirement calls this Deposit Tracking, but the deposit must not be a separate "
                         "one-off record — it is one row in this table, exactly like Booking, Contract, "
                         "Installment and Transfer.")),
  note="Every row's status is computed from what was actually paid against what is due and when. "
       "Never store it as a column for someone to change.",
  grow=False)

rec = modal("Record Payment", f'''
  {kv([("Payment Item", "Down Payment"), ("Required", "500,000 THB"),
       ("Paid to Date", "300,000 THB"), ("Outstanding", "200,000 THB")])}
  <div style="height:1px;background:{DIVIDER}"></div>
  {field("New Payment (THB)", "200,000", required=True)}
  {field("Payment Date", "18 Sep 2026", required=True)}
  {field("Payment Method", "Bank Transfer")}
  {field("Reference No.", "", placeholder="Transfer reference")}
  <div class="row" style="gap:10px;background:{SURFACE};border:1px dashed {DIVIDER};
       border-radius:13px;padding:11px 14px">
    {icon(I_UP,16,PRIMARY_L)}<span class="b2 grow" style="color:{TXT2}">Receipt</span>
    <button class="btn out sm">Upload</button>
  </div>
  {field("Remark", "")}
  <div class="col" style="gap:6px;background:rgba(239,68,68,.07);border:1px solid {ERROR}44;
       border-radius:13px;padding:11px 13px">
    <span class="cap" style="color:{ERROR};font-weight:700">Validate all of these on the server</span>
    {"".join(f'<div class="row" style="gap:7px"><span style="color:{ERROR}">·</span>'
             f'<span class="cap" style="color:{TXT2}">{t}</span></div>' for t in [
       "The new payment must be greater than zero",
       "The total must not exceed the amount due, unless overpayment is enabled",
       "The payment date must not be in the future",
       "The receipt goes to the private bucket through savePrivate() only"])}
  </div>''',
  '<button class="btn out sm">Cancel</button><button class="btn sm">Save Payment</button>', w=430)

snap = f'''<div class="card pad col grow" style="gap:12px;min-width:0">
  <h3 class="sec">PAYMENT PLAN MASTER → SNAPSHOT</h3>
  <div class="row" style="gap:14px;align-items:stretch">
    <div class="col" style="gap:7px;flex:1;min-width:0;background:{SURFACE};border:1px solid {DIVIDER};
         border-radius:13px;padding:12px 14px">
      <span class="b2" style="font-weight:700">payment_plan_masters</span>
      <span class="cap mut">Per project · marketing edits it freely</span>
      <span class="cap" style="color:{TXT2}">Plan A · Booking 50,000 · Contract 100,000 …</span>
    </div>
    <div class="col" style="justify-content:center">{icon(I_ARROW,20,SUCCESS)}</div>
    <div class="col" style="gap:7px;flex:1;min-width:0;background:{SURFACE};border:1px solid {SUCCESS}55;
         border-radius:13px;padding:12px 14px">
      <span class="b2" style="font-weight:700">deal_payment_plan_snapshots</span>
      <span class="cap mut">Copied when the deal is created · never editable again</span>
      <span class="cap" style="color:{TXT2}">SD-2026-000123 · Booking 50,000 · Contract 100,000 …</span>
    </div>
  </div>
  {note_box("error", "A deal must never reference the master plan live and nothing else. "
                     "When marketing edits the master in six months, an existing customer's contract "
                     "must not follow it.")}
  <span class="cap mut">The existing <code>projects.payment_plan</code> free text stays exactly as it is,
  as reference. Nothing to delete, nothing to move.</span>
</div>'''

rem = f'''<div class="card pad col" style="gap:12px;width:480px;flex-shrink:0">
  <h3 class="sec">PAYMENT REMINDERS — CREATED AS TASKS, NOT A SEPARATE BOARD</h3>
  <div class="row" style="gap:9px;flex-wrap:wrap">
    {"".join(f'<span class="chip" style="color:{PRIMARY_L};background:rgba(59,130,246,.16)">{t}</span>'
             for t in ["7 days before", "3 days before", "On due date", "Overdue +1 day"])}
  </div>
  <div class="col" style="gap:7px;background:{SURFACE};border:1px solid {DIVIDER};
       border-radius:13px;padding:12px 14px">
    <span class="b2" style="font-weight:700">Follow-up payment</span>
    {kv([("Customer", "David Wong"), ("Outstanding", "200,000 THB"),
         ("Assigned", "Sales Support"), ("Due", "30 Sep 2026")])}
  </div>
  {note_box("ok", "This uses the existing <code>tasks</code> table, which already carries dealId, "
                  "assigneeIds, dueDate and recurring. That is why the Follow-up Board can be removed "
                  "without losing any capability.")}
  {note_box("warn", "A reminder must never fire twice. Enforce it with a unique key in the database "
                    "(schedule row + reminder kind + date), not with a check in code.")}
</div>'''

body = f'''<div class="col" style="gap:16px">
  {panel("PAYMENT SUMMARY", body=summary, grow=False)}
  {sched}
  <div class="row" style="gap:16px;align-items:flex-start">
    <div class="col" style="gap:0;flex-shrink:0">{rec}</div>
    <div class="col grow" style="gap:16px;min-width:0">{snap}</div>
  </div>
  <div class="row" style="gap:16px;align-items:stretch">
    <div class="card pad col grow" style="gap:12px;min-width:0">
      <h3 class="sec">NEW TABLES FOR THIS PHASE — nothing existing is touched</h3>
      {table(["Table", "Purpose", "Constraint"], [
        ("<code>payment_plan_masters</code>", "Payment plan per project", "Keyed to project_id"),
        ("<code>payment_plan_master_items</code>", "Milestones in a plan", "Order + due-date formula"),
        ("<code>deal_payment_plan_snapshots</code>", "The plan as it stood when the deal was created", "Write once, never edit"),
        ("<code>deal_payment_schedules</code>", "Milestones on a deal", "unique(deal_id, seq)"),
        ("<code>deal_payment_transactions</code>", "Each individual payment", "Insert only, never update a total"),
      ], [290, 250, None])}
      {note_box("error", "The paid amount is the sum of the transactions. Never UPDATE a total directly, "
                         "and never hard-delete — reverse it with a new row marked Reversed.")}
    </div>
    {rem}
  </div>
</div>'''

open("Payment.dc.html", "w", encoding="utf-8").write(sheet(
    "5 · Payment",
    "Payment plan master + snapshot · schedule · recording a payment · reminders as tasks",
    body, W, H, badge="Phase 2"))
print("Payment.dc.html")
