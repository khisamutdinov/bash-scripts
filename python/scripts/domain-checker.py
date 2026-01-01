# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "python-whois",
#     "dnspython",
# ]
# ///

import json
import time
import dns.resolver
import whois
import argparse
import sys
from datetime import datetime

def is_active_dns(domain):
    """Fast check: does the domain resolve to an IP or Mail server?"""
    try:
        dns.resolver.resolve(domain, 'A', lifetime=2)
        return True
    except:
        try:
            dns.resolver.resolve(domain, 'MX', lifetime=2)
            return True
        except:
            return False

def check_whois(domain):
    """Slower check: queries WHOIS database for registration records."""
    try:
        w = whois.whois(domain)
        if w.registrar or w.creation_date:
            return {
                "registered": True,
                "registrar": w.registrar,
                "creation_date": str(w.creation_date[0] if isinstance(w.creation_date, list) else w.creation_date)
            }
        return {"registered": False}
    except Exception:
        return {"registered": False}

def main():
    parser = argparse.ArgumentParser(description="Bulk Domain Availability Checker (DNS + WHOIS)")
    parser.add_argument("input", help="Path to input text file (one domain per line)")
    parser.add_argument("output", help="Path to save results (JSON format)")
    parser.add_argument("--delay", type=float, default=1.5, help="Seconds between WHOIS queries (default: 1.5)")

    args = parser.parse_args()

    try:
        with open(args.input, "r") as f:
            domains = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Error: Input file '{args.input}' not found.")
        sys.exit(1)

    all_results = []
    print(f"Checking {len(domains)} domains. Outputting to {args.output}...")

    for domain in domains:
        print(f"  > {domain}...", end="\r")
        result = {
            "domain": domain,
            "checked_at": datetime.now().isoformat(),
            "status": "available",
            "details": {}
        }

        # Step 1: DNS Check
        if is_active_dns(domain):
            result["status"] = "taken"
            result["details"] = {"method": "dns_resolution"}
        else:
            # Step 2: WHOIS Check
            time.sleep(args.delay)
            whois_data = check_whois(domain)
            if whois_data["registered"]:
                result["status"] = "taken"
                result["details"] = {
                    "method": "whois_query",
                    "registrar": whois_data.get("registrar"),
                    "created": whois_data.get("creation_date")
                }
            else:
                result["status"] = "available"
                result["details"] = {"method": "whois_query"}

        all_results.append(result)

    with open(args.output, "w") as f:
        json.dump(all_results, f, indent=4)

    print(f"\nSuccess: Results saved to {args.output}")

if __name__ == "__main__":
    main()
