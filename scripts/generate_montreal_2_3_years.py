#!/usr/bin/env python3
"""
Generate Montreal 2-3 years experience AI Engineer salary chart (Min/Avg/Max)
"""

import pandas as pd
import plotly.graph_objects as go
import os

def generate_montreal_2_3_years_chart():
    """Generate bar chart showing min/avg/max for Montreal AI Engineers with 2-3 years experience"""
    
    # Load master data
    df = pd.read_csv('data/real_data/stat_master_salaries.csv')
    
    # Filter for Montreal, 2-3 years experience (using 0-3 years as closest match)
    montreal_2_3 = df[
        (df['city'] == 'Montreal') & 
        (df['exp_level'].isin(['0-3 years', '2-5 years']))
    ]
    
    if len(montreal_2_3) == 0:
        print("⚠️ No records found for Montreal 2-3 years experience")
        return
    
    # Calculate statistics
    min_salary = montreal_2_3['salary_median'].min()
    avg_salary = montreal_2_3['salary_median'].mean()
    max_salary = montreal_2_3['salary_median'].max()
    count = len(montreal_2_3)
    
    print(f"📊 Montreal AI Engineers (2-3 years experience):")
    print(f"Min: ${min_salary:,.0f}")
    print(f"Avg: ${avg_salary:,.0f}")
    print(f"Max: ${max_salary:,.0f}")
    print(f"Count: {count} records")
    
    # Create bar chart
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=['Min', 'Avg', 'Max'],
        y=[min_salary, avg_salary, max_salary],
        text=[f'${min_salary:,.0f}', f'${avg_salary:,.0f}', f'${max_salary:,.0f}'],
        textposition='outside',
        marker=dict(
            color=['#ef4444', '#10b981', '#2563eb'],
            line=dict(color='white', width=2)
        ),
        hovertemplate='<b>%{x}</b><br>$%{y:,.0f}<extra></extra>',
        showlegend=False
    ))
    
    fig.update_layout(
        title=dict(
            text=f'Montreal AI Engineer Salary (2-3 Years Experience)<br><sub>{count} records | $57K-$125K range</sub>',
            x=0.5,
            xanchor='center',
            font=dict(size=16, family='Inter, system-ui, sans-serif')
        ),
        yaxis=dict(
            title='Salary (CAD)',
            tickformat='$,.0f',
            gridcolor='#e5e9f0',
            zeroline=False
        ),
        xaxis=dict(
            title='',
            tickfont=dict(size=13, family='Inter, system-ui, sans-serif')
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family='Inter, system-ui, sans-serif', color='#374151'),
        margin=dict(l=60, r=30, t=80, b=60),
        height=400,
        hovermode='x unified'
    )
    
    # Save output
    os.makedirs('outputs/handout', exist_ok=True)
    output_path = 'outputs/handout/montreal_2_3_years.html'
    fig.write_html(output_path, include_plotlyjs=True)
    
    print(f"✅ Chart saved to {output_path}")

if __name__ == '__main__':
    generate_montreal_2_3_years_chart()
