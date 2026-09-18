# Kickoff message for the main project

Paste the block for the phase you are starting. One phase at a time — the next one starts only after
the previous is in production.

---

## Phase 1 — paste this

> Sales CRM Restructure, Phase 1 of 5. Do not start any other phase.
>
> Read these first, in this order, from repo `chaithanin/agency-care2`, branch
> `claude/agency-care-test-project-zo163o`, folder `design/sales-crm-restructure/`:
>
> 1. `BRIEF.md` — the whole requirement
> 2. `WORK_ORDERS.md` → **Phase 1** — your actual scope, with the files and line numbers
> 3. `DEPLOY_IMPACT.md` — what happens in production and what a rollback does not undo
> 4. `../PROJECT_RULES.md` — this project's own rules
>
> Design canvas, 10 sheets: https://claude.ai/artifact/SNAd42xy9r3icnxvxFfHhf
> Start at `Main.dc.html`, then `Migration.dc.html`.
>
> **Scope:** merge Holding and Reservation into one funnel stage while keeping the two separable in
> every report, and add the Sold Deal conversion wizard on the existing `bookings` table.
>
> **Branch from `feat/all-appointments-clean-on-118a2e2`.** Never `feat/crm-modules-jul-2026`.
>
> **Five things that are not negotiable:**
>
> 1. Populate `sub_status` on every row **before** changing `status`. Reverse the order and the
>    information needed to undo it no longer exists anywhere.
> 2. `bucketForStage()` in `api/src/common/report-status-stage.ts` must take the sub status as well.
>    `ReportBucket` already lists `holding` and `reservation` as separate columns — if you do not
>    widen it, the Lead Status report silently collapses them and its numbers change with no error.
>    Four callers move with it; `WORK_ORDERS.md` lists them by line.
> 3. Do **not** create a `sold_deals` table. `bookings` is already the deal.
> 4. Add columns; never drop one or change what an existing one means. Keep every old route alive.
> 5. **Do not deploy.** Open the PR and stop.
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

## Phases 2 to 5 — same block, three lines changed

> Sales CRM Restructure, **Phase N of 5**. Phase N−1 is in production. Do not start any other phase.
>
> … same reading list …
>
> `WORK_ORDERS.md` → **Phase N** is your scope, and its "Impact on the existing system" section says
> what you must not disturb.
>
> … same non-negotiables, minus the two Phase 1 specifics (points 1 and 2) …

The per-phase scope, the impact section and the "Done when" checklist all live in `WORK_ORDERS.md`,
so the kickoff message never needs to repeat them.

---

## If they ask a question you have not decided

Point them at `OPEN_DECISIONS.md`. Five questions are still open, each with a draft answer and a safe
default to build against. Nothing there blocks a phase.
