#!/usr/bin/env python3
"""
Extract salary data from Levels.fyi for AI/ML Engineers in Canada.

Levels.fyi provides:
- Company, Title, Level (L3-L8)
- Total Compensation, Base, Stock, Bonus
- Location, Years of Experience

How to collect:
1. Visit: https://www.levels.fyi/t/software-engineer/locations/canada
2. Filter by:
   - Location: Canada
   - Title: "Machine Learning Engineer" or "AI Engineer" or "ML Engineer"
   - Companies: All (or specific ones)
3. Export as CSV or save HTML page
4. Run this script
"""

import re
import argparse
import csv
from pathlib import Path
from bs4 import BeautifulSoup
import pandas as pd
from typing import List, Dict


def extract_salary_number(text):
    """Extract numeric salary from text like '150K' or '$150,000'."""
    if not text:
        return None
    
    clean = text.strip().replace('$', '').replace(',', '')
    
    if 'K' in clean or 'k' in clean:
        num_str = clean.replace('K', '').replace('k', '').strip()
        try:
            return int(float(num_str) * 1000)
        except:
            return None
    
    try:
        return int(float(clean))
    except:
        return None


def parse_levelsfyi_csv(csv_path: Path) -> List[Dict]:
    """
    Parse Levels.fyi CSV export.
    
    Expected columns (may vary):
    - Company
    - Title / Role
    - Level (L3, L4, L5, L6, L7, L8)
    - Location
    - Total Comp / Total Compensation
    - Base Salary
    - Stock
    - Bonus
    - Years of Experience
    - Timestamp / Date
    """
    data = []
    
    try:
        df = pd.read_csv(csv_path)
        
        print(f"  Found columns: {list(df.columns)}")
        
        # Normalize column names (case-insensitive)
        df.columns = [col.lower().strip() for col in df.columns]
        
        for idx, row in df.iterrows():
            # Extract company
            company = None
            for col in ['company', 'employer', 'company_name']:
                if col in df.columns:
                    company = row[col]
                    break
            
            if not company:
                continue
            
            # Extract title
            title = None
            for col in ['title', 'role', 'job_title']:
                if col in df.columns:
                    title = row[col]
                    break
            
            if not title or 'ai' not in str(title).lower() and 'ml' not in str(title).lower() and 'machine' not in str(title).lower():
                continue  # Skip non-AI/ML roles
            
            # Extract level
            level = None
            for col in ['level', 'seniority_level']:
                if col in df.columns:
                    level = row[col]
                    break
            
            # Extract location
            location = None
            for col in ['location', 'city', 'province']:
                if col in df.columns:
                    location = row[col]
                    break
            
            if not location:
                location = "Canada"
            
            # Extract compensation figures
            total_comp = None
            for col in ['total comp', 'total_comp', 'total compensation', 'total_compensation', 'compensation']:
                if col in df.columns:
                    total_comp = extract_salary_number(str(row[col]))
                    break
            
            base_salary = None
            for col in ['base', 'base salary', 'base_salary']:
                if col in df.columns:
                    base_salary = extract_salary_number(str(row[col]))
                    break
            
            stock = None
            for col in ['stock', 'equity', 'rsu', 'stock_value']:
                if col in df.columns:
                    stock = extract_salary_number(str(row[col]))
                    break
            
            bonus = None
            for col in ['bonus', 'signing bonus', 'signing_bonus']:
                if col in df.columns:
                    bonus = extract_salary_number(str(row[col]))
                    break
            
            # Experience
            experience = None
            for col in ['years of experience', 'years_of_experience', 'yoe', 'experience']:
                if col in df.columns:
                    experience = row[col]
                    break
            
            data.append({
                'source': 'Levels.fyi',
                'company': company,
                'title': title,
                'level': level,
                'location': location,
                'total_compensation_cad': total_comp,
                'base_salary_cad': base_salary,
                'stock_value_cad': stock,
                'bonus_cad': bonus,
                'years_of_experience': experience
            })
        
    except Exception as e:
        print(f"  Error reading CSV: {e}")
    
    return data


def parse_levelsfyi_html(html_path: Path) -> List[Dict]:
    """
    Parse Levels.fyi HTML page (if user saved page directly).
    
    Note: Levels.fyi uses complex JavaScript rendering,
    so saved HTML may have limited data. CSV export preferred.
    """
    data = []
    
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            html = f.read()
        
        soup = BeautifulSoup(html, 'lxml')
        
        # Look for salary data rows/cards
        # Structure varies by page, common patterns:
        
        # Pattern 1: Table rows
        rows = soup.find_all('tr')
        for row in rows:
            cells = row.find_all('td')
            if len(cells) < 5:
                continue
            
            try:
                cell_texts = [cell.get_text(strip=True) for cell in cells]
                
                # Check if this looks like a salary row
                if not any(key in str(cell_texts).lower() for key in ['k', '$', 'engineer', 'ai', 'ml']):
                    continue
                
                company = cell_texts[0] if len(cell_texts) > 0 else None
                title = cell_texts[1] if len(cell_texts) > 1 else None
                level = cell_texts[2] if len(cell_texts) > 2 else None
                location = cell_texts[3] if len(cell_texts) > 3 else None
                total_comp = extract_salary_number(cell_texts[4]) if len(cell_texts) > 4 else None
                
                if company and 'ai' in str(title).lower() or 'ml' in str(title).lower():
                    data.append({
                        'source': 'Levels.fyi',
                        'company': company,
                        'title': title,
                        'level': level,
                        'location': location or 'Canada',
                        'total_compensation_cad': total_comp,
                        'base_salary_cad': None,
                        'stock_value_cad': None,
                        'bonus_cad': None,
                        'years_of_experience': None
                    })
            except:
                continue
        
    except Exception as e:
        print(f"  Error reading HTML: {e}")
    
    return data


