# Closing finished Progress jobs on the portals (Relay; Dispatch steps to come)

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
