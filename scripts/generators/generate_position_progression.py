#!/usr/bin/env python3
import os
import pandas as pd
import plotly.graph_objects as go

os.makedirs('handout', exist_ok=True)
roles_path = 'data/role_evolution_sourced.csv'

if os.path.exists(roles_path):
    roles_df = pd.read_csv(roles_path, comment='#')
    
    if 'level' in roles_df.columns and 'years_from' in roles_df.columns and 'years_to' in roles_df.columns:
        # Create position progression data
        positions = roles_df[['level', 'years_from', 'years_to']].copy()
        positions['years_from'] = pd.to_numeric(positions['years_from'], errors='coerce')
        positions['years_to'] = pd.to_numeric(positions['years_to'], errors='coerce')
        positions = positions.dropna(subset=['years_from', 'years_to'])
        
        # Create a timeline visualization
        fig = go.Figure()
        
        colors = ['#636efa', '#EF553B', '#00cc96', '#ab63fa', '#FFA15A', '#19d3f3']
        
        for idx, row in positions.iterrows():
            level = row['level']
            start = row['years_from']
            end = row['years_to']
            duration = end - start
            
            fig.add_trace(go.Bar(
                x=[duration],
                y=[level],
                orientation='h',
                name=level,
                marker=dict(color=colors[idx % len(colors)]),
                text=f"{start:.1f}–{end:.0f} yrs",
                textposition="auto",
                hovertemplate=f"<b>{level}</b><br>Years: {start:.1f}–{end:.0f}<extra></extra>",
                showlegend=False,
                base=start
            ))
        
        fig.update_layout(
            title='AI Engineer Career Progression by Years of Experience',
            xaxis_title='Years of Experience',
            yaxis_title='Position Level',
            barmode='overlay',
            height=400,
            hovermode='closest',
            template='plotly_white',
            xaxis=dict(range=[0, 30])
        )
        
        out_html = 'handout/position_progression.html'
        fig.write_html(out_html, include_plotlyjs=True)
        print('Wrote', out_html)
    else:
        print('CSV missing expected columns')
else:
    print('Missing', roles_path)
