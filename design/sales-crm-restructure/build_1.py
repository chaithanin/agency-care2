# -*- coding: utf-8 -*-
"""Main.dc.html -- read this sheet first.
Four-domain architecture, what already exists, impact levels, build order, the 8 guardrails.
"""
from tokens import *
from shell import *

W, H = 1760, 2460

# -- 1) Four-domain map -------------------------------------------------
def domain_box(title, lines, color, tag):
    items = "".join(f'<div class="row" style="gap:7px"><span style="color:{color}">·</span>'
                    f'<span class="b2" style="color:{TXT2}">{l}</span></div>' for l in lines)
    return f'''<div class="col" style="gap:9px;flex:1;min-width:0;background:{SURFACE};
     border:1px solid {color}55;border-radius:16px;padding:15px 17px">
  <div class="row" style="gap:9px">
    <span class="b2 grow" style="font-weight:700;color:{color}">{title}</span>
    <span class="chip" style="color:{TXT3};background:rgba(107,114,128,.16)">{tag}</span>
  </div>
  <div class="col" style="gap:4px">{items}</div>
</div>'''

domains = "".join([
    domain_box("1 · LEAD MANAGEMENT",
               ["New → Contacted → Visit", "→ Holding / Reservation", "→ Sold Deal",
                "Core tables: customer_leads · bookings"], PRIMARY_L, "Existing"),
    domain_box("2 · SOLD DEAL MANAGEMENT",
               ["Deal → Contract → Payment", "→ Commission → Transfer",
                "Core tables: bookings + new finance tables"], SUCCESS, "Extend"),
    domain_box("3 · AGENCY MANAGEMENT",
               ["Agency → Agent → Visit", "→ Lead → Sold Deal → Performance",
                "Core tables: agencies · agency_staff"], SECOND, "Existing"),
    domain_box("4 · VISIT MANAGEMENT",
               ["Agency Visit / Customer Visit", "/ Site Visit — one record set",
                "Core table: office_visits"], WARNING, "Existing"),
])

map_panel = panel(
    "TARGET ARCHITECTURE — 4 CORE DOMAINS",
    body=f'<div class="row" style="gap:13px;align-items:stretch">{domains}</div>',
    note="The point is that every business object has exactly one source of truth. "
         "Today Site Visit, Visit Summary and Follow-up all record the same event in different places.",
    grow=False)

# -- 2) The principle that governs the whole set ------------------------
principle = f'''<div class="card pad col" style="gap:12px;border-color:{SUCCESS}66;
     background:linear-gradient(135deg,rgba(34,197,94,.09),{PAPER} 62%)">
  <div class="row" style="gap:10px">
    {icon(I_CHECK,18,SUCCESS)}
    <h3 class="h6 grow">The rule that governs everything here — disturb the existing workflow as little as possible</h3>
  </div>
  <p class="b2" style="color:{TXT2};margin:0">
    This requirement is a <b style="color:{TXT}">restructure</b>, not a rewrite.
    More than half of what it asks for already exists in the system people use every day.
    The correct job is to <b style="color:{TXT}">extend what is there</b>,
    not to stand up a parallel set of tables beside it.
  </p>
  <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:11px">
    {"".join(f"""<div class="col" style="gap:4px;background:{SURFACE};border:1px solid {DIVIDER};
       border-radius:13px;padding:11px 13px">
       <span class="b2" style="font-weight:700;color:{SUCCESS}">{t}</span>
       <span class="cap mut">{d}</span></div>"""
      for t, d in [
        ("Add, never alter", "New columns and tables are fine. Never drop a column or change what an existing one means."),
        ("Keep old routes alive", "A page that is folded away redirects, it is not deleted. People have it bookmarked."),
        ("Config before code", "Anything the config tables already handle (deal_stages) must not be hard-coded."),
        ("One phase at a time", "Five phases, one PR each. A phase ships to production before the next one starts."),
      ])}
  </div>
</div>'''

