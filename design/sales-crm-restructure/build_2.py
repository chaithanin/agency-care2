# -*- coding: utf-8 -*-
"""Lead.dc.html -- the existing Lead Status page, before and after Phase 1.
Drawn from web/src/pages/DealsPage.tsx so the change is visible as a change,
not as a redesign.
"""
from tokens import *
from shell import *

W, H = 3040, 2560

I_KANBAN = '<rect x="3" y="3" width="6" height="18" rx="1"></rect><rect x="10" y="3" width="6" height="13" rx="1"></rect><rect x="17" y="3" width="4" height="9" rx="1"></rect>'
I_TABLE  = '<rect x="3" y="4" width="18" height="16" rx="2"></rect><line x1="3" y1="10" x2="21" y2="10"></line><line x1="3" y1="15" x2="21" y2="15"></line>'
I_REPORT = '<path d="M4 20V10"></path><path d="M10 20V4"></path><path d="M16 20v-6"></path>'
I_REFR   = '<path d="M21 12a9 9 0 1 1-3-6.7"></path><polyline points="21 4 21 10 15 10"></polyline>'
I_GEAR   = '<circle cx="12" cy="12" r="3"></circle><path d="M19.4 15a1.6 1.6 0 0 0 .3 1.8l.1.1a2 2 0 1 1-2.8 2.8l-.1-.1a1.6 1.6 0 0 0-2.7 1.1V21a2 2 0 1 1-4 0v-.1A1.6 1.6 0 0 0 7 19.4a1.6 1.6 0 0 0-1.8.3l-.1.1a2 2 0 1 1-2.8-2.8l.1-.1a1.6 1.6 0 0 0-1.1-2.7H1a2 2 0 1 1 0-4h.1A1.6 1.6 0 0 0 2.6 7a1.6 1.6 0 0 0-.3-1.8l-.1-.1a2 2 0 1 1 2.8-2.8l.1.1a1.6 1.6 0 0 0 1.8.3H7a1.6 1.6 0 0 0 1-1.5V1a2 2 0 1 1 4 0v.1a1.6 1.6 0 0 0 2.7 1.1 1.6 1.6 0 0 0 1.8-.3l.1-.1a2 2 0 1 1 2.8 2.8l-.1.1a1.6 1.6 0 0 0-.3 1.8V7a1.6 1.6 0 0 0 1.5 1H21a2 2 0 1 1 0 4h-.1a1.6 1.6 0 0 0-1.5 1z"></path>'
I_CLOUD  = '<path d="M18 10h-1.3A7 7 0 1 0 4 15"></path><polyline points="12 12 12 21"></polyline><polyline points="8 17 12 21 16 17"></polyline>'
I_INFO   = '<circle cx="12" cy="12" r="9"></circle><line x1="12" y1="11" x2="12" y2="16"></line><circle cx="12" cy="8" r=".6" fill="currentColor"></circle>'

# ── page chrome, identical in both states ────────────────────────────
def toolbar():
    return f'''<div class="row" style="gap:7px;align-items:center">
  <h2 style="font-size:24px;font-weight:700;margin:0">Lead Status</h2>
  {icon(I_INFO,16,TXT3)}
  <div class="grow"></div>
  <div class="row" style="border:1px solid {DIVIDER};border-radius:6px;overflow:hidden">
    <div style="background:{SURFACE};padding:5px 9px">{icon(I_KANBAN,16,TXT)}</div>
    <div style="padding:5px 9px;border-left:1px solid {DIVIDER}">{icon(I_TABLE,16,TXT3)}</div>
  </div>
  {mui_iconbtn(I_REPORT)}{mui_iconbtn(I_REFR)}{mui_iconbtn(I_GEAR)}{mui_iconbtn(I_CLOUD)}
</div>'''

def filter_row(extra=""):
    return f'''<div class="row" style="gap:11px;flex-wrap:wrap;align-items:center;margin-top:16px">
  <div class="row" style="border:1px solid {DIVIDER};border-radius:6px;padding:7px 10px;
       width:210px;gap:7px">{icon(I_SEARCH,14,TXT3)}
    <span style="font-size:13px;color:{TXT3}">Search name / deal no. / phone</span></div>
  {mui_field("Agency", "All", 180)}
  {mui_field("Probability", "All", 150)}
  {mui_field("Deal Stage", "All", 150)}
  {extra}
  {mui_field("Date", "Created", 120)}
  {mui_field("From", "", 140, caret=False)}
  {mui_field("To", "", 140, caret=False)}
</div>'''

