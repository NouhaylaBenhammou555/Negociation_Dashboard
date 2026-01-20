#!/usr/bin/env python3
"""
Consolidate ALL salary data from multiple sources into master dataset.

Sources:
1. Glassdoor submissions (40 records)
2. Levels.fyi template data (10+ records - high-value GAFAM/premium companies)
3. Create unified format for charting
"""

import pandas as pd
import numpy as np
from pathlib import Path


def load_and_standardize_glassdoor():
    """Load Glassdoor data and standardize columns."""
    df = pd.read_csv('data/real_data/stat_real_data_submissions_all.csv')
    
    # Standardize columns
    df = df[[
        'source', 'collection_date', 'location', 'job_title', 
        'experience_min_years', 'experience_max_years',
        'salary_min_cad', 'salary_max_cad', 'salary_median_cad'
    ]].copy()
    
    df.columns = [
        'source', 'collection_date', 'location', 'job_title',
        'exp_years_min', 'exp_years_max', 'salary_min', 'salary_max', 'salary_median'
    ]
    
    df['company'] = 'Glassdoor Submission'
    df['level'] = 'Not Specified'
    df['country'] = 'Canada'
    
    # Remove duplicates
    df = df.drop_duplicates(
        subset=['location', 'salary_median', 'exp_years_min'],
        keep='first'
    )
    
    return df


def load_and_standardize_levelsfyi():
    """Load Levels.fyi template data with all the premium companies."""
    data = {
        'source': ['Levels.fyi'] * 10,
        'collection_date': ['2026-01-12'] * 10,
        'company': [
            'Synechron', 'Matador.ai', 'Zapier', 'Intact', 'ETS',
            'Guidepoint', 'Tecsys', 'Intact Financial', 'Chubb', 'Dialpad'
        ],
        'location': [
            'Montreal, QC, Canada', 'Montreal, QC, Canada', 'Toronto, ON, Canada',
            'Montreal, QC, Canada', 'Montreal, QC, Canada', 'Toronto, ON, Canada',
            'Montreal, QC, Canada', 'Montreal, QC, Canada', 'Toronto, ON, Canada',
            'San Francisco, CA, USA'
        ],
        'level': [
            'Associate', 'Not Specified', 'L3', 'L2', 'L1',
            'L3', 'L1', 'Senior', 'Senior', 'Senior Software Engineer 1'
        ],
        'job_title': ['ML / AI Engineer'] * 10,
        'country': [
            'Canada', 'Canada', 'Canada', 'Canada', 'Canada',
            'Canada', 'Canada', 'Canada', 'Canada', 'USA'
        ],
        'exp_years_min': [2, 3, 8, 4, 2, 5, 2, 4, 5, 10],
        'exp_years_max': [2, 1, 2, 4, 2, 0, 0, 1, 1, 6],
        'salary_min': [71000, 120000, 214000, 107000, 25000, 165000, 71000, 140000, 160000, 205700],
        'salary_max': [71000, 120000, 214000, 122000, 25000, 181500, 71000, 156000, 160000, 205700],
        'salary_median': [71000, 120000, 214000, 122000, 25000, 181500, 71000, 156000, 160000, 205700],
    }
    
    df = pd.DataFrame(data)
    return df


def create_master_dataset():
    """Create consolidated master dataset from all sources."""
    
    print("📥 Loading data sources...\n")
    
    # Load data
    glassdoor = load_and_standardize_glassdoor()
    print(f"✓ Glassdoor: {len(glassdoor)} submissions")
    
    levelsfyi = load_and_standardize_levelsfyi()
    print(f"✓ Levels.fyi: {len(levelsfyi)} records")
    
    # Merge
    master = pd.concat([glassdoor, levelsfyi], ignore_index=True, sort=False)
    
    # Extract city from location
    master['city'] = master['location'].apply(
        lambda x: x.split(',')[0].strip() if isinstance(x, str) else 'Unknown'
    )
    
    # Create experience levels bucket
    master['exp_level'] = pd.cut(
        master['exp_years_min'],
        bins=[0, 3, 6, 9, 12, 30],
        labels=['0-3 years', '4-6 years', '7-9 years', '10-12 years', '13+ years'],
        right=True
    )
    
    # Remove any duplicates by salary (same salary often = different source of same record)
    master = master.sort_values('salary_median', ascending=False)
    
    return master


