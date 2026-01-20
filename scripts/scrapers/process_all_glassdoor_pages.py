#!/usr/bin/env python3
"""
Process all Glassdoor HTML files in a directory and extract:
1. Overall salary statistics per location
2. Company-specific salary ranges per location
3. Consolidated data across all locations
"""

import re
import json
import argparse
from pathlib import Path
from bs4 import BeautifulSoup
import pandas as pd
from typing import Dict, List, Tuple


def extract_salary_number(text):
    """Extract numeric salary from text like '$86K' or '$117K'."""
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


def extract_location_from_filename(filename: str) -> str:
    """Extract location from filename like 'glassdoor_montreal.html' -> 'Montreal'."""
    # Remove extension
    name = Path(filename).stem
    
    # Remove 'glassdoor_' prefix
    if name.startswith('glassdoor_'):
        name = name[10:]
    
    # Capitalize
    return name.capitalize()


def extract_overall_stats(soup) -> Dict:
    """Extract overall salary statistics from the page header."""
    stats = {}
    
    # Base pay range (e.g., "$72K - $110K")
    base_pay_elem = soup.find('span', class_=re.compile('TotalPayRange_StyledAverageBasePay'))
    if base_pay_elem:
        base_pay_text = base_pay_elem.get_text(strip=True)
        parts = base_pay_text.split('–') or base_pay_text.split('-')
        if len(parts) == 2:
            stats['overall_min_cad'] = extract_salary_number(parts[0])
            stats['overall_max_cad'] = extract_salary_number(parts[1])
    
    # Average/median base pay
    avg_comp_elem = soup.find('span', class_=re.compile('TotalPayRange_StyledAverageComp'))
    if avg_comp_elem:
        avg_text = avg_comp_elem.get_text(strip=True)
        stats['overall_median_cad'] = extract_salary_number(avg_text)
    
    # Career progression data
    career_steps = soup.find_all('div', attrs={'data-test': re.compile('occ-career-progress')})
    career_data = []
    
    for step in career_steps:
        title_elem = step.find('a', class_=re.compile('CareerSteps_JobTitleLink')) or \
                     step.find('span', class_=re.compile('CareerSteps_JobTitleLink'))
        
        if title_elem:
            title = title_elem.get_text(strip=True)
            salary_elem = step.find('span')
            if salary_elem:
                salary_text = salary_elem.get_text(strip=True)
                # Parse range like "$89K–$160K/yr"
                salary_clean = salary_text.replace('/yr', '').strip()
                parts = salary_clean.split('–') or salary_clean.split('-')
                if len(parts) == 2:
                    career_data.append({
                        'title': title,
                        'min_cad': extract_salary_number(parts[0]),
                        'max_cad': extract_salary_number(parts[1])
                    })
    
    if career_data:
        stats['career_progression'] = career_data
    
    # Number of companies
    companies_header = soup.find('p', class_=re.compile('SalariesSubHeader_DesktopSalariesCount'))
    if companies_header:
        text = companies_header.get_text(strip=True)
        match = re.search(r'(\d+)\s+companies', text)
        if match:
            stats['total_companies'] = int(match.group(1))
    
    return stats


