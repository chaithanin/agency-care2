# Work order for the main project — Sales CRM Restructure (Master UX/UI + Functional Architecture)

> Copy this whole page and hand it over as-is.

---

This requirement is **not a screen revision**. It restructures the sales system into
**four core domains** — Lead Management · Sold Deal Management · Agency Management · Visit Management

## The rule that governs everything here — disturb the existing workflow as little as possible

The owner was explicit: **change things in a way that affects the current workflow as little as possible.**
So this is an **extension of what exists**, not a parallel system. Four rules govern every page:

| Rule | Detail |
| --- | --- |
| **Add, never alter** | New columns and tables are fine. **Never drop a column or change what an existing one means.** |
| **Keep old routes alive** | A folded page redirects; it is not deleted. People have them bookmarked and `in_app_notifications` deep-links to them. |
| **Config before code** | Anything the config tables already handle (`deal_stages`) must not be hard-coded. |
| **One phase at a time** | Five phases, one PR each. A phase ships to production before the next one starts. |

**Every release step must be reversible.** If the design produces a step that cannot be undone, the design is wrong.

## Branch

Branch from **`feat/all-appointments-clean-on-118a2e2`** only.
**Do not use `feat/crm-modules-jul-2026`.**

```bash
git branch --show-current
```

## The design to follow

Design canvas, 10 sheets — https://claude.ai/artifact/SNAd42xy9r3icnxvxFfHhf

Source files: repo `chaithanin/agency-care2`,
branch `claude/agency-care-test-project-zo163o`, folder `design/sales-crm-restructure/`

Per-phase work orders, with the measured impact on the existing system: [`WORK_ORDERS.md`](./WORK_ORDERS.md)

Open decisions and their drafted defaults: [`OPEN_DECISIONS.md`](./OPEN_DECISIONS.md)

**Start with `Main.dc.html`, then read `Migration.dc.html` immediately after.** Those two sheets
carry the table of what already exists, the impact levels, and how to keep the impact small.

---

## What already exists in production — surveyed, do not rebuild it

Surveyed on `feat/all-appointments-clean-on-118a2e2`. More than half of what the requirement asks for is already there.

| Topic | Where it lives today | What to do |
| --- | --- | --- |
| Lead funnel / stage | `deal_stages` + `api/src/common/kanban-stages.ts` | The stage table is **editable from config**. Ten stages today: `open` · `first_follow_up` · `second_follow_up` · `third_follow_up` · `holding` · `fourth_follow_up` · `reserve` · `missed` · `completed` · `cancelled` |
| Sub Status | `bookings.report_status` · `customer_leads.report_status` | Already stores `holding / reservation / open / 1st–3rd follow up / missed` — **this is the Sub Status the requirement asks for** |
| Sold Deal | `bookings` | Already has `saleId` `closerId` `agencyId` `agencyStaffId` `sellingPrice` `commissionPct` `cashback` `bookingNo`. **Do not create a new `sold_deals` table.** |
| Quota | `bookings.quota_category` | Live values already in use: Thai Quota · Thai Company · Foreign Quota · Sub-Ing-Sis · Lease-hold — **the Quota question is answered: it is Ownership Quota** |
| Central visit record | `office_visits` | Already has `leadId` `agencyId` `saleIds` `photos` `discussionTopics` `nextAction` `nextVisitDate` and soft delete. New columns only. |
| Planned agency visits | `visit_plans` + `visit_checkins` + `visit_reports` | Field-sales visits with GPS check-in — **a different thing from `office_visits`, do not merge them.** The Visit list reads both sources. |
| Task / reminder engine | `tasks` | Already has `dealId` `agencyId` `visitPlanId` `assigneeIds` `dueDate` recurring `report` — **this is the central task engine the requirement asks for** |
| Activity timeline | `deal_timeline` (`entity` + `entityId` + `type` + actor) | Already a shared timeline for any entity. **Nothing new needed.** |
| Audit | `audit_logs` (`metadata` = before / after / changes) | Already supports the field-change history |
| Payment plan master | `projects.payment_plan` is **one long free-text field** | Not enough — needs a master table plus a per-deal snapshot. Keep the existing field; do not delete it. |
| Customer payment schedule | **Does not exist.** `agency_deposits` is agency-side deposit money, a different thing | All new, but the shape of `deposit_transactions` is a good model to copy |
| Per-deal commission | `agency_commissions` is a monthly total per agency | Not tied to a deal — needs a new table. **Keep the existing one untouched.** |

