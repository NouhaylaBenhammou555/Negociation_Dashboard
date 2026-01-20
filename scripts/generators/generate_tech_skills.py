#!/usr/bin/env python3
import os
import pandas as pd
import plotly.graph_objects as go

os.makedirs('handout', exist_ok=True)
csv_path = 'data/technical_skills_evolution.csv'

if os.path.exists(csv_path):
    df = pd.read_csv(csv_path, parse_dates=['date'])
    df = df.sort_values('date')
    
    # Create line chart with multiple skills
    fig = go.Figure()
    skill_cols = [col for col in df.columns if col != 'date']
    colors = ['#107C10', '#FFB900', '#D13438', '#00BCF2', '#8764B8', '#E74856', '#00B294', '#FF8C00']
    
    for i, skill in enumerate(skill_cols):
        fig.add_trace(go.Scatter(
            x=df['date'], 
            y=df[skill],
            mode='lines+markers',
            name=skill.replace('_', ' '),
            line=dict(width=3, color=colors[i % len(colors)]),
            marker=dict(size=8)
        ))
    
    fig.update_layout(
        title='Technical Skills Evolution Over Time',
        xaxis_title='Date',
        yaxis_title='Proficiency Level (0-10)',
        height=500,
        hovermode='x unified',
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
    )
    
    out_html = 'handout/technical_skills_evolution.html'
    fig.write_html(out_html, include_plotlyjs=True)
    
    try:
        fig.write_image('handout/technical_skills_evolution.png', engine='kaleido')
    except Exception as e:
        print('Skipping PNG export:', e)
    
    print('Wrote', out_html)
else:
    print('Missing', csv_path)