def extract_companies(soup) -> List[Dict]:
    """Extract company salary data from Glassdoor HTML."""
    companies = []
    
    salary_items = soup.find_all('div', class_=re.compile('SalariesList_Item'))
    
    for item in salary_items:
        try:
            # Company name
            company_name_elem = item.find('p', class_=re.compile('salary-card_EmployerName'))
            if not company_name_elem:
                continue
            company_name = company_name_elem.get_text(strip=True)
            
            # Rating
            rating_elem = item.find('p', class_=re.compile('salary-card_Rating'))
            rating = float(rating_elem.get_text(strip=True)) if rating_elem else None
            
            # Total pay range
            total_pay_elem = item.find('div', class_=re.compile('salary-card_TotalPay'))
            total_pay = None
            min_pay = None
            max_pay = None
            
            if total_pay_elem:
                total_pay_text = total_pay_elem.get_text(strip=True)
                parts = total_pay_text.split('-')
                if len(parts) == 2:
                    min_pay = extract_salary_number(parts[0])
                    max_pay = extract_salary_number(parts[1])
                    total_pay = total_pay_text
            
            # Median salary
            median_elem = item.find('div', class_=re.compile('salary-card_BreakdownBold'))
            median_salary = None
            if median_elem:
                median_text = median_elem.get_text(strip=True)
                median_salary = extract_salary_number(median_text)
            
            # Job title
            job_title_elem = item.find('section', class_=re.compile('salary-card_TitleTrim'))
            job_title = job_title_elem.get_text(strip=True) if job_title_elem else "AI Engineer"
            
            # Open jobs
            open_jobs_elem = item.find('span', class_=re.compile('button_ButtonContent'))
            open_jobs = 0
            if open_jobs_elem:
                open_jobs_text = open_jobs_elem.get_text(strip=True)
                match = re.search(r'(\d+)\s+open', open_jobs_text)
                if match:
                    open_jobs = int(match.group(1))
            
            companies.append({
                'company_name': company_name,
                'rating': rating,
                'job_title': job_title,
                'total_pay_range': total_pay,
                'min_salary_cad': min_pay,
                'max_salary_cad': max_pay,
                'median_salary_cad': median_salary,
                'open_jobs': open_jobs
            })
            
        except Exception as e:
            print(f"    ⚠️  Error parsing company: {e}")
            continue
    
    return companies


def process_html_file(html_path: Path, location: str = None) -> Tuple[Dict, List[Dict]]:
    """Process a single HTML file and return overall stats + companies."""
    if not location:
        location = extract_location_from_filename(html_path.name)
    
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    soup = BeautifulSoup(html, 'lxml')
    
    # Extract overall statistics
    overall_stats = extract_overall_stats(soup)
    overall_stats['location'] = location
    overall_stats['source_file'] = html_path.name
    
    # Extract companies
    companies = extract_companies(soup)
    
    return overall_stats, companies


