# Work orders — one per phase

Five self-contained orders. **Hand over one at a time**, and only start the next once the previous
one is in production.

Every order assumes the main project has already read [`BRIEF.md`](./BRIEF.md),
[`OPEN_DECISIONS.md`](./OPEN_DECISIONS.md) and [`../PROJECT_RULES.md`](../PROJECT_RULES.md).

Common to all five:

- Branch from **`feat/all-appointments-clean-on-118a2e2`**. Never `feat/crm-modules-jul-2026`.
- Design canvas: https://claude.ai/artifact/SNAd42xy9r3icnxvxFfHhf
- Add columns, never alter existing ones. Keep every old route alive.
- Clear the build caches before trusting a build.
- **Do not deploy.** Open the PR and wait.
- Deploy-time effects and rollback limits per phase: [`DEPLOY_IMPACT.md`](./DEPLOY_IMPACT.md)

---

## Impact on the existing system — measured, not estimated

Every figure below comes from a grep over `feat/all-appointments-clean-on-118a2e2`.
**Re-run the counts before starting a phase** — if they have moved, the branch has moved.

| Phase | Schema risk | Read surface | The thing that can break quietly |
| --- | --- | --- | --- |
| 1 Core Sales | **Medium** — two columns plus a value remap on `bookings.status` | 21 × `'holding'`, 15 × `'reserve'` across 18 files | `bucketForStage()` collapsing two report columns into one |
| 2 Financial | **None** — all new tables | `AgencyDeposit` read by 6 services | Confusing customer payments with the existing agency deposits |
| 3 Commission | **Low** — 4 new nullable columns | `commissionPct` only 6 refs in 3 files; `cash_bonus` 105 refs, nearly all in the promotion module | Double-counting a promotion that is already an extra commission |
| 4 Agency & Visit | **Low** — 6 new nullable columns | `office_visits` 154 refs in 26 files; `visit_plans` 113 refs in 16 files | A wide read surface: the columns are safe, the aggregation is not |
| 5 Cleanup | **None** — no schema change | 3 routes, 3 menu entries, 1 in-app button | A button in `EmployeeFilePage` that carries a query param |

**Only Phase 1 rewrites existing values.** Phases 2 and 5 touch no schema at all. Phases 3 and 4 add
nullable columns and nothing else.

---

## Phase 1 — Core Sales Architecture

> Copy from here.

Merge Holding and Reservation into one funnel stage while keeping the two separable in every report,
and add the Sold Deal conversion wizard. Sheets: `Main.dc.html`, `Migration.dc.html`, `Lead.dc.html`,
`Convert.dc.html`, `Deal.dc.html`.

**Read `Migration.dc.html` before touching anything.** It has the measured blast radius and the one
change that can silently break a report.

### Impact on the existing system — the hinge file

`api/src/common/report-status-stage.ts` already translates between stage and sub status in both
directions. That is why this merge is small — and it is also where it can go wrong.

```
RS_TO_STAGE            holding → holding_reservation, reservation → holding_reservation
STAGE_TO_BUCKET        holding_reservation → needs the sub status to pick a column
STAGE_TO_REPORT_STATUS holding_reservation → cannot resolve without the sub status
```

`bucketForStage(stage)` must become `bucketForStage(stage, subStatus)`. The `ReportBucket` type
already lists `'holding'` and `'reservation'` as **separate columns** — if the signature is not
widened, both collapse into one and the Lead Status report quietly changes its numbers with no error
anywhere.

Callers to update with it:

| File | Line | What it does |
| --- | --- | --- |
| `api/src/deals/deals.service.ts` | 285, 347 | Board filter and the Lead Status report columns |
| `api/src/deals/deals.service.ts` | 1239 | Syncs the lead's status when a card is dragged |
| `api/src/deals/deals.service.ts` | 1376 | Maps a chosen report status back to a stage |
| `api/src/crm360/crm360.service.ts` | 165 | Counts deals into report buckets |
| `api/src/customer-lead/customer-lead.service.ts` | 723 | Status change from the lead side |
| `api/src/office-visit/office-visit.service.ts` | 28 | Status change from a visit |

### Schema — additive, and the order matters

