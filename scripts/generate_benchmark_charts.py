#!/usr/bin/env python3
"""
Generate Benchmark dashboard charts using REAL salary data.

Updates:
- KPI strip (salary statistics)
- Geography charts (cities in Canada)
- Experience progression
- Salary vs Experience scatter
- Percentiles
- Total Compensation
- Role Evolution (generic career progression)
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
import json


def load_data():
    """Load master salary dataset."""
    return pd.read_csv('data/real_data/stat_master_salaries.csv')


def generate_kpis(df):
    """Generate professional KPI strip with key statistics."""
    
    salary = df['salary_median'].dropna()
    canada_df = df[df['country'] == 'Canada']
    
    kpis = {
        'median': int(salary.median()),
        'p75': int(salary.quantile(0.75)),
        'count': len(df),
        'cities': canada_df['city'].nunique(),
    }
    
    # Professional KPI HTML
    median_fmt = f"${kpis['median']:,}"
    p75_fmt = f"${kpis['p75']:,}"
    count_fmt = kpis['count']
    cities_fmt = kpis['cities']
    
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: #f8f9fa;
            padding: 0;
        }}
        .kpi-strip {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 16px;
            padding: 24px;
            background: white;
        }}
        .kpi {{
            padding: 20px;
            border-radius: 12px;
            border: 1px solid #e5e9f0;
            transition: all 0.3s;
        }}
        .kpi:hover {{
            border-color: #107C10;
            box-shadow: 0 4px 12px rgba(16, 124, 16, 0.1);
        }}
        .kpi-value {{
            font-size: 32px;
            font-weight: 700;
            color: #107C10;
            margin-bottom: 6px;
            line-height: 1;
        }}
        .kpi-label {{
            font-size: 13px;
            color: #666;
            font-weight: 500;
        }}
        .kpi-subtext {{
            font-size: 12px;
            color: #999;
            margin-top: 4px;
        }}
    </style>
</head>
<body>
    <div class="kpi-strip">
        <div class="kpi">
            <div class="kpi-value">{median_fmt}</div>
            <div class="kpi-label">Median Salary</div>
            <div class="kpi-subtext">50th percentile</div>
        </div>
        <div class="kpi">
            <div class="kpi-value">{p75_fmt}</div>
            <div class="kpi-label">75th Percentile</div>
            <div class="kpi-subtext">Top 25% earn more</div>
        </div>
        <div class="kpi">
            <div class="kpi-value">{count_fmt}</div>
            <div class="kpi-label">Total Records</div>
            <div class="kpi-subtext">Real submissions</div>
        </div>
        <div class="kpi">
            <div class="kpi-value">{cities_fmt}</div>
            <div class="kpi-label">Canadian Cities</div>
            <div class="kpi-subtext">Toronto, Montreal, Vancouver...</div>
        </div>
    </div>
</body>
</html>"""
    
    return html, kpis


def generate_geo_chart(df):
    """Avg salary by geography (Canadian cities)."""
    
    canada_df = df[df['country'] == 'Canada'].copy()
    city_stats = canada_df.groupby('city')['salary_median'].agg(['mean', 'count']).reset_index()
    city_stats = city_stats[city_stats['count'] >= 1].sort_values('mean', ascending=False)
    city_stats = city_stats[~city_stats['city'].isin(['Aurora', 'Engineer'])]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=city_stats['city'],
        y=city_stats['mean'],
        marker=dict(color=city_stats['mean'], colorscale='Greens', showscale=False),
        text=city_stats['mean'].apply(lambda x: f'${x:,.0f}'),
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>Avg: $%{y:,.0f}<extra></extra>'
    ))
    
    fig.update_layout(
        title='Average Salary by Canadian City',
        xaxis_title='City',
        yaxis_title='Average Salary (CAD)',
        height=400,
        template='plotly_white',
        hovermode='x'
    )
    
    return fig


