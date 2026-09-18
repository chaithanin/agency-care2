# Ready-to-apply patches

One patch, six fixes, all from [`../CODE_AUDIT.md`](../CODE_AUDIT.md). They are the findings that need
no decision — every one is a filter that the rest of the project already applies, or a stale comment.

## Apply

```bash
git checkout feat/all-appointments-clean-on-118a2e2
git checkout -b fix/audit-safe-filters
git apply design/sales-crm-restructure/patches/0001-audit-safe-fixes.patch   # or: git apply < the file
```

The patch is against **`feat/all-appointments-clean-on-118a2e2` at `ba63900`**. If that branch has
moved, `git apply --3way` will still place all six; only the `report-status-stage.ts` hunk is likely
to need a look, because Phase 1 edits the same file.

## What is in it

| Finding | File | Change |
| --- | --- | --- |
| H1 | `api/src/home/home.service.ts` | Add `deletedAt: null, dataScope: { not: 'legacy' }` — the query had no `where` at all |
| H2 | `api/src/automation/automation.service.ts` | Give `bookingScope` the same base filter, so the funnel's deal count reconciles with the board |
| M1 | `api/src/report/report.service.ts` | Same two filters on the activity report's booking rows |
| L1 | `api/src/visit/visit-workflow.service.ts` | Same two filters on the KPI count |
| L3 | `api/prisma/schema.prisma` | `reportStatus` comment gains the three values the UI actually writes |
| L4 | `api/src/common/report-status-stage.ts` | Delete the dead `closed_deal` key |

17 insertions, 5 deletions, 6 files. No behaviour changes for correct data — these only stop deleted
and legacy rows being counted.

## How it was verified

Run on this exact patch, against a pristine checkout of `ba63900`:

| Check | Result |
| --- | --- |
| `git apply --check` on a pristine tree | applies cleanly |
| `prisma validate` | **valid** |
| `tsc --noEmit` error count, pristine | 844 |
| `tsc --noEmit` error count, patched | **844 — identical error set, diff is empty** |

The 844 are pre-existing and unrelated: the generated Prisma client is stale with respect to the
`agency_onboarding*` models, plus a `.spec.ts` file missing `@types/jest`. That is PR #9's territory,
not this patch's. **The point of the number is that the patch adds nothing to it.**

`tsc` cannot give a clean signal on this branch, so a count comparison is the honest check. Run the
full cache-cleared build from the brief before pushing anyway.

## What is deliberately NOT in it

| Finding | Why it is not patched |
| --- | --- |
| **H3** — the Kanban never updates unit status | This is Phase 1 scope, not a fix. The conversion wizard has to own it; there is no existing path to correct. |
| **M2** — `cancel()` returns a sold unit to `available` | Needs the cancellation policy that is still open in [`../OPEN_DECISIONS.md`](../OPEN_DECISIONS.md) §4. Patching it blind would encode a guess about money. |
| **M3** — deleting a lead orphans its deals and visits | Needs a decision: soft-delete leads like deals, or block the delete like agencies do. Both are defensible; neither is mine to pick. |
| **L2** — `genBookingNo()` is not concurrency-safe | Mechanical, but it changes how deal numbers are issued. Best done deliberately, with the `PrSequence` pattern, just before the Sold Deal wizard starts issuing them faster. |

## Suggested handling

Ship this as its own small PR **before Phase 1**, not folded into it. It touches six files that Phase 1
does not, it is easy to review on its own, and it makes the new dashboards reconcile with the board
from day one rather than inheriting three counting bugs.