```sql
ALTER TABLE "bookings" ADD COLUMN IF NOT EXISTS "funnel_stage" TEXT;
ALTER TABLE "bookings" ADD COLUMN IF NOT EXISTS "sub_status"   TEXT;

UPDATE "bookings" SET "funnel_stage" = 'holding_reservation', "sub_status" = 'holding'
  WHERE "status" = 'holding'   AND "funnel_stage" IS NULL;
UPDATE "bookings" SET "funnel_stage" = 'holding_reservation', "sub_status" = 'reservation'
  WHERE "status" = 'reserve'   AND "funnel_stage" IS NULL;
UPDATE "bookings" SET "funnel_stage" = "status" WHERE "funnel_stage" IS NULL;

UPDATE "bookings" SET "status" = 'holding_reservation'
  WHERE "status" IN ('holding','reserve');

UPDATE "deal_stages" SET "is_active" = false WHERE "key" IN ('holding','reserve');
```

**Populate `sub_status` completely before changing `status`.** Reverse the two and there is no way to
tell which rows were Holding and which were Reservation, and no way to get it back.

Plus `lead_status_history` (`old_stage`, `old_sub_status`, `new_stage`, `new_sub_status`,
`changed_at`, `changed_by`, `reason`) — **insert only, never update a past row**.

### Also in this phase

- `api/src/common/kanban-stages.ts` — replace the two entries with `holding_reservation`
- Board column shows the split (`Holding 14 · Reservation 8`); every card carries a sub-status pill
- **Dropping a card onto the merged column opens the Change Status modal and asks for the sub status.**
  It must never pick one silently.
- Sold Deal conversion wizard, five steps, on the existing `bookings` table —
  **do not create a `sold_deals` table**
- Agent options filtered by the selected agency, enforced on the server
- Direct lead source disables **and clears** Agency and Agent
- Create Sold Deal runs in one transaction; if any part fails the whole thing rolls back

### Done when

- [ ] Lead counts by `sub_status` before the move equal the counts after, for every value
- [ ] No row has `funnel_stage = 'holding_reservation'` with an empty `sub_status`
- [ ] The Lead Status report still shows Holding and Reservation as separate columns, with the same
      numbers as before
- [ ] A link bookmarked as `?status=holding` still opens and still finds data
- [ ] Converting with mandatory fields missing is rejected on the server
- [ ] Selecting an agent from another agency is rejected on the server
- [ ] `agency-mobile` calls the same API and gets the same answer

> Copy to here.

---

## Phase 2 — Financial

> Starts only once Phase 1 is in production.

Payment plan master with a per-deal snapshot, the payment schedule, recording payments, and reminders
as tasks. Sheet: `Payment.dc.html`.

All new tables. **Nothing existing is touched.**

| Table | Constraint |
| --- | --- |
| `payment_plan_masters` | Keyed to `project_id` |
| `payment_plan_master_items` | Order + due-date formula |
| `deal_payment_plan_snapshots` | Write once, never edit |
| `deal_payment_schedules` | `@@unique(deal_id, seq)` |
| `deal_payment_transactions` | Insert only, never update a total |

- The deposit is **one row in the schedule**, not a separate record
- The paid amount is the **sum of the transactions** — never UPDATE a total
- Never hard-delete; reverse with a new row marked Reversed
- Row status is computed from amounts and dates, never a column someone sets
- Reminders create rows in the existing `tasks` table — 7 days before, 3 days before, on the due
  date, overdue +1
- A reminder must never fire twice: **a unique key in the database**, not a check in code
- `projects.payment_plan` stays exactly as it is
- **Draft defaults from [`OPEN_DECISIONS.md`](./OPEN_DECISIONS.md): overpayment is rejected.**

### Impact on the existing system

**Schema risk: none.** Every table is new. No existing column is read, written or altered.

The one real hazard is conceptual, not technical:

| Existing thing | Refs | What must not happen |
| --- | --- | --- |
| `AgencyDeposit` + `DepositTransaction` | 9 refs across `deposits`, `report`, `home`, `agency`, `dashboard` services | These are **agency** deposits — money an agency places with the company. They are **not** customer payments. Do not extend them, do not read from them, do not merge the two. |
| Deposit Tracking page `/deposits` | menu + route | Keeps working untouched, showing agency deposits exactly as today |
| `bookings.deposit`, `bookings.bookingFee` | part of 42 `.deposit` refs | Leave them. They are the figures the Booking page shows today. The schedule is the new source of truth for what is actually owed and paid. |
| `projects.payment_plan` | 8 refs | Stays as reference text |

**Nothing existing changes behaviour in this phase.** If a current page renders differently after
Phase 2, something was touched that should not have been.

### Done when

