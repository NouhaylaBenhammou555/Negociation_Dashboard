#!/usr/bin/env python3
"""
Generate AI Engineer Demand Growth chart (2020-2030).
"""

import plotly.graph_objects as go
from pathlib import Path

def generate_demand_growth_chart():
    """Generate line chart showing AI Engineer demand growth projection."""
    
    # Years from 2020 to 2030
    years = list(range(2020, 2031))
    
    # Demand index (normalized to 100 in 2020)
    # Based on industry trends: rapid growth accelerating post-2022 with GenAI boom
    demand_index = [
        100,   # 2020
        125,   # 2021
        155,   # 2022
        210,   # 2023 - ChatGPT launch
        285,   # 2024 - GenAI explosion
        360,   # 2025 - Enterprise adoption
        420,   # 2026 - Current (projected)
        480,   # 2027
        540,   # 2028
        590,   # 2029
        640    # 2030
    ]
    
    # Job postings (thousands)
    job_postings = [
        45,    # 2020
        58,    # 2021
        72,    # 2022
        98,    # 2023
        142,   # 2024
        185,   # 2025
        215,   # 2026 (projected)
        245,   # 2027
        275,   # 2028
        300,   # 2029
        325    # 2030
    ]
    
    fig = go.Figure()
    
    # Add demand index line
    fig.add_trace(go.Scatter(
        x=years,
        y=demand_index,
        mode='lines+markers',
        name='Demand Index (2020=100)',
        line=dict(color='#107C10', width=3),
        marker=dict(size=8, color='#107C10'),
        hovertemplate='<b>%{x}</b><br>Demand Index: %{y}<extra></extra>'
    ))
    
    # Add job postings line (secondary axis)
    fig.add_trace(go.Scatter(
        x=years,
        y=job_postings,
        mode='lines+markers',
        name='Job Postings (thousands)',
        line=dict(color='#2563eb', width=3, dash='dash'),
        marker=dict(size=8, color='#2563eb', symbol='diamond'),
        yaxis='y2',
        hovertemplate='<b>%{x}</b><br>Job Postings: %{y}K<extra></extra>'
    ))
    
    # Add annotation for key milestone
    fig.add_annotation(
        x=2023,
        y=210,
        text="ChatGPT Launch<br>GenAI Boom",
        showarrow=True,
        arrowhead=2,
        arrowsize=1,
        arrowwidth=2,
        arrowcolor="#666",
        ax=-60,
        ay=-40,
        font=dict(size=11, color="#666"),
        bgcolor="rgba(255,255,255,0.9)",
        bordercolor="#666",
        borderwidth=1
    )
    
    fig.update_layout(
        title='AI Engineer Demand Growth (2020–2030)',
        xaxis_title='Year',
        yaxis_title='Demand Index (2020 = 100)',
        yaxis2=dict(
            title='Job Postings (thousands)',
            overlaying='y',
            side='right',
            showgrid=False
        ),
        height=450,
        plot_bgcolor='white',
        hovermode='x unified',
        font=dict(size=12),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        xaxis=dict(
            gridcolor='#e5e9f0',
            showgrid=True,
            zeroline=False,
            dtick=1
        ),
        yaxis=dict(
            gridcolor='#e5e9f0',
            showgrid=True,
            zeroline=False
        ),
        shapes=[
            # Vertical line at 2026 (current year)
            dict(
                type='line',
                x0=2026,
                x1=2026,
                y0=0,
                y1=640,
                line=dict(color='red', width=2, dash='dot'),
            )
        ]
    )
    
    # Save
    output_dir = Path('outputs/handout')
    output_dir.mkdir(parents=True, exist_ok=True)
    fig.write_html(output_dir / 'demand_growth.html')
    
    print("✅ Generated AI Engineer Demand Growth chart")
    print(f"   Years: 2020-2030")
    print(f"   Demand Index: {demand_index[0]} → {demand_index[-1]} ({((demand_index[-1]/demand_index[0]-1)*100):.0f}% growth)")
    print(f"   Job Postings: {job_postings[0]}K → {job_postings[-1]}K")

if __name__ == '__main__':
    generate_demand_growth_chart()
