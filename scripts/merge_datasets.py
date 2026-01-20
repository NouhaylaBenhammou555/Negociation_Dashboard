#!/usr/bin/env python3
"""
Merge new Levels.fyi data (53 records) with existing master dataset.
Updates stat_master_salaries.csv with complete data.
"""

import pandas as pd
from datetime import datetime

def standardize_levelsfyi_to_master(df_levelsfyi):
    """Convert Levels.fyi format to master dataset format"""
    
    records = []
    for _, row in df_levelsfyi.iterrows():
        # Parse location to extract city and country
        location = row['location'].strip()
        if ',' in location:
            parts = location.split(',')
            city = parts[0].strip()
            country = 'Canada' if 'Canada' in location else 'USA'
        else:
            city = location
            country = 'Canada'
        
        # Calculate experience level
        years = row['years_total'] if pd.notna(row['years_total']) else 0
        if years <= 3:
            exp_level = '0-3 years'
            exp_min, exp_max = 0, 3
        elif years <= 6:
            exp_level = '4-6 years'
            exp_min, exp_max = 4, 6
        elif years <= 9:
            exp_level = '7-9 years'
            exp_min, exp_max = 7, 9
        elif years <= 12:
            exp_level = '10-12 years'
            exp_min, exp_max = 10, 12
        else:
            exp_level = '13+ years'
            exp_min, exp_max = 13, 20
        
        # Get salary - use total compensation as median
        salary = row['total_compensation_cad'] if pd.notna(row['total_compensation_cad']) else 0
        
        record = {
            'source': 'Levels.fyi',
            'collection_date': datetime.now().strftime('%Y-%m-%d'),
            'location': location,
            'job_title': 'ML / AI Engineer',
            'exp_years_min': exp_min,
            'exp_years_max': exp_max,
            'salary_min': salary,
            'salary_max': salary,
            'salary_median': salary,
            'company': row['company'],
            'level': row['level'] if pd.notna(row['level']) and row['level'] != '-' else 'Not Specified',
            'country': country,
            'city': city,
            'exp_level': exp_level
        }
        records.append(record)
    
    return pd.DataFrame(records)

def check_duplicates(df_master, df_new):
    """Check for potential duplicate records"""
    duplicates = []
    
    for idx, new_row in df_new.iterrows():
        # Check if a similar record exists (same company, city, similar salary)
        potential_dups = df_master[
            (df_master['company'] == new_row['company']) &
            (df_master['city'] == new_row['city']) &
            (abs(df_master['salary_median'] - new_row['salary_median']) < 5000)
        ]
        
        if len(potential_dups) > 0:
            duplicates.append({
                'new_record': f"{new_row['company']} - {new_row['city']} - ${new_row['salary_median']:,.0f}",
                'existing_count': len(potential_dups)
            })
    
    return duplicates

def main():
    print("=" * 80)
    print("📊 MERGING DATASETS")
    print("=" * 80)
    
    # Load existing master dataset
    print("\n📂 Loading existing master dataset...")
    df_master = pd.read_csv('data/real_data/stat_master_salaries.csv')
    print(f"   ✓ Loaded {len(df_master)} existing records")
    print(f"   ✓ Sources: {df_master['source'].value_counts().to_dict()}")
    
    # Load new Levels.fyi data
    print("\n📂 Loading new Levels.fyi data...")
    df_levelsfyi = pd.read_csv('data/real_data/levelsfyi_67_complete.csv')
    print(f"   ✓ Loaded {len(df_levelsfyi)} new records")
    
    # Convert to master format
    print("\n🔄 Converting to master format...")
    df_new = standardize_levelsfyi_to_master(df_levelsfyi)
    print(f"   ✓ Converted {len(df_new)} records")
    
    # Check for duplicates
    print("\n🔍 Checking for duplicates...")
    duplicates = check_duplicates(df_master, df_new)
    if duplicates:
        print(f"   ⚠️  Found {len(duplicates)} potential duplicates:")
        for dup in duplicates[:5]:  # Show first 5
            print(f"      - {dup['new_record']}")
    else:
        print("   ✓ No duplicates found")
    
    # Remove old Levels.fyi records from master (we're replacing them with complete set)
    print("\n🗑️  Removing old Levels.fyi records from master...")
    old_levelsfyi_count = len(df_master[df_master['source'] == 'Levels.fyi'])
    df_master_clean = df_master[df_master['source'] != 'Levels.fyi']
    print(f"   ✓ Removed {old_levelsfyi_count} old Levels.fyi records")
    print(f"   ✓ Retained {len(df_master_clean)} records (Glassdoor + others)")
    
    # Merge datasets
    print("\n➕ Merging datasets...")
    df_merged = pd.concat([df_master_clean, df_new], ignore_index=True)
    print(f"   ✓ Total records: {len(df_merged)}")
    print(f"   ✓ Breakdown:")
    for source, count in df_merged['source'].value_counts().items():
        print(f"      - {source}: {count} records")
    
    # Save updated master dataset
    print("\n💾 Saving updated master dataset...")
    output_path = 'data/real_data/stat_master_salaries.csv'
    df_merged.to_csv(output_path, index=False)
    print(f"   ✓ Saved to: {output_path}")
    
    # Show statistics
    print("\n📈 UPDATED STATISTICS:")
    print(f"   Total Records: {len(df_merged)}")
    print(f"   Salary Range: ${df_merged['salary_median'].min():,.0f} - ${df_merged['salary_median'].max():,.0f}")
    print(f"   Median Salary: ${df_merged['salary_median'].median():,.0f}")
    print(f"   Mean Salary: ${df_merged['salary_median'].mean():,.0f}")
    print(f"   Countries: {df_merged['country'].nunique()} ({', '.join(df_merged['country'].unique())})")
    print(f"   Cities: {df_merged['city'].nunique()}")
    print(f"   Companies: {df_merged['company'].nunique()}")
    
    print("\n" + "=" * 80)
    print("✅ MERGE COMPLETE!")
    print("=" * 80)
    print("\n💡 Next step: Run generate_benchmark_charts.py to update all visualizations")

if __name__ == '__main__':
    main()