---

## Six business questions to lock before the database is touched

All six are settled. Five came from what is already in production; the commission basis was decided by the owner.

| # | Question | Proposed answer | State |
| --- | --- | --- | --- |
| 1 | When is a Sold Deal created? | An authorised approver confirms the sale **and** the mandatory fields are complete — **not** the deposit alone | Answer proposed |
| 2 | Is Deposit a condition or a status? | A **status** on one row of the payment schedule | Answer proposed |
| 3 | What is commission calculated on? | **Net Price = Sale Price − Discount − Promotion value**, no tax deducted. `basis` is still per entry, because the agency rate runs on Sale Price. | **Answered by the owner** |
| 4 | What does Quota mean? | **Answered: Ownership Quota.** Use the live values in `bookings.quota_category` | Answer proposed |
| 5 | One visit record or several? | `office_visits` is the source of truth; `visit_plans` stays | Answer proposed |
| 6 | Where does Agency Last Visit come from? | `MAX(office_visits.visit_at, visit_checkins.checkin_at)` — **computed, never entered** | Answer proposed |

**All three phases are unblocked.** Question 3 is answered, so Phase 3 can be planned alongside Phases 1 and 2.

---

## Build order — set by the owner, do not reorder

```
1 Business Rule → 2 Data Model → 3 Workflow / State Model → 4 Information Architecture
→ 5 Wireframe → 6 UI Design → 7 API → 8 Development → 9 Migration → 10 UAT
```

**Never start from Figma or the screens.** The owner's reason: starting from the front end means rebuilding several times over.

---

## Five phases — one PR each

| Phase | Scope | Impact | Watch out |
| --- | --- | --- | --- |
| **1** Core Sales Architecture | Merge Holding / Reservation + Sub Status · status-change history · conversion wizard · basic contract | Low | A stage added in config plus three columns. People see the board columns change; every row of data is still there. |
| **2** Financial | Payment plan master + snapshot · payment schedule · record payment · reminders | Medium | All new tables, nothing existing touched — but this is real money, so UAT with finance before it goes live. |
| **3** Commission | Per-deal entries · approval chain · payment tracking · new `promotion_value` column | Medium | `agency_commissions` stays as it is and the old reports keep working. |
| **4** Agency & Visit | New agency profile · central visit record · computed Last Visit · lightbox | Low | New columns on `office_visits`. `visit_plans` behaves exactly as before. |
| **5** Cleanup | Hide Follow-up Board · fold Site Visit / Visit Summary into views · regroup menu · reports | **High** | This is what people see every day, so it goes last — and every folded route needs a redirect. |

The whole set is far too large to review in one pass, and if it breaks nobody will know which phase broke it.

---

## 1 · Lead Management (Phase 1)

### Merging Holding / Reservation — done in config, not by renaming

Edit `api/src/common/kanban-stages.ts` — one file. Remove `holding` and `reserve` from the list and
add `holding_reservation`. That file is already the single source of truth for the board and for `sort_order`.

**Funnel stage is kept separate from sub status:**

```
Funnel Stage : holding_reservation
Sub Status   : holding | reservation
```

Inline migration inside `PrismaService.applyPendingMigrations()` — **the order matters**

