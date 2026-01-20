#!/usr/bin/env python3
"""
Extract all salary data from Levels.fyi HTML files
Parses the Material-UI table structure to get all 67 records
"""

import os
import re
from bs4 import BeautifulSoup
import pandas as pd
from pathlib import Path

def parse_salary_amount(text):
    """Extract numeric salary from text like '120 000 $CA' or '120,000 CAD'"""
    if not text:
        return None
    # Remove common currency symbols and text
    clean = re.sub(r'[\$,\s]', '', text)
    clean = re.sub(r'(CA|CAD|USD|k)', '', clean, flags=re.IGNORECASE)
    # Extract first number
    match = re.search(r'(\d+)', clean)
    return int(match.group(1)) if match else None

def parse_compensation_breakdown(text):
    """Parse base | stock | bonus from text like '100 k | 20 k | N/A'"""
    if not text or 'N/A' in text:
        parts = text.split('|') if text else []
    else:
        parts = text.split('|')
    
    result = {'base': None, 'stock': None, 'bonus': None}
    
    for i, part in enumerate(parts):
        part = part.strip()
        if part and part != 'N/A':
            # Remove currency symbols and extract number
            clean = re.sub(r'[\$,\s]', '', part)
            # Handle 'k' suffix (thousands)
            if 'k' in clean.lower():
                clean = re.sub(r'k', '', clean, flags=re.IGNORECASE)
                match = re.search(r'(\d+\.?\d*)', clean)
                if match:
                    value = int(float(match.group(1)) * 1000)
                else:
                    value = None
            else:
                match = re.search(r'(\d+)', clean)
                value = int(match.group(1)) if match else None
            
            if i == 0:
                result['base'] = value
            elif i == 1:
                result['stock'] = value
            elif i == 2:
                result['bonus'] = value
    
    return result

def parse_years_experience(text):
    """Parse years from text like '4 yrs' or '2-4 yrs'"""
    if not text:
        return None
    # Handle ranges like '2-4 yrs'
    match = re.search(r'(\d+)(?:-(\d+))?\s*yr', text)
    if match:
        # If range, take the average
        if match.group(2):
            return (int(match.group(1)) + int(match.group(2))) / 2
        return int(match.group(1))
    return None

def extract_from_html(html_path):
    """Extract salary records from a single HTML file"""
    print(f"\n📄 Processing: {os.path.basename(html_path)}")
    
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find all salary rows in the table
    salary_rows = soup.find_all('tr', class_=re.compile('salary-row_collapsedSalaryRow'))
    
    records = []
    
    for row in salary_rows:
        try:
            # Extract company name
            company_link = row.find('a', class_=re.compile('salary-row_companyName'))
            company_text = row.find('p', class_=re.compile('salary-row_companyName'))
            company = (company_link.text.strip() if company_link else 
                      company_text.text.strip() if company_text else None)
            
            if not company:
                continue
            
            # Extract location and date
            location_date = row.find('span', class_=re.compile('css-xlmjpr'))
            loc_date_text = location_date.text.strip() if location_date else ""
            
            # Split location and date by |
            if '|' in loc_date_text:
                location, date = loc_date_text.split('|', 1)
                location = location.strip()
                date = date.strip()
            else:
                location = loc_date_text
                date = None
            
            # Extract level
            level_elem = row.find('p', class_=re.compile('salary-row_levelName'))
            level = level_elem.text.strip() if level_elem else None
            
            # Extract years of experience
            exp_cells = row.find_all('td', class_=re.compile('css-w3va9g'))
            total_yrs = None
            company_yrs = None
            
            if exp_cells:
                exp_cell = exp_cells[0]
                # Total years
                total_p = exp_cell.find('p', class_='MuiTypography-body1')
                total_yrs = parse_years_experience(total_p.text) if total_p else None
                
                # Years at company
                company_span = exp_cell.find('span', class_='MuiTypography-caption')
                company_yrs = parse_years_experience(company_span.text) if company_span else None
            
            # Extract total compensation
            comp_cell = row.find('td', class_=re.compile('salary-row_totalCompCell'))
            total_comp = None
            base = None
            stock = None
            bonus = None
            
            if comp_cell:
                # Total compensation
                total_p = comp_cell.find('p', class_='MuiTypography-body1')
                if total_p:
                    total_comp = parse_salary_amount(total_p.text)
                
                # Breakdown (base | stock | bonus)
                breakdown_span = comp_cell.find('span', class_='MuiTypography-caption')
                if breakdown_span:
                    breakdown = parse_compensation_breakdown(breakdown_span.text)
                    base = breakdown['base']
                    stock = breakdown['stock']
                    bonus = breakdown['bonus']
            
            # Create record
            record = {
                'company': company,
                'location': location,
                'date': date,
                'level': level,
                'years_total': total_yrs,
                'years_at_company': company_yrs,
                'total_compensation_cad': total_comp,
                'base_salary_cad': base,
                'stock_yearly_cad': stock,
                'bonus_cad': bonus,
                'source': 'Levels.fyi'
            }
            
            records.append(record)
            print(f"   ✓ {company:30s} | {location:25s} | ${total_comp:,}" if total_comp else f"   ✓ {company}")
            
        except Exception as e:
            print(f"   ⚠️  Error parsing row: {e}")
            continue
    
    return records

def main():
    """Extract all salary data from all Levels.fyi HTML files"""
    html_dir = Path('data/levels.fyi_pages')
    
    if not html_dir.exists():
        print(f"❌ Directory not found: {html_dir}")
        return
    
    # Find all HTML files
    html_files = sorted(html_dir.glob('*.html'))
    
    print(f"🔍 Found {len(html_files)} HTML files to process")
    print("=" * 80)
    
    all_records = []
    
    for html_file in html_files:
        records = extract_from_html(html_file)
        all_records.extend(records)
        print(f"   📊 Extracted {len(records)} records from {html_file.name}")
    
    print("\n" + "=" * 80)
    print(f"✅ TOTAL EXTRACTED: {len(all_records)} records")
    
    if not all_records:
        print("❌ No records extracted!")
        return
    
    # Convert to DataFrame
    df = pd.DataFrame(all_records)
    
    # Save to CSV
    output_file = 'data/real_data/levelsfyi_67_complete.csv'
    df.to_csv(output_file, index=False)
    print(f"💾 Saved to: {output_file}")
    
    # Display summary statistics
    print("\n📈 SUMMARY STATISTICS:")
    print(f"   Total records: {len(df)}")
    print(f"   Companies: {df['company'].nunique()}")
    print(f"   Locations: {df['location'].nunique()}")
    
    if df['total_compensation_cad'].notna().any():
        print(f"\n💰 COMPENSATION (CAD):")
        print(f"   Min:    ${df['total_compensation_cad'].min():,.0f}")
        print(f"   Median: ${df['total_compensation_cad'].median():,.0f}")
        print(f"   Mean:   ${df['total_compensation_cad'].mean():,.0f}")
        print(f"   Max:    ${df['total_compensation_cad'].max():,.0f}")
    
    # Show first few records
    print("\n📋 SAMPLE RECORDS:")
    print(df[['company', 'location', 'total_compensation_cad', 'base_salary_cad']].head(10).to_string())

if __name__ == '__main__':
    main()
