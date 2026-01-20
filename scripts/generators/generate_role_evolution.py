#!/usr/bin/env python3
import os
import pandas as pd
import plotly.express as px

os.makedirs('handout', exist_ok=True)
roles_path = 'data/role_evolution_sourced.csv'

def end_year(r):
    try:
        if '+' in r:
            return int(r.replace('+',''))
        if '-' in r:
            return int(r.split('-')[-1])
        return int(r)
    except:
        return None

if os.path.exists(roles_path):
    # sourced CSV may have comment lines starting with '#'
    roles_df = pd.read_csv(roles_path, comment='#')
    # Expect columns: level,years_from,years_to,typical_titles,...
    if 'typical_titles' in roles_df.columns and 'years_to' in roles_df.columns and 'years_from' in roles_df.columns:
        role_evo = roles_df[['typical_titles','years_from','years_to']].copy()
        role_evo = role_evo.rename(columns={'typical_titles':'Typical_Title','years_from':'start_year','years_to':'end_year'})
        # use year columns as numeric
        role_evo['start_year'] = pd.to_numeric(role_evo['start_year'], errors='coerce')
        role_evo['end_year'] = pd.to_numeric(role_evo['end_year'], errors='coerce')
        role_evo = role_evo.dropna(subset=['start_year','end_year'])
        # Create a year range label
        role_evo['Year_Range'] = role_evo.apply(lambda r: f"{r['start_year']:.1f}–{r['end_year']:.0f} yrs", axis=1)
        fig = px.bar(role_evo, x='end_year', y='Typical_Title', orientation='h', labels={'end_year':'Years (approx)','Typical_Title':'Title'}, title='AI Role Titles by Approx Years', hover_data={'Year_Range':True, 'end_year':False})
        fig.update_layout(height=420)
        out_html = 'handout/role_evolution.html'
        fig.write_html(out_html, include_plotlyjs=True)
        print('Wrote', out_html)
    else:
        print('CSV present but missing expected columns (typical_titles, years_to, years_from):', roles_path)