```sql
-- 1) New columns only. Nothing existing is touched.
ALTER TABLE "bookings" ADD COLUMN IF NOT EXISTS "funnel_stage" TEXT;
ALTER TABLE "bookings" ADD COLUMN IF NOT EXISTS "sub_status"   TEXT;

-- 2) Fill them from the current status (idempotent, safe to re-run)
UPDATE "bookings" SET "funnel_stage" = 'holding_reservation', "sub_status" = 'holding'
  WHERE "status" = 'holding'   AND "funnel_stage" IS NULL;
UPDATE "bookings" SET "funnel_stage" = 'holding_reservation', "sub_status" = 'reservation'
  WHERE "status" = 'reserve'   AND "funnel_stage" IS NULL;
UPDATE "bookings" SET "funnel_stage" = "status" WHERE "funnel_stage" IS NULL;

-- 3) Only now move status onto the new stage. Always after step 2.
UPDATE "bookings" SET "status" = 'holding_reservation'
  WHERE "status" IN ('holding','reserve');

-- 4) Retire the old stages. Do not delete them: old reports still join for the label.
UPDATE "deal_stages" SET "is_active" = false WHERE "key" IN ('holding','reserve');
```

> **`sub_status` must be fully populated before `status` is changed.** Reverse the two and there is no
> way to tell which rows were Holding and which were Reservation — and **no way to get it back**.

### Status-change history

New table `lead_status_history` holding `old_stage` `old_sub_status` `new_stage` `new_sub_status`
`changed_at` `changed_by` `reason` — **insert only, never update a past row**.

### Screens

- **Pipeline view** — Holding and Reservation share one column, but the split (`Holding 14 · Reservation 8`)
  is shown under the heading and every card carries a sub-status pill
- **Cards** carry only Customer · Project · Sales Owner · Lead Age · Next Follow-up · Sub Status ·
  Last Activity — **do not pack every field onto the card**
- **Lead detail** — tabs Overview / Activities / Visits / Documents, with the activity timeline on the right
- **Change status modal** — choosing Reservation makes these mandatory: Unit · Reservation Date ·
  Reservation Amount · Reservation Expiry · Payment Plan

---

## 2 · Sold Deal (Phase 1)

**Use the existing `bookings` table. Do not create `sold_deals`** — `bookings` is already the deal.

### Five-step conversion wizard

A sale is created one way only, through the wizard. **Never let someone change a dropdown from
Reservation to Sold and be done.**

1. **Customer & Unit** — carried over from the lead. A unit held by another deal is blocked **on the server**.
2. **Sales Information** — Lead Source is Direct or Agency
   - Direct → Agency / Agent **disabled and cleared**
   - Agency → Agency / Agent required
   - **Agent options are filtered by the selected agency.** Cross-agency selection is rejected on the server.
   - FR-037 / FR-038 become **conditionally required**, not required at all times
3. **Contract** — Contract Date · Contract No. · **Quota (reuse the values in `quota_category`)** ·
   Special Request · contract attachment
4. **Payment Plan** — select from the master, **then copy a snapshot**
5. **Review** — Create Sold Deal does all of it in **one transaction**: build the payment schedule from
   the snapshot, set the unit to sold, write the timeline entry, create the first payment task.
   **If any part fails, the whole thing rolls back.**

The deal number continues the existing `bookingNo` sequence. **Do not start a second counter.**

### Five statuses that must stay separate — never one field with twenty values

| Status | Values |
| --- | --- |
| Deal Status | Draft → Confirmed → Contracted → Payment In Progress → Transfer Pending → Completed (+ Cancelled) |
| Payment Status | Unpaid → Partially Paid → Paid (+ Refunded) — **computed from the schedule, nobody sets it** |
| Contract Status | Unsigned → Signed |
| Commission Status | Calculated → Pending Approval → Approved → Paid (+ Rejected) — **per entry** |
| Transfer Status | Not Ready → Transfer Pending → Completed |

**Never make the funnel carry two stages called Sold and Sold Completed** — that mixes the sale with the fulfilment.

### Error UX

Never show "Something went wrong" — say what is missing and give a way to go and fix it.
The form has thirty fields, so it needs **Save as Draft + autosave**, and **a draft must not count as a sale**.

---

## 3 · Payment (Phase 2)

All new tables. **Nothing existing is touched.**

