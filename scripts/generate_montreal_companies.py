#!/usr/bin/env python3
"""
Generate Montreal companies compensation histogram.
"""

import pandas as pd
import plotly.graph_objects as go
from pathlib import Path

def generate_montreal_companies_chart():
    """Generate histogram of companies in Montreal with their compensation range."""
    
    # Load data
    df = pd.read_csv('data/real_data/stat_master_salaries.csv')
    
    # Filter for Montreal
    montreal_df = df[df['city'] == 'Montreal'].copy()
    
    # Remove Glassdoor Submission entries
    montreal_df = montreal_df[montreal_df['company'] != 'Glassdoor Submission']
    
    # Group by company and get compensation stats
    company_stats = montreal_df.groupby('company').agg({
        'salary_median': ['min', 'mean', 'max', 'count']
    }).reset_index()
    
    company_stats.columns = ['company', 'min_salary', 'avg_salary', 'max_salary', 'count']
    
    # Filter out companies with single records for cleaner viz (or keep all)
    # company_stats = company_stats[company_stats['count'] >= 1]
    
    # Sort by average salary
    company_stats = company_stats.sort_values('avg_salary', ascending=True)
    
    # Create figure
    fig = go.Figure()
    
    # Add error bars showing min to max range
    fig.add_trace(go.Bar(
        name='Average Salary',
        x=company_stats['avg_salary'],
        y=company_stats['company'],
        orientation='h',
        marker_color='#107C10',
        error_x=dict(
            type='data',
            symmetric=False,
            array=company_stats['max_salary'] - company_stats['avg_salary'],
            arrayminus=company_stats['avg_salary'] - company_stats['min_salary'],
            color='#333',
            thickness=1.5,
            width=6
        ),
        text=[f"${x:,.0f}<br>({c} records)" for x, c in zip(company_stats['avg_salary'], company_stats['count'])],
        textposition='auto',
        hovertemplate='<b>%{y}</b><br>' +
                      'Avg: $%{x:,.0f}<br>' +
                      'Range: $%{customdata[0]:,.0f} - $%{customdata[1]:,.0f}<br>' +
                      'Records: %{customdata[2]}<extra></extra>',
        customdata=company_stats[['min_salary', 'max_salary', 'count']].values
    ))
    
    fig.update_layout(
        title='Montreal AI Engineer Salaries by Company',
        xaxis_title='Salary (CAD)',
        yaxis_title='Company',
        height=max(400, len(company_stats) * 35),
        showlegend=False,
        plot_bgcolor='white',
        font=dict(size=12),
        margin=dict(l=150, r=50, t=60, b=60),
        xaxis=dict(
            gridcolor='#e5e9f0',
            showgrid=True,
            zeroline=False,
            tickformat='$,.0f'
        ),
        yaxis=dict(
            showgrid=False,
            showline=False
        )
    )
    
    # Save
    output_dir = Path('outputs/handout')
    output_dir.mkdir(parents=True, exist_ok=True)
    fig.write_html(output_dir / 'montreal_companies.html')
    
    print(f"✅ Generated Montreal companies chart: {len(company_stats)} companies")
    print(f"   Salary range: ${company_stats['min_salary'].min():,.0f} - ${company_stats['max_salary'].max():,.0f}")

if __name__ == '__main__':
    generate_montreal_companies_chart()
