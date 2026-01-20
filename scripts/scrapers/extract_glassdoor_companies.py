#!/usr/bin/env python3
"""
Extract salary ranges by company from Glassdoor HTML page.
"""

import re
import json
import argparse
from pathlib import Path
from bs4 import BeautifulSoup
import pandas as pd


def extract_salary_number(text):
    """Extract numeric salary from text like '$86K' or '$117K'."""
    if not text:
        return None
    
    # Remove $ and any non-numeric characters except K/k
    clean = text.strip().replace('$', '').replace(',', '')
    
    # Handle K notation
    if 'K' in clean or 'k' in clean:
        num_str = clean.replace('K', '').replace('k', '').strip()
        try:
            return int(float(num_str) * 1000)
        except:
            return None
    
    # Try direct conversion
    try:
        return int(float(clean))
    except:
        return None


def extract_companies_from_html(html_path):
    """Extract company salary data from Glassdoor HTML."""
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    soup = BeautifulSoup(html, 'lxml')
    
    companies = []
    
    # Find all salary card items
    salary_items = soup.find_all('div', class_=re.compile('SalariesList_Item'))
    
    print(f"Found {len(salary_items)} salary items")
    
    for idx, item in enumerate(salary_items):
        try:
            # Extract company name
            company_name_elem = item.find('p', class_=re.compile('salary-card_EmployerName'))
            if not company_name_elem:
                continue
            company_name = company_name_elem.get_text(strip=True)
            
            # Extract rating
            rating_elem = item.find('p', class_=re.compile('salary-card_Rating'))
            rating = float(rating_elem.get_text(strip=True)) if rating_elem else None
            
            # Extract total pay range (e.g., "$86K - $117K")
            total_pay_elem = item.find('div', class_=re.compile('salary-card_TotalPay'))
            total_pay = None
            min_pay = None
            max_pay = None
            
            if total_pay_elem:
                total_pay_text = total_pay_elem.get_text(strip=True)
                # Parse range like "$86K - $117K"
                parts = total_pay_text.split('-')
                if len(parts) == 2:
                    min_pay = extract_salary_number(parts[0])
                    max_pay = extract_salary_number(parts[1])
                    total_pay = total_pay_text
            
            # Extract median salary
            median_elem = item.find('div', class_=re.compile('salary-card_BreakdownBold'))
            median_salary = None
            if median_elem:
                median_text = median_elem.get_text(strip=True)
                median_salary = extract_salary_number(median_text)
            
            # Extract job title (should be "AI Engineer")
            job_title_elem = item.find('section', class_=re.compile('salary-card_TitleTrim'))
            job_title = job_title_elem.get_text(strip=True) if job_title_elem else "AI Engineer"
            
            # Extract open jobs count
            open_jobs_elem = item.find('span', class_=re.compile('button_ButtonContent'))
            open_jobs = 0
            if open_jobs_elem:
                open_jobs_text = open_jobs_elem.get_text(strip=True)
                match = re.search(r'(\d+)\s+open', open_jobs_text)
                if match:
                    open_jobs = int(match.group(1))
            
            company_data = {
                'company_name': company_name,
                'rating': rating,
                'job_title': job_title,
                'total_pay_range': total_pay,
                'min_salary_cad': min_pay,
                'max_salary_cad': max_pay,
                'median_salary_cad': median_salary,
                'open_jobs': open_jobs
            }
            
            companies.append(company_data)
            print(f"  {idx+1}. {company_name}: {total_pay} (Median: ${median_salary/1000:.0f}K)" if median_salary else f"  {idx+1}. {company_name}: {total_pay}")
            
        except Exception as e:
            print(f"  Error parsing item {idx}: {e}")
            continue
    
    return companies


def main():
    parser = argparse.ArgumentParser(description='Extract company salaries from Glassdoor HTML')
    parser.add_argument('html_file', help='Path to Glassdoor HTML file')
    parser.add_argument('--location', default='Montreal', help='Location name')
    parser.add_argument('--date', default='2026-01-12', help='Collection date (YYYY-MM-DD)')
    parser.add_argument('--out', default='data/real_data/stat_real_data_companies_montreal.csv',
                       help='Output CSV file')
    parser.add_argument('--json', help='Also save as JSON (optional)')
    
    args = parser.parse_args()
    
    html_path = Path(args.html_file)
    if not html_path.exists():
        print(f"Error: File not found: {html_path}")
        return 1
    
    print(f"\n=== Extracting company salaries from {html_path.name} ===\n")
    
    companies = extract_companies_from_html(html_path)
    
    if not companies:
        print("No companies found!")
        return 1
    
    print(f"\n=== Extracted {len(companies)} companies ===\n")
    
    # Convert to DataFrame
    df = pd.DataFrame(companies)
    
    # Add metadata
    df['location'] = args.location
    df['collection_date'] = args.date
    df['source'] = 'Glassdoor'
    
    # Reorder columns
    cols = ['source', 'collection_date', 'location', 'company_name', 'rating', 
            'job_title', 'total_pay_range', 'min_salary_cad', 'max_salary_cad', 
            'median_salary_cad', 'open_jobs']
    df = df[cols]
    
    # Save CSV
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, index=False)
    print(f"✓ Saved {len(companies)} companies to {out_path}")
    
    # Save JSON if requested
    if args.json:
        json_path = Path(args.json)
        json_path.parent.mkdir(parents=True, exist_ok=True)
        with open(json_path, 'w') as f:
            json.dump(companies, f, indent=2)
        print(f"✓ Saved JSON to {json_path}")
    
    # Print summary statistics
    print(f"\n=== Summary Statistics ===")
    print(f"Total companies: {len(df)}")
    print(f"Average rating: {df['rating'].mean():.2f}" if df['rating'].notna().any() else "")
    print(f"Median salary range: ${df['min_salary_cad'].median()/1000:.0f}K - ${df['max_salary_cad'].median()/1000:.0f}K")
    print(f"Average median salary: ${df['median_salary_cad'].mean()/1000:.0f}K")
    print(f"Total open jobs: {df['open_jobs'].sum()}")
    
    # Top 10 by median salary
    print(f"\n=== Top 10 by Median Salary ===")
    top10 = df.nlargest(10, 'median_salary_cad')[['company_name', 'median_salary_cad', 'rating']]
    for idx, row in top10.iterrows():
        print(f"  {row['company_name']}: ${row['median_salary_cad']/1000:.0f}K (⭐ {row['rating']:.1f})")
    
    return 0


if __name__ == '__main__':
    exit(main())