| Table | Purpose | Constraint |
| --- | --- | --- |
| `payment_plan_masters` | Payment plan per project | Keyed to `project_id` |
| `payment_plan_master_items` | Milestones in a plan | Order + due-date formula |
| `deal_payment_plan_snapshots` | The plan as it stood when the deal was created | **Write once, never edit** |
| `deal_payment_schedules` | Milestones on a deal | `@@unique(deal_id, seq)` |
| `deal_payment_transactions` | Each individual payment | **Insert only, never update a total** |

- The requirement calls this Deposit Tracking, but **the deposit must not be a separate one-off record** —
  it is one row in the schedule, exactly like Booking · Contract · Installment · Transfer
- **The paid amount is the sum of the transactions.** Never UPDATE a total directly.
- **Never hard-delete** — reverse it with a new row marked Reversed
- Every row's status is computed from what was paid against what is due and when.
  **Never store it as a column for someone to change.**
- **Snapshot the payment plan** — when marketing edits the master in six months, an existing customer's
  contract must not follow it
- The existing `projects.payment_plan` free text **stays exactly as it is**, as reference

### Record Payment — validate all of these on the server

- The new payment must be greater than zero
- The total must not exceed the amount due, unless overpayment is enabled
- The payment date must not be in the future
- The receipt goes to the private bucket through `savePrivate()` only

### Payment reminders — created as tasks, not a separate board

7 days before · 3 days before · on the due date · overdue +1 day → rows in the existing `tasks` table.
**This is why the Follow-up Board can be removed without losing any capability.**

A reminder must never fire twice. Enforce it with **a unique key in the database**
(schedule row + reminder kind + date), not with a check in code.

---

## 4 · Commission (Phase 3)

New tables `deal_commissions` + `deal_commission_events`. **`agency_commissions` stays untouched.**

One deal can carry several entries: Seller · Closer · Agency · Agent · Referral

### Net Price — decided by the owner

```
Net Price = Sale Price − Discount − Promotion value
```

**Tax is not deducted.** The owner named discount and promotion only. If VAT or withholding should
come out of the basis, say so before this phase is coded.

`basis` is still recorded per entry, because not every entry runs on Net Price:

| Entry | Basis | Example |
| --- | --- | --- |
| Agency | Sale Price | 3,500,000 · 3% = **105,000** |
| Seller | Net Price | 3,350,000 · 1% = **33,500** |
| Closer | Net Price | 3,350,000 · 1% = **33,500** |
| Agent | Agency commission | 105,000 · 20% = **21,000** |

Worked from Sale Price 3,500,000 − discount 50,000 − promotion value 100,000 = **Net Price 3,350,000**.

#### The formula needs one new column

| Field | Today | Action |
| --- | --- | --- |
| `bookings.selling_price` | Float — the sale price | Use as is |
| `bookings.discount` | Float, **already a baht amount** | Use as is |
| `bookings.promotion` | **String — free text, carries no number** | Keep it, do not touch it |
| `bookings.promotion_value` | **Does not exist** | **Add: Float, nullable** |

`discount` can be trusted as an amount rather than a percentage: `deals.service.ts` already computes
`value = sellingPrice − discount` in five places, so the deal value shown on the board is that
subtraction today. The meaning is settled — do not reinterpret it.

`promotion` stays exactly as it is, per the add-never-alter rule. The number goes in the new column.

#### Promotion value is a breakdown, not one number

The owner's rule: **cashback and cash bonus both count, depending on the promotion's conditions.**
So the deal must record which components went in and which did not — never a single opaque figure.

| Component | Source | THB | In basis? | Why |
| --- | --- | --- | --- | --- |
| Cashback | `bookings.cashback` | 60,000 | **yes** | Reduces what the customer effectively pays |
| Cash bonus | `bookings.cash_bonus` | 40,000 | **yes** | Same — money back to the customer |
| Additional-commission promo | promotion master | 30,000 | **no** | Adds commission, does not cut the price |
| **`promotion_value`** | **sum of the included lines** | **100,000** | | |

