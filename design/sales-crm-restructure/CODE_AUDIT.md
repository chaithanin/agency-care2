# Code audit — bugs and data linkage in the live system

Read against `chaithanin/agency-care`, branch `feat/all-appointments-clean-on-118a2e2`.
Every item below was verified in the source; none is inferred from the design.

Each finding says why it matters **for this restructure specifically**, because some of them decide
how Phase 1 and Phase 3 have to be built.

---

## 1 · The structural fact: there are no foreign keys

`Booking`, `CustomerLead`, `OfficeVisit`, `Unit` and `DealTimeline` declare **zero `@relation`
blocks**. Every link is a bare `String` column.

| Model | Id columns | `@relation` blocks |
| --- | --- | --- |
| `Booking` | 12 (`agencyId` `projectId` `saleId` `closerId` `leadId` `agencyStaffId` …) | **0** |
| `CustomerLead` | 7 | **0** |
| `OfficeVisit` | 5 (`leadId` `agencyId` `saleId` …) | **0** |
| `Unit` | 2 (`bookingId` `externalId`) | **0** |
| `DealTimeline` | 2 (`entityId` `actorId`) | **0** |

The codebase knows this and says so — `booking.service.ts:91`:

```ts
// resolve ชื่อ agency / project / sale (ไม่มี relation ตรง — join เอง)
```

**This is a convention, not an oversight**, and it is why every service builds `Map`s by hand instead
of using `include`. Three consequences follow, and all three land on this project:

- **No cascade and no integrity check.** Nothing stops a column pointing at a deleted row.
- **Prisma cannot join.** Each new screen costs a second query plus an in-memory map.
- **Phase 2 and 3 have to pick a side.** `deal_payment_schedules` and `deal_commissions` would be the
  first tables to carry a real FK to `bookings`. Either follow the convention (consistent, no
  integrity) or introduce FKs on the new tables only (safer for money, inconsistent with everything
  else). **This needs a decision before Phase 2 starts.** The recommendation below is to use real FKs
  on the new financial tables and say so explicitly, because an orphaned payment row is worse than an
  inconsistent convention.

---

## 2 · Confirmed bugs

### High

**H1 · The Home feed shows deleted deals to everyone**
`api/src/home/home.service.ts:120`

```ts
const bookings = await this.prisma.booking.findMany({ orderBy: { createdAt: 'desc' }, take: 50 });
```

No `where` at all. Soft-deleted deals (`deletedAt != null`) and legacy-imported deals
(`dataScope: 'legacy'`) both appear in the activity feed. Everywhere else in the project these are
filtered — `deals.service.ts` sets `deletedAt: null` at the top of every query function
(lines 240, 416, 989, 1164) and adds `dataScope: { not: 'legacy' }`.

*Fix:* `where: { deletedAt: null, dataScope: { not: 'legacy' } }`.

**H2 · The automation funnel counts every deal ever created**
`api/src/automation/automation.service.ts:175, 186`

```ts
const bookingScope = empId ? { OR: [{ saleId: user.id }, …] } : {};
…
this.prisma.booking.count({ where: bookingScope as never }),
```

For a manager (`empId` falsy) the scope is `{}`, so the funnel's "deals" number counts deleted deals
and legacy imports. The lead counts beside it *are* scoped. The funnel therefore does not reconcile
with the board or the Lead Status report.

*Fix:* start `bookingScope` from `{ deletedAt: null, dataScope: { not: 'legacy' } }`.

**H3 · Moving a deal on the Kanban never updates the unit**
`api/src/deals/deals.service.ts` — `prisma.unit` appears **0 times** in the whole file.

Unit status is only maintained in the Booking module:

- `booking.service.ts:142` — sets `unit.status = 'booked'`, `unit.bookingId = b.id`, **and only when
  `body.unitId` was supplied**
- `booking.service.ts:213` — releases it on cancel

So a deal that is created and driven to Closed Deals entirely from `/deals` leaves its unit
`available` forever. **This is the single most important finding for Phase 1**: the Sold Deal
conversion wizard promises to set the unit to `sold` in the same transaction, and there is no
existing code path it can reuse. The wizard has to own this, and it is new work, not a refactor.

### Medium

**M1 · The activity report includes deleted and legacy deals**
`api/src/report/report.service.ts:479`

The booking rows filter on the date range and optionally `saleId`, but carry neither `deletedAt` nor
`dataScope`. A deal someone deleted still counts in the activity report.

**M2 · Cancelling a deal can mark a sold unit available again**
`api/src/booking/booking.service.ts:213`

```ts
await this.prisma.unit.updateMany({
  where: { bookingId: id },
  data: { status: 'available', bookingId: null },
});
```

Unconditional. If the unit had reached `sold`, cancelling the booking silently returns it to the
price list. There is no guard on the current status.

*Fix:* only release when the unit is still `reserved` or `booked`; a `sold` unit needs an explicit
decision, which is exactly the refund/cancellation policy left open in `OPEN_DECISIONS.md`.

