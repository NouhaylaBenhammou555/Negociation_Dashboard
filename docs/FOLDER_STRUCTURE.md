# AI Salary Dashboard — Structure organisée

```
AI_Salary_Dashboard/
├── salary_handout_tabs.html          # Dashboard principal (point d'entrée)
├── dashboard.ipynb                    # Notebook Jupyter (analyse/exploration)
│
├── data/                              # Toutes les données
│   ├── sample_data/                   # Données synthétiques/exemples
│   │   ├── AI_Demand_By_Industry_2026.csv
│   │   ├── AI_Engineer_Demand_Timeline.csv
│   │   ├── Market_Analysis_Salary_Data.csv
│   │   ├── Salary_2-3_Years_Experience_Detailed.csv
│   │   └── Salary_By_Experience.csv
│   │
│   ├── templates/                     # Templates CSV pour ingestion
│   │   ├── investment_by_industry_template.csv
│   │   ├── jobs_timeline_template.csv
│   │   ├── salaries_glassdoor_template.csv
│   │   └── salaries_levels_template.csv
│   │
│   ├── real_data/                     # Données réelles (à peupler : stat_real_data_*)
│   │   └── (vide pour l'instant)
│   │
│   └── *.csv                          # Données actives (baseline synthétique)
│       ├── ai_geo.csv
│       ├── exp_23.csv
│       ├── exp_position_sector.csv
│       ├── industry.csv
│       ├── role_evolution_sourced.csv  # Réel (O*NET/BLS)
│       ├── technical_skills_evolution.csv
│       └── timeline.csv
│
├── outputs/                           # Tous les outputs générés
│   ├── handout/                       # Charts HTML/PNG
│   │   ├── kpis.html
│   │   ├── geo.html
│   │   ├── industry_share.html
│   │   ├── vis3_salary_distribution.html
│   │   ├── exp_progression.html
│   │   ├── salary_vs_exp.html
│   │   ├── percentiles.html
│   │   ├── total_comp.html
│   │   ├── vis6_ai_demand_timeline.html
│   │   ├── vis7_salary_projection.html
│   │   ├── vis8_investment_by_industry.html
│   │   ├── role_evolution.html
│   │   ├── position_progression.html
│   │   ├── salary_position_evolution.html
│   │   ├── value_propositions_radar.html
│   │   ├── salary_targets_gauge.html
│   │   ├── technical_skills_evolution.html
│   │   └── *.png (fallback images)
│   │
│   └── pdfs/                          # PDFs générés
│       ├── README.pdf
│       ├── negotiation.pdf
│       └── negotiation_soft.pdf
│
├── scripts/                           # Tous les scripts
│   ├── scrapers/                      # Scripts de scraping/parsing
│   │   └── extract_glassdoor_html.py
│   │
│   └── generators/                    # Scripts de génération
│       ├── convert_to_pdf.py
│       ├── generate_negotiation_pdf.py
│       ├── generate_negotiation_pdf_fr.py
│       ├── generate_negotiation_pdf_fr_soft.py
│       ├── generate_negotiation_visuals.py
│       ├── generate_position_progression.py
│       ├── generate_role_evolution.py
│       ├── generate_salary_position_evolution.py
│       ├── generate_tech_skills.py
│       └── generate_visuals.py
│
├── docs/                              # Documentation
│   ├── README.md
│   └── REAL_DATA_SCRAPING_PLAN.md
│
└── tools/                             # Outils divers (si nécessaire)
```

---

## Changements effectués

1. **data/** : organisé en 3 sous-dossiers
   - `sample_data/` : anciens CSV racine (AI_*, Salary_*, Market_*)
   - `templates/` : gabarits CSV pour ingestion de données réelles
   - `real_data/` : futur emplacement des exports réels (préfixés `stat_real_data_*`)

2. **outputs/** : centralise tous les fichiers générés
   - `handout/` : tous les HTMLs/PNGs de charts (anciennement `handout/` racine)
   - `pdfs/` : tous les PDFs (README, négociation)

3. **scripts/** : séparé en deux types
   - `scrapers/` : parsing/ingestion (Glassdoor, Levels, etc.)
   - `generators/` : génération de charts, PDFs, visuals

4. **docs/** : documentation centralisée (README, plan de scraping)

5. **Racine** : garde uniquement les fichiers essentiels
   - `salary_handout_tabs.html` (dashboard principal)
   - `dashboard.ipynb` (notebook)

---

## Prochaines étapes

1. Peupler `data/real_data/` avec les exports Glassdoor/Levels/LinkedIn → CSV préfixés `stat_real_data_*`
2. Mettre à jour les scripts générateurs pour lire prioritairement `data/real_data/stat_real_data_*` (fallback sur `data/*.csv`)
3. Régénérer tous les visuels avec données réelles