**A promotion of type `additional_commission` or `fixed_commission` must never reduce the basis.**
It changes the commission itself; deducting it as well pays the same benefit out twice.

#### The condition must be a flag, not free text

`Promotion.cashBonusCondition` is `@db.Text` today. No code can decide from prose, so the promotion
master needs an explicit flag.

| `promotion_type` | `reduces_commission_basis` |
| --- | --- |
| `cash_back` · `cash_bonus` | true |
| `discount` · `free_gift` | true |
| `additional_commission` | false |
| `fixed_commission` | false |
| `marketing_support` · `special_unit` · `custom` | **null — ask once** |

**`null` means nobody has decided yet, not false.** The wizard asks once, records who answered, and
stores the answer on the deal. Treating null as false would quietly inflate every basis.

**`promotion_value` is a snapshot**, exactly like the payment plan. Never recompute it from
`cashback` at read time — if someone edits `cashback` later, re-derive it explicitly and write an
audit entry.

#### Migration — additive only

```sql
ALTER TABLE "bookings"           ADD COLUMN IF NOT EXISTS "promotion_value" DOUBLE PRECISION;
ALTER TABLE "bookings"           ADD COLUMN IF NOT EXISTS "promotion_value_items" JSONB;
ALTER TABLE "promotions"         ADD COLUMN IF NOT EXISTS "reduces_commission_basis" BOOLEAN;
ALTER TABLE "agency_promotions"  ADD COLUMN IF NOT EXISTS "reduces_commission_basis" BOOLEAN;

-- Seed the flag from the promotion type. Everything else stays null on purpose.
UPDATE "agency_promotions" SET "reduces_commission_basis" = true
  WHERE "promotion_type" IN ('cash_back','cash_bonus') AND "reduces_commission_basis" IS NULL;
UPDATE "agency_promotions" SET "reduces_commission_basis" = false
  WHERE "promotion_type" IN ('additional_commission','fixed_commission')
    AND "reduces_commission_basis" IS NULL;

-- Existing deals: 0 with an explicit marker, so nobody mistakes an assumption for a checked figure.
UPDATE "bookings"
   SET "promotion_value" = 0,
       "promotion_value_items" = '[{"source":"backfill","amount":0,"included":true,
                                    "reason":"assumed at migration, never reviewed"}]'::jsonb
 WHERE "promotion_value" IS NULL;
```

**A null `promotion_value` counts as 0, never as “skip the deal”.** The backfill marks which rows were
assumed, so nobody later reads an old deal as having had no promotion when in fact nobody checked.

```
Calculated → Pending Approval → Approved → Ready for Payment → Paid
                    ↘ Rejected
```

Plus On Hold and Cancelled, which real operations need.

- **Commission must never be a free-text field**, and `bookings.commission_pct` must not carry on as the
  single value per deal (keep the old column for compatibility; the real entries live in the new table)
- Commission is calculated when the **payment condition is met**, not the moment the deal is created.
  The threshold is config per project, never hard-coded.
- **Once approved, Sales cannot edit.** Block it in the API, not by disabling a button.
- Changing the sale price recalculates any commission **still unapproved**. Entries **already approved
  must not change by themselves** — issue an adjustment instead.
- Rounding: round to two decimals **per entry**, then sum — not sum then round.
- Every action writes all five to `audit_logs`: who · when · old value · new value · reason

---

## 5 · Agency & Visit (Phase 4)

### Agency

Tabs: Overview / Agents / Visits / Leads / Sold Deals / Activity.
**No separate tabs for Site Visit Report, Visit Summary or Follow-up.**

**Last Visit = `MAX(office_visits.visit_at, visit_checkins.checkin_at)` — computed, with no field to type it into.**

The existing `agencies` and `agency_staff` tables are complete. This phase reorganises the page.

### Visit — extending `office_visits` with new columns only

| New column | Why |
| --- | --- |
| `visit_type` | Separates Agency / Site / Customer / Other (today there is only `purpose`) |
| `project_id` | Today only `interested_projects` exists, which means something else |
| `unit_no` | A site visit needs the unit that was shown |
| `agency_staff_id` | Identifies the agent who was met |
| `feedback` | There is a `result` field, but it does not separate the other side's view |
| `booking_id` | Links the visit to a deal |

