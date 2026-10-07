#!/usr/bin/env python3
"""Add a parsed Home Depot receipt to its job's Receipts & Payout section.

  python3 -I automation/hd_receipt.py MSG.json --save-pdf r.pdf > r.json
  python3 -I automation/post_receipt.py r.json r.pdf [--dry-run]

Uses the same back end the job pages use (op "receipt"). The receipt id is
"hd-<order #>", so a receipt is never added twice. A receipt for the exact
same amount already on the job (the crew added it by hand) also counts as
already there. Exit 0 = added, 3 = already there, 2 = needs a human.
"""
import base64, datetime, json, re, sys, urllib.error, urllib.request

BACKEND_URL = "https://script.google.com/macros/s/AKfycbzh70eY91CL5hnjsNk9ha8RZe4b3WGWI9KJWMINnk9pbHzOmMfruAlf4zoW8FU_m7O3Hw/exec"
BACKEND_KEY = "tp_aDqhdJoELbiXbjS4_65yjwYzEeWAeHB0"


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None


def api(body):
    """Apps Script answers a POST with a 302 to script.googleusercontent.com,
    which has to be fetched with a plain GET (no body, no content type)."""
    body = dict(body, k=BACKEND_KEY)
    req = urllib.request.Request(BACKEND_URL, data=json.dumps(body).encode(),
                                 headers={"Content-Type": "text/plain;charset=utf-8"})
    try:
        with urllib.request.build_opener(_NoRedirect).open(req, timeout=120) as r:
            raw = r.read()
    except urllib.error.HTTPError as e:
        if e.code not in (301, 302, 303, 307, 308):
            raise
        with urllib.request.urlopen(e.headers["Location"], timeout=120) as r:
            raw = r.read()
    j = json.loads(raw)
    if not j or not j.get("ok"):
        raise RuntimeError((j or {}).get("error") or "no answer")
    return j


def main():
    args = [a for a in sys.argv[1:] if a != "--dry-run"]
    dry = "--dry-run" in sys.argv
    r = json.load(open(args[0]))
    pdf = open(args[1], "rb").read()
    m = r.get("match") or {}
    if not m.get("turn"):
        print(json.dumps({"status": "needs-human", "why": m.get("error", "no match"), "order": r["order"], "po": r["po"], "candidates": m.get("candidates")}))
        sys.exit(2)
    if not (r["total"] > 0):
        print(json.dumps({"status": "needs-human", "why": "total is not positive (return?)", "order": r["order"], "total": r["total"]}))
        sys.exit(2)
    rid = "hd-" + re.sub(r"[^A-Za-z0-9-]", "", r["order"])
    existing = api({"op": "receipts", "turn": m["turn"]}).get("items", [])
    if any(e.get("id") == rid for e in existing):
        print(json.dumps({"status": "already-added", "order": r["order"], "turn": m["turn"]})); sys.exit(3)
    same = [e for e in existing if abs((float(e.get("amount") or 0)) - r["total"]) < 0.005]
    if same:
        # the crew already snapped this receipt into the job by hand — adding it again would double the supplies
        print(json.dumps({"status": "already-on-job", "order": r["order"], "turn": m["turn"], "amount": r["total"],
                          "existing_id": same[0].get("id"), "existing_by": same[0].get("by", "")}))
        sys.exit(3)
    mm, dd, yy = r["date"].split("/")
    # noon Eastern-ish; only the day matters for the list order
    at = int(datetime.datetime(int(yy), int(mm), int(dd), 16, 0, tzinfo=datetime.timezone.utc).timestamp())
    body = {"op": "receipt", "turn": m["turn"], "house": m["house"], "id": rid, "amount": round(r["total"], 2),
            "store": "Home Depot", "note": ("#" + r["order"] + " · PO: " + (r["po"] or "-"))[:120],
            "by": "Auto (email)", "at": at, "data": base64.b64encode(pdf).decode(),
            "mime": "application/pdf", "name": r.get("pdf_name") or (r["order"] + ".pdf"), "thumb": ""}
    if dry:
        body["data"] = "<%d bytes>" % len(pdf)
        print(json.dumps({"status": "dry-run", "would_send": body})); return
    api(body)
    print(json.dumps({"status": "added", "order": r["order"], "turn": m["turn"], "house": m["house"], "amount": r["total"]}))


if __name__ == "__main__":
    main()
