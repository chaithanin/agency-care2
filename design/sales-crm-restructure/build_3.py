# -*- coding: utf-8 -*-
"""Migration.dc.html -- how to do this with the least possible disturbance"""
from tokens import *
from shell import *

W, H = 1660, 2180

before = f'''<div class="col" style="gap:8px;flex:1;min-width:0">
  <span class="cap mut">In production today — api/src/common/kanban-stages.ts</span>
  <div class="col" style="gap:6px;background:{SURFACE};border:1px solid {DIVIDER};
       border-radius:14px;padding:13px 15px">
    {"".join(f'<div class="row" style="gap:8px"><span class="cap mut" style="width:18px">{i+1}</span>'
             f'<span class="b2" style="color:{TXT2}">{s}</span></div>'
             for i, s in enumerate(["open · Open", "first_follow_up · 1st Follow Up",
               "second_follow_up · 2nd Follow Up", "third_follow_up · 3rd Follow Up",
               "<b style='color:#FBBF24'>holding · Holding</b>", "fourth_follow_up · 4th Follow Up",
               "<b style='color:#FBBF24'>reserve · Reservation</b>", "missed · Missed",
               "completed · Closed Deals", "cancelled · Cancelled"]))}
  </div>
</div>'''

after = f'''<div class="col" style="gap:8px;flex:1;min-width:0">
  <span class="cap mut">After — one file edited, no data rewritten</span>
  <div class="col" style="gap:6px;background:{SURFACE};border:1px solid {SUCCESS}55;
       border-radius:14px;padding:13px 15px">
    {"".join(f'<div class="row" style="gap:8px"><span class="cap mut" style="width:18px">{i+1}</span>'
             f'<span class="b2" style="color:{TXT2}">{s}</span></div>'
             for i, s in enumerate(["open · Open", "first_follow_up · 1st Follow Up",
               "second_follow_up · 2nd Follow Up", "third_follow_up · 3rd Follow Up",
               "fourth_follow_up · 4th Follow Up",
               "<b style='color:#22C55E'>holding_reservation · Holding / Reservation</b>",
               "missed · Missed", "completed · Closed Deals", "cancelled · Cancelled"]))}
  </div>
  <span class="cap mut">The keys <code>holding</code> and <code>reserve</code> stay in
  <code>deal_stages</code> with <code>is_active = false</code> — they no longer appear as columns
  but old rows still resolve their label.</span>
</div>'''

sql = f'''<div class="col" style="gap:9px">
  <span class="cap mut">Inline migration inside <code>PrismaService.applyPendingMigrations()</code>
  — additive, nothing overwritten</span>
  <pre style="margin:0;background:{SURFACE};border:1px solid {DIVIDER};border-radius:14px;
       padding:14px 16px;font-size:12.5px;line-height:1.7;color:{TXT2};overflow:auto"><code>-- 1) New columns only. Nothing existing is touched.
ALTER TABLE "bookings" ADD COLUMN IF NOT EXISTS "funnel_stage" TEXT;
ALTER TABLE "bookings" ADD COLUMN IF NOT EXISTS "sub_status"   TEXT;

-- 2) Fill them from the current status (idempotent, safe to re-run)
UPDATE "bookings" SET "funnel_stage" = 'holding_reservation', "sub_status" = 'holding'
  WHERE "status" = 'holding'   AND "funnel_stage" IS NULL;
UPDATE "bookings" SET "funnel_stage" = 'holding_reservation', "sub_status" = 'reservation'
  WHERE "status" = 'reserve'   AND "funnel_stage" IS NULL;
UPDATE "bookings" SET "funnel_stage" = "status"
  WHERE "funnel_stage" IS NULL;

-- 3) Only now move status onto the new stage. Always after step 2.
UPDATE "bookings" SET "status" = 'holding_reservation'
  WHERE "status" IN ('holding','reserve');

-- 4) Retire the old stages. Do not delete them: old reports still join for the label.
UPDATE "deal_stages" SET "is_active" = false WHERE "key" IN ('holding','reserve');</code></pre>
  {note_box("error", "The order matters. sub_status must be fully populated before status is changed. "
                     "Reverse the two and there is no way to tell which rows were Holding and which "
                     "were Reservation — and no way to get it back.")}
</div>'''