def generate_salary_distribution(df):
    """Min/Avg/Max salary distribution by city."""
    
    # Load pre-calculated city stats
    city_stats = pd.read_csv('data/real_data/city_salary_stats.csv')
    
    # Sort by average salary for display
    city_stats = city_stats.sort_values('avg_salary', ascending=False)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Min',
        x=city_stats['city'],
        y=city_stats['min_salary'],
        marker_color='#fee5d9'
    ))
    
    fig.add_trace(go.Bar(
        name='Avg',
        x=city_stats['city'],
        y=city_stats['avg_salary'],
        marker_color='#fdae6b'
    ))
    
    fig.add_trace(go.Bar(
        name='Max',
        x=city_stats['city'],
        y=city_stats['max_salary'],
        marker_color='#e6550d'
    ))
    
    fig.update_layout(
        title='Salary Distribution (Min/Avg/Max) by City',
        xaxis_title='City',
        yaxis_title='Salary (CAD)',
        barmode='group',
        height=400,
        template='plotly_white',
        hovermode='x'
    )
    
    return fig


def generate_exp_progression(df):
    """Salary progression by experience level."""
    
    exp_stats = df.groupby('exp_level')['salary_median'].agg(['mean', 'median', 'count']).reset_index()
    exp_stats = exp_stats.dropna()
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=exp_stats['exp_level'],
        y=exp_stats['mean'],
        mode='lines+markers',
        name='Average',
        line=dict(color='#107C10', width=3),
        marker=dict(size=10)
    ))
    
    fig.add_trace(go.Scatter(
        x=exp_stats['exp_level'],
        y=exp_stats['median'],
        mode='lines+markers',
        name='Median',
        line=dict(color='#2563eb', width=2, dash='dash'),
        marker=dict(size=8)
    ))
    
    fig.update_layout(
        title='Salary Progression by Experience Level',
        xaxis_title='Experience Level',
        yaxis_title='Salary (CAD)',
        height=400,
        template='plotly_white',
        hovermode='x'
    )
    
    return fig


def generate_salary_vs_exp(df):
    """Scatter plot: Salary vs Experience."""
    
    plot_df = df[['exp_years_min', 'salary_median']].dropna().copy()
    plot_df.columns = ['experience', 'salary']
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=plot_df['experience'],
        y=plot_df['salary'],
        mode='markers',
        marker=dict(size=8, opacity=0.6, color='#107C10'),
        hovertemplate='<b>Experience:</b> %{x} yrs<br><b>Salary:</b> $%{y:,.0f}<extra></extra>'
    ))
    
    fig.update_layout(
        title='Salary vs Experience',
        xaxis_title='Years of Experience',
        yaxis_title='Salary (CAD)',
        height=400,
        template='plotly_white',
        hovermode='closest'
    )
    
    return fig


def generate_percentiles(df):
    """Salary percentiles."""
    
    salary = df['salary_median'].dropna()
    
    percentiles = {
        'P10': salary.quantile(0.10),
        'P25': salary.quantile(0.25),
        'P50': salary.quantile(0.50),
        'P75': salary.quantile(0.75),
        'P90': salary.quantile(0.90),
    }
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=list(percentiles.keys()),
        y=list(percentiles.values()),
        marker=dict(
            color=list(percentiles.values()),
            colorscale='Viridis',
            showscale=False
        ),
        text=[f'${v:,.0f}' for v in percentiles.values()],
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>$%{y:,.0f}<extra></extra>'
    ))
    
    fig.update_layout(
        title='Salary Percentiles (Montreal AI Engineers)',
        xaxis_title='Percentile',
        yaxis_title='Salary (CAD)',
        height=400,
        template='plotly_white',
        showlegend=False
    )
    
    return fig


def generate_total_comp(df):
    """Total compensation by experience (violin plot)."""
    
    exp_groups = df.dropna(subset=['salary_median'])
    
    fig = px.box(
        exp_groups,
        x='exp_level',
        y='salary_median',
        points='all',
        title='Total Compensation Distribution by Experience',
        labels={'exp_level': 'Experience Level', 'salary_median': 'Salary (CAD)'},
        height=400,
        template='plotly_white'
    )
    
    return fig


