#!/usr/bin/env python3
"""
Script to collect real salary data from public sources.
Prioritizes automated collection where possible, provides manual instructions otherwise.
"""
import argparse
import sys
from pathlib import Path

def check_dependencies():
    missing = []
    try:
        import requests
    except ImportError:
        missing.append("requests")
    try:
        import pandas as pd
    except ImportError:
        missing.append("pandas")
    
    if missing:
        print(f"Missing dependencies: {', '.join(missing)}")
        print(f"Install with: pip install {' '.join(missing)}")
        sys.exit(1)

def collect_statcan_data(output_dir: Path):
    """Collect salary data from Statistics Canada public tables."""
    import requests
    import pandas as pd
    
    print("\n=== Statistics Canada Data Collection ===")
    print("Attempting to fetch NOC 21211 (Software engineers) salary data...")
    
    # StatCan wage data by occupation (example table)
    # Note: actual table numbers may vary
    url = "https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1410034001"
    
    print(f"Manual collection required for StatCan.")
    print(f"1. Visit: {url}")
    print(f"2. Filter by NOC 21211, 21231 (Software/Data engineers)")
    print(f"3. Download CSV and save to: {output_dir / 'stat_real_data_statcan.csv'}")
    print(f"4. Expected columns: geography, occupation, year, wages_median, wages_avg")
    
    return False

def collect_glassdoor_instructions(output_dir: Path):
    """Provide instructions for Glassdoor data collection."""
    print("\n=== Glassdoor Data Collection ===")
    print("Manual HTML collection required (Glassdoor blocks automated scraping):")
    print()
    print("Steps:")
    print("1. Visit these URLs in your browser:")
    urls = [
        "https://www.glassdoor.ca/Salaries/montreal-ai-engineer-salary-SRCH_IL.0,8_IM990_KO9,20.htm",
        "https://www.glassdoor.ca/Salaries/toronto-ai-engineer-salary-SRCH_IL.0,7_IM976_KO8,19.htm",
        "https://www.glassdoor.ca/Salaries/vancouver-ai-engineer-salary-SRCH_IL.0,9_IM972_KO10,21.htm",
        "https://www.glassdoor.ca/Salaries/ai-ml-engineer-salary-SRCH_KO0,14.htm"
    ]
    for url in urls:
        print(f"   - {url}")
    
    print("\n2. For each page:")
    print("   - Right-click → Save As → 'Complete Webpage'")
    print("   - Save to: data/glassdoor_pages/")
    print("   - Name files: glassdoor_montreal.html, glassdoor_toronto.html, etc.")
    
    print("\n3. Run the parser:")
    print("   python3 scripts/scrapers/extract_glassdoor_html.py --html-dir data/glassdoor_pages \\")
    print("     --title 'AI Engineer' --location 'Canada' --date 2026-01-12 --currency CAD \\")
    print(f"     --out {output_dir / 'stat_real_data_glassdoor.csv'}")
    
    return False

def collect_levels_fyi_instructions(output_dir: Path):
    """Provide instructions for Levels.fyi data collection."""
    print("\n=== Levels.fyi Data Collection ===")
    print("Manual export required:")
    print()
    print("Steps:")
    print("1. Visit: https://www.levels.fyi/t/software-engineer/locations/canada")
    print("2. Apply filters:")
    print("   - Location: Montreal, Toronto, Vancouver")
    print("   - Title: Software Engineer, AI/ML Engineer")
    print("   - Company: (your choice)")
    print("3. Click 'Export' or copy table data")
    print("4. Save as CSV with columns:")
    print("   company,title,level,location,yoe,base_cad,bonus_cad,stock_cad,total_cad,date")
    print(f"5. Save to: {output_dir / 'stat_real_data_levels.csv'}")
    
    return False

def collect_linkedin_instructions(output_dir: Path):
    """Provide instructions for LinkedIn job postings data."""
    print("\n=== LinkedIn Jobs Timeline Collection ===")
    print("Manual tracking required:")
    print()
    print("Approach 1 - Manual search:")
    print("1. Search 'AI Engineer' + 'Machine Learning Engineer' on LinkedIn Jobs")
    print("2. Filter: Canada, Posted in last month")
    print("3. Record count monthly")
    print("4. Create CSV with columns: month,role_filter,location,postings_count")
    print(f"5. Save to: {output_dir / 'stat_real_data_jobs_timeline.csv'}")
    print()
    print("Approach 2 - Use existing market reports:")
    print("- AI Index Report (Stanford): https://aiindex.stanford.edu/")
    print("- Burning Glass / Lightcast labor market data")
    
    return False

def main():
    parser = argparse.ArgumentParser(description="Collect real salary data for AI Salary Dashboard")
    parser.add_argument("--source", choices=["all", "statcan", "glassdoor", "levels", "linkedin"],
                       default="all", help="Data source to collect")
    parser.add_argument("--output-dir", default="data/real_data", help="Output directory for real data")
    args = parser.parse_args()
    
    check_dependencies()
    
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("=" * 70)
    print("AI Salary Dashboard - Real Data Collection")
    print("=" * 70)
    
    sources = {
        "statcan": collect_statcan_data,
        "glassdoor": collect_glassdoor_instructions,
        "levels": collect_levels_fyi_instructions,
        "linkedin": collect_linkedin_instructions
    }
    
    if args.source == "all":
        for name, func in sources.items():
            func(output_dir)
    else:
        sources[args.source](output_dir)
    
    print("\n" + "=" * 70)
    print("Next Steps:")
    print("=" * 70)
    print(f"1. Follow instructions above to populate: {output_dir}/")
    print("2. Run: python3 scripts/generators/regenerate_all_charts.py --use-real-data")
    print("3. Refresh your dashboard to see real data")
    print()

if __name__ == "__main__":
    main()
