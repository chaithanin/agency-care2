# Kickoff messages for the main project — v2

Two things to hand over, **in this order**. Step 0 is a small PR that is already written and verified;
Phase 1 starts after it.

Everything below is against repo `chaithanin/agency-care2`, branch
`claude/agency-care-test-project-zo163o`, folder `design/sales-crm-restructure/`.

Design canvas, 10 sheets: https://claude.ai/artifact/SNAd42xy9r3icnxvxFfHhf

If the session cannot see that repo, [`FETCH.md`](./FETCH.md) has three tested ways to pull the
folder — the sparse clone is about 1 MB.

---

## Step 0 — paste this first

> A small fix PR, already written and verified. Do not fold it into anything else.
>
> Apply `design/sales-crm-restructure/patches/0001-audit-safe-fixes.patch` from repo
> `chaithanin/agency-care2`, branch `claude/agency-care-test-project-zo163o`, onto a new branch off
> `feat/all-appointments-clean-on-118a2e2`, and open it as its own PR.
>
> ```bash
> git checkout feat/all-appointments-clean-on-118a2e2
> git checkout -b fix/audit-safe-filters
> git apply design/sales-crm-restructure/patches/0001-audit-safe-fixes.patch
> ```
>
> Six files, 17 insertions, 5 deletions. Four queries were counting soft-deleted and legacy-imported
> deals; two are a stale comment and a dead key. Read `patches/README.md` first — it says what each
> fix is, how it was verified, and which audit findings were deliberately left out and why.
>
> It was verified against a pristine checkout of `ba63900`: `git apply --check` passes,
> `prisma validate` passes, and the `tsc --noEmit` error set is byte-identical to the unpatched tree
> at 844 errors. Those 844 are pre-existing — a stale generated Prisma client against the
> `agency_onboarding*` models, plus a spec file missing `@types/jest`. **Re-run the comparison rather
> than expecting zero.**
>
> Run the cache-cleared build from `BRIEF.md` before pushing anyway. **Do not deploy.**

---

## Phase 1 — paste this once Step 0 has merged

> Sales CRM Restructure, Phase 1 of 5. Do not start any other phase.
>
> Read these first, in this order, from repo `chaithanin/agency-care2`, branch
> `claude/agency-care-test-project-zo163o`, folder `design/sales-crm-restructure/`:
>
> 1. `BRIEF.md` — the whole requirement
> 2. `WORK_ORDERS.md` → **Phase 1** — your scope, with the files and line numbers
> 3. `CODE_AUDIT.md` **§4** — what the audit found that changes this phase's scope
> 4. `DEPLOY_IMPACT.md` — what happens in production, and what a rollback does **not** undo
> 5. `../PROJECT_RULES.md` — this project's own rules
>
> Design canvas: https://claude.ai/artifact/SNAd42xy9r3icnxvxFfHhf — start at `Main.dc.html`, then
> `Migration.dc.html`, then `Lead.dc.html`.
>
> **Scope:** merge Holding and Reservation into one funnel stage while keeping the two separable in
> every report, and add the Sold Deal conversion wizard on the existing `bookings` table.
>
> **Branch from `feat/all-appointments-clean-on-118a2e2`** (verified at `ba63900`).
> Never `feat/crm-modules-jul-2026`.
>
> **Six things that are not negotiable:**
>
> 1. Populate `sub_status` on every row **before** changing `status`. Reverse the order and the
>    information needed to undo it no longer exists anywhere. `DEPLOY_IMPACT.md` carries the recovery
>    SQL, and it only works if this order was followed.
> 2. `bucketForStage()` in `api/src/common/report-status-stage.ts` must take the sub status as well.
>    `ReportBucket` already lists `holding` and `reservation` as separate columns — if you do not
>    widen it, the Lead Status report silently collapses them and its numbers change with no error.
>    Six call sites move with it: `deals.service.ts` 245, 312, 1250, 1408 · `crm360.service.ts` 206,
>    242 · `customer-lead.service.ts:739` · `office-visit.service.ts:28`.
> 3. **The conversion wizard must set unit status itself.** `prisma.unit` appears **0 times** in
>    `deals.service.ts` — unit status is only maintained in the Booking module, and only when a
>    `unitId` was supplied. A deal driven to Closed Deals from `/deals` leaves its unit `available`
>    forever. This is new work inside Phase 1, not a refactor. See `CODE_AUDIT.md` H3.
> 4. Do **not** create a `sold_deals` table. `bookings` is already the deal.
> 5. Add columns; never drop one or change what an existing one means. Keep every old route alive.
> 6. **Do not deploy.** Open the PR and stop.
>
> **Keep the page looking like itself.** `Lead.dc.html` draws the real `/deals` page before and after.
> Three visual changes, nothing else moves: the two columns merge (keeping Reservation's colour and
> slot), two counters join the column header in the pill style `Won`/`Lost` already uses, and one chip
> joins the card's existing chip row. The toolbar, the left filter sidebar, the filter row, drag and
> drop, the orphan banner and the Table view are all untouched.
>
> One thing to confirm with the owner rather than decide: the merged column takes Reservation's slot,
> so Holding cards move one position right, past 4th Follow Up.
>
> Clear the build caches before you trust a build — a cached `nest build` hides errors Docker will
> catch, and a stale `.vite` gives you an old bundle:
>
> ```bash
> cd api && npx prisma validate
> rm -rf api/dist api/tsconfig.tsbuildinfo && (cd api && npx nest build)
> rm -rf web/dist web/node_modules/.vite && (cd web && npx vite build)
> ```
>
> In the PR, include a table of how many lines of existing files you touched, and the results of the
> "Done when" checklist in `WORK_ORDERS.md` Phase 1.

---

## Phases 2 to 5 — the same block, four lines changed

> Sales CRM Restructure, **Phase N of 5**. Phase N−1 is in production. Do not start any other phase.
>
> … same reading list …
>
> `WORK_ORDERS.md` → **Phase N** is your scope, and its "Impact on the existing system" section says
> what you must not disturb. `CODE_AUDIT.md` §4 says whether the audit changes this phase.
>
> … same non-negotiables, minus points 1, 2 and 3, which are Phase 1 only …

Before **Phase 2** starts, one decision must be made that is not in `OPEN_DECISIONS.md` because it is
architectural, not business: **`Booking` has no foreign keys at all** — all twelve id columns are bare
strings, by convention. `deal_payment_schedules` and `deal_commissions` would be the first tables with
a real FK to `bookings`. The recommendation in `CODE_AUDIT.md` §1 is to use real FKs on the new
financial tables and state it as a deliberate exception, because an orphaned payment row is worse than
an inconsistent convention.

---

## If they ask something that has not been decided

Point them at `OPEN_DECISIONS.md`. Five questions are still open, each with a draft answer and a safe
default to build against. Nothing there blocks a phase.

## What is deliberately not being handed over yet

`CODE_AUDIT.md` M2, M3 and L2 are real findings left unpatched on purpose: a cancelled *sold* unit and
deleting a lead both need a policy decision, and changing how deal numbers are issued is best done
just before the wizard starts issuing them faster. Do not let them be swept into a phase.
