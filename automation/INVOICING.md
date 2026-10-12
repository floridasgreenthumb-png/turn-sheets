# Invoicing finished Progress jobs – Dispatch and Relay (→ QuickBooks → Coupa)

Owner's instructions, 10/12. Dispatch and Relay jobs are both Progress Residential jobs with a
Coupa PO, and are invoiced exactly the same way; only where you find the finished job differs.

## When a job is ready
- **Dispatch:** done when it leaves Dispatch's Incomplete list (Portal Change Check writes
  `CLOSED | Dispatch | J00…`). It no longer shows in the active list: search Dispatch by the
  work-order number (J00…) to open it.
- **Relay:** done when it leaves Relay's active list (`CLOSED | Relay | T…`). It then shows under
  **Completed** or **Under Review** on Relay – open it there. The Relay job number (T…) identifies
  the job; the Coupa PO's Work Order is that number without the T (or the PO is shown on Relay).
For now the owner says when a job is ready to invoice.

## Part 1 – QuickBooks invoice (cloud session, Meridian connector)
1. Find the job's Coupa PO: the "Progress Residential Purchase Order #<PO>" email (from
   coupahost.com), or the board job `coupa-<PO>` / `dispatch-<J#>` (its statusNote has the PO).
   The PO number (or the job/work-order number) is the only unique key. Never match on
   amount or address alone.
2. Amounts: read the approved estimate on Dispatch (search by the J-number) or the Job Scope
   Cost on Relay (Completed / Under Review), and the Coupa PO total.
   - Differ by more than $5 → stop and tell the owner. Create nothing.
   - Differ by $5 or less → use the **Coupa amount**. The invoice is the lien waiver and must
     match Coupa exactly.
3. Before creating, check QuickBooks has no invoice yet with that WO#/PO in its description.
4. Create the invoice: customer **Progress Residential** (Id 3154, the customer the payments
   go to; not the other Progress customers), one line, item **Clean Up** (Id 30), Qty 1,
   amount = Coupa amount, TaxCodeRef NON, description `WO#<J-number or Relay T-number>\nPO <PO number>`.
   BillAddr Line1 "Progress Residential", Line2 = property street, Line3 = "City, FL ZIP"
   (same as the existing invoices). Invoice date = today (QuickBooks default), terms Net 30.
   Keep the standard lien-waiver customer memo (QuickBooks adds it by default).
5. Send it to the owner (BillEmail floridasgreenthumb@gmail.com) so the PDF lands in Gmail.
   Note the invoice number (DocNumber).

## Part 2 – Coupa submit (owner's laptop, Claude in Chrome)
1. Open Coupa. First check the **Invoices** tab: if an invoice for this PO is already there,
   it's done – don't submit again.
2. Find the PO by its PO number (or job number) and click **Submit Invoice** (create invoice
   from the PO). Lines and amount are already filled in from the PO; don't type them.
3. In this order:
   a. If the amount is **over $500**: FIRST attach the QuickBooks invoice PDF (from the
      owner's email) as the **lien waiver**. Its amount must equal the Coupa amount.
   b. **Remit To**: pick either of the two options in the drop-down (they are the same).
   c. **Invoice #** (at the top): type the QuickBooks invoice number.
   d. Click **Submit**.
4. **First 5 invoices: STOP before step 3d.** Leave the page filled in and tell the owner it's
   ready to check. After 5 have been checked, click Submit yourself.
   Count so far: 0 of 5.
5. **Check it went through:** Coupa shows the invoice was submitted successfully and the bar at
   the top turns **green**. If it doesn't turn green (error, red/yellow message, nothing
   happens): don't retry blindly – send the owner a push notification right away with the PO,
   job number and what Coupa showed, and add it to the failed list below.
6. Record every invoice in `$HOME/mnt/PORTAL WATCHER/invoices.json` on the laptop
   (one entry per job: portal, job number, PO, QuickBooks invoice #, amount, date, status
   `submitted` / `waiting for owner check` / `FAILED – <what Coupa showed>`). Failed ones stay
   on the list until the owner says they're fixed; mention them in every invoicing summary.
7. After a green submit, the Coupa invoice email clears the job from the Route Board as usual.

## Never
- Never submit when amounts differ by more than $5, when the PO can't be found by its number,
  or when an invoice for that WO/PO already exists in QuickBooks or Coupa.
- Never invoice an AMH, Maymont or owner-created Dispatch job with this process.
- Never submit twice: check Coupa's Invoices tab and invoices.json first.
