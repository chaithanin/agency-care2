# Deploy impact — what changes in production

Everything below was read out of `chaithanin/agency-care` on
`feat/all-appointments-clean-on-118a2e2`. It answers one question: **when a phase is deployed, what
actually changes in the running system, and how far back can it be taken?**

## The short answer

| | Phase 1 | Phase 2 | Phase 3 | Phase 4 | Phase 5 |
| --- | --- | --- | --- | --- | --- |
| Runs SQL against existing rows | **yes** | no | backfill only | no | **no SQL at all** |
| New tables | 1 | 5 | 2 | 0 | 0 |
| New columns on existing tables | 2 | 0 | 4 | 6 | 0 |
| New env vars or secrets | none | none | none | none | none |
| What users notice the next morning | board columns merge | a new page | a new tab | a new page | menu regrouped |
| **Revert by rolling back the container?** | **no — see below** | yes | yes | yes | yes |

**Only Phase 1 cannot be undone by a rollback.** Everything else is additive: roll the container
back and the new tables and columns simply stop being read.

---

## What actually runs on deploy

Migrations are inline, in `PrismaService.applyPendingMigrations()`, and `onModuleInit` starts them
**without awaiting**:

```ts
const migrationPromise = this.applyPendingMigrations().catch(...)   // not awaited
Promise.race([migrationPromise, timeoutPromise]).catch(...)         // 180s timeout
```

Three consequences that matter on the day:

1. **The container reports healthy before migrations finish.** There is a window where the new code
   is serving requests against a schema that is still being changed. Short for `ALTER TABLE … ADD
   COLUMN`, longer for Phase 1's row updates.
2. **A revision at 0% traffic may never run them.** Prisma connects lazily, on the first query. This
   is why the canary must be hit about 40 times and why `tables ready` has to appear in the log
   before traffic moves. Skipping the warm-up means the migration runs *after* the traffic switch,
   with real users on it.
3. **There is a 180-second ceiling.** If Phase 1's row update exceeds it on a large `bookings` table,
   the migration is abandoned with a logged error and the deploy still looks healthy. Count the rows
   first:

```sql
SELECT status, count(*) FROM bookings
 WHERE status IN ('holding','reserve') GROUP BY status;
```

If that is large, split Phase 1's data step out and run it on its own rather than at boot.

---

## Phase 1 — the only one that rewrites existing data

### What changes in the database

```sql
ALTER TABLE bookings ADD COLUMN funnel_stage TEXT;   -- additive
ALTER TABLE bookings ADD COLUMN sub_status   TEXT;   -- additive
UPDATE bookings SET status = 'holding_reservation'   -- destructive in place
  WHERE status IN ('holding','reserve');
UPDATE deal_stages SET is_active = false WHERE key IN ('holding','reserve');
```

### What users see change

- The board merges two columns into one. The split stays visible in the column heading and on every
  card as a sub-status pill.
- **Dragging a card onto the merged column now has to ask which sub status it is.** The old code
  inferred it from the column; after the merge it cannot. `deals.service.ts:1239` calls
  `reportStatusForStage(stage)` to sync the linked lead — that path must open the Change Status modal
  instead of guessing.
- The daily 08:05 digest (`deals.scheduler.ts`) derives its open stages from `deal_stages` at run
  time, so it follows the change on its own. **No action needed there** — worth knowing so nobody
  goes looking for it.

### Rolling the container back does not roll the data back

This is the part worth reading twice. After a rollback:

| | State |
| --- | --- |
| `bookings.status` | still `'holding_reservation'` — the container rollback does not touch rows |
| `deal_stages.holding` / `.reserve` | **re-activated automatically.** The old seed loop runs `ON CONFLICT … DO UPDATE SET is_active = true` for every key in its own list |
| `deal_stages.holding_reservation` | **stays active.** It is not in the old code's list, so nothing deactivates it |
| The Kanban board | **still works.** Columns come from the database (`dealStage.findMany`), so the merged column is still rendered with its deals in it |
| The Lead Status report | **silently undercounts.** `deals.service.ts:285` filters on `bucketForStage(d.status) !== null`, and the old `STAGE_TO_BUCKET` has no entry for `holding_reservation`, so every one of those deals drops out of the report while still showing on the board |
| CRM 360 bucket counts | same — `crm360.service.ts:165` drops them too |
| `sub_status`, `funnel_stage` | still there, ignored by the old code, harmless |

So the failure mode is **not a crash and not data loss — it is a report that quietly stops counting a
column's worth of deals.** That is harder to notice, which is why it is written down here.

### The recovery, and why it only works if the order was followed

```sql
UPDATE bookings
   SET status = CASE sub_status WHEN 'reservation' THEN 'reserve' ELSE 'holding' END
 WHERE status = 'holding_reservation';

UPDATE deal_stages SET is_active = true  WHERE key IN ('holding','reserve');
UPDATE deal_stages SET is_active = false WHERE key = 'holding_reservation';
```