merge = panel("MERGING HOLDING + RESERVATION — done in config, not by renaming",
              body=(f'<div class="row" style="gap:18px;align-items:flex-start">{before}'
                    f'<div class="col" style="justify-content:center;padding-top:40px">{icon(I_ARROW,22,SUCCESS)}</div>'
                    f'{after}</div>' + sql),
              note="deal_stages is already an admin-editable table and kanban-stages.ts is already the single "
                   "source of truth for the board. So this is one file plus two columns, not a new funnel.",
              grow=False)

IMPACTS = [
 ("Kanban board /deals", "Holding and Reservation become one column", 2,
  "Show the split (Holding 14 · Reservation 8) under the heading and put a sub-status pill on every card. People see exactly what they saw before."),
 ("Reports grouped by status", "The values holding / reserve disappear from new data", 3,
  "Group by <code>sub_status</code> instead of <code>status</code>, and backfill sub_status completely before the switch."),
 ("Saved filters and bookmarked links", "<code>?status=holding</code> returns nothing", 2,
  "Translate holding → (holding_reservation, sub=holding) in the API. Keep the translation for at least two months."),
 ("Follow-up Board /workflow-board", "Removed from the menu", 2,
  "Hide the menu entry only. The route stays and redirects to /tasks — <b>do not delete the route</b>; it is bookmarked and notifications deep-link to it."),
 ("Site Visit Report / Visit Summary Report", "Folded into views over one visit record", 2,
  "Both routes stay and point at the Visits page with a preset filter. The numbers must match the old pages before the switch."),
 ("Booking / Closed Deals / Deposit Tracking", "Untouched", 0,
  "Sold Deal uses the existing bookings table, so all three pages behave exactly as before, through every phase."),
 ("visit_plans / GPS check-in", "Untouched", 0,
  "Planned field visits are a different thing from office_visits. The Visit list simply reads both sources."),
 ("agency_commissions", "Untouched", 0,
  "The monthly agency total keeps working and keeps reporting. Per-deal commission is a separate new table."),
 ("projects.payment_plan", "Untouched", 0,
  "The existing free text stays as reference. The payment plan master is a new table that lives alongside it."),
 ("Mobile app (agency-mobile)", "Check before switching", 2,
  "If the app reads status directly, keep an API version that still returns the old values until the app ships an update."),
]
irows = [(f'<b>{a}</b>', f'<span class="cap" style="color:{TXT2}">{b}</span>', impact_chip(c),
          f'<span class="cap mut">{d}</span>') for a, b, c, d in IMPACTS]
impact_panel = panel("IMPACT ON WHAT PEOPLE USE EVERY DAY — and how to keep it small",
                     body=table(["Existing thing", "What happens", "Level", "How the impact is reduced"], irows,
                                [230, 250, 150, None]),
                     note="Only one row is ●●●, and it is solved by backfilling completely before the switch.",
                     grow=False)

OLD_MENU = [
  ("Leads &amp; Customers", ["Lead Registration", "Registration Report", "Contacts"], None),
  ("Sales", ["Lead Status", "Closed Deals", "Booking", "Deposit Tracking"], None),
  ("Agencies", ["Agency List", "Agency Matrix", "Promotions", "Promotion Templates",
                "Agency Transfers", "Location Verification", "Onboarding"], None),
  ("Field Work", ["My Day", "Activity Plan", "Activity Calendar", "Assignments",
                  "Site Visit Report", "Visit Summary Report"], None),
  ("Tasks &amp; Documents", ["Task", "…", "Follow-up Board", "…"], None),
]
NEW_MENU = [
  ("SALES", ["Leads <span style='color:#6B7280'>(was Lead Status)</span>",
             "Sold Deals <span style='color:#6B7280'>(was Closed Deals)</span>",
             "Payments <span style='color:#22C55E'>(new)</span>",
             "Booking <span style='color:#6B7280'>(unchanged)</span>"], SUCCESS),
  ("AGENCY", ["Agencies", "Agency Visits", "Agency Performance",
              "<span style='color:#6B7280'>remaining entries move to Master Data</span>"], SECOND),
  ("ACTIVITY", ["Visits <span style='color:#22C55E'>(Site Visit + Visit Summary folded in)</span>",
                "Tasks &amp; Reminders <span style='color:#22C55E'>(takes over the Follow-up Board)</span>",
                "Calendar"], WARNING),
  ("REPORTS", ["Sales · Payment · Commission · Agency · Visit"], PRIMARY_L),
  ("MASTER DATA", ["Projects · Units · Payment Plans · Promotions",
                   "Agencies · Users / Sales · Commission Rules"], INFO),
]
def menu_col(title, groups, dim=False):
    out = []
    for g, items, c in groups:
        li = "".join(f'<div class="row" style="gap:7px;padding-left:12px">'
                     f'<span style="color:{TXT3}">·</span>'
                     f'<span class="cap" style="color:{TXT3 if dim else TXT2}">{i}</span></div>'
                     for i in items)
        out.append(f'<div class="col" style="gap:4px"><span class="sec" '
                   f'style="color:{TXT3 if dim else (c or TXT2)}">{g}</span>{li}</div>')
    return (f'<div class="col" style="gap:13px;flex:1;min-width:0;background:{SURFACE};'
            f'border:1px solid {DIVIDER};border-radius:14px;padding:14px 16px">{"".join(out)}</div>')

