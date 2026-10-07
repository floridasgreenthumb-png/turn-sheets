"""Jobs in the portal (read from the hub's SCOPES list) and a matcher that
turns the "PO / Job Name" typed at the Home Depot register into one job.

Runners type things like "constinine", "6824 atlantic", "geese trail" — so
match on the house number if there is one, else fuzzy on the street name.
When a street has more than one job, keep the ones still open on the receipt
date; if that doesn't leave exactly one, return no match (flag for a human).
"""
import difflib, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STREET_WORDS = {"dr", "drive", "ave", "avenue", "ct", "court", "cir", "circle", "loop", "way", "rd", "road", "st", "street", "blvd", "ln", "lane", "trl", "trail"}


def load():
    html = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
    m = re.search(r"^var SCOPES = (\[.*?\]);\s*$", html, re.M)
    scopes = json.loads(m.group(1))
    out = []
    for s in scopes:
        if s["turn"] == "DEMO1":
            continue
        num, street = s["h1"].split(" ", 1)
        words = [w for w in re.findall(r"[a-z]+", street.lower()) if w not in STREET_WORDS]
        out.append(dict(s, num=num, words=words))
    return out


def _word_score(token, words):
    return max((difflib.SequenceMatcher(None, token, w).ratio() for w in words), default=0)


def candidates(po, all_jobs=None):
    all_jobs = all_jobs or load()
    po_l = (po or "").lower()
    nums = re.findall(r"\d{3,6}", po_l)
    tokens = [t for t in re.findall(r"[a-z]{3,}", po_l) if t not in STREET_WORDS]
    by_num = [j for j in all_jobs if j["num"] in nums]
    if by_num:
        return by_num
    best, hits = 0.0, []
    for j in all_jobs:
        sc = max((_word_score(t, j["words"]) for t in tokens), default=0)
        if sc >= 0.75:
            if sc > best + 0.05:
                best, hits = sc, [j]
            elif sc >= best - 0.05:
                hits.append(j)
    return hits


def match(po, date_mmddyyyy="", all_jobs=None):
    """-> {"turn","folder","house"} or {"error", "candidates"}"""
    c = candidates(po, all_jobs)
    if len(c) > 1 and date_mmddyyyy:
        mm, dd, yy = date_mmddyyyy.split("/")
        d = f"{yy}-{mm}-{dd}"
        # open on the receipt date = not completed, or completed on/after it
        open_then = [j for j in c if not j["completed"] or (j.get("completedDate") and j["completedDate"] >= d)]
        if open_then:
            c = open_then
        if len(c) > 1:
            # change orders (co=1) share the street with the main job — prefer one still open now
            still = [j for j in c if not j["completed"]]
            if len(still) == 1:
                c = still
    if len(c) == 1:
        j = c[0]
        return {"turn": j["turn"], "folder": j["liveUrl"].strip("/"), "house": j["h1"]}
    return {"error": "no job matches" if not c else "more than one job matches",
            "candidates": [j["turn"] + " " + j["h1"] for j in c]}
