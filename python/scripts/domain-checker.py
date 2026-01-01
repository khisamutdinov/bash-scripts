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
import os
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
    parser.add_argument("output", nargs='?', default=None, help="Path to save results. If omitted, a unique timestamped file is created.")
    parser.add_argument("--delay", type=float, default=1.5, help="Seconds between WHOIS queries (default: 1.5)")

    args = parser.parse_args()

    # --- 1. Refined Path Logic ---
    input_path = os.path.abspath(args.input)
    directory = os.path.dirname(input_path)
    base_name = os.path.splitext(os.path.basename(input_path))[0]

    if args.output:
        # Scenario: User specified a file. OVERRIDE allowed.
        output_path = os.path.abspath(args.output)
    else:
        # Scenario: Default name. Protect with timestamp if exists.
        default_name = f"{base_name}-results.json"
        output_path = os.path.join(directory, default_name)

        if os.path.exists(output_path):
            timestamp = int(time.time())
            output_path = os.path.join(directory, f"{base_name}-results-{timestamp}.json")

    # --- 2. Read Input File ---
    try:
        with open(input_path, "r") as f:
            domains = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Error: Input file '{args.input}' not found.")
        sys.exit(1)

    # --- 3. Process Domains ---
    all_results = []
    available_count = 0
    print(f"Checking {len(domains)} domains. Saving to: {os.path.basename(output_path)}")

    for domain in domains:
        print(f"  > {domain}...", end="\r")
        result = {
            "domain": domain,
            "checked_at": datetime.now().isoformat(),
            "status": "available",
            "details": {}
        }

        if is_active_dns(domain):
            result["status"] = "taken"
            result["details"] = {"method": "dns_resolution"}
        else:
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
                available_count += 1

        all_results.append(result)

    # --- 4. Final Save ---
    with open(output_path, "w") as f:
        json.dump(all_results, f, indent=4)

    print(f"\nFinished! Found {available_count} available domains.")
    print(f"Full report: {output_path}")

if __name__ == "__main__":
    main()