# -- 3) What already exists in production -------------------------------
EXIST = [
  ("Lead funnel / stage", "<code>deal_stages</code> + <code>api/src/common/kanban-stages.ts</code>",
   "The stage table is editable from config. Ten stages today: open · 1st–4th Follow Up · Holding · Reservation · Missed · Closed Deals · Cancelled",
   0, "Config only"),
  ("Sub Status", "<code>bookings.report_status</code> · <code>customer_leads.report_status</code>",
   "Already stores holding / reservation / open / 1st–3rd follow up / missed — this <b>is</b> the Sub Status the requirement asks for",
   0, "Existing"),
  ("Sold Deal", "<code>bookings</code>",
   "Already has saleId · closerId · agencyId · agencyStaffId · sellingPrice · commissionPct · cashback · bookingNo. <b>Do not create a new sold_deals table.</b>",
   1, "Add column"),
  ("Quota", "<code>bookings.quota_category</code>",
   "Live values already in use: Thai Quota · Thai Company · Foreign Quota · Sub-Ing-Sis · Lease-hold → <b>the Quota question is already answered: it is Ownership Quota</b>",
   0, "Existing"),
  ("Central visit record", "<code>office_visits</code>",
   "Already has leadId · agencyId · saleIds · photos · discussionTopics · nextAction · nextVisitDate · soft delete",
   1, "Add column"),
  ("Planned agency visits", "<code>visit_plans</code> + <code>visit_checkins</code> + <code>visit_reports</code>",
   "Field-sales visits with GPS check-in — <b>a different thing from office_visits, do not merge them.</b> The Visit list reads both sources.",
   1, "Existing"),
  ("Task / reminder engine", "<code>tasks</code>",
   "Already has dealId · agencyId · visitPlanId · assigneeIds · dueDate · recurring · report — <b>this is the central task engine the requirement asks for</b>",
   1, "Add column"),
  ("Activity timeline", "<code>deal_timeline</code> (entity + entityId + type + actor)",
   "Already a shared timeline that works for any entity. Nothing new needed.",
   0, "Existing"),
  ("Audit", "<code>audit_logs</code> (metadata = before / after / changes)",
   "Already supports the field-change history the requirement asks for",
   0, "Existing"),
  ("Payment plan master", "<code>projects.payment_plan</code> is <b>one long free-text field</b>",
   "Not enough — needs a master table plus a per-deal snapshot",
   2, "New table"),
  ("Customer payment schedule", "<b>Does not exist.</b> <code>agency_deposits</code> is agency-side deposit money, a different thing",
   "All new, but the shape of <code>deposit_transactions</code> is a good model to copy",
   2, "New table"),
  ("Per-deal commission", "<code>agency_commissions</code> is a monthly total per agency",
   "Not tied to a deal — needs a per-deal entry table. Keep the existing one untouched.",
   2, "New table"),
]
rows = [(n, f'<span class="cap">{loc}</span>', f'<span class="cap" style="color:{TXT2}">{d}</span>',
         impact_chip(lv) + " " + flow_chip(tag)) for n, loc, d, lv, tag in EXIST]
exist_panel = panel(
    "WHAT ALREADY EXISTS — surveyed on branch feat/all-appointments-clean-on-118a2e2",
    right='<span class="cap mut">Read this before writing a line of code</span>',
    body=table(["Topic", "Where it lives today", "State", "Impact"], rows, [176, 300, None, 210]),
    note="“Impact” means impact on the workflow people use every day. Anything marked ●●● needs a rollback plan.",
    grow=False)

# -- 4) Six business questions ------------------------------------------
Q = [
  ("When is a Sold Deal created?",
   "An authorised approver confirms the sale <b>and</b> the mandatory fields are complete — <b>not</b> the deposit alone",
   "If the deposit is the only trigger there is nowhere to hold the contract, payment schedule or commission before the customer pays — a circular dependency",
   True),
  ("Is Deposit a condition or a status?",
   "A <b>status</b> on one row of the payment schedule, not a condition for the deal to exist",
   "This keeps Booking, Contract, Down Payment, Installment and Transfer in one table",
   True),
  ("What is commission calculated on?",
   "<code>basis</code> must be stated per entry (Sale Price or Net Price). One value for the whole system is wrong.",
   "Today <code>bookings.commission_pct</code> holds a single value per deal, which cannot express several recipients",
   False),
  ("What does Quota mean?",
   "<b>Already answered: Ownership Quota.</b> Use the live values in <code>bookings.quota_category</code>",
   "Thai Quota · Thai Company · Foreign Quota · Sub-Ing-Sis · Lease-hold — real data exists, do not invent a new list",
   True),
  ("One visit record or several?",
   "<code>office_visits</code> is the source of truth. <code>visit_plans</code> stays for planned field visits.",
   "Visit Summary and Site Visit Report become <b>views</b> over one data set, not a second data set",
   True),
  ("Where does Agency Last Visit come from?",
   "MAX(office_visits.visit_at, visit_checkins.checkin_at) — <b>computed, never entered by hand</b>",
   "The moment there is a field to type it into, the number is wrong for every agency someone forgot",
   True),
]
qrows = []
for i, (q, a, why, settled) in enumerate(Q, 1):
    mark = ('<span class="chip" style="color:#22C55E;background:rgba(34,197,94,.14)">Answer proposed</span>'
            if settled else
            '<span class="chip" style="color:#FBBF24;background:rgba(251,191,36,.15)">Owner must decide</span>')
    qrows.append((f'<b>{i}. {q}</b>', f'<span class="b2">{a}</span>',
                  f'<span class="cap mut">{why}</span>', mark))
q_panel = panel(
    "SIX BUSINESS QUESTIONS THAT MUST BE LOCKED BEFORE THE DATABASE IS TOUCHED",
    body=table(["Question", "Proposed answer", "Why", "State"], qrows, [200, 330, None, 190]),
    note="Five are answerable from what is already in production. Only the commission basis needs the owner to decide.",
    grow=False)

