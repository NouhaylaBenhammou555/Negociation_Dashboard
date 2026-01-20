#!/usr/bin/env python3
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

os.makedirs('handout', exist_ok=True)

# VIS 3 — Min/Avg/Max Salary Distribution (Matplotlib)
try:
    ai_geo = pd.read_csv('data/ai_geo.csv')
    ai_geo_plot = ai_geo.set_index('Geography_Level')[['Min_Salary','Avg_Salary','Max_Salary']]
    ax = ai_geo_plot.plot(kind='bar', figsize=(10,5), color=['#D13438','#FFB900','#107C10'])
    ax.set_title('Salary Distribution by Geography (CAD)')
    ax.set_ylabel('Salary (CAD)')
    plt.tight_layout()
    vis3_png = 'handout/vis3_salary_distribution.png'
    plt.savefig(vis3_png)
    plt.close()
    with open('handout/vis3_salary_distribution.html','w') as f:
        f.write(f"<html><body><h3>Salary Distribution by Geography (CAD)</h3><img src=\"{os.path.basename(vis3_png)}\" style=\"width:100%\"></body></html>")
    print('Wrote', vis3_png)
except Exception as e:
    print('VIS3 failed:', e)

# VIS 5 — 2–3 Years Detailed Table (Print -> HTML table)
try:
    exp_23 = pd.read_csv('data/exp_23.csv')
    exp_23_filtered = exp_23[(exp_23['Years_Experience']=='2-3') & (exp_23['Role']=='AI Engineer')]
    out_html = 'handout/vis5_2_3_years_table.html'
    with open(out_html,'w') as f:
        f.write('<html><body><h3>Salary Details (2–3 Years Experience, CAD)</h3>')
        f.write(exp_23_filtered.to_html(index=False, classes='table'))
        f.write('</body></html>')
    print('Wrote', out_html)
except Exception as e:
    print('VIS5 failed:', e)

# VIS 6 — AI Demand Timeline (Seaborn)
try:
    timeline = pd.read_csv('data/timeline.csv')
    plt.figure(figsize=(10,5))
    sns.lineplot(data=timeline, x='Year', y='Job_Postings_Index', hue='Data_Type', linewidth=3)
    plt.title('AI Engineer Demand Growth (2020–2030)')
    plt.ylabel('Job Postings Index')
    plt.xlabel('Year')
    plt.tight_layout()
    vis6_png = 'handout/vis6_ai_demand_timeline.png'
    plt.savefig(vis6_png)
    plt.close()
    with open('handout/vis6_ai_demand_timeline.html','w') as f:
        f.write(f"<html><body><h3>AI Engineer Demand Growth (2020–2030)</h3><img src=\"{os.path.basename(vis6_png)}\" style=\"width:100%\"></body></html>")
    print('Wrote', vis6_png)
except Exception as e:
    print('VIS6 failed:', e)

# VIS 7 — AI Salary Projection (Seaborn)
try:
    timeline = pd.read_csv('data/timeline.csv')
    if 'Avg_Salary_CAD' not in timeline.columns and 'Avg_Salary_USD' in timeline.columns:
        usd_to_cad = 1.35
        timeline['Avg_Salary_CAD'] = timeline['Avg_Salary_USD'] * usd_to_cad
    plt.figure(figsize=(10,5))
    sns.lineplot(data=timeline, x='Year', y='Avg_Salary_CAD', color='#107C10', linewidth=3, marker='o')
    plt.title('AI Engineer Salary Projection (CAD)')
    plt.ylabel('Salary (CAD)')
    plt.xlabel('Year')
    plt.tight_layout()
    vis7_png = 'handout/vis7_salary_projection.png'
    plt.savefig(vis7_png)
    plt.close()
    with open('handout/vis7_salary_projection.html','w') as f:
        f.write(f"<html><body><h3>AI Engineer Salary Projection (CAD)</h3><img src=\"{os.path.basename(vis7_png)}\" style=\"width:100%\"></body></html>")
    print('Wrote', vis7_png)
except Exception as e:
    print('VIS7 failed:', e)

# VIS 8 — AI Investment by Industry (Seaborn)
try:
    industry = pd.read_csv('data/industry.csv')
    industry_sorted = industry.sort_values('AI_Investment_Billion_USD', ascending=False)
    plt.figure(figsize=(10,6))
    sns.barplot(data=industry_sorted, y='Industry', x='AI_Investment_Billion_USD', palette='viridis')
    plt.title('AI Investment by Industry (2026, Billion USD)')
    plt.xlabel('Investment (Billion USD)')
    plt.tight_layout()
    vis8_png = 'handout/vis8_investment_by_industry.png'
    plt.savefig(vis8_png)
    plt.close()
    with open('handout/vis8_investment_by_industry.html','w') as f:
        f.write(f"<html><body><h3>AI Investment by Industry (2026, Billion USD)</h3><img src=\"{os.path.basename(vis8_png)}\" style=\"width:100%\"></body></html>")
    print('Wrote', vis8_png)
except Exception as e:
    print('VIS8 failed:', e)
