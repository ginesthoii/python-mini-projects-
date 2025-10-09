#!/usr/bin/env python3
import sys, re, json, argparse
from urllib.parse import urlparse

def sanitize(s: str) -> str:
    s = s.strip()
    if re.match(r'^\w+://', s):
        s = urlparse(s).hostname or s
    s = re.sub(r'[:/].*$', '', s)
    s = re.sub(r'^(www\.)+', '', s, flags=re.IGNORECASE)
    return s.lower()

def rdap_fetch(domain: str, timeout: float = 10.0):
    import requests
    r = requests.get(f"https://rdap.org/domain/{domain}", timeout=timeout)
    if r.status_code == 404:
        return {"available": True}
    r.raise_for_status()
    return r.json()

def summarize_rdap(data: dict, domain: str):
    def ev(action):
        for e in data.get("events") or []:
            if e.get("eventAction") == action:
                return e.get("eventDate")
        return None

    registrar = None
    for ent in data.get("entities") or []:
        if "registrar" in (ent.get("roles") or []):
            v = ent.get("vcardArray") or []
            if len(v) == 2:
                for item in v[1]:
                    if item and item[0] == "fn" and len(item) >= 4:
                        registrar = item[3]

    nameservers = [ns.get("ldhName") for ns in (data.get("nameservers") or []) if ns.get("ldhName")]
    return {
        "source": "rdap.org",
        "domain": (data.get("ldhName") or domain).upper(),
        "registrar": registrar,
        "created": ev("registration"),
        "updated": ev("last changed"),
        "expires": ev("expiration"),
        "nameservers": nameservers,
        "status": data.get("status"),
        "available": False
    }

def legacy_whois(domain: str):
    import whois
    w = whois.whois(domain)
    def to_list(x): return x if isinstance(x, (list, tuple)) else ([x] if x else [])
    def first(x): return to_list(x)[0] if to_list(x) else None
    def iso(x): 
        from datetime import datetime
        if x is None: return None
        if isinstance(x, datetime): return x.isoformat()
        return str(x)
    return {
        "source": "python-whois",
        "domain": (w.get("domain_name") or domain),
        "registrar": w.get("registrar"),
        "created": iso(first(w.get("creation_date"))),
        "updated": iso(first(w.get("updated_date"))),
        "expires": iso(first(w.get("expiration_date"))),
        "nameservers": sorted({ns.upper() for ns in to_list(w.get("name_servers"))}),
        "status": to_list(w.get("status")),
        "available": False
    }

def lookup(domain_raw: str, timeout: float):
    d = sanitize(domain_raw)
    if "." not in d:
        raise ValueError(f"Invalid domain: {domain_raw}")
    # RDAP first
    try:
        data = rdap_fetch(d, timeout=timeout)
        if data.get("available"):
            return {"source": "rdap.org", "domain": d.upper(), "available": True}
        return summarize_rdap(data, d)
    except Exception:
        pass
    # whoisit second (optional)
    try:
        import whoisit
        data = whoisit.domain(d)
        if isinstance(data, dict) and (data.get("ldhName") or data.get("handle")):
            nameservers = [ns.get("ldhName") for ns in (data.get("nameservers") or []) if ns.get("ldhName")]
            return {
                "source": "whoisit",
                "domain": (data.get("ldhName") or d).upper(),
                "registrar": None,
                "created": None, "updated": None, "expires": None,
                "nameservers": nameservers,
                "status": data.get("status"),
                "available": False
            }
    except Exception:
        pass
    # legacy WHOIS last
    return legacy_whois(d)

def main():
    ap = argparse.ArgumentParser(description="Domain RDAP/WHOIS lookup with sane defaults.")
    ap.add_argument("domains", nargs="+", help="domain(s) or URLs")
    ap.add_argument("--json", action="store_true", help="output JSON")
    ap.add_argument("--timeout", type=float, default=10.0, help="HTTP timeout seconds (default 10)")
    args = ap.parse_args()

    results = []
    exit_code = 0
    for dom in args.domains:
        try:
            info = lookup(dom, timeout=args.timeout)
            results.append(info)
            if info.get("available"):  # mark available with special code
                exit_code = max(exit_code, 10)
        except Exception as e:
            results.append({"domain": sanitize(dom).upper(), "error": str(e)})
            exit_code = max(exit_code, 2)

    if args.json:
        print(json.dumps(results if len(results) > 1 else results[0], indent=2))
    else:
        try:
            from rich.table import Table
            from rich.console import Console
            console = Console()
            tbl = Table(show_header=True, header_style="bold")
            tbl.add_column("Domain"); tbl.add_column("Registrar"); tbl.add_column("Created")
            tbl.add_column("Expires"); tbl.add_column("Status"); tbl.add_column("Avail?")
            for r in results:
                if "error" in r:
                    tbl.add_row(r.get("domain","?"), "—", "—", "—", f"ERROR: {r['error']}", "—")
                else:
                    status = ", ".join(r.get("status") or [])[:80]
                    tbl.add_row(
                        r.get("domain","?"),
                        r.get("registrar") or "—",
                        (r.get("created") or "—"),
                        (r.get("expires") or "—"),
                        status or "—",
                        "YES" if r.get("available") else "NO"
                    )
            console.print(tbl)
        except Exception:
            # fallback plain text
            for r in results:
                print(json.dumps(r, indent=2))

    sys.exit(exit_code)

if __name__ == "__main__":
    main()