menu_panel = panel("MENU — regrouped into the four domains without changing a single route",
  body=(f'''<div class="row" style="gap:16px;align-items:flex-start">
    <div class="col grow" style="gap:8px;min-width:0"><span class="cap mut">Today</span>{menu_col("", OLD_MENU, dim=True)}</div>
    <div class="col" style="justify-content:center;padding-top:60px">{icon(I_ARROW,22,SUCCESS)}</div>
    <div class="col grow" style="gap:8px;min-width:0"><span class="cap mut">Proposed</span>{menu_col("", NEW_MENU)}</div>
  </div>''' +
  note_box("ok", "Almost all of this is a label and ordering change in Layout.tsx. Every path stays the same, "
                 "so permissions are unaffected, notification deep links keep working, and the whole thing "
                 "reverts by reverting one file.")),
  note="Before any menu entry is hidden, trace the route, the API, the permission, the widget on Home and the "
       "deep links in in_app_notifications — it is not just deleting a line from Layout.tsx.",
  grow=False)

ROLL = [
 ("1", "Ship the new columns and the backfill, with no screen changes",
  "Everything behaves as before; there is just more data in the database", "Stop using the columns"),
 ("2", "Ship an API that accepts both the old and the new values",
  "Old and new callers both work", "Revert the code; no data is lost"),
 ("3", "Switch the screens over to the new values",
  "People start seeing the merged column", "Revert the screens immediately — the API still accepts the old values"),
 ("4", "Retire the old stages in deal_stages",
  "The old columns leave the board", "<code>UPDATE deal_stages SET is_active=true</code>"),
 ("5", "Clean up — after at least a month in real use",
  "The old-value support code is removed", "Only once the logs show nobody is sending old values"),
]
rrows = [(f'<b>{a}</b>', b, f'<span class="cap mut">{c}</span>',
          f'<span class="cap" style="color:{SUCCESS}">{d}</span>') for a, b, c, d in ROLL]
roll_panel = panel("RELEASE ORDER — every step reversible",
  body=table(["Step", "What ships", "What people see", "How to roll it back"], rrows, [60, 340, 300, None]),
  note="No step is one-way. If the design produces a step that cannot be undone, the design is wrong.",
  grow=False)

checks = panel("PROVE BEFORE EACH SWITCH",
  body="".join(check(x) for x in [
    "Lead counts by sub_status before the move equal the counts after, for every value",
    "No row has funnel_stage = holding_reservation with an empty sub_status",
    "Every report produces the same numbers as before, compared line by line",
    "A link bookmarked as ?status=holding still opens and still finds data",
    "/workflow-board, /site-visit-report and /visit-summary-report still open, no 404",
    "Deep links in in_app_notifications that point at folded pages still land correctly",
    "agency-mobile calls the same API and still gets the same answer",
  ]), grow=False)

body = f'''<div class="col" style="gap:16px">
  {note_box("ok", "This sheet is the answer to “disturb the existing workflow as little as possible”. "
                  "Every choice here is reversible, and none of them forces anyone to change how they "
                  "work partway through.")}
  {merge}
  {impact_panel}
  {menu_panel}
  <div class="row" style="gap:16px;align-items:stretch">
    <div class="col grow" style="gap:0;min-width:0">{roll_panel}</div>
    <div class="col" style="gap:0;width:420px;flex-shrink:0">{checks}</div>
  </div>
</div>'''

open("Migration.dc.html", "w", encoding="utf-8").write(sheet(
    "2 · Migration — least possible disturbance",
    "Merge the stage in config · impact table · regroup the menu without changing routes · a reversible release order",
    body, W, H, badge="Read with Main"))
print("Migration.dc.html")
