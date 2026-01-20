#!/usr/bin/env python3
"""
Extract detailed individual salary records from Levels.fyi HTML pages.

This script intelligently parses visible text content to extract individual salary records
with company names, levels, experience, and compensation breakdowns.
"""

import re
import argparse
from pathlib import Path
from typing import List, Dict, Optional
import pandas as pd
from bs4 import BeautifulSoup


def extract_text_content(html_path: str) -> str:
    """Extract clean text content from HTML."""
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    soup = BeautifulSoup(html, 'lxml')
    
    # Remove script and style elements
    for script in soup(["script", "style"]):
        script.decompose()
    
    # Get text
    text = soup.get_text(separator='\n', strip=True)
    return text


def parse_salary_value(value_str: str) -> Optional[int]:
    """Parse salary value to CAD integer.
    Examples: "71K", "71 000", "107k|5k|10k", "214 000 $CA"
    """
    if not value_str or 'N/A' in value_str:
        return None
    
    # Clean up
    value_str = value_str.strip().replace('$CA', '').replace('$', '').replace(',', '').replace(' ', '')
    
    # Handle variations
    if 'k' in value_str.lower():
        try:
            num = float(value_str.lower().replace('k', ''))
            return int(num * 1000)
        except:
            pass
    
    try:
        return int(float(value_str))
    except:
        return None


def extract_records_from_text(text: str) -> List[Dict]:
    """Extract salary records from plain text using pattern matching."""
    records = []
    
    # Split by company names or obvious record boundaries
    # Look for patterns like: CompanyName | City | Level | Experience | Salary | Breakdown
    
    lines = text.split('\n')
    
    # Known company names and patterns
    companies = {
        'Synechron', 'Matador', 'Matador.ai', 'Zapier', 'Intact', 'Intact Financial',
        'ETS', 'Hightouch', 'Guidepoint', 'Tecsys', 'Chubb', 'Dialpad',
        'Google', 'Meta', 'Apple', 'Amazon', 'Microsoft', 'Netflix', 'Stripe', 'Uber',
        'Shopify', 'Twilio', 'Slack', 'Gitlab', 'Figma', 'Notion'
    }
    
    levels = ['L1', 'L2', 'L3', 'L4', 'L5', 'L6', 'L7', 'L8', 
              'Senior', 'Junior', 'Associate', 'Staff', 'Principal', 'Director']
    
    current_record = {}
    
    for i, line in enumerate(lines):
        line = line.strip()
        if not line or len(line) < 3:
            continue
        
        # Check for company name
        for company in companies:
            if company.lower() in line.lower():
                if current_record and 'company' in current_record:
                    # Save previous record if complete
                    if 'salary_cad' in current_record:
                        records.append(current_record.copy())
                
                current_record = {
                    'source': 'Levels.fyi',
                    'collection_date': '2026-01-12',
                    'company': company,
                    'job_title': 'ML / AI Engineer'
                }
                break
        
        # Look for location (City, Province pattern)
        if 'current_record' in dir() and current_record:
            location_match = re.search(
                r'([A-Za-z\s]+),\s*([A-Z]{2}),\s*Canada|Remote',
                line
            )
            if location_match:
                if 'Remote' in line:
                    current_record['location'] = 'Remote'
                else:
                    current_record['location'] = line.strip()
            
            # Level detection
            for level in levels:
                if level in line:
                    current_record['level'] = level
                    break
            
            # Experience pattern (e.g., "2 yrs / 2 yrs")
            exp_match = re.search(r'(\d+)\s+yrs?\s+[/|]\s+(\d+)\s+yrs?', line, re.I)
            if exp_match:
                current_record['total_experience_years'] = int(exp_match.group(1))
                current_record['company_experience_years'] = int(exp_match.group(2))
            
            # Salary with breakdown (e.g., "107 k | 5 k | 10 k")
            salary_breakdown = re.search(
                r'(\d+\s*\d*\s*\d*)\s*[k|K]?\s*\|\s*(\d+\s*\d*)\s*[k|K]?\s*\|\s*(\d+\s*\d*)\s*[k|K]?',
                line
            )
            if salary_breakdown:
                base_str = salary_breakdown.group(1).strip()
                stock_str = salary_breakdown.group(2).strip()
                bonus_str = salary_breakdown.group(3).strip()
                
                base = parse_salary_value(base_str + 'k')
                stock = parse_salary_value(stock_str + 'k')
                bonus = parse_salary_value(bonus_str + 'k')
                
                current_record['base_salary_cad'] = base
                current_record['stock_cad'] = stock
                current_record['bonus_cad'] = bonus
                current_record['total_compensation_cad'] = (base or 0) + (stock or 0) + (bonus or 0)
            
            # Simple salary (e.g., "214 000" or "120K")
            elif 'salary_cad' not in current_record:
                salary_match = re.search(r'(\d+\s*\d*\s*\d*)\s*(?:\$|k|K)\s*(?:CAD)?', line)
                if salary_match and 'company' in current_record:
                    salary_str = salary_match.group(1).replace(' ', '')
                    salary_val = parse_salary_value(salary_str + 'k' if len(salary_str) <= 3 else salary_str)
                    if salary_val:
                        current_record['total_compensation_cad'] = salary_val
                        current_record['base_salary_cad'] = salary_val
    
    # Add last record
    if current_record and 'company' in current_record and 'total_compensation_cad' in current_record:
        records.append(current_record)
    
    return records