- [ ] Due 500,000 and paid 300,000 gives outstanding 200,000 and status Partially Paid
- [ ] A payment above the amount due is rejected on the server
- [ ] A payment dated in the future is rejected
- [ ] Editing the master plan does not change any existing deal
- [ ] The same reminder cannot be written twice
- [ ] Receipts land in the private bucket via `savePrivate()`, never on container disk

---

## Phase 3 — Commission

> Starts only once Phase 2 is in production.

Per-deal commission entries, the approval chain, and payment tracking. Sheet: `Commission.dc.html`.

New tables `deal_commissions` and `deal_commission_events`. **`agency_commissions` stays untouched.**

### The basis — decided

```
Net Price = Sale Price − Discount − Promotion value
```

Tax is **not** deducted. `basis` is still recorded per entry: the agency rate runs on Sale Price, the
agent rate runs on the agency commission.

`bookings.discount` is already a baht amount — `deals.service.ts` computes `sellingPrice − discount`
in five places. Do not reinterpret it.

`bookings.promotion` is free text, so promotion value needs new columns:

```sql
ALTER TABLE "bookings"          ADD COLUMN IF NOT EXISTS "promotion_value" DOUBLE PRECISION;
ALTER TABLE "bookings"          ADD COLUMN IF NOT EXISTS "promotion_value_items" JSONB;
ALTER TABLE "promotions"        ADD COLUMN IF NOT EXISTS "reduces_commission_basis" BOOLEAN;
ALTER TABLE "agency_promotions" ADD COLUMN IF NOT EXISTS "reduces_commission_basis" BOOLEAN;
```

- Cashback and cash bonus **both count, conditionally** — the deal stores the per-line breakdown
- `additional_commission` and `fixed_commission` promotions **never** reduce the basis; they change
  the commission itself, and deducting them too pays the same benefit out twice
- `null` on the flag means **nobody has decided**, not false
- `promotion_value` is a **snapshot** — editing `cashback` later does not move it on its own
- Round to two decimals **per entry**, then sum
- Once approved, Sales cannot edit — blocked at the API
- **Draft default from [`OPEN_DECISIONS.md`](./OPEN_DECISIONS.md): entries stay in `Calculated` and
  do not advance on their own until the payment threshold is decided.**

### Impact on the existing system

**Schema risk: low.** Four new nullable columns. Nothing altered.

| Existing thing | Refs | Effect |
| --- | --- | --- |
| `bookings.commissionPct` | **6 refs in 3 files** (`deals.service.ts`, `DealsPage.tsx`, `AgencyDetailPage.tsx`) | Left in place and still rendered. New entries live in the new table. A small surface — but check all three before assuming it is unused. |
| `agency_commissions` | 9 refs | Untouched. The monthly agency total and its reports keep working. |
| `bookings.cashback` | 10 refs | Read-only input to the breakdown. Never rewritten by this phase. |
| `cash_bonus` | **105 refs**, nearly all in the Agency Promotion module (`cashBonusEnabled`, `cashBonusAmount`, `cashBonusCondition` …) | **The largest surface in this phase.** The promotion module owns these fields. Phase 3 only *reads* them and adds one flag beside them. |
| `Promotion.cashBonusCondition` | `@db.Text` | Stays. The new boolean flag sits next to it; the prose is not parsed and not migrated. |

**The risk here is arithmetic, not breakage.** Nothing visibly changes for existing users — but a
promotion counted in the wrong direction silently changes what people are paid. That is why the
per-line breakdown is stored on the deal instead of a single figure.

### Done when

- [ ] Sale Price 3,500,000 at 3% on Sale Price gives 105,000
- [ ] 3,500,000 − 50,000 − 100,000 at 1% on Net Price gives 33,500
- [ ] An `additional_commission` promotion is excluded from the basis
- [ ] A null `reduces_commission_basis` makes the wizard ask; it is never assumed false
- [ ] Changing the sale price recalculates unapproved entries only
- [ ] Every action writes who, when, old value, new value and reason to `audit_logs`

---

## Phase 4 — Agency & Visit

> Starts only once Phase 3 is in production.

New agency profile, the central visit record, computed Last Visit, and the photo lightbox.
Sheets: `Agency.dc.html`, `Visit.dc.html`.

New columns on `office_visits` only: `visit_type`, `project_id`, `unit_no`, `agency_staff_id`,
`feedback`, `booking_id`. `photos`, `discussionTopics`, `nextAction`, `nextVisitDate` and soft delete
already exist.