`photos` · `discussionTopics` · `nextAction` · `nextVisitDate` · soft delete already exist. **Nothing to add there.**

**`visit_plans` / `visit_checkins` / `visit_reports` are untouched** — planned field-sales visits are a
different thing. The Visit list simply reads both sources.

**Add Visit reveals fields by type** (progressive disclosure), and **a hidden field must also be cleared**.

**Photo lightbox** — ← → to move · ESC to close · zoom · caption · thumbnails · swipe on mobile ·
Download shown by permission and checked on the server.

> If `GCS_PRIVATE_BUCKET` is missing from a revision, the service writes files to the container disk and
> they are destroyed for good on the next deploy. **This already happened to Photo Evidence.**

---

## 6 · Cleanup (Phase 5) — the phase that affects people most

**Do it last**, and every item needs a way back.

| Existing thing | What happens | How the impact is reduced |
| --- | --- | --- |
| Kanban board `/deals` | Holding and Reservation become one column | Show the split under the heading, sub-status pill on every card |
| Reports grouped by `status` | `holding` / `reserve` disappear from new data | Group by `sub_status`, and backfill completely before the switch |
| Links like `?status=holding` | Return nothing | Translate old values in the API. **Keep it for at least two months.** |
| Follow-up Board `/workflow-board` | Removed from the menu | **Hide the menu entry only. The route stays and redirects to `/tasks`.** |
| `/site-visit-report` · `/visit-summary-report` | Folded into views | Both routes stay and point at Visits with a preset filter |
| Booking / Closed Deals / Deposit Tracking | **Untouched** | Sold Deal uses the existing `bookings` table, so all three keep working through every phase |
| `agency-mobile` | Check before switching | If the app reads `status` directly, keep an API that returns the old values until the app updates |

**Before hiding any menu entry, trace the route, the API, the permission, the widget on Home and the
deep links in `in_app_notifications`** — it is not just deleting a line from `Layout.tsx`.

Measured for the three folded routes (see [`WORK_ORDERS.md`](./WORK_ORDERS.md) Phase 5): no
notification link points at any of them. The two live traps are the `?employeeId=` query parameter
on the button in `EmployeeFilePage.tsx:168`, and `@Get('workflow-board')` in `visit.controller.ts:251`,
which is an API endpoint that merely shares the name with the page.

### New menu — regrouped into the four domains without changing a route

```
SALES        Leads (was Lead Status) · Sold Deals (was Closed Deals) · Payments (new) · Booking (unchanged)
AGENCY       Agencies · Agency Visits · Agency Performance
ACTIVITY     Visits (Site Visit + Visit Summary folded in) · Tasks & Reminders · Calendar
REPORTS      Sales · Payment · Commission · Agency · Visit
MASTER DATA  Projects · Units · Payment Plans · Promotions · Agencies · Users / Sales · Commission Rules
```

Almost all of it is a label and ordering change in `Layout.tsx`. **Every path stays the same**, so
permissions are unaffected, deep links keep working, and it reverts by reverting one file.

### Release order — every step reversible

| Step | What ships | How to roll it back |
| --- | --- | --- |
| 1 | New columns and the backfill, no screen changes | Stop using the columns |
| 2 | An API that accepts both old and new values | Revert the code; no data is lost |
| 3 | Switch the screens to the new values | Revert the screens — the API still accepts the old values |
| 4 | Retire the old stages in `deal_stages` | `UPDATE deal_stages SET is_active=true` |
| 5 | Clean up (after at least a month in real use) | Only once the logs show nobody sends old values |

---

## Dashboard · Permissions · Design System

- **The dashboard must answer operational questions** — Sales Funnel · Payment Attention ·
  Agency Follow-up · Conversion. **Every number must lead to the real records.**
