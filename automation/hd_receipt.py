#!/usr/bin/env python3
"""Pull a Home Depot e-receipt PDF out of a Gmail RAW message and read it.

  python3 -I automation/hd_receipt.py <gmail-raw.json | message.eml> [--save-pdf out.pdf]

Prints JSON: order, date, po (the "PO / Job Name" typed at checkout), total,
subtotal, tax, items, and the matching job (see jobs.py) when one is clear.
"""
import base64, email, json, os, re, subprocess, sys, tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import jobs


def load_pdf(path):
    data = open(path, "rb").read()
    if data.lstrip().startswith(b"{"):
        raw = json.loads(data)["raw"]
        raw += "=" * (-len(raw) % 4)
        data = base64.urlsafe_b64decode(raw)
    msg = email.message_from_bytes(data)
    for part in msg.walk():
        if part.get_content_type() == "application/pdf" or (part.get_filename() or "").lower().endswith(".pdf"):
            return part.get_payload(decode=True), part.get_filename() or "receipt.pdf"
    raise SystemExit("no PDF attachment in " + path)


def money(s):
    return float(s.replace("$", "").replace(",", ""))


def parse(text):
    def grab(rx, default=""):
        m = re.search(rx, text)
        return m.group(1).strip() if m else default
    out = {
        "order": grab(r"Order #\s*(H?\d{4}-\d+)"),
        "date": grab(r"(\d{2}/\d{2}/\d{4}),\s*\d"),
        "store": grab(r"Location\s+(.+)"),
        "po": grab(r"PO / Job Name\s*(.*)"),
        "subtotal": money(grab(r"Subtotal\s+(-?\$[\d,]+\.\d\d)", "0")),
        "tax": money(grab(r"Sales Tax\s+(-?\$[\d,]+\.\d\d)", "0")),
        "total": money(grab(r"Order Total\s+(-?\$[\d,]+\.\d\d)", "0")),
        "items": [],
    }
    for m in re.finditer(r"^\s*\d\d\s{2,}(.+?)\s{2,}\S+\s+\d+\s+\$([\d,]+\.\d\d)\s*/\s*\w+\s+(\d+)\s+\$([\d,]+\.\d\d)", text, re.M):
        out["items"].append({"desc": m.group(1).strip(), "qty": int(m.group(3)), "amount": money(m.group(4))})
    return out


def main():
    args = sys.argv[1:]
    save = None
    if "--save-pdf" in args:
        i = args.index("--save-pdf"); save = args[i + 1]; del args[i:i + 2]
    pdf, name = load_pdf(args[0])
    with tempfile.NamedTemporaryFile(suffix=".pdf") as f:
        f.write(pdf); f.flush()
        text = subprocess.run(["pdftotext", "-layout", f.name, "-"], capture_output=True, text=True, check=True).stdout
    r = parse(text)
    r["pdf_name"] = name
    r["match"] = jobs.match(r["po"], r["date"])
    if save:
        open(save, "wb").write(pdf)
    print(json.dumps(r, indent=1))


if __name__ == "__main__":
    main()
