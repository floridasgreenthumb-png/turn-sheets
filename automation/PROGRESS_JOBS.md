# Progress Residential jobs – Dispatch & Relay: the whole process in one place

(Owner's instructions, 10/12. This file replaces CLOSING.md and INVOICING.md.)

## The flow at a glance
1. Job comes in (Dispatch / Relay offer) → accepted → on the Route Board.
2. Crew does the work → photo email arrives ("Job photos – …" or RouteMaker "Completed: …").
3. Close it out on the portal (Relay: Claude does it all; Dispatch: owner does before photos +
   estimate, Claude does the rest once the Coupa PO email arrives).
4. Invoice: QuickBooks invoice (Clean Up, Coupa amount) → Coupa Submit Invoice (lien waiver if > $500).
5. Dispatch only: mark Complete after the Coupa invoice is green.
First 5 of each: stop before the final click so the owner can check.

# Part A – Closing out jobs

Owner's instructions, 10/12. Runs on the owner's laptop (Claude in Chrome); the Relay tab is
kept open and logged in (auto-refresh extension).

## Where the job came from
Use the Route Board (`jobs` collection: portal "Relay" / ids `relay-T…`, "Dispatch" / `dispatch-J…`,
or a Coupa job whose workOrder is a Relay or Dispatch number). Only Relay jobs use the steps below.

## Trigger: the job-photo emails
Scan Gmail (owner asked every ~15 min) for new photo emails and match them to a board job by
**street address** (house number + street name must match; then confirm the job number):
- `Job photos - <street> (Turn <n>) - completed by <crew> (part X of Y)` from
  floridasgreenthumb@gmail.com, photos attached. Wait until ALL parts (X of Y) are in; the body
  says how many photos each part has – the total must add up before uploading.
- `Completed: <ADDRESS>` from notifications@routemakerpro.com (RouteMaker Pro), with BEFORE /
  AFTER photos (attached and/or linked). Use these for the same address if there's no
  "Job photos" email.
Never upload photos to a job unless the address matches exactly and only one open job has it.
Most photo emails are regular mowing customers (not on Relay or Dispatch): ignore any email whose
address matches no open Relay or Progress Dispatch job. Dispatch jobs that aren't Progress
(no Progress J-number, owner-created) are ignored too.
Label handled emails so they aren't used twice (Gmail label `job-closed`).

## Which photos
Upload only the **AFTER** photos (Relay and Dispatch). Photos given as links (RouteMaker) may be
downloaded from the link, but always upload the actual picture files – never paste a link in
place of a picture.

## Not done yet → pause for a change order
If the email notes say the job is not done / needs more work: do NOT close it. On Relay click
**Pause**, choose the reason **Change Order**, and pick a date one week from today. A paused job is NOT closed and NOT invoiced.
Then email the owner (to floridasgreenthumb@gmail.com, subject "Change order needed - <address>
(<job #>)") with the job number, address and the crew's note saying what's left to do.

## Relay closing steps (Relay asks no questions on Start Job / Job Complete)
1. Open the job on Relay by its job number (T…). If it can't be found by the T-number, stop and
   tell the owner.
2. Save the AFTER photos for that job from the email(s) to the laptop.
3. Click **Start Job**.
4. At the bottom, click **Attachments**, attach ALL the after photos, and **Upload** them.
5. Click **Job Complete**. Relay sometimes sticks: click again until the option to complete
   the job goes away.
6. Then invoice it: follow automation/INVOICING.md (QuickBooks invoice → Coupa submit).

## Safety
- First 5 closings: stop before **Job Complete** and let the owner check the uploaded photos.
- Never close a job whose photos can't be matched to it with certainty.
- Never click Decline, Cancel or anything that changes price or schedule.

## Dispatch closing steps (owner, 10/12)
**FOR NOW (owner, 10/12): the owner uploads the BEFORE photos and submits the estimate himself.**
Claude starts at step 4, only once the Coupa "Purchase Order" email for that job has arrived
(= the estimate is approved): upload the AFTER photos, invoice (QuickBooks + Coupa), mark Complete.
Steps 2–3 below are kept for later.
Order matters:
1. Open the job on Dispatch (search by its work-order number J00…; finished jobs may not be in
   the active list).
2. **Attachments → upload the BEFORE photos**, labelled **Before** (Dispatch lets you label each
   upload Before or After).
3. **Estimate:** pick the matching preset option in the drop-down for what was done (e.g.
   pressure wash house, trim trees). If no option clearly fits, stop and ask the owner, and add
   his answer to the "Estimate option choices" list below. In **Description**, write the
   resolution to the issue stated in the work order (what was done to fix it).
   If the chosen option's price is **under $250, change it to $250**. Click **Save Estimate**, then
   **Submit Estimate**. Estimates of $250 or less are approved automatically; higher ones wait
   for Progress to approve.
4. **Attachments → upload the AFTER photos**, labelled **After**.
5. Wait for the Coupa PO: once the estimate is approved, Coupa emails "Purchase Order approved" /
   "Progress Residential Purchase Order #<PO>" for that work order (its Work Order = the J-number
   shown at the top of the Dispatch work order). The PO number comes from that email. No PO email
   yet → don't invoice; check again next run.
   When the before and after photos are saved, the estimate is approved AND the PO is in: invoice it –
   QuickBooks (item Clean Up) and Coupa exactly as in automation/INVOICING.md (lien waiver PDF
   first if over $500, Remit To, invoice #, Submit, must turn green).
6. After the Coupa invoice is in (green), mark the job **Complete** on Dispatch.
Photos: in the photo emails each picture is labelled Before or After underneath it – use that.
Not finished per the notes → don't estimate or close; tell the owner (change order).
First 5: stop before Submit Estimate and before Complete so the owner can check.

### Estimate option choices (learned from the owner)
(none yet – add "work described as X → option Y" as the owner answers)


# Part B – Invoicing

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


# Part C – AMH (American Homes 4 Rent) close-out (owner, 10/13)
- Owner adds the before photos and the bid. Ready when a "Bid approved" email for the WO is in
  Gmail AND the AMH portal shows bid approved / Work in Progress.
- Claude: upload AFTER photos on the AMH work order, complete the job, submit for validation.
  No invoice goes to AMH or Coupa.
- QuickBooks: customer "American Homes 4 rent" (Id 3367, NOT the CDR one Id 3728), item Clean Up,
  amount = approved bid, description = WO number, Ship To = job address, today's date; email it to
  floridasgreenthumb@gmail.com. No duplicates.
- Dispatch update: ready when Dispatch shows the estimate Approved AND the Coupa PO email is in.
