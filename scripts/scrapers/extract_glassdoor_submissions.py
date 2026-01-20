#!/usr/bin/env python3
"""
Extract individual salary submissions from Glassdoor HTML pages.
These are user-submitted salaries with experience level, location, and date.
"""

import re
import argparse
from pathlib import Path
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime


def extract_salary_number(text):
    """Extract numeric salary from text like '$92K' or '$108K'."""
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


def parse_experience_years(exp_text):
    """Parse experience text like '4-6 Years' into numeric values."""
    if not exp_text:
        return None, None
    
    # Pattern: "X-Y Years"
    match = re.search(r'(\d+)-(\d+)\s*Years?', exp_text, re.IGNORECASE)
    if match:
        return int(match.group(1)), int(match.group(2))
    
    # Pattern: "X Years"
    match = re.search(r'(\d+)\s*Years?', exp_text, re.IGNORECASE)
    if match:
        years = int(match.group(1))
        return years, years
    
    return None, None


def extract_submissions_from_html(html_path):
    """Extract individual salary submissions from Glassdoor HTML."""
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    soup = BeautifulSoup(html, 'lxml')
    
    submissions = []
    
    # Look for salary submission cards/entries
    # Common patterns in Glassdoor individual submissions
    
    # Method 1: Look for salary range patterns with location and experience
    salary_pattern = re.compile(
        r'AI Engineer\s*\|?\s*'
        r'(\d+-\d+\s+Years?|Less than 1 Year)'
        r'\s*([^|]+?)\s*'
        r'submitted on\s+([A-Za-z]+\s+\d+,\s+\d{4})'
        r'\s*\$?([\d,]+-[\d,]+K?|\d+K)\s*/yr',
        re.IGNORECASE | re.DOTALL
    )
    
    # Find all matches
    for match in salary_pattern.finditer(html):
        try:
            experience = match.group(1).strip()
            location = match.group(2).strip()
            submitted_date = match.group(3).strip()
            salary_text = match.group(4).strip()
            
            # Parse experience
            exp_min, exp_max = parse_experience_years(experience)
            
            # Parse salary
            if '-' in salary_text:
                parts = salary_text.replace('$', '').split('-')
                salary_min = extract_salary_number(parts[0])
                salary_max = extract_salary_number(parts[1])
                salary_median = int((salary_min + salary_max) / 2) if salary_min and salary_max else None
            else:
                salary_median = extract_salary_number(salary_text)
                salary_min = salary_median
                salary_max = salary_median
            
            # Parse location (extract city)
            city_match = re.match(r'([^,]+)', location)
            city = city_match.group(1).strip() if city_match else location
            
            submission = {
                'job_title': 'AI Engineer',
                'experience_text': experience,
                'experience_min_years': exp_min,
                'experience_max_years': exp_max,
                'location': city,
                'location_full': location,
                'submitted_date': submitted_date,
                'salary_min_cad': salary_min,
                'salary_max_cad': salary_max,
                'salary_median_cad': salary_median,
                'salary_text': salary_text
            }
            
            submissions.append(submission)
            
        except Exception as e:
            print(f"    ⚠️  Error parsing submission: {e}")
            continue
    
    # Method 2: Parse from structured HTML elements if regex fails
    if len(submissions) == 0:
        print("    Trying structured HTML parsing...")
        
        # Look for common Glassdoor salary card structures
        salary_cards = soup.find_all(['div', 'article'], class_=re.compile(r'salary|submission|report', re.I))
        
        for card in salary_cards:
            try:
                text = card.get_text(separator='|', strip=True)
                
                # Look for AI Engineer entries
                if 'AI Engineer' not in text:
                    continue
                
                # Extract components
                exp_match = re.search(r'(\d+-\d+)\s*Years?', text)
                loc_match = re.search(r'([A-Za-z\s]+),\s*([A-Z]{2})', text)
                date_match = re.search(r'submitted on\s+([A-Za-z]+\s+\d+,\s+\d{4})', text)
                salary_match = re.search(r'\$?([\d,]+K?(?:\s*-\s*[\d,]+K?)?)\s*/yr', text)
                
                if exp_match and loc_match and salary_match:
                    experience = exp_match.group(0)
                    city = loc_match.group(1).strip()
                    location_full = f"{city}, {loc_match.group(2)}"
                    salary_text = salary_match.group(1)
                    submitted_date = date_match.group(1) if date_match else None
                    
                    exp_min, exp_max = parse_experience_years(experience)
                    
                    if '-' in salary_text:
                        parts = salary_text.split('-')
                        salary_min = extract_salary_number(parts[0])
                        salary_max = extract_salary_number(parts[1])
                        salary_median = int((salary_min + salary_max) / 2) if salary_min and salary_max else None
                    else:
                        salary_median = extract_salary_number(salary_text)
                        salary_min = salary_median
                        salary_max = salary_median
                    
                    submission = {
                        'job_title': 'AI Engineer',
                        'experience_text': experience,
                        'experience_min_years': exp_min,
                        'experience_max_years': exp_max,
                        'location': city,
                        'location_full': location_full,
                        'submitted_date': submitted_date,
                        'salary_min_cad': salary_min,
                        'salary_max_cad': salary_max,
                        'salary_median_cad': salary_median,
                        'salary_text': salary_text
                    }
                    
                    submissions.append(submission)
                    
            except Exception as e:
                continue
    
    return submissions


