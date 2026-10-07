# Route Board refresh (open portal jobs → map)

Board: https://claude.ai/artifact/PR2nsTnSqLiWwj6WGwBuoz (private, `db` capability).
Collections: `jobs/<id>` (one per open job), `plan/<id>` (the user's route/done ticks —
never write these), `meta/sync` {lastRun, counts}, `settings/home` {address, lat, lng}.
Job ids: `coupa-<PO>`, `dispatch-<J-number>`, `amh-<WO>` (or `amh-<address>` for turns).
Job fields: company (progress|amh|maymont), portal, ref, street, city, state, zip, lat, lng,
geo (exact|approx|none), title, items, amount, needBy, received, status
(new|open|approved|check), statusNote, tenant, phone, project, workOrder, updatedAt.

Runs hourly 7 AM–7 PM Mon–Sat, and again in the 9 PM nightly run.
Work only on emails newer than `meta/sync.lastRun` (search with `newer_than:2h`
plus the date check, so nothing is missed between runs).

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
| Newest **"Portal status update"** email (from Claude in Chrome, to floridasgreenthumb@gmail.com) | it lists every open job per portal. Jobs it marks pending validation / complete / closed / canceled → delete. Jobs it lists as open → status open + its status text. Jobs it lists that aren't on the board → add. |
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
