# Route Board refresh (open portal jobs → map)

Board: https://claude.ai/artifact/PR2nsTnSqLiWwj6WGwBuoz (private, `db` capability).
Collections: `jobs/<id>` (one per open job), `plan/<id>` (the user's route/done ticks —
never write these), `meta/sync` {lastRun, counts}, `settings/home` {address, lat, lng}.
Job ids: `coupa-<PO>`, `dispatch-<J-number>`, `amh-<WO>` (or `amh-<address>` for turns).
Job fields: company (progress|amh|maymont), portal, ref, street, city, state, zip, lat, lng,
geo (exact|approx|none), title, items, amount, needBy, received, status
(new|open|approved|check), statusNote, tenant, phone, project, workOrder, updatedAt.

Runs hourly 7 AM–7 PM Mon–Sat (Eastern) in the Route Board session.
Work only on emails newer than `meta/sync.lastRun` (search with `newer_than:2h`
plus the date check, so nothing is missed between runs).

## Source of truth
AMH, Relay and Maymont close jobs inside their own portals and send no email when a job
closes (the only later email is an invoice or payment). So email can add jobs but can't say
a job is done: **the portal is the source of truth.** If a portal shows a job open, it is
open. Dispatch jobs stay open until the user closes them in Dispatch. That means the daily
"Portal status update" email (below) is what clears finished AMH/Relay/Maymont/Dispatch jobs.
Coupa jobs clear on their invoice emails as before.

## What adds, changes or removes a job
| Email | Effect |
|---|---|
| Coupa `Progress Residential Purchase Order #<PO>` (not "Reminder", not "Copy") | add `coupa-<PO>`: read PLAIN_TEXT; ship-to street/city/zip, Project Number, Work Order, earliest Need By, line items, total; status open "PO issued, not invoiced yet". If its Work Order is a Dispatch J-number already on the board, delete that `dispatch-` job and set portal "Dispatch + Coupa". |
| Coupa email naming an invoice for a PO / a newer "Your Coupa invoice report" export (`automation/coupa_payments.py` logic: PO has a non-void invoice) | delete `coupa-<PO>` |
| Dispatch "New Offer" | add `dispatch-<J#>` status new (address, tenant, phone, job type, description, due date) |
| Dispatch "Estimate was just Approved" | that tenant's newest open job → status approved |
| Dispatch "has been canceled" / completed / closed | delete that job |
| AMH "New Work Order is Available for Acceptance" | add `amh-<WO>` status new, city+zip only (approx pin) |
| AMH "Bids approved for order #<WO>" | street, amount; status check "Bid approved – done? (pending validation)" |
| AMH note / Services Ordered / staff email | update street, statusNote (keep it short) |
| AMH ACH payment (cdr@yardi.com) listing the WO, or amount-matching approved WOs exactly | delete |
| Maymont `Work Order for <address>, <B#>, ... Status - <status>` | add/update `maymont-<B#>` (address from subject, amount from "approved amount for this bid") |
| Maymont "Vendor Survey" for an address | delete that address's Maymont job (done) |
| Newest **"Portal status update"** email (from Claude in Chrome, to floridasgreenthumb@gmail.com) | one section per portal (`PORTAL:` name, `LIST: complete / partial / COULD NOT READ`, then one line per job: number \| address \| status \| extras). Only use sections marked `LIST: complete`; skip the others and say which were skipped. In a complete section: jobs marked pending validation / complete / closed / canceled → delete; jobs listed open → status open + the portal's status text in statusNote; listed jobs not on the board → add; board jobs from that portal **not in the list** → delete (the portal no longer has them). Safety: if one email would delete more than half of a portal's board jobs, set them to status check "Not in portal list" instead and mention it in the summary. Relay lines match board Progress jobs by project number (`project` field). |
| Relay "Project Team Notification" | nothing on its own; the job appears when its Coupa PO arrives (match on project number) |

Never delete a job the user ticked for a route today (`plan/<id>.route == true`); set
statusNote instead. Ignore the placeholder tenant "Progress Residential Resident".

## Steps
1. Read `meta/sync` and `jobs` (ArtifactData list, cursor through all).
2. Search Gmail for the emails above since lastRun; build adds/updates/deletes.
3. Geocode new/changed addresses: write them to a JSON list and run
   `python3 -I automation/geocode.py <file> <scratch>/geocache.json`.
4. ArtifactData `batch` (≤50 per call, pin `if_version` on existing docs): set new jobs,
   update changed ones, delete removed ones; then update `meta/sync` lastRun + counts.
5. If `settings/home` has `pending: true`, geocode its address and update lat/lng.
6. Summary line: "Board: +N new, M updated, K removed, T open".

## Later (planned, not active): closing Dispatch jobs
The user closes Dispatch jobs by hand today and wants Claude to do it eventually. Plan:
the board marks a Dispatch job "ready to close" (user ticks it done on the board, or its
Coupa invoice is in); Claude in Chrome closes only jobs on that list, after the user okays
the list, and reports each one in the next Portal status update. Not turned on yet.