- **Permission matrix** of seven roles as drawn, but **mapped onto the real roles**
  (`manager` `super_admin` `admin` `closer` `sales` `hr` `marketing` `staff` `read_only` `agency_user`).
  **No new values in the `UserRole` enum.**
- **Nobody can delete a deal or a financial record** — Void · Cancelled · Reversed, always
- Desktop-first 1440px · sidebar 240 · right panel 320–360 · spacing 4/8/12/16/24/32
- At most five tabs per page; use sections, not tabs, for content on the same page
- **Colour alone never carries meaning — every status needs a label**
- Shared components: Activity Timeline · Status Badge · Task Pill · Photo Pill + Lightbox ·
  Financial Summary · Filter Bar

---

## Project rules that apply

**Read [`design/PROJECT_RULES.md`](../PROJECT_RULES.md) in full before writing code** — it summarises
the main project's own `CONTRIBUTING.md` and `DEPLOYMENT.md`. In short:

| Rule | Detail |
| --- | --- |
| **UI is English only** | No hard-coded Thai in the UI or in reports |
| **`user.role`, not `activeRole`** | `CONTRIBUTING.md` states it directly · `@Roles()` takes enum values only · position-based rights go through `userGrants(...)` in the service |
| **`emitChange('<resource>')`** | Every mutation with a screen watching it must call this, or the page will not refresh |
| **Schema and migration ship together** | Inline SQL in `applyPendingMigrations()`. Schema alone gives an immediate 500. |
| **Files go through `StorageService`** | Never write to disk in production |
| **No non-ASCII file names** | They break the Docker build — keep them out via `.dockerignore` |

---

## Eight things a developer must not do — the owner's technical guardrails

1. Never merge Holding + Reservation by renaming a string and nothing else
2. Never relabel Closed Deal as Sold Deal and call the job done
3. Never build Deposit or Commission as free-text fields
4. Never make Visit Summary a second copy of the data
5. Never let Agency Last Visit be typed in by hand
6. Never delete history to solve a navigation problem
7. Never hard-delete a financial transaction
8. Never let an edit to the payment plan master change an existing deal

---

## Must pass before pushing (every PR)

**Read the "build checks" section of [`design/PROJECT_RULES.md`](../PROJECT_RULES.md) first.**

A local `nest build` uses an incremental cache and **will not surface errors** the Docker build catches.
A stale `.vite` produces an old bundle. **Clear the caches or the result means nothing.**

```bash
cd api && npx prisma validate
rm -rf api/dist api/tsconfig.tsbuildinfo && (cd api && npx nest build)
rm -rf web/dist web/node_modules/.vite && (cd web && npx vite build)
```

Count the menu entries in the built bundle. Every one must be greater than zero.

```bash
cd web && B=$(cat dist/assets/*.js)
for s in "Lead Status" "Closed Deals" "Registration Report" "Advertising Requests" \
         "LINE Checker" "Staff Calendar" "Social Media" "Call Log"; do
  printf '%-24s %s\n' "$s" "$(printf '%s' "$B" | grep -c "$s")"
done
```

### Prove before each switch

- [ ] Lead counts by `sub_status` before the move equal the counts after, **for every value**
- [ ] No row has `funnel_stage = 'holding_reservation'` with an empty `sub_status`
- [ ] Every report produces the same numbers as before, compared line by line
- [ ] A link bookmarked as `?status=holding` still opens and still finds data
- [ ] `/workflow-board` · `/site-visit-report` · `/visit-summary-report` still open, no 404
- [ ] The `?employeeId=` filter from `EmployeeFilePage` still works on the folded report
- [ ] `@Get('workflow-board')` in `visit.controller.ts` still exists and still responds
- [ ] `agency-mobile` calls the same API and still gets the same answer

### QA cases to write, including the failure paths

- A lead in Holding → migration completes → stage is `holding_reservation`, sub status is `holding`,
  and the old history is intact