def sidebar():
    return f'''<div class="col" style="width:196px;flex-shrink:0;gap:0;padding-right:16px;
     border-right:1px solid {DIVIDER}">
  <div class="row" style="gap:8px;padding-bottom:6px">
    <span style="font-size:13px;font-weight:700;color:{TXT2}" class="grow">Filters</span>
    <span style="font-size:12px;color:{PRIMARY_L}">Clear all</span>
  </div>
  {sidebar_section("Salesperson", [sidebar_row("All", True), sidebar_row("John Smith"),
                                   sidebar_row("Sarah Lee"), sidebar_row("May P.")])}
  {sidebar_section("Interested In", [
    f'<div class="row" style="gap:5px;flex-wrap:wrap">'
    f'{mui_chip("Marina Golden Bay")}{mui_chip("HARMONIA")}{mui_chip("LOVEIT")}</div>'])}
  {sidebar_section("Labels", [sidebar_row("All", True), sidebar_row("FO", dot="#EC407A"),
                              sidebar_row("TC", dot="#5C6BC0"), sidebar_row("No Labels", dot="#9CA3AF")])}
  {sidebar_section("Next Action", [sidebar_row("All", True), sidebar_row("Upcoming"),
                                   sidebar_row("Overdue"), sidebar_row("None")])}
</div>'''

# ── cards ────────────────────────────────────────────────────────────
P_MGB = mui_chip("Marina Golden Bay")
P_HAR = mui_chip("HARMONIA")
L_FO  = mui_chip("FO", "secondary")

def cards_open():
    return [mui_card("Lead A", "ABC Property · &#128100; John Tan", "open", (P_MGB,), "1 u", "3.20M"),
            mui_card("Lead B", "XYZ Realty", "open", (mui_chip("LOVEIT"),), "1 u", "2.80M")]

def cards_f1():
    return [mui_card("Lead D", "ABC Property", "first_follow_up", (mui_chip("LOVEIT"), L_FO),
                     "1 u", "2.90M", follow="Next follow-up 24 Sep")]

def cards_f4():
    return [mui_card("Lead G", "XYZ Realty", "fourth_follow_up", (P_MGB,), "1 u", "3.10M")]

def card_hold(sub_chip=None):
    ch = (P_HAR, sub_chip) if sub_chip else (P_HAR,)
    return mui_card("Anna Petrova", "ABC Property · &#128100; Linda Wong", "holding", ch,
                    "1 u", "4.10M", follow="Next follow-up 22 Sep")

def card_resv(sub_chip=None):
    ch = (P_MGB, sub_chip) if sub_chip else (P_MGB,)
    return mui_card("David Wong", "ABC Property · &#128100; John Tan", "reservation", ch,
                    "1 u", "3.50M", follow="Overdue 18 Sep", overdue=True)

def card_hold2(sub_chip=None):
    ch = (P_MGB, sub_chip) if sub_chip else (P_MGB,)
    return mui_card("Lee Chen", "Direct", "holding", ch, "1 u", "2.60M")

# ── BEFORE ───────────────────────────────────────────────────────────
before_cols = "".join([
  mui_col("Open", 32, 34, "96.40M", cards_open()),
  mui_col("1st Follow Up", 18, 19, "54.10M", cards_f1()),
  mui_col("2nd Follow Up", 12, 12, "35.90M", []),
  mui_col("3rd Follow Up", 9, 9, "27.20M", []),
  mui_col("Holding", 14, 15, "44.80M", [card_hold(), card_hold2()]),
  mui_col("4th Follow Up", 7, 7, "21.00M", cards_f4()),
  mui_col("Reservation", 8, 8, "24.60M", [card_resv()]),
  mui_col("Missed", 5, 5, "14.20M", []),
  mui_col("Closed Deals", 11, 12, "38.50M", []),
  mui_col("Cancelled", 3, 3, "8.40M", []),
])

before = panel("THE PAGE TODAY — /deals",
  right='<span class="cap mut">drawn from web/src/pages/DealsPage.tsx · money() renders 96.40M, with no currency symbol</span>',
  body=(f'{toolbar()}{filter_row()}'
        f'<div class="row" style="gap:20px;align-items:flex-start;margin-top:18px">{sidebar()}'
        f'<div class="row" style="gap:12px;align-items:flex-start;overflow:hidden">{before_cols}</div></div>'),
  note="Ten columns, in this order. Holding sits before 4th Follow Up; Reservation sits after it.",
  grow=False)

