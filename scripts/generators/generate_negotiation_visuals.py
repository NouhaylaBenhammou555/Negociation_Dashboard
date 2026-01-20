#!/usr/bin/env python3
import os
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

os.makedirs('handout', exist_ok=True)

# 1. Suggested Salary Targets (Gauge Chart)
fig1 = go.Figure(go.Indicator(
    mode = "gauge+number+delta",
    value = 95000,
    title = {'text': "Target Salary (CAD)"},
    delta = {'reference': 85000},
    domain = {'x': [0, 1], 'y': [0, 1]},
    gauge = {
        'axis': {'range': [70000, 130000]},
        'bar': {'color': "#2563eb"},
        'steps': [
            {'range': [70000, 85000], 'color': "#fee2e2"},
            {'range': [85000, 95000], 'color': "#fef3c7"},
            {'range': [95000, 110000], 'color': "#dcfce7"},
            {'range': [110000, 130000], 'color': "#dbeafe"}
        ],
        'threshold': {
            'line': {'color': "red", 'width': 4},
            'thickness': 0.75,
            'value': 110000
        }
    }
))

fig1.add_annotation(
    text="Conservative: $85k | Target: $95k | Aspirational: $110k | With Equity: $115-125k",
    xref="paper", yref="paper",
    x=0.5, y=-0.15,
    showarrow=False,
    font=dict(size=11, color="#666"),
    align="center"
)

fig1.update_layout(height=450, template='plotly_white')
fig1.write_html('handout/salary_targets_gauge.html', include_plotlyjs='cdn')
print("Wrote handout/salary_targets_gauge.html")

# 2. Key Value Propositions (Radar Chart - 5 competencies)
# Tuned to be more realistic and nuanced (not all above market)
categories = ['Full-Stack AI Expertise', 'Proven Delivery', 'Cutting-Edge Tech', 'End-to-End Ownership', 'Growth Trajectory']
# Profile scores (0-100): a balanced self-assessment
values = [78, 82, 76, 80, 74]

fig2 = go.Figure(data=go.Scatterpolar(
    r=values,
    theta=categories,
    fill='toself',
    name='Your Profile',
    line=dict(color='#2563eb'),
    fillcolor='rgba(37, 99, 235, 0.25)'
))

fig2.add_trace(go.Scatterpolar(
    r=[80, 80, 78, 80, 80],
    theta=categories,
    fill='toself',
    name='Market Average',
    line=dict(color='#cbd5e1', dash='dash'),
    fillcolor='rgba(203, 213, 225, 0.1)'
))

fig2.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[0, 100],
            tickfont=dict(size=10)
        ),
        angularaxis=dict(tickfont=dict(size=11))
    ),
    showlegend=True,
    title='Key Value Propositions (vs Market Average) — Calibrated',
    height=500,
    template='plotly_white',
    hovermode='closest'
)

# Add brief footnote for context
fig2.add_annotation(text='Scores indicatifs basés sur livraisons (8), domaines couverts (5) et stack utilisée',
                    xref='paper', yref='paper', x=0.5, y=-0.12,
                    showarrow=False, font=dict(size=11, color='#64748b'))

fig2.write_html('handout/value_propositions_radar.html', include_plotlyjs='cdn')
print("Wrote handout/value_propositions_radar.html")

# 3. Strategic Questions (Visual Checklist/Timeline)
questions = [
    {'q': 'Role Clarity', 'color': '#3b82f6'},
    {'q': 'Salary Range', 'color': '#10b981'},
    {'q': 'Leadership Path', 'color': '#f59e0b'},
    {'q': 'Values Alignment', 'color': '#8b5cf6'},
    {'q': 'Trust & Potential', 'color': '#ec4899'},
    {'q': 'Retention vs Replacement', 'color': '#ef4444'}
]

fig3 = go.Figure()

for idx, item in enumerate(questions):
    fig3.add_trace(go.Bar(
        y=[item['q']],
        x=[1],
        orientation='h',
        marker=dict(color=item['color']),
        name=item['q'],
        text=f"✓ Ask",
        textposition='auto',
        hovertemplate=f"<b>{item['q']}</b><extra></extra>",
        showlegend=False
    ))

fig3.update_layout(
    barmode='overlay',
    title='Strategic Questions to Ask',
    xaxis=dict(visible=False, range=[0, 1.2]),
    yaxis=dict(tickfont=dict(size=12)),
    height=400,
    template='plotly_white',
    margin=dict(l=200, r=50, t=80, b=50)
)

fig3.write_html('handout/strategic_questions.html', include_plotlyjs='cdn')
print("Wrote handout/strategic_questions.html")

# 4. Talking Points (Feature Importance / Skill Bars)
talking_points = [
    {'point': 'Market Alignment (90%)', 'score': 90, 'color': '#2563eb'},
    {'point': 'Versatility (8 projects)', 'score': 88, 'color': '#10b981'},
    {'point': 'Innovation (Agentic AI, GraphRAG)', 'score': 92, 'color': '#f59e0b'},
    {'point': 'Leadership Growth (+100%)', 'score': 85, 'color': '#8b5cf6'},
    {'point': 'Impact (5 deployed tools)', 'score': 87, 'color': '#ec4899'}
]

fig4 = go.Figure()

for item in talking_points:
    fig4.add_trace(go.Bar(
        y=[item['point']],
        x=[item['score']],
        orientation='h',
        marker=dict(color=item['color']),
        text=f"{item['score']}%",
        textposition='auto',
        hovertemplate='<b>%{y}</b><br>Strength: %{x}%<extra></extra>',
        showlegend=False
    ))

fig4.update_layout(
    title='Key Talking Points (Strength by Topic)',
    xaxis_title='Relevance & Strength (%)',
    yaxis_title='',
    xaxis=dict(range=[0, 105]),
    height=400,
    template='plotly_white',
    margin=dict(l=250, r=50, t=80, b=50),
    hovermode='closest'
)

fig4.write_html('handout/talking_points.html', include_plotlyjs='cdn')
print("Wrote handout/talking_points.html")

# 5. Soft Skills Evolution (for visual support)
skills_data = {
    'Skill': ['Communication', 'Leadership', 'Problem-Solving', 'Adaptability', 'Negotiation'],
    'Growth_Pct': [80, 100, 53, 75, 60],
    'Current_Level': [8.5, 8.0, 7.5, 8.0, 7.0]
}

skills_df = pd.DataFrame(skills_data)

fig5 = go.Figure()

fig5.add_trace(go.Bar(
    x=skills_df['Skill'],
    y=skills_df['Growth_Pct'],
    name='Growth %',
    marker=dict(color='#10b981'),
    text=skills_df['Growth_Pct'].astype(str) + '%',
    textposition='auto',
    hovertemplate='<b>%{x}</b><br>Growth: %{y}%<extra></extra>'
))

fig5.update_layout(
    title='Soft Skills Growth Over 2 Years',
    yaxis_title='Growth Percentage (%)',
    xaxis_title='',
    height=400,
    template='plotly_white',
    hovermode='x'
)

fig5.write_html('handout/soft_skills_growth.html', include_plotlyjs=True)
print("Wrote handout/soft_skills_growth.html")

print("\n✓ All negotiation visuals generated successfully!")
