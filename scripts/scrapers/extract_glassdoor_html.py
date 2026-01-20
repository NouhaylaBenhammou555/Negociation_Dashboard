import argparse
import csv
import re
from pathlib import Path

try:
    from bs4 import BeautifulSoup
except ImportError:  # pragma: no cover
    raise SystemExit("Please install beautifulsoup4: pip install beautifulsoup4")


def parse_amount(raw: str) -> float | None:
    if not raw:
        return None
    m = re.search(r"([\d.,]+)\s*([kK]?)", raw)
    if not m:
        return None
    num = m.group(1).replace(",", "")
    try:
        val = float(num)
    except ValueError:
        return None
    if m.group(2).lower() == "k":
        val *= 1000
    return val


def extract_percentile(text: str, labels: list[str]) -> float | None:
    for lab in labels:
        pattern = rf"{lab}[^$£€]*([$£€]?[\d.,]+\s*[kK]?)"
        m = re.search(pattern, text, flags=re.IGNORECASE)
        if m:
            amt = parse_amount(m.group(1))
            if amt:
                return amt
    return None


def extract_median(text: str) -> float | None:
    patterns = [r"median[^$£€]*([$£€]?[\d.,]+\s*[kK]?)", r"average base pay[^$£€]*([$£€]?[\d.,]+\s*[kK]?)"]
    for pat in patterns:
        m = re.search(pat, text, flags=re.IGNORECASE)
        if m:
            amt = parse_amount(m.group(1))
            if amt:
                return amt
    return None


def extract_all_numbers(text: str) -> list[float]:
    nums = []
    for m in re.finditer(r"[$£€]?\s*([\d.,]+\s*[kK]?)", text):
        amt = parse_amount(m.group(1))
        if amt:
            nums.append(amt)
    return nums


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract Glassdoor salary percentiles from saved HTML page(s).")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("html_path", nargs='?', help="Path to a saved Glassdoor salaries HTML page")
    group.add_argument("--html-dir", dest="html_dir", help="Directory containing saved Glassdoor HTML pages (*.html)")
    parser.add_argument("--title", default="AI Engineer", help="Role title")
    parser.add_argument("--location", default="Montreal", help="Location label")
    parser.add_argument("--date", default="2025-12-31", help="Date for the snapshot (YYYY-MM-DD)")
    parser.add_argument("--currency", default="CAD", help="Currency code")
    parser.add_argument("--out", default="data/salaries_glassdoor.csv", help="Output CSV path")
    args = parser.parse_args()

    def process_one(html_file: Path):
        text = html_file.read_text(encoding="utf-8", errors="ignore")
        soup = BeautifulSoup(text, "html.parser")
        flat = soup.get_text(" ", strip=True)

        p10 = extract_percentile(flat, ["10th", "10%", "10 percentile"])
        p25 = extract_percentile(flat, ["25th", "25%", "25 percentile", "low end"])
        p50 = extract_percentile(flat, ["50th", "50%", "median", "middle", "typical"])
        p75 = extract_percentile(flat, ["75th", "75%", "75 percentile", "high end"])
        p90 = extract_percentile(flat, ["90th", "90%", "90 percentile", "top"])

        if p50 is None:
            p50 = extract_median(flat)

        # Fallback: if only three numbers present, map to p25/p50/p75 heuristically
        nums = extract_all_numbers(flat)
        if not any([p10, p25, p50, p75, p90]) and len(nums) >= 3:
            nums_sorted = sorted(nums)
            p25 = nums_sorted[0]
            p50 = nums_sorted[len(nums_sorted)//2]
            p75 = nums_sorted[-1]

        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)

        exists = out_path.exists()
        with out_path.open("a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if not exists:
                writer.writerow(["source","date","title","location","p10_cad","p25_cad","p50_cad","p75_cad","p90_cad","currency"])
            writer.writerow([
                "Glassdoor",
                args.date,
                args.title,
                args.location,
                p10 or "",
                p25 or "",
                p50 or "",
                p75 or "",
                p90 or "",
                args.currency
            ])

        print(f"Parsed {html_file.name} → {out_path}")

    if args.html_dir:
        html_dir = Path(args.html_dir)
        if not html_dir.exists():
            raise SystemExit(f"Directory not found: {html_dir}")
        files = sorted(html_dir.glob("*.html"))
        if not files:
            raise SystemExit(f"No .html files in {html_dir}")
        for f in files:
            process_one(f)
    else:
        html_path = Path(args.html_path)
        if not html_path.exists():
            raise SystemExit(f"HTML file not found: {html_path}")
        process_one(html_path)


if __name__ == "__main__":
    main()