# ── AFTER ────────────────────────────────────────────────────────────
SUB_H = mui_chip("Holding", "new")
SUB_R = mui_chip("Reservation", "new")

after_cols = "".join([
  mui_col("Open", 32, 34, "96.40M", cards_open()),
  mui_col("1st Follow Up", 18, 19, "54.10M", cards_f1()),
  mui_col("2nd Follow Up", 12, 12, "35.90M", []),
  mui_col("3rd Follow Up", 9, 9, "27.20M", []),
  mui_col("4th Follow Up", 7, 7, "21.00M", cards_f4()),
  mui_col("Holding / Reservation", 22, 23, "69.40M",
          [card_resv(SUB_R), card_hold(SUB_H), card_hold2(SUB_H)],
          extra_chips=mui_hdr_chip("H 14") + mui_hdr_chip("R 8"),
          highlight=True, width=268),
  mui_col("Missed", 5, 5, "14.20M", []),
  mui_col("Closed Deals", 11, 12, "38.50M", []),
  mui_col("Cancelled", 3, 3, "8.40M", []),
])

after = panel("AFTER PHASE 1 — the same page",
  right=f'<span class="chip" style="color:{SUCCESS};background:rgba(34,197,94,.14)">3 changes only</span>',
  body=(f'{toolbar()}{filter_row(mui_field("Sub Status", "All", 140))}'
        f'<div class="row" style="gap:20px;align-items:flex-start;margin-top:18px">{sidebar()}'
        f'<div class="row" style="gap:12px;align-items:flex-start;overflow:hidden">{after_cols}</div></div>'),
  note="Nine columns. Everything outlined in green is new; everything else is byte-for-byte the page above.",
  grow=False)

# ── what changed / what did not ──────────────────────────────────────
CHANGED = [
  ("1", "Two columns become one",
   "<code>Holding</code> and <code>Reservation</code> become <code>Holding / Reservation</code>, "
   "keeping Reservation's colour <code>#FFA726</code> and Reservation's slot in the order",
   "The column header already renders <code>col.color</code> and <code>col.label</code> from "
   "<code>deal_stages</code> — no component changes"),
  ("2", "Two counters in the column header",
   "<code>H 14</code> and <code>R 8</code>, in the same white pill the header already uses for "
   "<code>Won</code> and <code>Lost</code>",
   "Reuses the existing chip style at <code>DealsPage.tsx:421</code> — nothing new is designed"),
  ("3", "One more chip on the card",
   "The sub status joins the existing project / label chip row",
   "Same <code>height 18 · fontSize 10</code> chip the projects and labels already use. "
   "No new row, no change to card height"),
]
crows = [(f'<b style="color:{SUCCESS}">{n}</b>', f'<b>{t}</b>',
          f'<span class="cap" style="color:{TXT2}">{d}</span>',
          f'<span class="cap mut">{w}</span>') for n, t, d, w in CHANGED]

SAME = [
  "Page title, the info tooltip, and every icon button",
  "Kanban / Table toggle, Report, Refresh, Stage settings, Venio import",
  "The whole left filter sidebar — Salesperson, Interested In, Labels, Next Action",
  "Search, Agency, Probability, Deal Stage, Date, From, To",
  "Column width, header height, card layout, card height",
  "Drag and drop between columns",
  "The orphan warning banner",
  "The Table view",
  "Every other column: Open, 1st–4th Follow Up, Missed, Closed Deals, Cancelled",
]
same_items = "".join(
  f'<div class="row" style="gap:8px">{icon(I_CHECK,13,SUCCESS)}'
  f'<span class="b2" style="color:{TXT2}">{t}</span></div>' for t in SAME)

diff = panel("THE ONLY THREE VISUAL CHANGES",
  body=(table(["#", "Change", "What it is", "Why it costs almost nothing"], crows, [40, 210, 330, None]) +
        f'<div class="row" style="gap:20px;align-items:flex-start;margin-top:6px">'
        f'<div class="col grow" style="gap:8px;min-width:0">'
        f'<span class="sec" style="color:{SUCCESS}">UNCHANGED</span>{same_items}</div>'
        f'<div class="col" style="width:420px;flex-shrink:0;gap:11px">'
        + note_box("warn", "<b>One decision to confirm.</b> The merged column takes Reservation's "
                           "colour and Reservation's position, so Holding cards move one slot to the "
                           "right, past 4th Follow Up. The alternative is Holding's slot and grey "
                           "<code>#78909C</code> — fewer cards move, but the column looks less "
                           "advanced than Missed beside it.")
        + note_box("error", "Dropping a card onto the merged column can no longer tell which sub "
                            "status it is. It must open the modal below and ask — never pick one "
                            "silently.")
        + '</div></div>'),
  grow=False)