def main():
    parser = argparse.ArgumentParser(description='Process all Glassdoor HTML files')
    parser.add_argument('--html-dir', default='data/glassdoor_pages',
                       help='Directory containing Glassdoor HTML files')
    parser.add_argument('--date', default='2026-01-12', help='Collection date (YYYY-MM-DD)')
    parser.add_argument('--out-dir', default='data/real_data',
                       help='Output directory for CSV files')
    parser.add_argument('--consolidated', action='store_true',
                       help='Create consolidated CSV with all locations')
    
    args = parser.parse_args()
    
    html_dir = Path(args.html_dir)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    
    if not html_dir.exists():
        print(f"❌ Error: Directory not found: {html_dir}")
        return 1
    
    # Find all HTML files
    html_files = list(html_dir.glob('*.html'))
    
    if not html_files:
        print(f"❌ No HTML files found in {html_dir}")
        return 1
    
    print(f"\n{'='*60}")
    print(f"  Processing {len(html_files)} Glassdoor HTML files")
    print(f"{'='*60}\n")
    
    all_overall_stats = []
    all_companies = []
    
    for html_file in sorted(html_files):
        print(f"📄 {html_file.name}")
        
        try:
            overall_stats, companies = process_html_file(html_file)
            
            location = overall_stats['location']
            
            # Add metadata
            overall_stats['collection_date'] = args.date
            overall_stats['source'] = 'Glassdoor'
            
            for company in companies:
                company['location'] = location
                company['collection_date'] = args.date
                company['source'] = 'Glassdoor'
            
            # Print summary
            print(f"   📍 Location: {location}")
            print(f"   💰 Overall range: ${overall_stats.get('overall_min_cad', 0)/1000:.0f}K - ${overall_stats.get('overall_max_cad', 0)/1000:.0f}K")
            print(f"   📊 Median: ${overall_stats.get('overall_median_cad', 0)/1000:.0f}K")
            print(f"   🏢 Companies: {len(companies)}")
            print(f"   💼 Open jobs: {sum(c['open_jobs'] for c in companies)}")
            
            # Career progression
            if 'career_progression' in overall_stats:
                print(f"   📈 Career levels: {len(overall_stats['career_progression'])}")
                for level in overall_stats['career_progression']:
                    print(f"      • {level['title']}: ${level['min_cad']/1000:.0f}K - ${level['max_cad']/1000:.0f}K")
            
            # Save individual location files
            location_clean = location.lower().replace(' ', '_')
            
            # Save companies CSV
            if companies:
                companies_df = pd.DataFrame(companies)
                companies_csv = out_dir / f'stat_real_data_companies_{location_clean}.csv'
                companies_df.to_csv(companies_csv, index=False)
                print(f"   ✅ Saved: {companies_csv.name}")
            
            # Collect for consolidated files
            all_overall_stats.append(overall_stats)
            all_companies.extend(companies)
            
            print()
            
        except Exception as e:
            print(f"   ❌ Error processing {html_file.name}: {e}\n")
            continue
    
    # Create consolidated files
    if args.consolidated and all_companies:
        print(f"{'='*60}")
        print(f"  Creating consolidated datasets")
        print(f"{'='*60}\n")
        
        # All companies consolidated
        all_companies_df = pd.DataFrame(all_companies)
        consolidated_csv = out_dir / 'stat_real_data_all_companies.csv'
        all_companies_df.to_csv(consolidated_csv, index=False)
        print(f"✅ Consolidated companies: {consolidated_csv}")
        print(f"   Total companies: {len(all_companies_df)}")
        print(f"   Total locations: {all_companies_df['location'].nunique()}")
        print(f"   Total open jobs: {all_companies_df['open_jobs'].sum()}")
        
        # Overall stats per location
        overall_df = pd.DataFrame(all_overall_stats)
        # Flatten career_progression if exists
        if 'career_progression' in overall_df.columns:
            overall_df = overall_df.drop('career_progression', axis=1)
        
        overall_csv = out_dir / 'stat_real_data_location_stats.csv'
        overall_df.to_csv(overall_csv, index=False)
        print(f"✅ Location statistics: {overall_csv}")
        
        # Summary by location
        print(f"\n{'='*60}")
        print(f"  Summary by Location")
        print(f"{'='*60}\n")
        
        location_summary = all_companies_df.groupby('location').agg({
            'company_name': 'count',
            'median_salary_cad': 'mean',
            'open_jobs': 'sum',
            'rating': 'mean'
        }).round(0)
        
        location_summary.columns = ['Companies', 'Avg Median Salary', 'Total Jobs', 'Avg Rating']
        
        for location, row in location_summary.iterrows():
            print(f"📍 {location}:")
            print(f"   Companies: {int(row['Companies'])}")
            print(f"   Avg Median: ${int(row['Avg Median Salary'])/1000:.0f}K")
            print(f"   Total Jobs: {int(row['Total Jobs'])}")
            print(f"   Avg Rating: {row['Avg Rating']:.1f} ⭐")
            print()
        
        # Top 10 companies across all locations
        print(f"{'='*60}")
        print(f"  Top 10 Companies (by Median Salary)")
        print(f"{'='*60}\n")
        
        top10 = all_companies_df.nlargest(10, 'median_salary_cad')[
            ['company_name', 'location', 'median_salary_cad', 'rating', 'open_jobs']
        ]
        
        for idx, row in top10.iterrows():
            print(f"  {row['company_name']} ({row['location']})")
            print(f"     💰 ${int(row['median_salary_cad'])/1000:.0f}K  |  ⭐ {row['rating']:.1f}  |  💼 {int(row['open_jobs'])} jobs")
        
        print()
    
    print(f"\n{'='*60}")
    print(f"  ✅ Processing complete!")
    print(f"{'='*60}\n")
    
    return 0


if __name__ == '__main__':
    exit(main())
