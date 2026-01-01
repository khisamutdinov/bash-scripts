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
import re
from datetime import datetime

# Common "High Value" dictionary words for tech/business
PREMIUM_KEYWORDS = {
    'ai', 'tech', 'app', 'pay', 'cloud', 'dev', 'data', 'web', 'link',
    'smart', 'fast', 'pro', 'go', 'get', 'my', 'the', 'best', 'shop'
}

def predict_premium(domain):
    """
    Heuristically predicts if a domain might be premium.
    Checks for length, character types, and specific keywords.
    """
    name = domain.split('.')[0]
    tld = domain.split('.')[-1]

    reasons = []

    # 1. Length Check (Very short is almost always premium)
    if len(name) <= 3:
        reasons.append("Ultra-short (<= 3 chars)")
    elif len(name) <= 5:
        reasons.append("Short name (<= 5 chars)")

    # 2. Character Complexity (No numbers/hyphens is higher value)
    if name.isalpha():
        if len(name) < 7:
            reasons.append("Pure alphabetic short-name")

    # 3. Keyword Check
    if any(kw in name.lower() for kw in PREMIUM_KEYWORDS):
        reasons.append("Contains high-value keyword")

    # 4. TLD Value
    if tld in ['ai', 'io', 'com', 'app']:
        if len(name) < 6:
            reasons.append(f"High-demand TLD (.{tld}) with short name")

    return reasons

def is_active_dns(domain):
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
    try:
        w = whois.whois(domain)
        if w.registrar or w.creation_date:
            return {"registered": True, "registrar": w.registrar}
        return {"registered": False}
    except Exception:
        return {"registered": False}

def main():
    parser = argparse.ArgumentParser(description="Bulk Domain Checker with Premium Prediction")
    parser.add_argument("input", help="Input text file")
    parser.add_argument("output", nargs='?', default=None, help="Output JSON file")
    parser.add_argument("--delay", type=float, default=1.5, help="Delay between WHOIS queries")

    args = parser.parse_args()

    input_path = os.path.abspath(args.input)
    directory = os.path.dirname(input_path)
    base_name = os.path.splitext(os.path.basename(input_path))[0]

    if args.output:
        output_path = os.path.abspath(args.output)
    else:
        output_path = os.path.join(directory, f"{base_name}-results.json")
        if os.path.exists(output_path):
            output_path = os.path.join(directory, f"{base_name}-results-{int(time.time())}.json")

    try:
        with open(input_path, "r") as f:
            domains = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Error: {args.input} not found.")
        sys.exit(1)

    all_results = []
    print(f"Analyzing {len(domains)} domains...")

    for domain in domains:
        print(f"  > Processing: {domain}...", end="\r")

        result = {
            "domain": domain,
            "status": "available",
            "premium_prediction": {"is_likely_premium": False, "reasons": []}
        }

        if is_active_dns(domain):
            result["status"] = "taken"
        else:
            time.sleep(args.delay)
            whois_data = check_whois(domain)
            if whois_data["registered"]:
                result["status"] = "taken"
            else:
                # Predictive Logic for Available Domains
                reasons = predict_premium(domain)
                if reasons:
                    result["premium_prediction"] = {
                        "is_likely_premium": True,
                        "reasons": reasons
                    }

        all_results.append(result)

    with open(output_path, "w") as f:
        json.dump(all_results, f, indent=4)

    print(f"\nDone! Results saved to {os.path.basename(output_path)}")

if __name__ == "__main__":
    main()
