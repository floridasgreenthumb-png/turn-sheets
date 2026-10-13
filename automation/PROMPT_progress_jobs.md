You are closing out and invoicing finished jobs for Florida's Green Thumb - Progress Residential (Relay and Dispatch) and American Homes 4 Rent (AMH) - using Claude in Chrome (my Chrome, already logged in), Gmail, the Meridian QuickBooks connector, and the Route Board (ArtifactData, url https://claude.ai/artifact/PR2nsTnSqLiWwj6WGwBuoz, collection "jobs"). Follow these steps exactly.

GROUND RULES
- Only Progress jobs from Relay (job numbers T…) or Dispatch (Progress work orders J00…), and AMH work orders (WO numbers). Ignore every other photo email (regular mowing customers), Maymont, and Dispatch jobs I created myself (no J-number).
- This close-out work overrides any older "AMH read only" rule: on AMH you may upload after photos, complete the job and submit it for validation, as in STEP 3C. Do AMH in your own new tab (if it shows the login page, click Log in once and wait; never type a password).
- Never touch the Chrome tab with the banner "CLAUDE WATCHER IS RUNNING IN THIS TAB". Reuse the open Relay tab and leave it open on Home. Close any other tabs you open.
- Never type passwords, never click Decline/Cancel, never change prices on Relay, never submit anything twice.
- FIRST 5 OF EACH (Relay Job Complete, Dispatch Complete, AMH complete/submit for validation, Coupa Submit): stop before the final click, email me "Ready to check - <address> (<job #>)", and continue only after I reply OK.
- Log every job in PORTAL WATCHER/invoices.json: portal, job #, PO, QuickBooks invoice #, amount, date, status (closed / submitted / waiting for my check / paused - change order / FAILED - reason).

STEP 1 - FIND FINISHED JOBS
Search Gmail for photo emails without the label "job-closed":
- "Job photos - <street> (Turn …) - completed by … (part X of Y)" - wait until all parts are in.
- "Completed: <address>" from notifications@routemakerpro.com.
Match the street address (house number + street) to exactly one job on the Route Board (portal Relay / ids relay-T…, Dispatch / dispatch-J…, a Coupa job whose workOrder is that T or J number, or AMH / amh-…). No match or more than one → skip.
Photos: use only the AFTER photos (labelled "after" under each picture / in the file name). You may download photos from the email links, but always upload the picture files, never a link.

STEP 2 - NOT FINISHED?
If the email notes say the job isn't done / needs more work: don't close or invoice it.
- Relay: open the job, click Pause, reason Change Order, date one week from today.
- Both: email me "Change order needed - <address> (<job #>)" with the crew's note. Label the photo email job-closed.

STEP 3A - CLOSE A RELAY JOB
1. Open the job on Relay by its T-number (if you can't find it, stop and email me).
2. Click Start Job.
3. At the bottom click Attachments, attach all the AFTER photos, and Upload.
4. Click Job Complete. Relay sticks - click again until the option to complete goes away.
Then go to STEP 4.

STEP 3B - DISPATCH JOB (I upload the before photos and set the estimate myself)
1. Ready only when the job shows the estimate Approved on Dispatch AND the Coupa email "Progress Residential Purchase Order #<PO>" / Purchase Order approved whose Work Order = the job's J-number. That means the estimate is approved. No PO email yet → skip this job until next time.
2. Open the job on Dispatch by searching its J-number (it may no longer be in the active list).
3. Attachments → upload the AFTER photos, labelled After.
Then go to STEP 4. After STEP 4 turns green, mark the job Complete on Dispatch.

STEP 3C - AMH JOB (I add the before photos and the bid myself)
1. Ready only when BOTH: a "Bid approved" email for that work order (WO number) is in Gmail, AND the AMH portal shows the order as bid approved / Work in Progress. Otherwise skip until next time.
2. Open the work order on AMH (https://www.amh.com/my-amh/vendor-admin-orders, by its WO number). Upload the AFTER photos. Then complete the job and submit it for validation (for payment). AMH does not take an invoice.
3. QuickBooks invoice (AMH is NOT invoiced in Coupa): if an invoice already mentions this WO, don't make another. Customer = "American Homes 4 rent" (Id 3367) - NOT "American Homes 4 rent CDR" (Id 3728). Item Clean Up, qty 1, amount = the approved bid amount, description = the WO number, Ship To = the job's address, today's date. Send it to floridasgreenthumb@gmail.com.
4. Label the photo email job-closed and log it in invoices.json. AMH skips STEP 4.

STEP 4 - INVOICE (Relay and Dispatch only)
1. Get the Coupa PO number from the PO email (Work Order = J-number, or T-number without the T). The PO number or job number is the only key - never match on amount or address alone.
2. Compare the job amount (Relay Job Scope Cost, or the approved Dispatch estimate) with the Coupa PO total. More than $5 apart → stop and email me. Otherwise use the COUPA amount.
3. QuickBooks: if an invoice already mentions this PO or job #, don't make another. Create the invoice: customer Progress Residential (Id 3154 - not the other Progress customers), item Clean Up (Id 30), qty 1, amount = Coupa amount, description "WO#<job #>" and "PO <PO>", bill-to address Line1 "Progress Residential", Line2 street, Line3 "City, FL ZIP", today's date. Send it to floridasgreenthumb@gmail.com so the PDF arrives in Gmail. Note the invoice number.
4. Coupa: open the Invoices tab first - if this PO already has an invoice, stop (already done). Otherwise open the PO and click Submit Invoice (lines and amount are already filled in). In this order:
   a. If the amount is over $500: FIRST attach the QuickBooks invoice PDF from Gmail as the lien waiver (it must equal the Coupa amount).
   b. Remit To: pick either of the two options (they're the same).
   c. Type the QuickBooks invoice number at the top.
   d. Click Submit.
5. It must say submitted successfully and turn GREEN at the top. If not: don't retry - send me a push notification and an email with the PO, job # and what Coupa showed, and log it as FAILED.
6. Label the photo email job-closed and update invoices.json.

FINISH with a short summary: jobs closed, invoices submitted (job, PO, invoice #, amount), jobs waiting for my check, change orders, and anything FAILED or skipped and why.
