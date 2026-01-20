#!/usr/bin/env python3
"""
Extract individual salary records from Levels.fyi HTML pages.

Each record contains:
- Company name
- Location (City, Province, Country)
- Level (L1-L8, Senior, Associate, etc.)
- Job title / Tag
- Years of experience (total + at company)
- Total compensation
- Breakdown: Base | Stock | Bonus
- Date posted
"""

import re
import argparse
from pathlib import Path
from bs4 import BeautifulSoup
import pandas as pd
from typing import List, Dict


def parse_salary_string(salary_text):
    """Parse salary with possible breakdown.
    Examples:
    - "71 000 $CA"
    - "214 000 $CA" 
    - "120 k | N/A | N/A"
    - "107 k | 5 k | 10 k"
    - "875,5 k $CA includes Equity"
    """
    if not salary_text:
        return None, None, None, None
    
    # Remove currency markers and clean up
    text = salary_text.replace('$CA', '').replace('$', '').replace(',', '.').strip()
    
    # Check if has breakdown (| separated)
    if '|' in text:
        parts = [p.strip() for p in text.split('|')]
        try:
            total = int(float(parts[0].replace('k', '').replace('K', '').strip()) * 1000) if parts[0] and 'N/A' not in parts[0] else None
            base = int(float(parts[1].replace('k', '').replace('K', '').strip()) * 1000) if len(parts) > 1 and parts[1] and 'N/A' not in parts[1] else None
            stock = int(float(parts[2].replace('k', '').replace('K', '').strip()) * 1000) if len(parts) > 2 and parts[2] and 'N/A' not in parts[2] else None
            bonus = int(float(parts[3].replace('k', '').replace('K', '').strip()) * 1000) if len(parts) > 3 and parts[3] and 'N/A' not in parts[3] else None
            
            # If total not provided but have base, calculate
            if not total and base:
                total = (base or 0) + (stock or 0) + (bonus or 0)
            
            return total, base, stock, bonus
        except:
            pass
    
    # Single number (just total)
    try:
        match = re.search(r'([\d.]+)\s*[k|K]?', text)
        if match:
            total = int(float(match.group(1)) * 1000)
            return total, None, None, None
    except:
        pass
    
    return None, None, None, None


def parse_experience(exp_text):
    """Parse experience text like '2 yrs' or '2 yrs / 1 yr at company'."""
    if not exp_text:
        return None, None
    
    # Extract numbers
    numbers = re.findall(r'(\d+)', exp_text)
    
    if len(numbers) >= 2:
        return int(numbers[0]), int(numbers[1])  # total, at_company
    elif len(numbers) == 1:
        return int(numbers[0]), None
    
    return None, None


