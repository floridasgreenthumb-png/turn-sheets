#!/usr/bin/env python3
"""Turn a Coupa "invoice report" export into the payments Progress made.

  python3 -I automation/coupa_payments.py <gmail-raw.json | report.zip | .xlsx> \
      [--from 2026-01-01] [--to 2026-10-07] > payments.json

Coupa's export (Invoices page -> Export, arrives as "Your Coupa invoice
report" with invoice_header_list.zip) lists each invoice with a Paid flag and
"Payment# Domestic ACH - #204930 on 05/26/2026 for USD 245.00" lines. This
groups those lines by payment number into one payment each, oldest first:
  {"payment_no", "method", "date", "total", "invoices": [{"doc", "amount", "invoice_date"}]}
Duplicate lines (Coupa repeats some) are dropped. No financial data is kept here.
"""
import base64, datetime, email, io, json, re, sys, zipfile
from collections import OrderedDict

import openpyxl

PAT = re.compile(r"Payment#\s*(.*?)\s*-?\s*#?\s*(\d+)\s+on\s+(\d\d/\d\d/\d{4})\s+for\s+USD\s+([\d,]+\.\d\d)")


def load_xlsx(path):
    data = open(path, "rb").read()
    if data.lstrip().startswith(b"{"):
        raw = json.loads(data)["raw"]
        raw += "=" * (-len(raw) % 4)
        msg = email.message_from_bytes(base64.urlsafe_b64decode(raw))
        data = next(p.get_payload(decode=True) for p in msg.walk() if (p.get_filename() or "").endswith(".zip"))
    if data[:2] == b"PK" and not path.endswith(".xlsx"):
        z = zipfile.ZipFile(io.BytesIO(data))
        data = z.read(next(n for n in z.namelist() if n.endswith(".xlsx")))
    return openpyxl.load_workbook(io.BytesIO(data), read_only=True).active


def main():
    a = sys.argv[1:]
    opt = lambda k, d: a[a.index(k) + 1] if k in a else d
    lo = opt("--from", "2000-01-01")
    hi = opt("--to", datetime.date.today().isoformat())
    rows = list(load_xlsx(a[0]).iter_rows(values_only=True))
    head = rows[0]
    col = {h: i for i, h in enumerate(head)}
    pays = OrderedDict()
    for r in rows[1:]:
        if not r[col["Paid"]] or r[col["Invoice #"]] in ("", None):
            continue
        inv_date = datetime.datetime.strptime(r[col["Invoice Date"]], "%m/%d/%y").date().isoformat()
        seen = set()
        for m in PAT.finditer(r[col["Payment Information"]] or ""):
            key = m.group(0)
            if key in seen:
                continue
            seen.add(key)
            method, no, d, amt = m.group(1).strip(), m.group(2), m.group(3), float(m.group(4).replace(",", ""))
            d = datetime.datetime.strptime(d, "%m/%d/%Y").date().isoformat()
            p = pays.setdefault(no, {"payment_no": no, "method": method, "date": d, "total": 0.0, "invoices": []})
            p["invoices"].append({"doc": str(r[col["Invoice #"]]), "amount": amt, "invoice_date": inv_date})
            p["total"] = round(p["total"] + amt, 2)
    out = sorted((p for p in pays.values() if lo <= p["date"] <= hi), key=lambda p: (p["date"], p["payment_no"]))
    json.dump(out, sys.stdout, indent=1)


if __name__ == "__main__":
    main()
