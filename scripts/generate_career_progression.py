#!/usr/bin/env python3
"""
Generate Career Progression chart - Position levels by years of experience.
"""

import plotly.graph_objects as go
from pathlib import Path

def generate_career_progression_chart():
    """Generate career progression chart showing typical position levels by experience."""
    
    # Career stages with typical year ranges
    stages = [
        {'level': 'Intern', 'years_min': 0, 'years_max': 0.5, 'salary_min': 25000, 'salary_max': 50000},
        {'level': 'Entry Level', 'years_min': 0, 'years_max': 2, 'salary_min': 60000, 'salary_max': 85000},
        {'level': 'Junior', 'years_min': 1, 'years_max': 3, 'salary_min': 70000, 'salary_max': 95000},
        {'level': 'Mid-Level', 'years_min': 3, 'years_max': 5, 'salary_min': 85000, 'salary_max': 120000},
        {'level': 'Senior', 'years_min': 5, 'years_max': 8, 'salary_min': 110000, 'salary_max': 160000},
        {'level': 'Staff/Lead', 'years_min': 7, 'years_max': 10, 'salary_min': 140000, 'salary_max': 200000},
        {'level': 'Principal', 'years_min': 9, 'years_max': 13, 'salary_min': 170000, 'salary_max': 250000},
        {'level': 'Distinguished/Executive', 'years_min': 12, 'years_max': 20, 'salary_min': 220000, 'salary_max': 450000},
    ]
    
    fig = go.Figure()
    
    # Add horizontal bars for each career stage
    colors = ['#e3f2fd', '#bbdefb', '#90caf9', '#64b5f6', '#42a5f5', '#1e88e5', '#1565c0', '#0d47a1']
    
    for i, stage in enumerate(stages):
        years_mid = (stage['years_min'] + stage['years_max']) / 2
        years_width = stage['years_max'] - stage['years_min']
        salary_mid = (stage['salary_min'] + stage['salary_max']) / 2
        
        fig.add_trace(go.Bar(
            y=[stage['level']],
            x=[years_width],
            base=[stage['years_min']],
            orientation='h',
            name=stage['level'],
            marker_color=colors[i],
            marker_line_color='#333',
            marker_line_width=1.5,
            hovertemplate=f"<b>{stage['level']}</b><br>" +
                         f"Years: {stage['years_min']}-{stage['years_max']}<br>" +
                         f"Typical Salary: ${stage['salary_min']:,.0f}-${stage['salary_max']:,.0f}<br>" +
                         "<extra></extra>",
            showlegend=False
        ))
        
        # Add salary range text on the bar
        fig.add_annotation(
            x=years_mid,
            y=stage['level'],
            text=f"${salary_mid/1000:.0f}K",
            showarrow=False,
            font=dict(size=11, color='#000', weight='bold'),
            xanchor='center'
        )
    
    fig.update_layout(
        title='AI Engineer Career Progression Path',
        xaxis_title='Years of Experience',
        yaxis_title='Position Level',
        height=500,
        plot_bgcolor='white',
        barmode='overlay',
        font=dict(size=12),
        margin=dict(l=150, r=50, t=60, b=60),
        xaxis=dict(
            gridcolor='#e5e9f0',
            showgrid=True,
            zeroline=True,
            range=[0, 20],
            dtick=2
        ),
        yaxis=dict(
            showgrid=False,
            showline=False,
            categoryorder='array',
            categoryarray=['Intern', 'Entry Level', 'Junior', 'Mid-Level', 'Senior', 'Staff/Lead', 'Principal', 'Distinguished/Executive']
        ),
        hovermode='closest'
    )
    
    # Save
    output_dir = Path('outputs/handout')
    output_dir.mkdir(parents=True, exist_ok=True)
    fig.write_html(output_dir / 'career_progression.html')
    
    print("✅ Generated Career Progression chart")
    print(f"   Levels: {len(stages)} career stages")
    print(f"   Range: Intern (0-0.5 yrs, $25K-$50K) → Executive (12-20 yrs, $220K-$450K)")

if __name__ == '__main__':
    generate_career_progression_chart()