def main():
    parser = argparse.ArgumentParser(description='Extract individual salary submissions from Glassdoor HTML')
    parser.add_argument('html_files', nargs='*', help='Path to Glassdoor HTML file(s)')
    parser.add_argument('--html-dir', help='Process all HTML files in directory')
    parser.add_argument('--out', default='data/real_data/stat_real_data_submissions_all.csv',
                       help='Output CSV file')
    parser.add_argument('--date', default='2026-01-12', help='Collection date (YYYY-MM-DD)')
    
    args = parser.parse_args()
    
    html_files = []
    
    if args.html_dir:
        html_dir = Path(args.html_dir)
        if not html_dir.exists():
            print(f"Error: Directory not found: {html_dir}")
            return 1
        html_files = list(html_dir.glob('*.html'))
    elif args.html_files:
        html_files = [Path(f) for f in args.html_files]
    else:
        print("Error: Provide either --html-dir or html_files")
        return 1
    
    if not html_files:
        print("No HTML files to process!")
        return 1
    
    print(f"\n=== Extracting salary submissions from {len(html_files)} files ===\n")
    
    all_submissions = []
    
    for html_path in sorted(html_files):
        print(f"Processing: {html_path.name}")
        
        submissions = extract_submissions_from_html(html_path)
        
        # Add metadata
        for sub in submissions:
            sub['source'] = 'Glassdoor'
            sub['collection_date'] = args.date
            sub['source_file'] = html_path.name
        
        all_submissions.extend(submissions)
        print(f"  Found {len(submissions)} submissions\n")
    
    if not all_submissions:
        print("❌ No submissions found!")
        return 1
    
    # Convert to DataFrame
    df = pd.DataFrame(all_submissions)
    
    # Reorder columns
    cols = ['source', 'collection_date', 'source_file', 'job_title', 
            'experience_text', 'experience_min_years', 'experience_max_years',
            'location', 'location_full', 'submitted_date',
            'salary_min_cad', 'salary_max_cad', 'salary_median_cad', 'salary_text']
    df = df[[c for c in cols if c in df.columns]]
    
    # Save CSV
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, index=False)
    
    print(f"\n✅ Saved {len(df)} submissions to {out_path}\n")
    
    # Print summary statistics
    print(f"=== Summary Statistics ===")
    print(f"Total submissions: {len(df)}")
    print(f"Unique locations: {df['location'].nunique()}")
    print(f"Date range: {df['submitted_date'].min()} to {df['submitted_date'].max()}" if 'submitted_date' in df.columns else "")
    
    # By location
    print(f"\n=== By Location ===")
    location_stats = df.groupby('location').agg({
        'salary_median_cad': ['count', 'mean', 'min', 'max']
    }).round(0)
    
    for location, row in location_stats.iterrows():
        count = int(row[('salary_median_cad', 'count')])
        avg = int(row[('salary_median_cad', 'mean')])
        min_sal = int(row[('salary_median_cad', 'min')])
        max_sal = int(row[('salary_median_cad', 'max')])
        print(f"  {location}: {count} submissions | Avg: ${avg/1000:.0f}K | Range: ${min_sal/1000:.0f}K-${max_sal/1000:.0f}K")
    
    # By experience
    print(f"\n=== By Experience Level ===")
    exp_stats = df.groupby('experience_text').agg({
        'salary_median_cad': ['count', 'mean']
    }).round(0).sort_values(('salary_median_cad', 'mean'))
    
    for exp, row in exp_stats.iterrows():
        count = int(row[('salary_median_cad', 'count')])
        avg = int(row[('salary_median_cad', 'mean')])
        print(f"  {exp}: {count} submissions | Avg: ${avg/1000:.0f}K")
    
    return 0


if __name__ == '__main__':
    exit(main())