def create_sample_levelsfyi_csv():
    """Create a sample CSV template for manual entry."""
    sample_data = [
        {
            'Company': 'Google',
            'Title': 'Machine Learning Engineer',
            'Level': 'L4',
            'Location': 'Toronto, ON',
            'Total Comp': '250K',
            'Base Salary': '180K',
            'Stock': '50K',
            'Bonus': '20K',
            'Years of Experience': 3
        },
        {
            'Company': 'Meta',
            'Title': 'AI Engineer',
            'Level': 'L5',
            'Location': 'Vancouver, BC',
            'Total Comp': '320K',
            'Base Salary': '200K',
            'Stock': '100K',
            'Bonus': '20K',
            'Years of Experience': 5
        },
        {
            'Company': 'Amazon',
            'Title': 'Machine Learning Scientist',
            'Level': 'L5',
            'Location': 'Toronto, ON',
            'Total Comp': '290K',
            'Base Salary': '185K',
            'Stock': '80K',
            'Bonus': '25K',
            'Years of Experience': 4
        },
        {
            'Company': 'Shopify',
            'Title': 'ML Engineer',
            'Level': 'L4',
            'Location': 'Ottawa, ON',
            'Total Comp': '240K',
            'Base Salary': '170K',
            'Stock': '50K',
            'Bonus': '20K',
            'Years of Experience': 3
        },
        {
            'Company': 'Microsoft',
            'Title': 'AI Engineer',
            'Level': 'L5',
            'Location': 'Vancouver, BC',
            'Total Comp': '310K',
            'Base Salary': '200K',
            'Stock': '90K',
            'Bonus': '20K',
            'Years of Experience': 5
        }
    ]
    
    template_path = Path('data/real_data/levelsfyi_template.csv')
    template_path.parent.mkdir(parents=True, exist_ok=True)
    
    df = pd.DataFrame(sample_data)
    df.to_csv(template_path, index=False)
    
    print(f"\n✅ Created template: {template_path}")
    print(f"   Edit this file and populate with real Levels.fyi data")
    return template_path


def main():
    parser = argparse.ArgumentParser(
        description='Extract salary data from Levels.fyi (CSV or HTML format)'
    )
    parser.add_argument('--csv', help='Path to Levels.fyi CSV export')
    parser.add_argument('--html', help='Path to Levels.fyi saved HTML page')
    parser.add_argument('--create-template', action='store_true',
                       help='Create sample CSV template for manual entry')
    parser.add_argument('--out', default='data/real_data/stat_real_data_levelsfyi.csv',
                       help='Output CSV file')
    parser.add_argument('--date', default='2026-01-12',
                       help='Collection date (YYYY-MM-DD)')
    
    args = parser.parse_args()
    
    if args.create_template:
        create_sample_levelsfyi_csv()
        print("\n📋 Template created! Steps:")
        print("1. Edit the template file")
        print("2. Add data from Levels.fyi")
        print("3. Run: python3 scripts/scrapers/extract_levelsfyi_data.py --csv data/real_data/levelsfyi_template.csv")
        return 0
    
    data = []
    
    if args.csv:
        csv_path = Path(args.csv)
        if not csv_path.exists():
            print(f"❌ CSV file not found: {csv_path}")
            return 1
        
        print(f"\n📊 Parsing Levels.fyi CSV: {csv_path.name}")
        data = parse_levelsfyi_csv(csv_path)
    
    elif args.html:
        html_path = Path(args.html)
        if not html_path.exists():
            print(f"❌ HTML file not found: {html_path}")
            return 1
        
        print(f"\n🌐 Parsing Levels.fyi HTML: {html_path.name}")
        data = parse_levelsfyi_html(html_path)
    
    else:
        print("❌ Provide either --csv, --html, or --create-template")
        return 1
    
    if not data:
        print("❌ No salary data found!")
        return 1
    
    # Add metadata
    for entry in data:
        entry['collection_date'] = args.date
    
    # Convert to DataFrame
    df = pd.DataFrame(data)
    
    # Save
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, index=False)
    
    print(f"\n✅ Saved {len(df)} entries to {out_path}")
    
    # Summary
    print(f"\n=== Summary ===")
    print(f"Total entries: {len(df)}")
    print(f"Unique companies: {df['company'].nunique()}")
    print(f"Locations: {', '.join(df['location'].unique())}")
    
    if 'total_compensation_cad' in df.columns:
        avg_comp = df['total_compensation_cad'].mean()
        if avg_comp:
            print(f"Avg Total Comp: ${avg_comp/1000:.0f}K")
    
    print(f"\n=== By Level ===")
    if 'level' in df.columns:
        for level, group in df.groupby('level'):
            avg = group['total_compensation_cad'].mean()
            print(f"  {level}: {len(group)} entries | Avg: ${avg/1000:.0f}K" if avg else f"  {level}: {len(group)} entries")
    
    return 0


if __name__ == '__main__':
    exit(main())
