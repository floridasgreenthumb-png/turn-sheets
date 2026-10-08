# Nightly: Progress Residential remittances → QuickBooks payments

Runs with the 9 PM nightly job. Uses the **Meridian Connector for QuickBooks**
(company "Florida's Green Thumb", company_id e28aa95a-740e-4ae9-b163-5fef79bc1253)
and Gmail.

## Source emails
- From `DoNotReply@yardi.com`, subject `Remittance amount $X YYYY-MM-DD`.
  Body lists Transaction Reference No, Transaction Date, and a table of
  Invoice # / Invoice Date / Payment Amount, plus a Total.
- Done = Gmail label `qb-payment-recorded` (label ID `Label_15`).
- Search: `from:DoNotReply@yardi.com subject:Remittance -label:qb-payment-recorded`
  Oldest first. At most 25 remittances per night.

## Checks (all customers, all sources)
- Do NOT enter a check payment unless it has a cleared date. The Coupa export only
  shows the issue date ("Check - #1234 on MM/DD/YYYY"), which is not a cleared date,
  so Coupa check payments are never entered. Leave them alone (no discount line, no
  payment) and list them in the summary as "check, not cleared".
- Check payments already entered on 2026-10-07 stay as they are (user's decision).

## Fixed values
- Customer: Progress Residential (QuickBooks customer Id `3154`).
- Deposit to, by payment date (bank switch was **July 2, 2026**):
  - 2026-07-02 or later → **MID FLA BIZ ACCT** (account Id `1150040000`)
  - before 2026-07-02 → **liberty bank** (account Id `238`)
- Discounts: account **Discounts given** (Id `245`).

## Per remittance
1. Read the email (PLAIN_TEXT). Parse ref no, transaction date, and each
   invoice # + paid amount. Check the lines add up to the Total.
2. Query QuickBooks: `SELECT * FROM Invoice WHERE DocNumber IN (...)`.
   Every invoice must exist, belong to customer 3154, and still be open.
3. For each invoice compare paid vs current Balance:
   - equal → apply in full.
   - paid is exactly 2% less (round(balance*0.02, 2) == balance - paid, ±$0.01)
     → discount (≤ 7 days after the invoice date is a normal early-pay discount; more than
     7 days is a late discount: still accept it, and log it — see "Late-discount tab"):
     get_entity the invoice, sparse update_entity with the full existing
     Line list (keep line Ids) plus a DiscountLineDetail line for the
     difference (PercentBased false, DiscountAccountRef 245, description
     "2% early-pay discount (paid within 7 days) - Progress ACH <ref>").
   - anything else (short/over pay, invoice missing, already paid, wrong
     customer, totals don't add up) → do NOT touch any invoice in this
     remittance; list it under "needs you" with the reason; leave unlabeled.
4. Only if every invoice in the remittance passed step 3: create_entity
   Payment — CustomerRef 3154, TotalAmt = remittance total, TxnDate = the
   Transaction Date, PaymentRefNum = ref no, DepositToAccountRef as above,
   PrivateNote "Progress Residential ACH <ref> (Yardi remittance <date>).
   Invoices ...", one Line per invoice with LinkedTxn to the invoice Id.
   Before creating, query `SELECT * FROM Payment WHERE CustomerRef = '3154'`
   for the same TxnDate and TotalAmt — if one exists, it's already entered:
   just label the email.
5. Re-query the invoices; all must show Balance 0. Then label the email.
6. Use a new random UUID operation_id per mutation; never retry a failed
   QuickBooks validation unchanged.

## Summary
Payments recorded (date, ref, total, # invoices, discounts), and
remittances that need a person with the reason.

## Backlog (Jan 1, 2026 → now) from the Coupa export
Source: the newest Gmail message `from:coupahost.com subject:"Your Coupa invoice report"`
(the user clicks Export on Coupa's Invoices page; the zip arrives by email).
1. get_message RAW → saved file → `python3 -I automation/coupa_payments.py <file> --from 2026-01-01 > <scratch>/coupa.json`
   (one entry per Progress payment: payment_no, method, date, total, invoices[doc, amount, invoice_date]).
2. Already-done check: query QuickBooks payments for customer 3154 with
   TxnDate >= 2026-01-01 (paginate) and collect their PaymentRefNum values.
   Skip any Coupa payment whose `Coupa <payment_no>` is in that set.
3. Work oldest first, **max 50 payments per night**. For each one apply the
   same per-invoice rules as above (exact match, or exact 2% discount — on time
   is ≤ 7 days after the invoice date; later ones are accepted and logged per "Late-discount tab"). Extra rules:
   - If every invoice already has Balance 0 → it was entered from a Yardi
     email (different ref no.) → skip, nothing to record.
   - If some are 0 and some open, or anything else doesn't match → leave the
     whole payment alone and list it under "needs you".
   - Payment: TxnDate = Coupa date, PaymentRefNum = `Coupa <payment_no>`,
     PrivateNote "Progress Residential <method> #<payment_no> (from Coupa
     export). Invoices ...", deposit account by date per the rule above.
4. Summary line: "Backlog: X recorded tonight, Y left, Z need you".

## Coupa Status column (Voided / Disputed)
The export has a Status column (Approved, Disputed, Draft, Voided, Pending Approval).
Voided and Disputed rows are the user's own invoice mistakes. They never count as paid:
`coupa_payments.py` only reads rows with the Paid flag and a payment line, and so far no
Voided/Disputed row has one. Never record a payment from such a row. When reporting what
Progress still owes, list QuickBooks invoices whose Coupa row is Voided/Disputed
separately ("your Coupa mistakes, not owed as billed") instead of counting them as unpaid.

## Late-discount tab (hidden)
Any Progress payment where an invoice was paid exactly 2% short but MORE than 7 days
after the invoice date (QuickBooks TxnDate) goes on a hidden running tab: the
`late_discounts` collection in the Route Board artifact's database
(https://claude.ai/artifact/PR2nsTnSqLiWwj6WGwBuoz, not shown on the page).
One doc per invoice, id `coupa-<payment_no>-<invoice>` (or `yardi-<ref>-<invoice>`):
payer, payment, paymentDate, invoice, qbInvoiceDate, coupaInvoiceDate (if known),
daysAfterInvoice, daysAfterCoupaInvoice (if known), invoiceBalance, paid,
discountTaken, qbStatus ("not entered yet" / "entered"), note, loggedAt.
Use `set` for new docs only; skip ids that already exist. The user ACCEPTS these
discounts: add the 2% discount line (description "2% discount taken late (accepted) -
Progress <ref>"), record the payment as usual (add "LATE DISCOUNT accepted" to the
PrivateNote), and set the doc's qbStatus to "entered <date>, discount accepted
(QBO payment <Id>)". Anything that isn't exactly 2% short still goes under "needs you".
Mention new ones in the summary as "Late discounts: N new ($X)".

## Dennis Realty eCheck payments
- Source: `from:noreply@propertyware.com subject:"Pending Deposit To Account" -label:qb-payment-recorded`
  (Dennis Property Management via Propertyware). Body: Payment Date, Total Payment,
  Payment Method eCheck, Deposit Account XXXXXXXX2334, then an Invoice # / Amount Paid table.
  Oldest first, max 25 per night. Only eCheck payments (Dennis paid by paper check before
  the bank switch; those are not handled here).
- Customer: DENNIS REALTY (QuickBooks customer Id `2818`).
- Deposit to: **American Express Business Checking** (account Id `265`) — always.
- Same per-remittance steps as Progress above, except there is **no 2% discount** for
  Dennis: every invoice must be open and its balance must equal the amount paid exactly.
  Anything else (short/over pay, invoice missing or already paid, lines not adding up to
  the total) → touch nothing, leave unlabeled, list under "needs you".
- Payment: TxnDate = Payment Date, PaymentRefNum = `eCheck <MMDDYYYY>`, PrivateNote
  "Dennis Realty eCheck (Propertyware) <date>, $<total>. Invoices ...". Before creating,
  check there's no existing Payment for customer 2818 with the same TxnDate and TotalAmt.
- Label the email `qb-payment-recorded` (Label_15) once the invoices show Balance 0.

## American Homes 4 Rent (not automated yet — user will say when)
- AMH ACH payments ("ACH Payment Sent" from cdr@yardi.com, details in PDF attachments)
  are deposited to **American Express Business Checking** (account Id `265`, created
  2026-10-07). Never deposit AMH payments to MID FLA or liberty bank.
