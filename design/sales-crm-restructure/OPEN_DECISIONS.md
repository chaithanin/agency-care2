# Open decisions — draft

Five questions are still open. **Nothing is blocked by them**: each one has a draft answer below,
chosen so the safe behaviour is the default and so a later decision only ever *relaxes* a rule
rather than having to undo data.

Fill in the **Decision** line when the owner decides. Until then the main project builds the draft.

## Fill-in summary

| # | Question | Draft answer | Decision | Decided by / when |
| --- | --- | --- | --- | --- |
| 1 | When does commission become calculable? | Down Payment fully paid, configurable per project | | |
| 2 | Is overpayment allowed? | No — the server rejects it | | |
| 3 | Can Sales see company-wide figures? | No — reuse the existing `visibleOr()` rule | | |
| 4 | Customer cancels after paying | No automatic refund; Finance enters it by hand | | |
| 5 | The three promotion types left `null` | Ask per promotion; leaning noted below | | |

---

## 1 · When does commission become calculable?

**Why it matters** — commission entries exist from the moment a deal is created, but they must not
reach Pending Approval before the company has actually been paid enough to justify them.

**Draft answer**
Commission moves from **Calculated** to **Pending Approval** when the deal's paid total covers the
**Down Payment** milestone — that is, Booking, Contract and Down Payment are all `Paid`.

Configurable per project, not hard-coded: `payment_plan_masters.commission_trigger_seq` names the
milestone, and the per-deal snapshot copies it, so changing the master later does not move the
threshold on an existing deal.

**Until it is decided** — entries are created in `Calculated` and **do not advance on their own**.
Someone moves them to Pending Approval by hand. Safe in both directions: nothing is paid early,
and nothing is lost.

**Where it lands** — `payment_plan_masters.commission_trigger_seq` (Int, nullable) plus the same
field on `deal_payment_plan_snapshots`.

**Decision:** ______________________________________________

---

## 2 · Is overpayment allowed?

**Why it matters** — if a customer pays more than a milestone is worth, either the system rejects it
or it has to have somewhere to put the excess. Deciding this after money has landed is expensive.

**Draft answer**
**No.** The server rejects any payment that would push a milestone's paid total above its amount.

**Until it is decided** — reject. This is deliberately the strict direction: a rule can always be
relaxed later, but money that was accepted into the wrong place has to be unpicked by hand.

**If it is allowed later** — the excess becomes an explicit credit row on the deal. It must never be
silently absorbed into the next milestone, because then the schedule stops matching the contract.

**Where it lands** — validation in the record-payment endpoint, plus a flag
(`allow_overpayment`, system or project level) if it is ever turned on.

**Decision:** ______________________________________________

---

## 3 · Can Sales see company-wide figures?

**Why it matters** — the new Payments, Commission and dashboard pages all show totals. If they invent
their own scoping, two pages will disagree about the same number.

**Draft answer**
**No.** Reuse the rule the system already has. `deals.service.ts` has `visibleOr()`: a salesperson
sees deals where they are the sale, the closer, the creator, or where they are assigned to the lead.
Company-wide totals stay at Manager and above.

Every new page reuses that clause rather than writing its own.

**Until it is decided** — reuse `visibleOr()`. It is both the safe default and the least work, and
it keeps the new pages consistent with the board people already use.

**Where it lands** — the payment, commission and dashboard services call the same helper.

> If the answer turns out to be yes, be specific about *which* figures: seeing the company's total
> sales is a different question from seeing another salesperson's commission.

**Decision:** ______________________________________________

---

## 4 · A customer cancels after paying

**Why it matters** — this is the one path that moves money backwards. Guessing here is how a system
ends up quietly refunding the wrong amount.

**Draft answer**
**The system never computes a refund by itself.**

- Cancelling sets Deal Status to `Cancelled`. Payment Status is left as it is.
- A refund is an explicit transaction entered by Finance, with an amount and a reason.
- Nothing is hard-deleted. The reversal is a new row, never an edit to the original.

Whether the booking fee is forfeited, a fee is deducted, or the full amount is returned stays a
**policy Finance applies by hand** until it is written down here. Once it is written down it can be
automated, and the manual path still works.

**Until it is decided** — as above. No money moves automatically.

**Where it lands** — `deal_payment_transactions` with a `reversal` type, and the `Refunded` payment
status on the deal.

**Decision:** ______________________________________________

---

## 5 · The three promotion types left as `null`

**Why it matters** — `reduces_commission_basis` decides whether a promotion comes out of the
commission basis. `null` means nobody has decided, and it must never be read as `false`.

**Draft answer**
Leave all three `null` and **ask once, per promotion**, recording who answered. The leanings below
are a starting point, not a decision:

| `promotion_type` | Leaning | Reasoning |
| --- | --- | --- |
| `marketing_support` | probably **false** | Support given to the agency, not a price cut to the customer |
| `special_unit` | probably **true** | Effectively a price concession on that unit |
| `custom` | **must ask** | By definition it varies |

**Until it is decided** — the wizard asks and records the answer on the deal. Nothing is assumed.

**If a standing rule exists** — say so and the migration seeds these three the same way it already
seeds `cash_back`, `cash_bonus`, `additional_commission` and `fixed_commission`.

**Decision:** ______________________________________________

---

## Already decided — for reference

| Topic | Decision |
| --- | --- |
| Commission basis | Net Price = Sale Price − Discount − Promotion value |
| Tax | Not deducted from the basis |
| Cashback and cash bonus | Both count toward promotion value, conditionally — resolved by the `reduces_commission_basis` flag, with the per-deal breakdown stored on the deal |
| Sold Deal trigger | An authorised approver confirms the sale **and** the mandatory fields are complete |
| Deposit | A status on one row of the payment schedule, not a condition for the deal to exist |
| Quota | Ownership Quota — reuse the live values in `bookings.quota_category` |
| Visit source of truth | `office_visits`; `visit_plans` stays for planned field visits |
| Agency Last Visit | `MAX(office_visits.visit_at, visit_checkins.checkin_at)` — computed, never entered |
| Approach | Add columns, never alter existing ones |