- Converting a Reservation to a Sold Deal with mandatory fields missing → rejected **on the server**
- Selecting an agent from a different agency → rejected on the server
- An agency with 5 visits → opening the profile shows the newest visit date as Last Visit
- Due 500,000, paid 300,000 → outstanding 200,000, status Partially Paid
- Sale Price 3,500,000, rate 3% on Sale Price → commission 105,000
- Sale Price 3,500,000, discount 50,000, promotion value 100,000, rate 1% on Net Price →
  Net Price 3,350,000 and commission 33,500
- A deal with `promotion_value` null → treated as 0, and the commission still calculates
- A promotion of type `additional_commission` → **excluded** from the basis, not deducted
- A promotion whose `reduces_commission_basis` is null → the wizard asks; it is **never** assumed false
- Editing `cashback` after the deal exists → `promotion_value` does **not** move on its own;
  re-deriving it writes an audit entry
- A visit with 3 photos → clicking the photo pill opens the lightbox with all 3 reachable
- Recording a payment above the amount due → rejected
- Sales attempting to edit an approved commission → rejected at the API
- Deleting a deal or a financial record → no endpoint exists to call

## Deploying

**Read [`design/PROJECT_RULES.md`](../PROJECT_RULES.md) in full before deploying.**

```powershell
.\deploy.ps1
```

The script runs a secret preflight, then deploys a **canary at 0% traffic**.

1. **Warm it first.** Hit `https://canary---agency-care-oohrdxzlwq-df.a.run.app/api/health`
   about 40 times — migrations run in the background after startup, and a revision at 0% traffic
   will never run them if nobody calls it.
2. Confirm the migration ran — look for `tables ready` in the logs.
3. Only then switch traffic, **pinned to a specific revision**.

```bash
gcloud run services update-traffic agency-care --project gtg-crm-499607 \
  --region asia-east2 --to-revisions <REV>=100 --remove-tags canary
```

### Never use `--to-latest`

The header of `deploy.ps1` says so itself: *"Never use `update-traffic --to-latest` —
that is what let the wrong build take production."* It has already happened once, and eight menu
entries disappeared from the live site.

### Never assemble a `gcloud run deploy` command by hand

`--set-env-vars` and `--set-secrets` **replace the entire set**. Anything left out is lost.
That is how `GCS_PRIVATE_BUCKET` went missing once, and the uploaded files were destroyed for good.
`deploy.ps1` has a secret preflight — use it.

To change one variable use `--update-env-vars` / `--update-secrets` (merge, not replace).

### Instances must be min = max = 1

`max=1` because socket.io has no Redis adapter. `min=1` because the scheduled jobs are in-process
`@Cron` — at scale-to-zero the LINE reports simply never fire and nobody finds out.

## Deliverables

1. **One PR per phase**, five in total — not one PR for everything
2. Every PR branches from `feat/all-appointments-clean-on-118a2e2`
3. Every PR carries a table of **how many lines of existing files it touched**, plus all check results
4. A phase ships to production before the next one starts
5. **Do not deploy yet** — wait for the owner's go-ahead

## Still open for the owner

**These are drafted, not blocking.** Each one has a draft answer and a safe default in
[`OPEN_DECISIONS.md`](./OPEN_DECISIONS.md) — build the draft, and fill the decision in there when the
owner decides. Every default is the strict direction, so a later decision only relaxes a rule rather
than having to undo data.

| # | Question | Draft answer being built |
| --- | --- | --- |
| 1 | When does commission become calculable? | Down Payment fully paid, configurable per project |
| 2 | Is overpayment allowed? | No — the server rejects it |
| 3 | Can Sales see company-wide figures? | No — reuse the existing `visibleOr()` rule in `deals.service.ts` |
| 4 | Customer cancels after paying | No automatic refund; Finance enters a reversal by hand |
| 5 | The three promotion types left `null` | Ask once per promotion; nothing assumed |

### Decisions already recorded

- **Commission basis:** Net Price = Sale Price − Discount − Promotion value
- **Tax:** not deducted from the basis
- **Cashback and cash bonus:** both count toward promotion value, conditionally — resolved by the
  `reduces_commission_basis` flag, with the per-deal breakdown stored on the deal
- **Approach:** add columns, never alter existing ones