# ── change status modal, drawn as a MUI dialog ───────────────────────
m = f'''<div class="col" style="width:430px;flex-shrink:0;background:{PAPER};
     border:1px solid {DIVIDER};border-radius:10px;overflow:hidden;
     box-shadow:0 24px 64px rgba(0,0,0,.5)">
  <div style="padding:16px 20px 10px">
    <span style="font-size:18px;font-weight:600">Update Lead Status</span>
  </div>
  <div class="col" style="gap:16px;padding:8px 20px 16px">
    {mui_field("Funnel Stage", "Holding / Reservation", 388)}
    <div class="col" style="gap:0">
      <span style="font-size:11px;color:{TXT3};margin-bottom:4px">Sub Status *</span>
      {radio("Holding", False, "no money down yet")}
      {radio("Reservation", True, "reservation fee paid")}
    </div>
    {mui_field("Effective Date", "18 Sep 2026", 388, caret=False)}
    {mui_field("Remark", "", 388, caret=False)}
    <div class="col" style="gap:9px;background:rgba(251,191,36,.08);
         border:1px solid {WARNING}44;border-radius:8px;padding:12px 14px">
      <span style="font-size:11px;font-weight:700;color:{WARNING}">
        Choosing Reservation makes these mandatory</span>
      {mui_field("Unit *", "A2508", 356)}
      {mui_field("Reservation Date *", "18 Sep 2026", 356, caret=False)}
      {mui_field("Reservation Amount", "50,000", 356, caret=False)}
      {mui_field("Payment Plan", "Plan A - Standard", 356)}
    </div>
  </div>
  <div class="row" style="gap:10px;justify-content:flex-end;padding:12px 20px 16px">
    <span style="font-size:13px;font-weight:600;color:{TXT2};padding:6px 12px">CANCEL</span>
    <span style="font-size:13px;font-weight:600;color:{PRIMARY_L};padding:6px 12px">UPDATE STATUS</span>
  </div>
</div>'''

conv = f'''<div class="card pad col grow" style="gap:13px;min-width:0">
  <h3 class="sec">WHAT THE MERGE MUST NOT COST</h3>
  {table(["Path", "Count", "Rate"], [
    ("Visit &rarr; Holding", "41 &rarr; 14", f'<b style="color:{PRIMARY_L}">34%</b>'),
    ("Holding &rarr; Reservation", "14 &rarr; 8", f'<b style="color:{SUCCESS}">57%</b>'),
    ("Holding &rarr; Lost", "14 &rarr; 4", f'<b style="color:{ERROR}">29%</b>'),
    ("Reservation &rarr; Sold", "8 &rarr; 5", f'<b style="color:{SUCCESS}">62%</b>'),
    ("Reservation &rarr; Cancelled", "8 &rarr; 1", f'<b style="color:{ERROR}">13%</b>'),
  ], [230, 130, 90])}
  {note_box("error", "The board may show one column. The database must keep <code>sub_status</code> "
                     "on every row, or this table cannot be produced at all.")}
  <div class="col" style="gap:6px">
    <span class="cap mut">And the report keeps its two columns</span>
    <span class="b2" style="color:{TXT2}">The Lead Status report type <code>ReportBucket</code>
    already lists <code>holding</code> and <code>reservation</code> separately.
    <b style="color:{TXT}">Widen <code>bucketForStage()</code> to take the sub status</b>, or both
    collapse into one and the numbers change with nothing on screen to say so.</span>
  </div>
</div>'''

body = f'''<div class="col" style="gap:18px">
  {note_box("ok", "The brief for this sheet was: keep the page looking as close to the current one as "
                  "possible. So this is the real page, drawn from its own source, with the change "
                  "marked on it — not a redesign.")}
  {before}
  {after}
  {diff}
  <div class="row" style="gap:18px;align-items:flex-start">{m}{conv}</div>
</div>'''

open("Lead.dc.html", "w", encoding="utf-8").write(sheet(
    "1 · Lead Management",
    "The existing Lead Status board, before and after Phase 1 - three visual changes, nothing else moves",
    body, W, H, badge="Phase 1"))
print("Lead.dc.html")
