#!/usr/bin/env python3
"""Add lat/lng to job records using the free U.S. Census geocoder.

  python3 -I automation/geocode.py jobs.json [cache.json] > jobs_geo.json

Each job needs street/city/state/zip. Sets lat, lng and geo = "exact" | "approx" | "none".
New-construction streets the Census map doesn't have yet get "approx": the
average spot of other jobs in the same ZIP (or city). A cache file avoids
looking up the same address twice.
"""
import json, os, sys, time, urllib.parse, urllib.request

URL = "https://geocoding.geo.census.gov/geocoder/locations/onelineaddress"


def lookup(addr):
    q = urllib.parse.urlencode({"address": addr, "benchmark": "Public_AR_Current", "format": "json"})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(URL + "?" + q, timeout=30) as r:
                m = json.loads(r.read())["result"]["addressMatches"]
            return (m[0]["coordinates"]["y"], m[0]["coordinates"]["x"]) if m else None
        except Exception:
            time.sleep(1 + attempt * 2)
    return None


def main():
    jobs = json.load(open(sys.argv[1]))
    cpath = sys.argv[2] if len(sys.argv) > 2 else None
    cache = json.load(open(cpath)) if cpath and os.path.exists(cpath) else {}
    for j in jobs:
        if j.get("lat") is not None or not j.get("street"):
            continue
        key = f'{j["street"]}, {j.get("city","")}, {j.get("state","FL")} {j.get("zip","")}'.strip().upper()
        if key not in cache:
            cache[key] = lookup(key)
        if cache[key]:
            j["lat"], j["lng"], j["geo"] = cache[key][0], cache[key][1], "exact"
    for j in jobs:  # approximate the rest from neighbours in the same ZIP, then city
        if j.get("lat") is not None:
            continue
        for field in ("zip", "city"):
            near = [o for o in jobs if o.get("geo") == "exact" and j.get(field) and str(o.get(field, "")).upper() == str(j[field]).upper()]
            if near:
                j["lat"] = sum(o["lat"] for o in near) / len(near)
                j["lng"] = sum(o["lng"] for o in near) / len(near)
                j["geo"] = "approx"
                break
        else:
            j["lat"] = j["lng"] = None
            j["geo"] = "none"
    if cpath:
        json.dump(cache, open(cpath, "w"))
    json.dump(jobs, sys.stdout, indent=1)


if __name__ == "__main__":
    main()
