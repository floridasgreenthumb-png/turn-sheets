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

## Fixed values
- Customer: Progress Residential (QuickBooks customer Id `3154`).
- Deposit to: **MID FLA BIZ ACCT** (account Id `1150040000`).
  Exception: payments dated before the bank switch go to **liberty bank**
  (Id `238`). The switch date is not set yet — until it is, only process
  remittances dated 2026-09-01 or later and list older ones as "needs bank".
- Discounts: account **Discounts given** (Id `245`).

## Per remittance
1. Read the email (PLAIN_TEXT). Parse ref no, transaction date, and each
   invoice # + paid amount. Check the lines add up to the Total.
2. Query QuickBooks: `SELECT * FROM Invoice WHERE DocNumber IN (...)`.
   Every invoice must exist, belong to customer 3154, and still be open.
3. For each invoice compare paid vs current Balance:
   - equal → apply in full.
   - paid is exactly 2% less (round(balance*0.02, 2) == balance - paid, ±$0.01)
     AND transaction date − invoice date < 7 days → early-pay discount:
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
   same per-invoice rules as above (exact match, or exact 2% discount with
   payment date − invoice date < 7 days). Extra rules:
   - If every invoice already has Balance 0 → it was entered from a Yardi
     email (different ref no.) → skip, nothing to record.
   - If some are 0 and some open, or anything else doesn't match → leave the
     whole payment alone and list it under "needs you".
   - Payment: TxnDate = Coupa date, PaymentRefNum = `Coupa <payment_no>`,
     PrivateNote "Progress Residential <method> #<payment_no> (from Coupa
     export). Invoices ...", deposit account per the bank rule above.
4. Summary line: "Backlog: X recorded tonight, Y left, Z need you".
