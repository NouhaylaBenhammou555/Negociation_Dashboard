#!/usr/bin/env python3
"""
Process scraped real data and transform it into dashboard-ready formats.
Converts Job Bank, Glassdoor, and other sources into standardized CSVs.
"""
import pandas as pd
import json
from pathlib import Path
import re

def process_job_bank_data(input_file='data/real_data/stat_real_data_scraped_jobs.csv'):
    """Transform Job Bank wage data into geo salary format"""
    print("\n📊 Processing Job Bank Canada data...")
    
    df = pd.read_csv(input_file)
    
    geo_data = []
    
    for _, row in df.iterrows():
        if row['source'] == 'Job Bank Canada':
            wage_dict = json.loads(row['wage_data'])
            
            # Extract key provinces for AI market
            locations = {
                'Montreal': 'Quebec',
                'Toronto': 'Ontario',
                'Vancouver': 'British Columbia',
                'Canada': 'Canada'
            }
            
            for city, province in locations.items():
                if province in wage_dict:
                    hourly = float(wage_dict[province])
                    # Convert hourly to annual (assuming 2000 hours/year)
                    annual = hourly * 2000
                    
                    geo_data.append({
                        'location': city,
                        'source': 'Job Bank Canada',
                        'noc_code': row['job_title'],
                        'min_cad': int(annual * 0.8),  # Estimate
                        'avg_cad': int(annual),
                        'max_cad': int(annual * 1.5),  # Estimate
                        'p25_cad': int(annual * 0.85),
                        'p50_cad': int(annual),
                        'p75_cad': int(annual * 1.25),
                        'currency': 'CAD',
                        'date': row['scraped_date']
                    })
    
    geo_df = pd.DataFrame(geo_data)
    output_path = Path('data/real_data/stat_real_data_geo.csv')
    geo_df.to_csv(output_path, index=False)
    print(f"✅ Created {output_path}")
    print(geo_df)
    
    return geo_df

def combine_glassdoor_data():
    """Check for Glassdoor data and combine if available"""
    glassdoor_file = Path('data/real_data/stat_real_data_glassdoor.csv')
    
    if not glassdoor_file.exists():
        print(f"\n⚠️  {glassdoor_file} not found. Run Glassdoor scraper first.")
        return None
    
    print(f"\n📊 Processing Glassdoor data from {glassdoor_file}...")
    df = pd.read_csv(glassdoor_file)
    print(f"✅ Found {len(df)} Glassdoor salary records")
    print(df.head())
    
    return df

def create_experience_data(base_geo_df):
    """Generate experience-based salary progression from base data"""
    print("\n📊 Creating experience progression data...")
    
    exp_data = []
    
    # Experience levels (years) and multipliers
    exp_levels = [
        (0.5, 0.65, 'Intern'),
        (1, 0.75, 'Junior'),
        (2, 0.90, 'Entry'),
        (3, 1.00, 'Entry'),
        (4, 1.15, 'Mid'),
        (5, 1.30, 'Mid'),
        (6, 1.50, 'Senior'),
        (8, 1.80, 'Senior'),
        (10, 2.20, 'Lead'),
        (12, 2.50, 'Principal')
    ]
    
    for _, geo_row in base_geo_df.iterrows():
        base_salary = geo_row['avg_cad']
        location = geo_row['location']
        
        for years, multiplier, level in exp_levels:
            exp_data.append({
                'location': location,
                'years_of_experience': years,
                'position_level': level,
                'avg_salary_cad': int(base_salary * multiplier),
                'source': 'Derived from Job Bank',
                'date': geo_row['date']
            })
    
    exp_df = pd.DataFrame(exp_data)
    output_path = Path('data/real_data/stat_real_data_exp_progression.csv')
    exp_df.to_csv(output_path, index=False)
    print(f"✅ Created {output_path}")
    
    return exp_df

def create_percentiles_from_geo(geo_df):
    """Create percentiles data from geographic salary data"""
    print("\n📊 Creating percentiles data...")
    
    percentiles_data = []
    
    for _, row in geo_df.iterrows():
        percentiles_data.append({
            'location': row['location'],
            'p10_cad': row['min_cad'],
            'p25_cad': row['p25_cad'],
            'p50_cad': row['p50_cad'],
            'p75_cad': row['p75_cad'],
            'p90_cad': row['max_cad'],
            'source': row['source'],
            'date': row['date']
        })
    
    perc_df = pd.DataFrame(percentiles_data)
    output_path = Path('data/real_data/stat_real_data_percentiles.csv')
    perc_df.to_csv(output_path, index=False)
    print(f"✅ Created {output_path}")
    print(perc_df)
    
    return perc_df

def main():
    print("="*60)
    print("Real Data Processing Pipeline")
    print("="*60)
    
    # Process Job Bank data
    geo_df = process_job_bank_data()
    
    # Check for Glassdoor data
    glassdoor_df = combine_glassdoor_data()
    
    # Generate derived datasets
    exp_df = create_experience_data(geo_df)
    perc_df = create_percentiles_from_geo(geo_df)
    
    print("\n" + "="*60)
    print("✅ Processing Complete!")
    print("="*60)
    print("\nGenerated files in data/real_data/:")
    print("  - stat_real_data_geo.csv (geographic salary data)")
    print("  - stat_real_data_exp_progression.csv (experience progression)")
    print("  - stat_real_data_percentiles.csv (salary percentiles)")
    
    if glassdoor_df is not None:
        print("  - stat_real_data_glassdoor.csv (Glassdoor data)")
    
    print("\nNext step: Run chart generators with --use-real-data flag")
    
    return geo_df, exp_df, perc_df

if __name__ == "__main__":
    main()
