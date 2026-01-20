import plotly.graph_objects as go

# Timeline points
timeline = ['Dec 2023', 'May 2024', 'Nov 2024', 'Jun 2025', 'Dec 2025']

# Salaries in thousands CAD
market_median = [65, 75, 85, 95, 105]
my_path = [55, 61, 63.5, 65, 71]

# Position labels for hover info
market_positions = ['Entry', 'Entry', 'Mid', 'Mid', 'Mid']
my_positions = ['JR Associate'] * len(timeline)

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=timeline, y=market_median,
    mode='lines+markers', name='Évolution normale (médiane marché)',
    line=dict(color='#2563eb', width=3), marker=dict(size=8),
    hovertemplate='Date: %{x}<br>Salaire: %{y}K CAD<br>Position: %{customdata}<extra></extra>',
    customdata=market_positions
))

fig.add_trace(go.Scatter(
    x=timeline, y=my_path,
    mode='lines+markers', name='Mon parcours (JR Associate)',
    line=dict(color='#ef4444', width=3), marker=dict(size=8),
    hovertemplate='Date: %{x}<br>Salaire: %{y}K CAD<br>Position: %{customdata}<extra></extra>',
    customdata=my_positions
))

fig.update_layout(
    title='Évolution Salaire — Marché vs Moi (2023–2025)',
    xaxis_title='Timeline',
    yaxis_title='Salaire (K CAD)',
    template='plotly_white',
    hovermode='x unified',
    legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
)

fig.add_annotation(
    text='Stagnation de poste: JR Associate (0–3 ans)',
    x='Jun 2025', y=58,
    showarrow=False, font=dict(size=12, color='#6b7280')
)

# Write to handout
fig.write_html('/home/nouhayla/AI_Salary_Dashboard/handout/salary_position_evolution.html', include_plotlyjs=True, full_html=True)
print('Wrote handout/salary_position_evolution.html')