def extract_levelsfyi_records(html_path) -> List[Dict]:
    """Extract individual salary records from Levels.fyi HTML."""
    
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    soup = BeautifulSoup(html, 'lxml')
    
    records = []
    
    # Method 1: Look for structured tables/lists
    # Levels.fyi uses various selectors, try multiple patterns
    
    # Look for rows that contain salary data
    potential_rows = soup.find_all(['tr', 'div'], class_=re.compile(r'row|item|record|salary|entry', re.I))
    
    # Also look for company names followed by location and salary
    text = soup.get_text()
    
    # Parse line by line, looking for company + location + level + salary patterns
    lines = text.split('\n')
    
    current_record = {}
    
    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue
        
        # Company names to match
        company_keywords = [
            'Synechron', 'Matador', 'Zapier', 'Intact', 'ETS', 'Hightouch', 
            'Guidepoint', 'Tecsys', 'Chubb', 'Dialpad', 'Google', 'Meta', 'Amazon',
            'Microsoft', 'Apple', 'Netflix', 'Stripe', 'Airbnb', 'Uber', 'Shopify'
        ]
        
        # Check if this line contains a company name
        company_found = None
        for company in company_keywords:
            if company.lower() in line.lower():
                company_found = company
                break
        
        if company_found:
            current_record['company'] = company_found
        
        # Location patterns (City, Province, Country)
        location_match = re.search(
            r'([A-Za-z\s]+),\s*([A-Z]{2}),\s*Canada|([A-Za-z\s]+),\s*ON|([A-Za-z\s]+),\s*QC|Remote',
            line
        )
        if location_match:
            if 'Remote' in line:
                current_record['location'] = 'Remote'
            elif location_match.group(1):
                current_record['location'] = f"{location_match.group(1).strip()}, {location_match.group(2)}, Canada"
            else:
                current_record['location'] = line
        
        # Level detection (L1-L8, Senior, Associate, etc.)
        level_match = re.search(r'\b(L[1-8]|Senior|Junior|Associate|Staff|Principal|Director)\b', line, re.I)
        if level_match:
            current_record['level'] = level_match.group(1)
        
        # Job title / tag (ML / AI, Software Engineer, etc.)
        if 'ML' in line or 'AI' in line or 'Machine Learning' in line:
            current_record['job_title'] = 'ML / AI Engineer'
        elif 'Software Engineer' in line:
            current_record['job_title'] = 'Software Engineer'
        
        # Experience pattern
        exp_match = re.search(r'(\d+)\s*yrs?(?:\s+.*?(\d+)\s*yrs?)?', line, re.I)
        if exp_match:
            total_exp = int(exp_match.group(1))
            company_exp = int(exp_match.group(2)) if exp_match.group(2) else None
            current_record['total_experience_years'] = total_exp
            if company_exp:
                current_record['company_experience_years'] = company_exp
        
        # Salary patterns
        salary_match = re.search(r'(\d+\s*\d*)\s*(?:\$|k|K)?(?:\s*CAD?|\s*USD?)?\s*(?:includes?\s+Equity)?', line)
        if salary_match and len(current_record) > 2:  # Only if we have some context
            salary_str = line
            total, base, stock, bonus = parse_salary_string(salary_str)
            
            if total:
                current_record['total_compensation_cad'] = total
                current_record['base_salary_cad'] = base
                current_record['stock_cad'] = stock
                current_record['bonus_cad'] = bonus
                
                # If we have a complete record, save it
                if 'company' in current_record and 'location' in current_record:
                    current_record['source'] = 'Levels.fyi'
                    current_record['collection_date'] = '2026-01-12'
                    records.append(current_record.copy())
                    current_record = {}
    
    # Method 2: More robust line-by-line parsing of visible records
    # Parse the text looking for the exact pattern shown by user
    
    pattern = r'([A-Za-z\s\.]+?)\s+([A-Za-z]+(?:\s+[A-Za-z]+)?),\s*([A-Z]{2}),\s*Canada\s*\|\s*([^|]+)\s+(L[0-9]|Senior|Junior|Associate)?[^|]*\s+(ML\s*/\s*AI)?[^|]*(\d+)\s*yrs?\s+(\d+)\s*yrs?\s+(\d+\s*\d*\s*\d*)\s*\$CA'
    
    for match in re.finditer(pattern, text):
        try:
            record = {
                'source': 'Levels.fyi',
                'collection_date': '2026-01-12',
                'company': match.group(1).strip(),
                'city': match.group(2).strip(),
                'province': match.group(3).strip(),
                'country': 'Canada',
                'location': f"{match.group(2).strip()}, {match.group(3).strip()}, Canada",
                'posted_date': match.group(4).strip() if match.group(4) else None,
                'level': match.group(5).strip() if match.group(5) else None,
                'job_title': 'ML / AI Engineer',
                'total_experience_years': int(match.group(7)) if match.group(7) else None,
                'company_experience_years': int(match.group(8)) if match.group(8) else None,
            }
            
            # Parse salary
            salary_str = match.group(9)
            total, base, stock, bonus = parse_salary_string(salary_str + ' $CA')
            record['total_compensation_cad'] = total
            record['base_salary_cad'] = base
            record['stock_cad'] = stock
            record['bonus_cad'] = bonus
            
            records.append(record)
        except:
            pass
    
    # Remove duplicates
    seen = set()
    unique_records = []
    for r in records:
        key = (r.get('company'), r.get('location'), r.get('total_compensation_cad'))
        if key not in seen:
            seen.add(key)
            unique_records.append(r)
    
    return unique_records


