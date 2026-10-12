# Invoicing finished Dispatch jobs (Progress Residential → QuickBooks → Coupa)

Owner's instructions, 10/12. Relay invoicing comes later (owner will give the steps).

## When a job is ready
A Dispatch job is done when it leaves Dispatch's Incomplete list (the Portal Change Check
writes `CLOSED | Dispatch | J00…` in its "Portal changes" email). For now the owner says
when a job is ready to invoice.

## Part 1 – QuickBooks invoice (cloud session, Meridian connector)
1. Find the job's Coupa PO: the "Progress Residential Purchase Order #<PO>" email (from
   coupahost.com), or the board job `coupa-<PO>` / `dispatch-<J#>` (its statusNote has the PO).
   The PO number (or the job/work-order number) is the only unique key. Never match on
   amount or address alone.
2. Amounts: read the approved estimate on Dispatch (search Dispatch by the J-number; the
   job is no longer in the active list) and the Coupa PO total.
   - Differ by more than $5 → stop and tell the owner. Create nothing.
   - Differ by $5 or less → use the **Coupa amount**. The invoice is the lien waiver and must
     match Coupa exactly.
3. Before creating, check QuickBooks has no invoice yet with that WO#/PO in its description.
4. Create the invoice: customer **Progress Residential** (Id 3154, the customer the payments
   go to; not the other Progress customers), one line, item **Clean Up** (Id 30), Qty 1,
   amount = Coupa amount, TaxCodeRef NON, description `WO#<J-number>\nPO <PO number>`.
   BillAddr Line1 "Progress Residential", Line2 = property street, Line3 = "City, FL ZIP"
   (same as the existing invoices). Invoice date = today (QuickBooks default), terms Net 30.
   Keep the standard lien-waiver customer memo (QuickBooks adds it by default).
5. Send it to the owner (BillEmail floridasgreenthumb@gmail.com) so the PDF lands in Gmail.
   Note the invoice number (DocNumber).

## Part 2 – Coupa submit (owner's laptop, Claude in Chrome)
1. Open Coupa, find the PO by its PO number (or job number).
2. Click **Submit Invoice** (create invoice from the PO). Lines and amount are already filled
   in from the PO; don't type them.
3. **Remit To**: pick either of the two options in the drop-down (they are the same).
4. **Invoice #** (at the top): type the QuickBooks invoice number.
5. If the amount is **over $500**: attach the QuickBooks invoice PDF (from the owner's email)
   as the **lien waiver**. Its amount must equal the Coupa amount.
6. **First 5 invoices: STOP before clicking Submit.** Leave the page filled in and tell the
   owner it's ready to check. After 5 have been checked, click Submit yourself.
   Count so far: 0 of 5.
7. After submitting, the Coupa invoice email will clear the job from the Route Board as usual.

## Never
- Never submit when amounts differ by more than $5, when the PO can't be found by its number,
  or when an invoice for that WO/PO already exists in QuickBooks or Coupa.
- Never invoice an AMH, Maymont or owner-created Dispatch job with this process.