def generate_role_evolution(df):
    """Generic role progression by years."""
    
    roles = {
        '0-2 years': 'Junior AI Engineer',
        '3-5 years': 'AI Engineer',
        '6-8 years': 'Senior AI Engineer',
        '9-12 years': 'Lead AI Engineer',
        '13+ years': 'Principal / Director',
    }
    
    exp_buckets = pd.cut(df['exp_years_min'], bins=[0, 2, 5, 8, 12, 30], 
                         labels=['0-2 years', '3-5 years', '6-8 years', '9-12 years', '13+ years'])
    
    role_data = df.copy()
    role_data['role'] = exp_buckets
    role_salary = role_data.groupby('role')['salary_median'].mean()
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=role_data['exp_years_min'],
        y=role_data['salary_median'],
        mode='markers',
        marker=dict(
            size=8,
            color=role_data['exp_years_min'],
            colorscale='Greens',
            showscale=True,
            colorbar=dict(title='Years Exp')
        ),
        text=[roles.get(str(r), 'AI Engineer') for r in role_data['role']],
        hovertemplate='<b>%{text}</b><br>Exp: %{x} yrs<br>Salary: $%{y:,.0f}<extra></extra>'
    ))
    
    fig.update_layout(
        title='Role Evolution — Typical Progression by Experience',
        xaxis_title='Years of Experience',
        yaxis_title='Salary (CAD)',
        height=400,
        template='plotly_white',
        hovermode='closest'
    )
    
    return fig


def main():
    print("📊 Generating Benchmark charts with REAL data...\n")
    
    df = load_data()
    output_dir = Path('outputs/handout')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. KPIs
    print("📈 KPIs...")
    kpi_html, kpi_data = generate_kpis(df)
    (output_dir / 'kpis.html').write_text(kpi_html)
    
    # 2. Geography
    print("🌍 Geography chart...")
    fig = generate_geo_chart(df)
    fig.write_html(output_dir / 'geo.html')
    
    # 3. Salary Distribution
    print("📊 Salary distribution...")
    fig = generate_salary_distribution(df)
    fig.write_html(output_dir / 'vis3_salary_distribution.html')
    
    # 4. Experience Progression
    print("⏱️  Experience progression...")
    fig = generate_exp_progression(df)
    fig.write_html(output_dir / 'exp_progression.html')
    
    # 5. Salary vs Experience
    print("📈 Salary vs Experience...")
    fig = generate_salary_vs_exp(df)
    fig.write_html(output_dir / 'salary_vs_exp.html')
    
    # 6. Percentiles
    print("📊 Percentiles...")
    fig = generate_percentiles(df)
    fig.write_html(output_dir / 'percentiles.html')
    
    # 7. Total Compensation
    print("💰 Total compensation...")
    fig = generate_total_comp(df)
    fig.write_html(output_dir / 'total_comp.html')
    
    # 8. Role Evolution
    print("👔 Role evolution...")
    fig = generate_role_evolution(df)
    fig.write_html(output_dir / 'role_evolution.html')
    
    # 9. Career Progression (keep existing but use real data ranges)
    print("📈 Career progression...")
    fig = generate_exp_progression(df)
    fig.update_layout(title='Career Progression by Years')
    fig.write_html(output_dir / 'position_progression.html')
    
    print("\n✅ All benchmark charts updated with REAL data!")
    print(f"📁 Saved to: {output_dir}")
    print(f"\n📊 Data used: {len(df)} salary records")
    print(f"   • Glassdoor: {len(df[df['source'] == 'Glassdoor'])} submissions")
    print(f"   • Levels.fyi: {len(df[df['source'] == 'Levels.fyi'])} records")
    print(f"   • Cities: {df[df['country'] == 'Canada']['city'].nunique()}")
    
    return 0


if __name__ == '__main__':
    exit(main())
