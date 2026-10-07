#!/usr/bin/env python3
"""Merge what each portal's emails say into one list of currently open jobs.

  python3 -I automation/build_board.py <jobs-dir> [--today YYYY-MM-DD] > board.json

Reads (from <jobs-dir>, written by the hourly run's email readers):
  coupa_geo.json      open Coupa POs (not invoiced), already geocoded
  dispatch_relay.json Dispatch jobs + Relay project notices
  amh.json            AMH work orders
  portal_status.json  optional: the Claude in Chrome "Portal status update" list
Output: job records for the board (id, company, portal, ref, address, status ...).
Rules are in automation/BOARD.md.
"""
import datetime, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import jobs as hub_jobs

D = sys.argv[1]
TODAY = sys.argv[sys.argv.index("--today") + 1] if "--today" in sys.argv else datetime.date.today().isoformat()
def days_ago(d):
    return (datetime.date.fromisoformat(TODAY) - datetime.date.fromisoformat(d)).days if d else 999
def load(name, default):
    p = os.path.join(D, name)
    return json.load(open(p)) if os.path.exists(p) else default
def norm(s):
    return re.sub(r"[^a-z0-9]", "", (s or "").lower())

out = {}
coupa = load("coupa_geo.json", [])
dr = load("dispatch_relay.json", {"dispatch": [], "relay": []})
amh = [r for r in load("amh.json", []) if r.get("type") == "work_order" or "wo" in r]
status = load("portal_status.json", [])            # [{company, portal, ref, status, ...}]
hub = {(s["h1"].split(" ", 1)[0], norm(s["h1"].split(" ", 1)[1])[:6]): s for s in hub_jobs.load()}

# --- Progress: Coupa POs that are not invoiced yet -------------------------
by_wo = {}
for c in coupa:
    c = dict(c)
    out[c["id"]] = c
    if c.get("workOrder"):
        by_wo[c["workOrder"]] = c
by_project = {c["project"]: c for c in out.values() if c.get("project")}

# --- Progress: Relay projects ---------------------------------------------
for r in dr.get("relay", []):
    if r["project"] in by_project:
        j = by_project[r["project"]]
        j["portal"] = "Relay + Coupa"
        continue
    # A Relay project with no Coupa PO yet isn't scheduled work: it shows up
    # on the board once Progress issues the PO (matched on project number).
    continue

# --- Progress: Dispatch jobs ----------------------------------------------
for d in dr.get("dispatch", []):
    if d.get("canceled") or d.get("completed") or "555555" in (d.get("phone") or ""):
        continue
    if d.get("job_number") in by_wo:                # already on the board as a Coupa PO
        j = by_wo[d["job_number"]]
        j["portal"] = "Dispatch + Coupa"
        j.update(tenant=d.get("tenant"), phone=d.get("phone"), title=d.get("job_title") or j.get("title"))
        continue
    last = d.get("approved") or d.get("offered")
    if days_ago(last) > 14:
        continue
    st = "approved" if d.get("approved") else "new"
    if st == "approved" and days_ago(d["approved"]) > 7:
        st = "check"
    jid = "dispatch-" + (d.get("job_number") or norm(d.get("tenant")) + norm(d.get("street")))
    due = d.get("due_date") or ""
    m = re.match(r"(\d+)/(\d+)/(\d{4})", due)
    out[jid] = dict(
        id=jid, company="progress", portal="Dispatch", ref=d.get("job_number") or "",
        street=d.get("street"), city=d.get("city"), state=d.get("state") or "FL", zip=d.get("zip"),
        tenant=d.get("tenant"), phone=d.get("phone"), title=(d.get("job_type") or "") + (" – " + d["description"] if d.get("description") else ""),
        priority=d.get("priority"), received=d.get("offered"),
        needBy=(f"{m.group(3)}-{int(m.group(1)):02d}-{int(m.group(2)):02d}" if m else None),
        status=st, statusNote={"new": "Offer", "approved": "Estimate approved", "check": "Approved over a week ago"}[st])

# --- American Homes 4 Rent ------------------------------------------------
for a in amh:
    if a.get("paid") or a.get("paid_likely"):
        continue
    kinds = {e.get("kind") for e in a.get("events", [])}
    street = a.get("street") or None
    if not a.get("wo"):                             # Services Ordered (turn) by address
        num, rest = ((street or "").split(" ", 1) + [""])[:2]
        h = hub.get((num, norm(rest)[:6]))
        if h and h.get("completed"):
            continue
    if "bid_approved" in kinds:
        st, note = "check", "Bid approved – done? (pending validation)"
    elif kinds <= {"available"}:
        if days_ago(a.get("first_seen")) > 3:
            continue                                # offer likely taken or expired
        st, note = "new", "Available to accept"
    else:
        if days_ago(a.get("last_activity")) > 21:
            continue
        st, note = "check", (a.get("last_note") or "Active in AMH portal")[:120]
    jid = "amh-" + (a.get("wo") or norm(street))
    out[jid] = dict(
        id=jid, company="amh", portal="AMH", ref=("WO " + a["wo"]) if a.get("wo") else "Turn",
        street=street, city=a.get("city"), state="FL", zip=a.get("zip"),
        title=a.get("job_type") or "", amount=a.get("approved_amount"),
        received=a.get("first_seen"), status=st, statusNote=note)
    if a.get("wo") == "9874219":
        out[jid]["statusNote"] = "AMH 10/2: HOA says violations still unresolved"

# --- Claude in Chrome portal list overrides status ------------------------
for s in status:
    key = s.get("id") or {"AMH": "amh-", "Dispatch": "dispatch-", "Relay": "relay-"}.get(s.get("portal"), "") + str(s.get("ref", "")).replace("WO ", "")
    if key in out:
        if re.search(r"pending validation|complete|closed|cancel", s.get("status", ""), re.I):
            del out[key]
        else:
            out[key]["status"] = "open"
            out[key]["statusNote"] = s.get("status")

json.dump(sorted(out.values(), key=lambda j: j["id"]), sys.stdout, indent=1)