def main():
    parser = argparse.ArgumentParser(description='Extract Levels.fyi detailed salary records')
    parser.add_argument('--html', help='Single HTML file path')
    parser.add_argument('--html-dir', help='Directory containing HTML files')
    parser.add_argument('--out', default='data/real_data/stat_real_data_levelsfyi_detailed.csv',
                       help='Output CSV file')
    
    args = parser.parse_args()
    
    all_records = []
    
    if args.html:
        html_path = Path(args.html)
        if not html_path.exists():
            print(f"❌ {html_path} not found")
            return 1
        
        print(f"📄 Processing: {html_path.name}")
        text = extract_text_content(str(html_path))
        records = extract_records_from_text(text)
        all_records.extend(records)
        print(f"✓ Extracted {len(records)} records")
    
    elif args.html_dir:
        html_dir = Path(args.html_dir)
        if not html_dir.exists():
            print(f"❌ {html_dir} not found")
            return 1
        
        html_files = sorted(html_dir.glob('*.html'))
        print(f"\n📂 Processing {len(html_files)} files...\n")
        
        for html_path in html_files:
            print(f"📄 {html_path.name}...")
            text = extract_text_content(str(html_path))
            records = extract_records_from_text(text)
            all_records.extend(records)
            print(f"  ✓ {len(records)} records")
    
    else:
        print("❌ Provide --html or --html-dir")
        return 1
    
    if not all_records:
        print("❌ No records extracted")
        return 1
    
    # Remove duplicates by (company, location, salary)
    seen = set()
    unique_records = []
    for r in all_records:
        key = (r.get('company'), r.get('location'), r.get('total_compensation_cad'))
        if key not in seen:
            seen.add(key)
            unique_records.append(r)
    
    # Convert to DataFrame
    df = pd.DataFrame(unique_records)
    
    # Reorder and select columns
    cols = ['source', 'collection_date', 'company', 'location', 'level', 'job_title',
            'total_experience_years', 'company_experience_years',
            'total_compensation_cad', 'base_salary_cad', 'stock_cad', 'bonus_cad']
    df = df[[c for c in cols if c in df.columns]]
    
    # Save
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, index=False)
    
    print(f"\n{'='*70}")
    print(f"✅ Extracted {len(df)} unique records → {out_path}")
    print(f"{'='*70}\n")
    
    # Summary stats
    if 'total_compensation_cad' in df.columns:
        salary_col = df['total_compensation_cad'].dropna()
        print(f"💰 Salary Statistics:")
        print(f"  Avg: ${salary_col.mean():,.0f}")
        print(f"  Min: ${salary_col.min():,.0f}")
        print(f"  Max: ${salary_col.max():,.0f}")
        print(f"  Median: ${salary_col.median():,.0f}")
        print()
    
    if 'company' in df.columns:
        print(f"🏢 Companies: {df['company'].nunique()}")
        print(df['company'].value_counts().head(10).to_string())
        print()
    
    if 'level' in df.columns and df['level'].notna().any():
        print(f"📊 By Level:")
        for level, group in df.groupby('level'):
            if pd.notna(level):
                avg = group['total_compensation_cad'].mean()
                count = len(group)
                print(f"  {level}: {count} | Avg ${avg:,.0f}")
        print()
    
    print("✨ Done!")
    return 0


if __name__ == '__main__':
    exit(main())