**`visit_plans` / `visit_checkins` / `visit_reports` are untouched.** The Visit list reads both
sources.

- Last Visit = `MAX(office_visits.visit_at, visit_checkins.checkin_at)`, **with no field to type into**
- Add Visit reveals fields by type, and a hidden field is **cleared**, not just hidden
- Lightbox: ← → , ESC, zoom, caption, thumbnails, swipe on mobile
- Download is checked on the server, not merely hidden
- File names ASCII only

### Impact on the existing system

**Schema risk: low** — six nullable columns on one table. **Read surface: wide.**

| Existing thing | Refs | Effect |
| --- | --- | --- |
| `office_visits` | **154 refs across 26 files** | The six new columns are nullable, so all 26 keep working unchanged. But this is the widest read surface in the whole project — any change to *how* visits are aggregated reaches a long way. Add columns; do not touch the existing queries. |
| `visit_plans` | **113 refs across 16 files** | Untouched. Planned field visits with GPS check-in keep behaving exactly as today. |
| `visit_checkins` | 8 refs | Read-only — Last Visit takes `MAX()` across this and `office_visits`. |
| `visit_reports` | 23 refs | Untouched. |

**Why the impact rating is split.** Adding the columns is genuinely low risk. Building the combined
Visit list on top of two sources with 267 references between them is not — that part deserves its own
review pass, and the numbers it produces must be compared against the existing pages before the
list replaces anything.

### Done when

- [ ] An agency with 5 visits shows the newest visit date as Last Visit
- [ ] There is no editable Last Visit field anywhere
- [ ] A visit with 3 photos opens the lightbox with all 3 reachable
- [ ] Switching visit type clears the fields it hides
- [ ] `visit_plans` behaves exactly as before
- [ ] `GCS_PRIVATE_BUCKET` is confirmed present before any traffic switch

---

## Phase 5 — Cleanup

> Starts only once Phase 4 is in production. **This is the one people feel.**

Fold the duplicate pages into views and regroup the menu. Sheets: `Migration.dc.html`,
`Dashboard.dc.html`.

- Follow-up Board: **hide the menu entry, keep the route, redirect to `/tasks`**
- `/site-visit-report` and `/visit-summary-report`: keep both routes, point them at Visits with a
  preset filter, and **prove the numbers match the old pages first**
- Regroup the menu into the four domains — **label and order only, every path unchanged**
- Reports

### Impact on the existing system

**Schema risk: none.** No database change at all. Everything here is routing and labels.

The surface is small and fully enumerated:

| Where | Line | What it is |
| --- | --- | --- |
| `web/src/App.tsx` | 194, 195, 229 | The three routes — **keep all three, redirect them** |
| `web/src/components/Layout.tsx` | 235, 236, 243 | The three menu entries — hide these |
| `web/src/pages/EmployeeFilePage.tsx` | 168 | **A button: `navigate('/site-visit-report?employeeId=' + emp.id)`** |
| `api/src/visit/visit.controller.ts` | 251 | `@Get('workflow-board')` — **an API endpoint, not the page** |

**Two traps, both easy to miss:**

1. **The `EmployeeFilePage` button carries a query parameter.** Folding Site Visit Report into a
   filtered Visits view must keep `?employeeId=` working, or that button lands on an unfiltered list
   and shows the wrong person's visits — with no error.
2. **`@Get('workflow-board')` in `visit.controller.ts` is an API endpoint that happens to share the
   name.** Removing the front-end page must not remove it, and searching for the string will hit both.

**Checked, and better than expected:** notification deep links do **not** point at any of the three
folded routes. The stored links are `/agencies`, `/news`, `/notifications`, `/projects`, `/task`,
`/tasks`; the ones built at runtime are `/customers/:id`, `/agencies/:id`, `/deals` and
`/deals?owner=`. Still worth re-checking before the switch, since links are written at runtime — but
this is not the risk it looked like.

> Separately noticed: one stored link is `/task` while the route is `/tasks`. Pre-existing, unrelated
> to this work, and worth a look on its own.


### Done when

- [ ] `/workflow-board`, `/site-visit-report` and `/visit-summary-report` all still open, no 404
- [ ] Deep links in `in_app_notifications` still land correctly
- [ ] The folded report pages produce the same numbers as the originals, compared line by line
- [ ] Every menu path is unchanged; only labels and order moved
- [ ] The whole phase reverts by reverting `Layout.tsx`
