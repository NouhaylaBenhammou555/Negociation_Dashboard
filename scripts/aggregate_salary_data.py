#!/usr/bin/env python3
"""
Consolidate and aggregate salary data from multiple sources.

Creates:
- Master consolidated dataset
- By-city aggregations
- By-experience-level aggregations
- Percentile analysis
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List


def load_glassdoor_data(csv_path: str) -> pd.DataFrame:
    """Load and clean Glassdoor submission data."""
    df = pd.read_csv(csv_path)
    
    # Extract company name from job_title or use a default
    if 'job_title' in df.columns:
        df['company_name'] = df['job_title'].apply(
            lambda x: x.split(' at ')[-1].strip() if ' at ' in str(x) else 'Unknown'
        )
    
    # Remove duplicates (each submission appears 2x)
    df = df.drop_duplicates(subset=['location', 'salary_median_cad', 'experience_min_years'], keep='first')
    
    # Clean location names
    df['city'] = df['location'].apply(lambda x: x.split(',')[0].strip() if isinstance(x, str) else x)
    
    return df


def create_city_aggregations(df: pd.DataFrame) -> pd.DataFrame:
    """Create salary statistics by city."""
    if 'salary_median_cad' not in df.columns or 'city' not in df.columns:
        return pd.DataFrame()
    
    city_stats = df.groupby('city')['salary_median_cad'].agg([
        ('count', 'count'),
        ('avg_salary', 'mean'),
        ('min_salary', 'min'),
        ('median_salary', 'median'),
        ('p25_salary', lambda x: x.quantile(0.25)),
        ('p75_salary', lambda x: x.quantile(0.75)),
        ('max_salary', 'max'),
        ('std_salary', 'std')
    ]).reset_index()
    
    city_stats.columns = ['city', 'submissions', 'avg_salary_cad', 'min_salary_cad', 
                          'median_salary_cad', 'p25_salary_cad', 'p75_salary_cad', 
                          'max_salary_cad', 'std_salary_cad']
    
    return city_stats.sort_values('submissions', ascending=False)


def create_experience_aggregations(df: pd.DataFrame) -> pd.DataFrame:
    """Create salary statistics by experience level."""
    if 'salary_median_cad' not in df.columns or 'experience_min_years' not in df.columns:
        return pd.DataFrame()
    
    # Create experience buckets
    df['exp_level'] = pd.cut(df['experience_min_years'], 
                              bins=[0, 3, 6, 9, 12, 20],
                              labels=['0-3 years', '4-6 years', '7-9 years', '10-12 years', '13+ years'])
    
    exp_stats = df.groupby('exp_level')['salary_median_cad'].agg([
        ('count', 'count'),
        ('avg_salary', 'mean'),
        ('min_salary', 'min'),
        ('median_salary', 'median'),
        ('p25_salary', lambda x: x.quantile(0.25)),
        ('p75_salary', lambda x: x.quantile(0.75)),
        ('max_salary', 'max'),
    ]).reset_index()
    
    exp_stats.columns = ['experience_level', 'submissions', 'avg_salary_cad', 'min_salary_cad',
                        'median_salary_cad', 'p25_salary_cad', 'p75_salary_cad', 'max_salary_cad']
    
    return exp_stats


def create_city_experience_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """Create salary matrix by city and experience."""
    if 'salary_median_cad' not in df.columns:
        return pd.DataFrame()
    
    # Create experience buckets
    df['exp_level'] = pd.cut(df['experience_min_years'], 
                              bins=[0, 3, 6, 9, 12, 20],
                              labels=['0-3y', '4-6y', '7-9y', '10-12y', '13+y'])
    
    df['city'] = df['location'].apply(lambda x: x.split(',')[0].strip() if isinstance(x, str) else x)
    
    matrix = df.pivot_table(
        values='salary_median_cad',
        index='city',
        columns='exp_level',
        aggfunc='median'
    ).reset_index()
    
    return matrix


def create_company_rankings(df: pd.DataFrame, min_submissions: int = 2) -> pd.DataFrame:
    """Create top employers by median salary."""
    if 'salary_median_cad' not in df.columns or 'company_name' not in df.columns:
        return pd.DataFrame()
    
    company_stats = df.groupby('company_name').agg({
        'salary_median_cad': ['count', 'median', 'mean', 'min', 'max'],
        'location': lambda x: x.mode()[0] if len(x.mode()) > 0 else 'Unknown'
    }).reset_index()
    
    company_stats.columns = ['company_name', 'submissions', 'median_salary_cad', 
                            'avg_salary_cad', 'min_salary_cad', 'max_salary_cad', 'top_location']
    
    company_stats = company_stats[company_stats['submissions'] >= min_submissions]
    return company_stats.sort_values('median_salary_cad', ascending=False)


def main():
    data_dir = Path('data/real_data')
    glassdoor_file = data_dir / 'stat_real_data_submissions_all.csv'
    
    if not glassdoor_file.exists():
        print(f"❌ {glassdoor_file} not found")
        return 1
    
    print("📊 Consolidating salary data...\n")
    
    # Load Glassdoor data
    print("📥 Loading Glassdoor submissions...")
    df = load_glassdoor_data(str(glassdoor_file))
    print(f"✓ Loaded {len(df)} unique submissions")
    print(f"  Cities: {df['city'].nunique()}")
    print(f"  Companies: {df['company_name'].nunique()}\n")
    
    # City aggregations
    print("🏙️  Creating city-level aggregations...")
    city_agg = create_city_aggregations(df)
    city_file = data_dir / 'stat_agg_by_city.csv'
    city_agg.to_csv(city_file, index=False)
    print(f"✓ Saved {len(city_agg)} cities → {city_file.name}")
    print(city_agg[['city', 'submissions', 'median_salary_cad']].to_string(index=False))
    print()
    
    # Experience aggregations
    print("📈 Creating experience-level aggregations...")
    exp_agg = create_experience_aggregations(df)
    exp_file = data_dir / 'stat_agg_by_experience.csv'
    exp_agg.to_csv(exp_file, index=False)
    print(f"✓ Saved {len(exp_agg)} experience levels → {exp_file.name}")
    print(exp_agg[['experience_level', 'submissions', 'median_salary_cad']].to_string(index=False))
    print()
    
    # City × Experience matrix
    print("🗓️  Creating city × experience matrix...")
    matrix = create_city_experience_matrix(df)
    matrix_file = data_dir / 'stat_matrix_city_experience.csv'
    matrix.to_csv(matrix_file, index=False)
    print(f"✓ Saved matrix → {matrix_file.name}\n")
    
    # Top employers
    print("🏢 Creating top employer rankings...")
    companies = create_company_rankings(df, min_submissions=2)
    company_file = data_dir / 'stat_top_employers.csv'
    companies.to_csv(company_file, index=False)
    print(f"✓ Saved {len(companies)} employers → {company_file.name}")
    print(companies[['company_name', 'submissions', 'median_salary_cad', 'top_location']].head(10).to_string(index=False))
    print()
    
    # Overall statistics
    print("="*70)
    print("📊 OVERALL STATISTICS (Glassdoor Canada AI Engineer Salaries)")
    print("="*70)
    print(f"Total Submissions: {len(df)}")
    print(f"Date Range: {df['submitted_date'].min()} to {df['submitted_date'].max()}")
    print(f"\n💰 Salary Range:")
    print(f"  Min:    ${df['salary_min_cad'].min():>10,.0f} CAD")
    print(f"  P25:    ${df['salary_median_cad'].quantile(0.25):>10,.0f} CAD")
    print(f"  Median: ${df['salary_median_cad'].median():>10,.0f} CAD")
    print(f"  P75:    ${df['salary_median_cad'].quantile(0.75):>10,.0f} CAD")
    print(f"  Max:    ${df['salary_max_cad'].max():>10,.0f} CAD")
    print(f"  Avg:    ${df['salary_median_cad'].mean():>10,.0f} CAD")
    
    print(f"\n📍 Top 5 Cities by submission count:")
    for city, count in df['city'].value_counts().head(5).items():
        avg_sal = df[df['city'] == city]['salary_median_cad'].median()
        print(f"  {city:20s} {count:3d} submissions | ${avg_sal:>10,.0f} median")
    
    print(f"\n⏱️  Experience Distribution:")
    for level, count in df['experience_min_years'].value_counts().sort_index().items():
        avg_sal = df[df['experience_min_years'] == level]['salary_median_cad'].mean()
        pct = 100 * count / len(df)
        print(f"  {level:2d} years: {count:3d} ({pct:5.1f}%) | ${avg_sal:>10,.0f} avg")
    
    print("\n✨ All aggregations complete!")
    return 0


if __name__ == '__main__':
    exit(main())
