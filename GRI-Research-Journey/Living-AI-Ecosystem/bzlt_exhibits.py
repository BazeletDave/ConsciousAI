"""Reproduce GRI BZLT Americas FLA Institutional public-data exhibits.
No dependencies, network, personal data, or side effects. Run in this directory.
"""
import csv
from pathlib import Path

rows = list(csv.DictReader((Path(__file__).parent / "BZLT-Americas-FLA-Institutional-Evidence.csv").open(encoding="utf-8", newline="")))
def value(entity, period, metric):
    matches = [int(r["value"]) for r in rows if r["entity"] == entity and r["period"] == str(period) and r["metric"] == metric]
    assert len(matches) == 1, (entity, period, metric, matches)
    return matches[0]

print("Consolidated issuer revenue, USD millions; not Florida revenue")
for issuer in ("Trulieve", "Curaleaf", "Verano"):
    old = value(issuer, 2024, "net_revenue")
    new = value(issuer, 2025, "net_revenue")
    print(f"{issuer}: 2024={old / 1e6:.3f}, 2025={new / 1e6:.3f}, change={(new / old - 1) * 100:+.2f}%")

yes = value("Florida", 2024, "amendment_3_yes")
no = value("Florida", 2024, "amendment_3_no")
print(f"Florida Amendment 3: yes={yes:,}, no={no:,}, yes share={100 * yes / (yes + no):.2f}%")
assert yes / (yes + no) < .60

sales = value("Colorado", 2025, "marijuana_sales")
receipts = value("Colorado", 2025, "marijuana_tax_fee_revenue")
print(f"Colorado 2025 sales={sales:,}, tax and fee receipts={receipts:,}, descriptive ratio={100 * receipts / sales:.2f}%")
print("Ratio is not a statutory or effective tax rate.")