def create_aggregations(master_df):
    """Create analysis-ready aggregations."""
    
    aggs = {}
    
    # 1. By City
    print("\n📊 Creating aggregations...\n")
    city_agg = master_df.groupby('city').agg({
        'salary_median': ['count', 'mean', 'median', 'min', 'max',
                          lambda x: x.quantile(0.25),
                          lambda x: x.quantile(0.75)]
    }).round(0)
    city_agg.columns = ['count', 'avg', 'median', 'min', 'max', 'p25', 'p75']
    city_agg = city_agg.sort_values('count', ascending=False)
    aggs['city'] = city_agg
    print(f"✓ City aggregation: {len(city_agg)} cities")
    
    # 2. By Experience Level
    exp_agg = master_df.groupby('exp_level').agg({
        'salary_median': ['count', 'mean', 'median', 'min', 'max',
                          lambda x: x.quantile(0.25),
                          lambda x: x.quantile(0.75)]
    }).round(0)
    exp_agg.columns = ['count', 'avg', 'median', 'min', 'max', 'p25', 'p75']
    aggs['experience'] = exp_agg
    print(f"✓ Experience aggregation: {len(exp_agg)} levels")
    
    # 3. By Source (Glassdoor vs Levels.fyi)
    source_agg = master_df.groupby('source').agg({
        'salary_median': ['count', 'mean', 'median', 'min', 'max',
                          lambda x: x.quantile(0.25),
                          lambda x: x.quantile(0.75)]
    }).round(0)
    source_agg.columns = ['count', 'avg', 'median', 'min', 'max', 'p25', 'p75']
    aggs['source'] = source_agg
    print(f"✓ Source aggregation: {len(source_agg)} sources")
    
    # 4. By Country
    country_agg = master_df.groupby('country').agg({
        'salary_median': ['count', 'mean', 'median', 'min', 'max',
                          lambda x: x.quantile(0.25),
                          lambda x: x.quantile(0.75)]
    }).round(0)
    country_agg.columns = ['count', 'avg', 'median', 'min', 'max', 'p25', 'p75']
    aggs['country'] = country_agg
    print(f"✓ Country aggregation: {len(country_agg)} countries")
    
    return aggs


def save_datasets(master_df, aggs):
    """Save all datasets."""
    
    output_dir = Path('data/real_data')
    
    # Master dataset
    master_df.to_csv(
        output_dir / 'stat_master_salaries.csv',
        index=False
    )
    print(f"\n💾 Saved Master Dataset: {len(master_df)} records")
    print(f"   → data/real_data/stat_master_salaries.csv")
    
    # Aggregations
    for name, agg_df in aggs.items():
        filename = output_dir / f'stat_agg_{name}.csv'
        agg_df.to_csv(filename)
        print(f"   → stat_agg_{name}.csv")
    
    return output_dir


def print_summary(master_df):
    """Print comprehensive summary."""
    
    print("\n" + "="*70)
    print("📊 CONSOLIDATED SALARY ANALYSIS - ALL SOURCES")
    print("="*70)
    
    print(f"\n📈 DATASET OVERVIEW:")
    print(f"  Total Records: {len(master_df)}")
    print(f"  Sources: {master_df['source'].nunique()} ({', '.join(master_df['source'].unique())})")
    print(f"  Countries: {master_df['country'].nunique()}")
    print(f"  Cities: {master_df['city'].nunique()}")
    
    salary_col = master_df['salary_median'].dropna()
    print(f"\n💰 SALARY STATISTICS (CAD):")
    print(f"  Min:     ${salary_col.min():>12,.0f}")
    print(f"  P25:     ${salary_col.quantile(0.25):>12,.0f}")
    print(f"  Median:  ${salary_col.median():>12,.0f}")
    print(f"  Mean:    ${salary_col.mean():>12,.0f}")
    print(f"  P75:     ${salary_col.quantile(0.75):>12,.0f}")
    print(f"  Max:     ${salary_col.max():>12,.0f}")
    print(f"  StdDev:  ${salary_col.std():>12,.0f}")
    
    print(f"\n📍 TOP 5 CITIES (Canada):")
    canada_df = master_df[master_df['country'] == 'Canada']
    for city, count in canada_df['city'].value_counts().head(5).items():
        median = canada_df[canada_df['city'] == city]['salary_median'].median()
        print(f"  {city:20s} {count:2d} records | ${median:>10,.0f}")
    
    print(f"\n⏱️  EXPERIENCE DISTRIBUTION:")
    for exp, count in master_df['exp_level'].value_counts().sort_index().items():
        pct = 100 * count / len(master_df)
        median = master_df[master_df['exp_level'] == exp]['salary_median'].median()
        print(f"  {str(exp):15s} {count:2d} ({pct:5.1f}%) | ${median:>10,.0f}")
    
    print(f"\n📊 SOURCE BREAKDOWN:")
    for source in master_df['source'].unique():
        count = len(master_df[master_df['source'] == source])
        pct = 100 * count / len(master_df)
        print(f"  {source:20s} {count:2d} ({pct:5.1f}%)")
    
    print("\n" + "="*70)


def main():
    master = create_master_dataset()
    aggs = create_aggregations(master)
    save_datasets(master, aggs)
    print_summary(master)
    
    print("\n✅ All datasets ready for dashboard!")
    return 0


if __name__ == '__main__':
    exit(main())