# -- 5) Build order ------------------------------------------------------
ORDER = ["Business Rule", "Data Model", "Workflow / State", "Information Architecture",
         "Wireframe", "UI Design", "API", "Development", "Migration", "UAT"]
chips = []
for i, s in enumerate(ORDER):
    chips.append(f'<span class="chip" style="color:{PRIMARY_L};background:rgba(59,130,246,.16)">'
                 f'{i+1}. {s}</span>')
    if i != len(ORDER) - 1:
        chips.append(f'<span style="color:{TXT3}">→</span>')
order_panel = panel(
    "BUILD ORDER — set by the owner, do not reorder",
    body=(f'<div class="row" style="gap:8px;flex-wrap:wrap;align-items:center">{"".join(chips)}</div>'
          + note_box("warn", "Starting from Figma or the front end means rebuilding several times over. "
                             "The six questions above must be locked before the database or the API is touched.")),
    grow=False)

# -- 6) Five phases ------------------------------------------------------
PHASES = [
  ("Phase 1", "Core Sales Architecture",
   ["Merge Holding / Reservation into one stage + Sub Status", "Record status-change history",
    "Sold Deal conversion wizard", "Basic contract"], 1,
   "A stage added in a config table plus three new columns. People see the board columns change; every row of data is still there."),
  ("Phase 2", "Financial",
   ["Payment plan master + snapshot", "Payment schedule", "Record payment",
    "Reminders before and after the due date"], 2,
   "All new tables, nothing existing touched — but this is real money, so UAT with finance before it goes live."),
  ("Phase 3", "Commission",
   ["Per-deal commission entries", "Approval chain", "Payment tracking"], 2,
   "New tables. agency_commissions stays exactly as it is and the old reports keep working."),
  ("Phase 4", "Agency & Visit",
   ["New agency profile", "Central visit record + visit type", "Computed Last Visit",
    "Photo lightbox"], 1,
   "New columns on office_visits plus new screens. visit_plans behaves exactly as before."),
  ("Phase 5", "Cleanup",
   ["Hide the Follow-up Board", "Fold Site Visit Report / Visit Summary Report into views",
    "Regroup the menu into the four domains", "Reports"], 3,
   "This is what people see every day, so it goes last — and every folded route needs a redirect."),
]
prows = []
for tag, name, items, lv, risk in PHASES:
    li = "<br>".join(f'<span style="color:{TXT3}">·</span> {x}' for x in items)
    prows.append((f'<b>{tag}</b><br><span class="cap mut">{name}</span>',
                  f'<span class="cap" style="color:{TXT2}">{li}</span>',
                  impact_chip(lv), f'<span class="cap mut">{risk}</span>'))
phase_panel = panel(
    "FIVE PHASES — one PR per phase, never one PR for all of it",
    body=table(["Phase", "Scope", "Impact", "Reason / watch out"], prows, [150, 330, 150, None]),
    note="The whole set is far too large to review in one pass, and if it breaks nobody will know which phase broke it.",
    grow=False)

# -- 7) Eight prohibitions ------------------------------------------------
BANS = [
  "Never merge Holding + Reservation by renaming a string and nothing else",
  "Never relabel Closed Deal as Sold Deal and call the job done",
  "Never build Deposit or Commission as free-text fields",
  "Never make Visit Summary a second copy of the data",
  "Never let Agency Last Visit be typed in by hand",
  "Never delete history to solve a navigation problem",
  "Never hard-delete a financial transaction",
  "Never let an edit to the payment plan master change an existing deal",
]
ban_items = "".join(
    f'''<div class="row" style="gap:10px;background:rgba(239,68,68,.07);border:1px solid {ERROR}44;
      border-radius:13px;padding:10px 13px">
      <span style="color:{ERROR};font-weight:700;font-size:13px;flex-shrink:0">{i+1}</span>
      <span class="b2" style="color:{TXT2}">{b}</span></div>''' for i, b in enumerate(BANS))
ban_panel = panel(
    "EIGHT THINGS A DEVELOPER MUST NOT DO — set by the owner as technical guardrails",
    body=f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:10px">{ban_items}</div>',
    grow=False)

body = f'''<div class="col" style="gap:16px">
  {principle}
  {map_panel}
  {exist_panel}
  {q_panel}
  <div class="row" style="gap:16px;align-items:stretch">
    <div class="col grow" style="gap:16px">{order_panel}{phase_panel}</div>
  </div>
  {ban_panel}
</div>'''

open("Main.dc.html", "w", encoding="utf-8").write(sheet(
    "Sales CRM Restructure — read this first",
    "Master UX/UI + Functional Architecture · 4 core domains · "
    "governing rule: disturb the existing workflow as little as possible",
    body, W, H, badge="Read first"))
print("Main.dc.html")
