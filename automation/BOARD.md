# Route Board refresh (open portal jobs → map)

Board: https://claude.ai/artifact/PR2nsTnSqLiWwj6WGwBuoz (private, `db` capability).
Collections: `jobs/<id>` (one per open job), `plan/<id>` (the user's route/done ticks —
never write these), `meta/sync` {lastRun, counts}, `settings/home` {address, lat, lng}.
Job ids: `coupa-<PO>`, `dispatch-<J-number>`, `amh-<WO>` (or `amh-<address>` for turns).
Job fields: company (progress|amh|maymont), portal, ref, street, city, state, zip, lat, lng,
geo (exact|approx|none), title, items, amount, needBy, received, status
(new|price|waiting|approved|open|check), statusNote, tenant, phone, project, workOrder, updatedAt.

Runs hourly 7 AM–6 PM Mon–Sat (Eastern) in the Route Board session.
Work only on emails newer than `meta/sync.lastRun` (search with `newer_than:2h`
plus the date check, so nothing is missed between runs).

## Job stages (AMH and Dispatch)
New job → user looks at it and adds a price in the portal (**Needs price**) → some need the
estimate approved first (**Waiting approval**) → **Approved – can close** → user does the
work and closes it in the portal → it disappears from the portal → removed from the board.

## Source of truth
AMH, Relay and Maymont close jobs inside their own portals and send no email when a job
closes (the only later email is an invoice or payment). So email can add jobs but can't say
a job is done: **the portal is the source of truth.** If a portal shows a job open, it is
open. Dispatch jobs stay open until the user closes them in Dispatch. Claude in Chrome checks the portals
hourly and emails only what changed ("Portal changes", below); that is what clears finished
AMH/Relay/Dispatch jobs.
Maymont is not in the Chrome check (little work). Each hourly run adds new Maymont jobs from
their work-order emails (sender dispatch@maymonthomes.com). Never delete a Maymont job: the
user deletes them by hand.
AMH jobs are added by the AMH watcher, not by this refresh. Do not add AMH jobs here (not from
AMH emails, not from Portal changes `NEW | AMH` lines). Updating or removing AMH jobs already on
the board still works as below.
Coupa jobs clear on their invoice emails as before.

## What adds, changes or removes a job
| Email | Effect |
|---|---|
| Coupa `Progress Residential Purchase Order #<PO>` (not "Reminder", not "Copy") | add `coupa-<PO>`: read PLAIN_TEXT; ship-to street/city/zip, Project Number, Work Order, earliest Need By, line items, total; status open "PO issued, not invoiced yet". Only add it if the job is still open and not already on the board: if its Work Order is a Dispatch J-number already on the board, update that `dispatch-` job instead (keep its id; portal "Dispatch + Coupa", amount, PO number in statusNote); if it is a Dispatch J-number not on the board (already closed), skip it; if it is a Relay job already on the board (same address/amount), skip it. |
| Coupa email naming an invoice for a PO / a newer "Your Coupa invoice report" export (`automation/coupa_payments.py` logic: PO has a non-void invoice) | delete `coupa-<PO>` |
| Dispatch "New Offer" | add `dispatch-<J#>` status new (address, tenant, phone, job type, description, due date) |
| Dispatch "Estimate was just Approved" | that tenant's newest open job → status approved |
| Dispatch "has been canceled" / completed / closed | delete that job |
| AMH "New Work Order is Available for Acceptance" | nothing (the AMH watcher adds AMH jobs) |
| AMH "Bids approved for order #<WO>" | street, amount; status check "Bid approved – done? (pending validation)" |
| AMH note / Services Ordered / staff email | update street, statusNote (keep it short) |
| AMH ACH payment (cdr@yardi.com) listing the WO, or amount-matching approved WOs exactly | delete |
| Maymont `Work Order for <address>, <B#>, ... Status - <status>` (from dispatch@maymonthomes.com) | add `maymont-<B#>`, or update it if already there (address from subject, amount from "approved amount for this bid", status note = the Status in the subject) |
| Maymont "Vendor Survey" for an address | nothing (the user deletes Maymont jobs by hand) |
| **"Portal changes"** emails (from Claude in Chrome, to floridasgreenthumb@gmail.com; at most one per hour, only when something changed) | process every one newer than lastRun, oldest first. Lines: `NEW \| <portal> \| <job #> \| <address> \| <stage> \| <extras>`, `CHANGED \| <portal> \| <job #> \| <stage>`, `GONE \| <portal> \| <job #> \| <address>`. NEW → add (or update if already there); skip `NEW | AMH` lines (the watcher adds AMH jobs). CHANGED → update status from the stage. GONE (no longer in the portal = the user closed it) → delete. Stage → status: "needs price" → price; "waiting approval" → waiting; "approved" → approved (AMH/Dispatch: can close now); anything else → open. Put the portal's own wording in statusNote. Match AMH by WO, Dispatch by J-number, Relay by project number (`project` field of the Progress job). A line matching nothing → skip and mention it. Jobs not mentioned are left alone. `PROBLEM` lines → mention in the summary. |
| Relay "Project Team Notification" | nothing on its own; the job appears when its Coupa PO arrives (match on project number) |

Never delete a job the user ticked for a route today (`plan/<id>.route == true`); set
statusNote instead. Ignore the placeholder tenant "Progress Residential Resident".

## Steps
1. Read `meta/sync` and `jobs` (ArtifactData list, cursor through all).
2. Search Gmail for the emails above since lastRun; build adds/updates/deletes. Query:
   `newer_than:2h (from:coupahost.com OR "Portal changes" OR from:dispatch.me OR from:amh.com OR
   from:cdr@yardi.com OR from:maymonthomes.com)`.
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