**M3 · Deleting a lead orphans its deals and visits**
`api/src/customer-lead/customer-lead.service.ts:764`

```ts
const deleted = await this.prisma.customerLead.delete({ where: { id } });
```

A hard delete, with no cleanup. `Booking.leadId` and `OfficeVisit.leadId` are left pointing at a row
that no longer exists, and no FK stops it. The deal keeps rendering — `deals.service.ts` looks the
lead up separately and simply finds nothing — so this fails silently rather than loudly.

Note the contrast: `Booking` has a proper soft delete (`deletedAt`, `deletedById`), and
`agency.service.ts:143` refuses to delete an agency that still has deals. Leads have neither guard.

### Low

**L1 · A KPI count includes deleted deals** — `api/src/visit/visit-workflow.service.ts:447`,
`booking.count({ where: { createdAt: range } })`.

**L2 · `genBookingNo()` is not concurrency-safe** — `api/src/booking/booking.service.ts:69`

```ts
const count = await this.prisma.booking.count({ where: { bookingNo: { startsWith: prefix } } });
return `${prefix}-${p(count + 1)}`;
```

Count-then-format. Two creates in the same millisecond produce the same number. `bookingNo` is
`@unique`, so the result is a failed create rather than a duplicate — a bad error message, not
corrupted data. **Relevant because the Sold Deal wizard continues this sequence.** The project
already has the right pattern elsewhere: `PrSequence` (`schema.prisma:1410`) is a singleton row with
`lastSeq`, incremented in a transaction.

**L3 · The `reportStatus` schema comment is out of date** — `schema.prisma:2458` documents
`holding|reservation|open|first_follow_up|second_follow_up|third_follow_up|missed`, but the UI also
writes `fourth_follow_up`, `completed` and `cancelled` (`CustomerFormDialog.tsx:59`,
`MyVisitsPage.tsx:68`, `DealsPage.tsx:51`). Anyone implementing Phase 1 from the comment will build
the wrong value set.

**L4 · A dead key with an asymmetric round trip** — `report-status-stage.ts:15` maps
`closed_deal → 'completed'`, but `STAGE_TO_REPORT_STATUS` maps `completed → 'completed'`. A lead
whose `reportStatus` were `closed_deal` would be silently rewritten to `completed` on the next stage
sync. **No UI writes `closed_deal`**, so this is latent, not firing. Worth deleting rather than
fixing, while Phase 1 is in that file anyway.

---

## 3 · Things that look wrong and are not

Stated because a reviewer will trip over them:

- **`deals.service.ts` soft-delete coverage is complete.** A crude grep suggests four queries miss
  `deletedAt`, but each one's `where` is initialised with `deletedAt: null` earlier in the function
  (lines 240, 416, 989, 1164). Nothing to fix.
- **`agency.service.ts:143` counting deleted deals as delete-blockers is conservative by design.**
  It refuses to delete an agency that has any deal history, including deleted ones. That is the safe
  direction; leave it.
- **`crm360.service.ts:129` is correctly scoped** — `deletedAt: null, dataScope: { not: 'legacy' }`.
- **`venio.service.ts:345` deliberately has no scope** — it enriches Venio rows by `venioDealNo` and
  is meant to see imported data.

---

## 4 · What this means per phase

| Phase | What the audit changes |
| --- | --- |
| **1** | **H3 is scope.** The conversion wizard must set unit status itself — no existing code path does it from `/deals`. L3 means the value set comes from the UI files, not the schema comment. L4 is a free cleanup while in that file. |
| **2** | The **FK decision** in §1 must be made first. Recommendation: real FKs on the new financial tables, stated as a deliberate exception. M2 overlaps the cancellation policy still open in `OPEN_DECISIONS.md`. |
| **3** | The FK decision again, plus: commission totals must filter `deletedAt` and `dataScope` from the start, or they inherit H1/H2/M1 on day one. |
| **4** | M3 — the central Visit record links to leads by a bare `leadId` that can already be orphaned. Decide whether the Visit list shows or hides visits whose lead is gone. |
| **5** | Nothing. This phase touches no data. |

---

## 5 · Suggested order, if these get fixed

None of them blocks the restructure. If they are picked up, this order costs least:

1. **H1, H2, M1, L1** — four one-line `where` additions. Independent, and they make the new
   dashboards reconcile with the board from the start.
2. **L3, L4** — documentation and a dead key, free while Phase 1 is already editing those files.
3. **H3** — becomes part of Phase 1 rather than a separate fix.
4. **M2, M3** — need a policy decision first (what a cancelled sold unit does, whether leads should
   soft-delete like deals do). Worth raising with the owner rather than patching.
5. **L2** — swap `genBookingNo()` to the `PrSequence` pattern the project already uses. Best done
   before the Sold Deal wizard starts issuing numbers at a higher rate.
