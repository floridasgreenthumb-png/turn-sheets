# Route Board refresh — task prompt (standalone)

Paste everything below the line as the task / routine prompt. It needs these connectors:
**Gmail** and the **Artifact / ArtifactData** tools (the board's database). GitHub access to
`floridasgreenthumb-png/turn-sheets` is optional (only for the geocode script and this file).

---

You keep my Route Board up to date. The board is the artifact
https://claude.ai/artifact/PR2nsTnSqLiWwj6WGwBuoz — a list + map of my open portal jobs
(Progress Residential via Coupa / Dispatch / Relay, AMH, Maymont). Its data lives in the
artifact's database; read and write it with the ArtifactData tool (url = the board).

## Hard rules
- Never write the `plan` collection (my route ticks), the `late_discounts` collection (owned by
  another chat), or `photos/<jobId>` (crew uploads).
- Don't send email. Don't touch QuickBooks. Don't accept or decline offers in any portal.
- Never delete a Maymont job (I delete those by hand). Never delete a job I ticked for today's
  route (`plan/<id>.route == true`) — set its statusNote instead.
- Do NOT add AMH jobs (my AMH watcher adds them). Updating or removing AMH jobs already on the
  board is fine.
- When changing an existing job use `update` (merge), never `set`, so `link` and `photos` survive.
  Pin every write with `if_version`. Other sessions also edit the board: always list the jobs
  first and never add a job that is already there; if a pinned write fails, re-read and redo it.
- Plain wording. No menu directions you aren't sure of.

## Data
- `jobs/<id>`: one doc per open job. Ids: `coupa-<PO>`, `dispatch-<J-number>`, `amh-<WO>`,
  `relay-<T-number>`, `maymont-<B-number>`.
  Fields: company (progress|amh|maymont), portal, ref, street, city, state, zip, lat, lng,
  geo (exact|approx|none), title, items, amount, needBy (YYYY-MM-DD), received, status,
  statusNote, tenant, phone, project, workOrder, po, priority, link, updatedAt.
- status is one of: new, price (needs price), waiting (waiting approval), approved, open, check.
- `meta/sync` = {lastRun (ISO time, Eastern), counts: {jobs}}. `settings/home` = my home address.

## Each run
1. Get `meta/sync`. List all `jobs` (page through them).
2. Gmail search, covering the time since lastRun (adjust newer_than), then keep only emails
   newer than lastRun:
   `newer_than:4h (from:coupahost.com OR "Portal changes" OR from:dispatch.me OR from:amh.com OR from:cdr@yardi.com OR from:maymonthomes.com) -subject:"marked as Paid" -subject:"Approved to Pay" -subject:"Reminder to Acknowledge"`
   Open each relevant thread (PLAIN_TEXT). Big Dispatch/Coupa emails: the job details are
   before "Accept Job" / before the PO terms.
3. Apply, oldest first:
   - **"Portal changes"** (my Claude in Chrome portal check emails these to me). Lines:
     `NEW|ADDED | portal | job # | address | stage`, `CHANGED | portal | job # | stage`,
     `GONE|CLOSED | portal | job # | address`, `PROBLEM | ...`.
     NEW → add (or update if there); skip `NEW | AMH`. CHANGED → set status from the stage:
     needs price → price, waiting approval → waiting, approved → approved, anything else → open;
     put the portal's wording in statusNote. GONE/CLOSED → delete. Match AMH by WO, Dispatch by
     J-number, Relay by T-number / workOrder / project. A line matching nothing → skip and tell me.
     PROBLEM lines → tell me.
   - **Coupa "Progress Residential Purchase Order #<PO>"** (not Reminder, not Copy, Revised only
     updates): add `coupa-<PO>` (ship-to address, Project Number, Work Order, earliest Need By,
     line items, total; status open, note "PO issued, not invoiced yet") ONLY if still open and
     not already on the board. If the Work Order is a Dispatch J-number on the board → update that
     dispatch job instead (portal "Dispatch + Coupa", amount, PO in statusNote). J-number not on
     the board → skip (already closed). Same job as a Relay job on the board (same address /
     amount / work order) → add the PO number to that Relay job instead of a new job.
   - **Coupa invoice for a PO** → delete `coupa-<PO>`.
   - **Dispatch "New Offer"** → add `dispatch-<J#>` status new (address, tenant, phone, job type,
     description, due date). "Estimate was just Approved" → that tenant's open job → approved.
     "has been canceled" / completed / closed → delete that job.
   - **AMH**: "New Work Order is Available" → nothing. "Bids approved for order #WO" → that job:
     amount, status approved, note "Bid approved $X". Notes / staff emails → short statusNote.
     ACH payment (cdr@yardi.com) naming the WO → delete.
   - **Maymont** `Work Order for <address>, <B#>, ... Status - <status>` from
     dispatch@maymonthomes.com → add or update `maymont-<B#>` (amount = "approved amount for this
     bid", statusNote = the Status). Vendor Survey → nothing.
   - Payments ("marked as Paid", ACH) and Coupa reminders → nothing.
4. New or changed addresses need lat/lng so they show on the map. Use the free U.S. Census
   geocoder: `https://geocoding.geo.census.gov/geocoder/locations/onelineaddress?address=<street, city, ST zip>&benchmark=Public_AR_Current&format=json`
   → result.addressMatches[0].coordinates (y = lat, x = lng), geo "exact". If it can't be
   found, leave lat/lng out and set geo "none" (the board shows "not on map").
5. One ArtifactData `batch` (≤50 writes): new jobs (`set`), changes (`update`, pinned),
   deletions (`delete`, pinned), and `meta/sync` (lastRun = this run's time, counts.jobs).
6. Reply with one line: `Board: +N new, M updated, K removed, T open`, then short notes only for
   things I must do by hand (offers to accept, problems from the portal check, anything skipped).

## Open items at handover (10/14, 7 PM run; 32 jobs on the board)
- The portal check keeps listing 13 Dispatch jobs with "#" ids instead of J-numbers
  (21830 Pristine Lake Blvd, 13439 White Elk Loop, 5012 Mirror Ridge Ct, 9207 Cypresswood Cir,
  4830 Sky Blue Dr, 4743 Willow Dr, 4855 Gulfstream Pl, 2404 Corrine St, 1120 Crimson Clover Ln,
  5711 Lassies Way, 28643 Fairweather Dr, 703 Fayette Pl, 5519 Reflections Blvd). Not added —
  waiting on me to say if they belong on the board. Keep skipping them until I say.
- Coupa revised change-order PO 00296390 (Relay T5041661) from $240.88 to $740.88; the board's
  T5041661 job was not changed.
- The Chrome portal check sometimes runs without the laptop (no portals checked) and its
  Accept clicks are refused — offers need a hand accept.
