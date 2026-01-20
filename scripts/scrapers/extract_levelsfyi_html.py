#!/usr/bin/env python3
"""
Extract comprehensive salary data from Levels.fyi HTML pages.
Levels.fyi data includes:
- Company names
- Roles/Titles  
- Levels (L3-L8, Staff, Principal, etc.)
- Locations
- Total Compensation breakdown (Base + Stock + Bonus)
- Years of experience estimates
"""

import re
import json
from pathlib import Path
from bs4 import BeautifulSoup
import pandas as pd
import argparse


def extract_salary_numbers(text):
    """Extract all salary numbers from text."""
    if not text:
        return []
    
    # Pattern: $123K or 123,456 or 123K
    pattern = r'[\$]?([\d,]+\.?\d*)[KkM]?'
    matches = re.findall(pattern, str(text))
    
    numbers = []
    for match in matches:
        try:
            num_str = match.replace(',', '')
            if 'K' in str(text) or 'k' in str(text):
                num = int(float(num_str) * 1000)
            elif 'M' in str(text):
                num = int(float(num_str) * 1000000)
            else:
                num = int(float(num_str))
            
            if 50000 <= num <= 500000:  # Reasonable salary range
                numbers.append(num)
        except:
            pass
    
    return numbers


def extract_levelsfyi_data(html_path):
    """Extract all available data from Levels.fyi HTML."""
    
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    soup = BeautifulSoup(html, 'lxml')
    
    data = {
        'page_title': None,
        'companies': [],
        'total_compensation_data': [],
        'salary_ranges': []
    }
    
    # Extract page title
    title_tag = soup.find('title')
    if title_tag:
        data['page_title'] = title_tag.get_text(strip=True)
    
    # Method 1: Extract from text content (robust for JS-rendered pages)
    all_text = soup.get_text()
    
    # Look for company names (often in capital letters)
    company_pattern = r'(Google|Meta|Amazon|Microsoft|Apple|Netflix|Uber|Stripe|Airbnb|Twitter|Salesforce|Adobe|Intel|IBM|Nvidia|Shopify|Snap|Square|Twilio|Coinbase|Roblox|Databricks|Instacart|Palantir|Discord|Slack|GitHub|GitLab|HashiCorp|Datadog|Figma|Notion|Retool|Loom|Amplitude|Segment|Mixpanel)'
    
    companies_found = set(re.findall(company_pattern, all_text, re.IGNORECASE))
    data['companies'] = sorted(list(companies_found))
    
    # Method 2: Look for compensation patterns
    # Pattern: "Base: $XXX   Stock: $XXX   Bonus: $XXX"
    comp_pattern = r'(\$[\d,]+[KM]?).*?(\$[\d,]+[KM]?).*?(\$[\d,]+[KM]?)'
    
    for match in re.finditer(comp_pattern, all_text):
        try:
            parts = match.groups()
            salaries = [extract_salary_numbers(p)[0] if extract_salary_numbers(p) else 0 for p in parts]
            if any(salaries) and sum(salaries) > 100000:
                data['total_compensation_data'].append({
                    'base': salaries[0],
                    'stock': salaries[1],
                    'bonus': salaries[2],
                    'total': sum(salaries)
                })
        except:
            pass
    
    # Method 3: Extract salary ranges and numbers
    salary_numbers = []
    salary_pattern = r'\$?([\d,]+)(?:[KkM])?(?:\s*-\s*\$?([\d,]+))?'
    
    for match in re.finditer(salary_pattern, all_text):
        try:
            min_str = match.group(1).replace(',', '')
            if match.group(2):
                max_str = match.group(2).replace(',', '')
            else:
                max_str = min_str
            
            min_val = int(float(min_str) * 1000 if 'K' in match.group(0) or 'k' in match.group(0) else int(float(min_str)))
            max_val = int(float(max_str) * 1000 if 'K' in match.group(0) or 'k' in match.group(0) else int(float(max_str)))
            
            if 50000 <= min_val <= 500000:
                salary_numbers.append((min_val, max_val))
        except:
            pass
    
    # Deduplicate salary ranges
    salary_numbers = list(set(salary_numbers))
    data['salary_ranges'] = [{'min': s[0], 'max': s[1], 'avg': (s[0] + s[1]) // 2} for s in sorted(salary_numbers)]
    
    # Method 4: Look for level indicators
    levels_found = re.findall(r'\b(L[3-8]|IC[3-8]|Senior|Staff|Principal|Director|Executive)\b', all_text, re.IGNORECASE)
    data['levels'] = list(set(levels_found))
    
    # Method 5: Extract locations
    locations_pattern = r'(Toronto|Vancouver|Montreal|Calgary|Ottawa|Seattle|San Francisco|New York|London|Singapore|Toronto ON|Vancouver BC)'
    locations_found = re.findall(locations_pattern, all_text, re.IGNORECASE)
    data['locations'] = list(set(locations_found))
    
    return data


def generate_levelsfyi_summary_csv(html_path, output_csv):
    """Generate a CSV with aggregate Levels.fyi data."""
    
    extracted = extract_levelsfyi_data(html_path)
    
    records = []
    
    # Create one record per company with aggregated data
    for company in extracted['companies']:
        records.append({
            'source': 'Levels.fyi',
            'company_name': company,
            'job_title': 'AI Engineer / ML Engineer (estimate)',
            'data_type': 'Aggregate from Levels.fyi page',
            'salary_ranges_found': len(extracted['salary_ranges']),
            'avg_salary_usd': int(sum([r['avg'] for r in extracted['salary_ranges']]) / len(extracted['salary_ranges'])) if extracted['salary_ranges'] else None,
            'min_salary_usd': min([r['min'] for r in extracted['salary_ranges']]) if extracted['salary_ranges'] else None,
            'max_salary_usd': max([r['max'] for r in extracted['salary_ranges']]) if extracted['salary_ranges'] else None,
            'locations': ', '.join(extracted['locations'][:3]),  # Top 3
            'levels_found': ', '.join(extracted['levels'][:3]),
        })
    
    if not records:
        # If no companies found, create a generic summary
        records.append({
            'source': 'Levels.fyi',
            'company_name': 'Multiple Companies',
            'job_title': 'AI Engineer / ML Engineer',
            'data_type': 'Summary from Levels.fyi page',
            'salary_ranges_found': len(extracted['salary_ranges']),
            'avg_salary_usd': int(sum([r['avg'] for r in extracted['salary_ranges']]) / len(extracted['salary_ranges'])) if extracted['salary_ranges'] else None,
            'min_salary_usd': min([r['min'] for r in extracted['salary_ranges']]) if extracted['salary_ranges'] else None,
            'max_salary_usd': max([r['max'] for r in extracted['salary_ranges']]) if extracted['salary_ranges'] else None,
            'locations': ', '.join(extracted['locations']),
            'levels_found': ', '.join(extracted['levels']),
        })
    
    df = pd.DataFrame(records)
    df.to_csv(output_csv, index=False)
    
    return df, extracted


def main():
    parser = argparse.ArgumentParser(description='Extract salary data from Levels.fyi HTML')
    parser.add_argument('--html', required=True, help='Path to Levels.fyi HTML file')
    parser.add_argument('--out', default='data/real_data/stat_real_data_levelsfyi_aggregate.csv',
                       help='Output CSV file')
    parser.add_argument('--json', help='Also save detailed JSON extraction')
    
    args = parser.parse_args()
    
    html_path = Path(args.html)
    if not html_path.exists():
        print(f"❌ Error: {html_path} not found")
        return 1
    
    print(f"\n{'='*70}")
    print(f"  Extracting Levels.fyi data from: {html_path.name}")
    print(f"{'='*70}\n")
    
    # Extract data
    df, extracted = generate_levelsfyi_summary_csv(html_path, args.out)
    
    # Save CSV
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    print(f"✅ Saved aggregate CSV: {out_path}")
    
    # Save JSON if requested
    if args.json:
        json_path = Path(args.json)
        json_path.parent.mkdir(parents=True, exist_ok=True)
        with open(json_path, 'w') as f:
            json.dump(extracted, f, indent=2, default=str)
        print(f"✅ Saved detailed JSON: {json_path}")
    
    # Print summary
    print(f"\n{'='*70}")
    print(f"  Summary Statistics")
    print(f"{'='*70}\n")
    
    print(f"Page Title: {extracted['page_title']}")
    print(f"\n📊 Companies Found: {len(extracted['companies'])}")
    if extracted['companies']:
        for company in sorted(extracted['companies'])[:10]:
            print(f"  • {company}")
        if len(extracted['companies']) > 10:
            print(f"  ... and {len(extracted['companies']) - 10} more")
    
    print(f"\n💰 Salary Ranges Found: {len(extracted['salary_ranges'])}")
    if extracted['salary_ranges']:
        sorted_ranges = sorted(extracted['salary_ranges'], key=lambda x: x['avg'])
        print(f"  Min: ${sorted_ranges[0]['min']:,} USD")
        print(f"  Median: ${sorted_ranges[len(sorted_ranges)//2]['avg']:,} USD")
        print(f"  Max: ${sorted_ranges[-1]['max']:,} USD")
    
    print(f"\n🎯 Levels Found: {', '.join(extracted['levels']) if extracted['levels'] else 'None detected'}")
    
    print(f"\n📍 Locations Found: {', '.join(extracted['locations']) if extracted['locations'] else 'None detected'}")
    
    print(f"\n📋 Compensation Components Found: {len(extracted['total_compensation_data'])}")
    if extracted['total_compensation_data']:
        avg_total = sum([c['total'] for c in extracted['total_compensation_data']]) / len(extracted['total_compensation_data'])
        print(f"  Avg Total Compensation: ${int(avg_total):,} USD")
    
    print(f"\n{'='*70}\n")
    
    return 0


if __name__ == '__main__':
    exit(main())
