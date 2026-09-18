# Sales CRM Restructure — Master UX/UI + Functional Architecture

Design canvas: https://claude.ai/artifact/SNAd42xy9r3icnxvxFfHhf

Message to hand the main project: [`COMMAND.md`](./COMMAND.md) — paste one phase at a time.

The full requirement: [`BRIEF.md`](./BRIEF.md)

Per-phase work orders, with the measured impact on the existing system:
[`WORK_ORDERS.md`](./WORK_ORDERS.md)

What changes in production on deploy: [`DEPLOY_IMPACT.md`](./DEPLOY_IMPACT.md)

Bugs and data-linkage findings in the live system: [`CODE_AUDIT.md`](./CODE_AUDIT.md)

Open decisions, drafted with safe defaults: [`OPEN_DECISIONS.md`](./OPEN_DECISIONS.md)

This requirement restructures Agency Care's sales side into **four core domains**, with one
governing rule from the owner: **disturb the existing workflow as little as possible.**

**These are static mockups. The figures are illustrative, nothing is wired to an API, and no
production code was changed.**

## Sheets

| File | Topic |
| --- | --- |
| `Main.dc.html` | **Read first** — the four domains, what already exists, impact levels, build order, the 8 guardrails |
| `Migration.dc.html` | **Read second** — merging the stage in config, the impact table, regrouping the menu without changing routes, a reversible release order |
| `Lead.dc.html` | 1 · Lead Management — pipeline view, lead detail, change status |
| `Convert.dc.html` | 3 · Convert to Sold Deal — the five-step wizard |
| `Deal.dc.html` | 4 · Sold Deal — detail page, five separate statuses |
| `Payment.dc.html` | 5 · Payment — master + snapshot, schedule, record payment |
| `Commission.dc.html` | 6 · Commission — per-deal entries, workflow, approval |
| `Agency.dc.html` | 7 · Agency — new profile, computed Last Visit |
| `Visit.dc.html` | 8 · Visit — one visit record, conditional form, photo lightbox |
| `Dashboard.dc.html` | 9 · Dashboard, permission matrix, design system |

## The four rules that govern the whole set

| Rule | Detail |
| --- | --- |
| **Add, never alter** | New columns and tables are fine. Never drop one or change what it means. |
| **Keep old routes alive** | A folded page redirects; it is not deleted. |
| **Config before code** | Anything `deal_stages` already handles must not be hard-coded. |
| **One phase at a time** | Five phases, one PR each. |

Every release step must be reversible.

## Build order — do not reorder

```
Business Rule → Data Model → Workflow / State Model → Information Architecture
→ Wireframe → UI Design → API → Development → Migration → UAT
```

The owner's own instruction: never start from Figma or the screens.

## Already in production — surveyed, do not rebuild it

| Table / file | State |
| --- | --- |
| `deal_stages` + `api/src/common/kanban-stages.ts` | The funnel is **editable from config**. Merging Holding / Reservation is a one-file change. |
| `bookings` | **This is the sold deal.** Has closer, agency, agent, quota, commission_pct, bookingNo. Do not create `sold_deals`. |
| `bookings.quota_category` | Thai Quota · Thai Company · Foreign Quota · Sub-Ing-Sis · Lease-hold — **the Quota question is already answered** |
| `bookings.report_status` · `customer_leads.report_status` | Already holds the sub status the requirement asks for |
| `office_visits` | The central visit record. Photos, discussion topics, next action, soft delete all present. |
| `visit_plans` / `visit_checkins` / `visit_reports` | Planned field visits — **a different thing, do not merge** |
| `tasks` | The central task engine, with `dealId` and `assigneeIds` |
| `deal_timeline` | The shared activity timeline |
| `audit_logs` | Field change history |
| Payment schedule / per-deal commission | **Do not exist** — new tables, nothing existing touched |

## Eight things a developer must not do

1. Never merge Holding + Reservation by renaming a string and nothing else
2. Never relabel Closed Deal as Sold Deal and call the job done
3. Never build Deposit or Commission as free-text fields
4. Never make Visit Summary a second copy of the data
5. Never let Agency Last Visit be typed in by hand
6. Never delete history to solve a navigation problem
7. Never hard-delete a financial transaction
8. Never let an edit to the payment plan master change an existing deal

## Theme values taken from the real project

`web/src/theme/ThemeContext.tsx`, dark mode, from `chaithanin/agency-care`
branch `feat/all-appointments-clean-on-118a2e2` = revision **agency-care-00886-nus**

## Rebuilding the sheets

```bash
cd design/sales-crm-restructure
for i in 1 2 3 4 5 6 7 8 9; do python3 build_$i.py; done
```
