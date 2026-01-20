# Plan de données réelles et scraping

## 1) Salaires & percentiles (Benchmark + Négociation)
- **Types de données**
  - Par ville (Montreal, Toronto, Vancouver, Remote Canada) : p10, p25, p50, p75, p90, currency, sample_size.
  - Points individuels : title, level, location, years_of_experience (YOE), base, bonus, stock, total, currency, date.
  - Agrégés YOE : yoe_bucket, location, p25/p50/p75, avg_base, avg_total.
  - Total comp 2–3 ans : base, bonus, equity, total.
- **Sources potentielles**
  - Glassdoor Salaries (public pages) — percentiles/fourchettes par ville.
  - Levels.fyi (export CSV/JSON) — points individuels avec YOE et comp détaillée.
  - Statistique Canada (NOC 21211/21231) — salaires annuels par région (P10/P50/P90 si dispo).
  - Indeed/LinkedIn Salaries (estimations) — complément si accessible.
- **Scraping / ingestion**
  - Glassdoor : sauvegarde HTML manuelle + parsing (script `scripts/extract_glassdoor_html.py`).
  - Levels.fyi : export manuel CSV/JSON ; ingestion directe sans scraping.
  - StatCan : téléchargement CSV via tables publiques ; ingestion pandas.

## 2) Geo (Min/Avg/Max par localisation)
- **Données** : p10/p25/p50/p75/p90 ou min/avg/max par ville, currency.
- **Sources** : Glassdoor (par ville), Levels.fyi (filtre location), StatCan (par CMA si dispo).
- **Scraping / ingestion** : mêmes inputs que (1). Mapping vers `ai_geo` et percentiles.

## 3) Salaire vs Expérience & Progression
- **Données** : points (YOE, salary, location, title/level), courbe agrégée par YOE.
- **Sources** : Levels.fyi (principal), Glassdoor (si buckets YOE), StatCan (tenure, plus agrégé).
- **Scraping / ingestion** : ingestion CSV/JSON Levels.fyi ; agrégation pandas.

## 4) Total Compensation 2–3 ans & Table détaillée
- **Données** : base, bonus, equity, total pour YOE 2–3, par ville.
- **Sources** : Levels.fyi (filtre YOE 2–3, location), Glassdoor (si dispo), StatCan (bonus rarement couvert).
- **Scraping / ingestion** : filtrage YOE dans l’export Levels.fyi.

## 5) Percentiles globaux & Cibles Négociation
- **Données** : p25/p50/p75 (et p10/p90) pour la jauge et la carte « targets ».
- **Sources** : Glassdoor percentiles ; Levels.fyi percentiles calculés ; StatCan P10/P50/P90.
- **Scraping / ingestion** : calcul pandas sur les exports.

## 6) Demande (Timeline) & Projection Salaire
- **Données** : month, postings_count ou postings_index (base 100), éventuellement salary_index.
- **Sources** : LinkedIn Jobs, Indeed (comptage offres par mois pour AI/ML Engineer Canada).
- **Scraping / ingestion** : export/capture mensuelle (CSV) ; pas de scraping live ici. On ingère via `jobs_timeline`.

## 7) Investissements par industrie (vis8)
- **Données** : industry, year, amount (USD/CAD), source.
- **Sources** : Crunchbase/PitchBook exports ; Stanford AI Index/OECD si tables publiques.
- **Scraping / ingestion** : export CSV (pas de scraping live) ; ingestion directe.

## 8) Rôle / Évolution titres
- **Données** : level, years_from, years_to, titles, source.
- **Sources** : O*NET, BLS (réel) ; NOC (Canada) ; ESCO (UE).
- **Scraping / ingestion** : fichiers téléchargés ou copiés ; déjà réel (role_evolution_sourced.csv). Option d’ajouter NOC/ESCO comme métadonnées.

## 9) Contributions & Skills (Contributions tab)
- **Données** : counts par stream, listes de skills.
- **Sources** : interne (non public).
- **Scraping / ingestion** : non concerné.

## 10) Compétences techniques (optionnel)
- **Données** : skill, date, proficiency (0–9).
- **Sources** : interne ou surveys publiques (Stack Overflow, GitHub API contributions) si tu fournis les exports.
- **Scraping / ingestion** : non prioritaire.

---

# Plan de scraping / ingestion pratique

1) **Glassdoor (percentiles)**
   - Action : sauvegarder la page salaries → `scripts/extract_glassdoor_html.py data/page.html --title "AI/ML Engineer" --location "Montreal" --date YYYY-MM-DD --currency CAD`.
   - Sortie : `data/salaries_glassdoor.csv` (sera renommé en `stat_real_data_glassdoor.csv`).

2) **Levels.fyi (points & YOE)**
   - Action : export CSV/JSON (manuel) filtré Canada. Colonnes : title, level, location, yoe, base, bonus, stock, total, currency, date.
   - Sortie : renommer en `stat_real_data_levels.csv`.

3) **StatCan (NOC 21211/21231)**
   - Action : télécharger le CSV des salaires par région/percentiles (si dispo). Colonnes : region, p10/p50/p90, currency.
   - Sortie : `stat_real_data_statcan.csv`.

4) **Demand timeline (LinkedIn/Indeed)**
   - Action : export mensuel (ou comptage manuel) → CSV `month,role_filter,location,postings_count`.
   - Sortie : `stat_real_data_jobs_timeline.csv`.

5) **Investissements (Crunchbase/PitchBook/AI Index)**
   - Action : export par industrie (year, industry, amount, currency).
   - Sortie : `stat_real_data_investment_by_industry.csv`.

---

# Mapping vers les charts
- Geo / Min-Avg-Max / Percentiles / Salary vs Exp / Total Comp : `stat_real_data_glassdoor.csv` + `stat_real_data_levels.csv` (YOE) → remplacent `ai_geo.csv`, `exp_23.csv`, `exp_position_sector.csv`.
- Jauge & Targets : percentiles dérivés (P25/P50/P75) → remplace valeurs synthétiques.
- Timeline & Projection : `stat_real_data_jobs_timeline.csv` → vis6/vis7.
- Investment : `stat_real_data_investment_by_industry.csv` → vis8.
- Role/Evolution : déjà réel (O*NET/BLS), option d’ajouter NOC/ESCO dans la meta.

---

# Nommage
- Dès qu’on bascule sur du réel : prefix `stat_real_data_*.csv` et update des scripts pour pointer dessus (fallback sur anciens noms si absent).