**This is only possible because `sub_status` was populated before `status` was changed.** If the two
steps run in the other order, the information needed to write that `CASE` no longer exists anywhere.
That ordering rule is not style — it is the difference between a recoverable deploy and an
unrecoverable one.

Keep this snippet next to the deploy command for the Phase 1 release, and take a database backup
before the traffic switch.

---

## Phase 2 — new tables only

Five new tables. No existing column is read, written or altered.

| What | Effect on production |
| --- | --- |
| Existing `/deposits` page | Unchanged. It shows **agency** deposits, which are not customer payments. |
| `AgencyDeposit` / `DepositTransaction` | Untouched. Read by the `deposits`, `report`, `home`, `agency` and `dashboard` services — all keep working. |
| `bookings.deposit`, `bookings.bookingFee` | Left as they are. The Booking page still renders them. |
| Rollback | Roll the container back and the new tables stop being read. Nothing to undo. |

**Receipts go through `StorageService.savePrivate()`.** Confirm `GCS_PRIVATE_BUCKET` is present on the
revision **before** the traffic switch. If it is missing, files are written to the container disk and
destroyed on the next deploy — this already happened once to Photo Evidence.

---

## Phase 3 — four nullable columns and a backfill

```sql
ALTER TABLE bookings          ADD COLUMN promotion_value DOUBLE PRECISION;  -- nullable
ALTER TABLE bookings          ADD COLUMN promotion_value_items JSONB;       -- nullable
ALTER TABLE promotions        ADD COLUMN reduces_commission_basis BOOLEAN;  -- nullable
ALTER TABLE agency_promotions ADD COLUMN reduces_commission_basis BOOLEAN;  -- nullable
```

Plus a backfill that only ever writes rows where the column is `NULL`, so it is safe to re-run.

| What | Effect on production |
| --- | --- |
| `bookings.commissionPct` | Still stored, still rendered in `DealsPage`, `AgencyDetailPage` and `deals.service.ts`. Six references, three files — check all three, but nothing changes for users. |
| `agency_commissions` | Untouched. The monthly agency total and its reports keep working. |
| The Agency Promotion module | Only **read**. Its `cashBonus*` fields are untouched; one nullable flag is added beside them. |
| Rollback | Fully reversible. The old code never reads the new columns. |

**Nothing visibly changes for existing users in this phase.** The risk is arithmetic: a promotion
counted in the wrong direction changes what people are paid, with nothing on screen to signal it.
That is why the per-line breakdown is stored on the deal rather than a single figure.

---

## Phase 4 — six nullable columns on one table

`office_visits` gains `visit_type`, `project_id`, `unit_no`, `agency_staff_id`, `feedback`,
`booking_id`. All nullable.

| What | Effect on production |
| --- | --- |
| The other 26 files reading `office_visits` | Unaffected — nullable columns change no existing query |
| `visit_plans` / `visit_checkins` / `visit_reports` | Untouched. GPS check-in behaves exactly as today. |
| The combined Visit list | **This is the part that needs care.** It reads two sources with 267 references between them. The columns are safe; the aggregation is where numbers can drift. Compare its output against the existing pages before it replaces anything. |
| Rollback | Fully reversible. |

---

## Phase 5 — no database change at all

Routing and labels only. Nothing runs against the database.

| Where | Line | On deploy |
| --- | --- | --- |
| `web/src/App.tsx` | 194, 195, 229 | The three routes stay and redirect |
| `web/src/components/Layout.tsx` | 235, 236, 243 | Three menu entries hidden |
| `web/src/pages/EmployeeFilePage.tsx` | 168 | **Navigates to `/site-visit-report?employeeId=…`** — the folded view must keep the query parameter or this button silently shows the wrong person's visits |
| `api/src/visit/visit.controller.ts` | 251 | `@Get('workflow-board')` is an **API endpoint** sharing the page's name. Do not remove it with the page. |

Checked: no notification deep link points at any of the three folded routes — neither the stored
literals (`/agencies`, `/news`, `/notifications`, `/projects`, `/task`, `/tasks`) nor the ones built at
run time (`/customers/:id`, `/agencies/:id`, `/deals`, `/deals?owner=`).

**Rollback: revert `Layout.tsx` and `App.tsx`.** This is the phase people feel most and the one
easiest to take back.

---

## Deploy checklist per phase

Before the traffic switch, on every phase:

- [ ] `.\deploy.ps1` — canary at 0%, never a hand-built `gcloud run deploy`
- [ ] Warm the canary about 40 times; confirm `tables ready` in the log
- [ ] `min-instances = max-instances = 1` unchanged
- [ ] `GCS_PRIVATE_BUCKET` present on the revision (Phases 2 and 4 write files)
- [ ] Traffic switched **pinned to a revision**, never `--to-latest`

Phase 1 only, additionally:

- [ ] Row count taken before the deploy (`SELECT status, count(*) …`)
- [ ] Database backup taken before the traffic switch
- [ ] The recovery SQL above pasted somewhere to hand
- [ ] After the switch: the Lead Status report still shows Holding and Reservation as separate
      columns, with the same totals as the day before
