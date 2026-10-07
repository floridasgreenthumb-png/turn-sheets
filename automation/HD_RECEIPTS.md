# Daily: Home Depot e-receipts → job Receipts & Payout

Runs every day at 9 PM Eastern. Each Home Depot e-receipt email has a PDF; the
**PO / Job Name** typed at the register says which house it was for. The receipt
(PDF + order total incl. tax) is added to that job's Receipts & Payout, which
takes it off the payout as supplies.

## Steps (for the scheduled Claude run)

1. Gmail search:
   `from:HomeDepot@order.homedepot.com subject:"your Home Depot receipt" after:2026/09/27 -label:portal-receipt-added`
   (Receipts from Sept 27, 2026 on only. `portal-receipt-added` is a Gmail label — look up its ID with list_labels; create it if missing.)
2. For each message: `get_message` with `messageFormat: RAW`. The result is too big to
   show, so it is saved to a file — use that path.
3. `python3 -I automation/hd_receipt.py <saved.json> --save-pdf <scratch>/<order>.pdf > <scratch>/<order>.json`
4. `python3 -I automation/post_receipt.py <scratch>/<order>.json <scratch>/<order>.pdf`
   - exit 0 `added`, or 3 `already-added` / `already-on-job` (the crew already put a
     receipt for the exact amount on that job by hand) → label the message
     `portal-receipt-added`.
   - exit 2 `needs-human` (job name unclear, two jobs match, or a return) → do NOT
     label; list it in the summary.
5. End with a short summary: what was added (house, order #, amount) and anything
   that needs a person. Never guess a job.

Jobs come from `SCOPES` in `/index.html`, so new jobs are picked up automatically
once they're on the hub.
