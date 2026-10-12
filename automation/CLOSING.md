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

## Relay closing steps
1. Open the job on Relay (by its job number T…).
2. Save all photos for that job from the email(s) to the laptop.
3. Click **Start Job**.
4. At the bottom, click **Attachments**, attach ALL the photos, and **Upload** them.
5. Click **Job Complete**. Relay sometimes sticks: click again until the option to complete
   the job goes away.
6. Then invoice it: follow automation/INVOICING.md (QuickBooks invoice → Coupa submit).

## Safety
- First 5 closings: stop before **Job Complete** and let the owner check the uploaded photos.
- Never close a job whose photos can't be matched to it with certainty.
- Never click Decline, Cancel or anything that changes price or schedule.