def main():
    parser = argparse.ArgumentParser(description='Extract individual salary records from Levels.fyi')
    parser.add_argument('--html', help='Single HTML file')
    parser.add_argument('--html-dir', help='Directory with multiple HTML files')
    parser.add_argument('--out', default='data/real_data/stat_real_data_levelsfyi_records.csv',
                       help='Output CSV file')
    parser.add_argument('--date', default='2026-01-12', help='Collection date')
    
    args = parser.parse_args()
    
    all_records = []
    
    if args.html:
        html_path = Path(args.html)
        if not html_path.exists():
            print(f"❌ Error: {html_path} not found")
            return 1
        print(f"\n📄 Processing: {html_path.name}")
        records = extract_levelsfyi_records(html_path)
        all_records.extend(records)
        print(f"  Found {len(records)} records")
    
    elif args.html_dir:
        html_dir = Path(args.html_dir)
        if not html_dir.exists():
            print(f"❌ Error: {html_dir} not found")
            return 1
        
        html_files = list(html_dir.glob('*.html'))
        print(f"\n📂 Processing {len(html_files)} HTML files...\n")
        
        for html_path in sorted(html_files):
            print(f"📄 {html_path.name}")
            records = extract_levelsfyi_records(html_path)
            all_records.extend(records)
            print(f"  ✓ Found {len(records)} records")
    
    else:
        print("❌ Provide either --html or --html-dir")
        return 1
    
    if not all_records:
        print("❌ No records found!")
        return 1
    
    # Convert to DataFrame
    df = pd.DataFrame(all_records)
    
    # Reorder columns
    cols = ['source', 'collection_date', 'company', 'location', 'city', 'province',
            'level', 'job_title', 'total_experience_years', 'company_experience_years',
            'total_compensation_cad', 'base_salary_cad', 'stock_cad', 'bonus_cad', 'posted_date']
    cols = [c for c in cols if c in df.columns]
    df = df[cols]
    
    # Save
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, index=False)
    
    print(f"\n{'='*70}")
    print(f"✅ Saved {len(df)} records to {out_path}")
    print(f"{'='*70}\n")
    
    # Summary
    print(f"Companies: {df['company'].nunique()}")
    print(f"Cities: {df['city'].nunique() if 'city' in df.columns else 'N/A'}")
    print(f"Levels: {', '.join(df['level'].unique()) if 'level' in df.columns and df['level'].notna().any() else 'Not specified'}")
    
    print(f"\n💰 Salary Statistics:")
    print(f"  Avg Total Comp: ${df['total_compensation_cad'].mean():,.0f} CAD")
    print(f"  Min: ${df['total_compensation_cad'].min():,.0f} CAD")
    print(f"  Max: ${df['total_compensation_cad'].max():,.0f} CAD")
    print(f"  Median: ${df['total_compensation_cad'].median():,.0f} CAD")
    
    print(f"\n📊 By Level:")
    if 'level' in df.columns:
        for level, group in df.groupby('level'):
            if pd.notna(level):
                avg = group['total_compensation_cad'].mean()
                count = len(group)
                print(f"  {level}: {count} records | Avg ${avg:,.0f} CAD")
    
    print(f"\n📍 By City:")
    if 'city' in df.columns:
        for city, group in df.groupby('city'):
            if pd.notna(city):
                avg = group['total_compensation_cad'].mean()
                count = len(group)
                print(f"  {city}: {count} records | Avg ${avg:,.0f} CAD")
    
    print()
    return 0


if __name__ == '__main__':
    exit(main())
