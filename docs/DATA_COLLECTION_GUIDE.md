# Guide de Collecte des Sources de Données Supplémentaires

## 🎯 Sources Prioritaires à Ajouter

### 1. **Glassdoor - Autres Villes** (Priorité: HAUTE)
**Status**: 5/10 villes collectées

#### Villes à collecter:
- [ ] Toronto direct: `https://www.glassdoor.ca/Salaries/toronto-ai-engineer-salary-SRCH_IL.0,7_IM976_KO8,19.htm`
- [ ] Vancouver direct: `https://www.glassdoor.ca/Salaries/vancouver-ai-engineer-salary-SRCH_IL.0,9_IM972_KO10,21.htm`
- [ ] Calgary: `https://www.glassdoor.ca/Salaries/calgary-ai-engineer-salary-SRCH_IL.0,7_IM911_KO8,19.htm`
- [ ] Ottawa: `https://www.glassdoor.ca/Salaries/ottawa-ai-engineer-salary-SRCH_IL.0,6_IM913_KO7,18.htm`
- [ ] Canada (national): `https://www.glassdoor.ca/Salaries/canada-ai-engineer-salary-SRCH_IN3_KO7,18.htm`

**Comment collecter:**
1. Ouvre chaque URL dans le navigateur
2. Scroll down pour charger toutes les soumissions
3. Ctrl+S → Save as `glassdoor_[ville].html` dans `data/glassdoor_pages/`
4. Répète pour chaque page de soumissions (bouton "Next")

**Extraction:**
```bash
python3 scripts/scrapers/extract_glassdoor_submissions.py \
  --html-dir data/glassdoor_pages \
  --out data/real_data/stat_real_data_submissions_all.csv
```

---

### 2. **Levels.fyi** (Priorité: HAUTE)
**Type**: Salaires par entreprise tech avec niveaux (L3, L4, L5, etc.)

#### URLs à visiter:
- AI/ML Engineer Canada: `https://www.levels.fyi/t/software-engineer/locations/canada`
- Filter: "Machine Learning Engineer" ou "AI Engineer"

**Comment collecter:**
1. Va sur Levels.fyi
2. Filter par:
   - Location: Canada
   - Title: "Machine Learning Engineer" / "AI Engineer"
   - Companies: Google, Meta, Amazon, Microsoft, Shopify, etc.
3. Export data:
   - Option A: Copie le tableau → Excel → Save as CSV
   - Option B: Save page as HTML → parse avec script

**Fichier de sortie**: `data/real_data/stat_real_data_levelsfyi.csv`

**Colonnes attendues:**
- company, title, level, location, total_comp, base_salary, stock, bonus, years_experience

---

### 3. **LinkedIn Salary Insights** (Priorité: MOYENNE)
**Type**: Salaires moyens par entreprise et location

#### URL:
`https://www.linkedin.com/salary/ai-engineer-salaries-in-canada`

**Comment collecter:**
1. LinkedIn Premium requis (ou compte gratuit limité)
2. Search: "AI Engineer" + Location
3. Screenshot ou copie manuelle des données
4. Create CSV: `data/real_data/stat_real_data_linkedin.csv`

**Colonnes:**
- company, location, median_salary, salary_range, sample_size

---

### 4. **Payscale.com** (Priorité: MOYENNE)
**Type**: Salaires détaillés avec skills, certifications

#### URL:
`https://www.payscale.com/research/CA/Job=Artificial_Intelligence_(AI)_Engineer/Salary`

**Comment collecter:**
1. Visit URL
2. Note data par:
   - Experience level
   - Skills (Python, TensorFlow, PyTorch)
   - Location
   - Education (Bachelor, Master, PhD)
3. Manual entry ou screenshot → parse

**Fichier**: `data/real_data/stat_real_data_payscale.csv`

---

### 5. **Built In** (Priorité: BASSE)
**Type**: Startups et tech companies canadiennes

#### URLs:
- Toronto: `https://www.builtincanada.com/salaries/ai-machine-learning/ai-engineer/toronto`
- Vancouver: `https://www.builtincanada.com/salaries/ai-machine-learning/ai-engineer/vancouver`

**Comment collecter:**
Save HTML → parse company listings

---

### 6. **Government of Canada - Job Bank** (DÉJÀ COLLECTÉ)
**Status**: ✅ Collecté mais salaires trop bas (générique tech, pas AI-specific)
**Fichier**: `data/real_data/stat_real_data_scraped_jobs.csv`

**Note**: Garder comme baseline minimum, mais ne pas utiliser comme référence principale.

---

### 7. **Statistics Canada (StatCan)** (Priorité: BASSE)
**Type**: Données macro sur les salaires tech

#### URLs:
- NOC 21211 (Data Scientists): https://www.jobbank.gc.ca/marketreport/wages-occupation/5485/ca
- NOC 21231 (Software Engineers): https://www.jobbank.gc.ca/marketreport/wages-occupation/5486/ca

**Status**: Données trop génériques pour AI Engineer spécifique

---

## 📊 Récapitulatif des Sources

| Source | Priorité | Status | Type de Données | Fichier de Sortie |
|--------|----------|--------|-----------------|-------------------|
| Glassdoor Montreal | HAUTE | ✅ Collecté (5 pages) | Soumissions individuelles | `stat_real_data_submissions_all.csv` |
| Glassdoor Toronto | HAUTE | ❌ À collecter | Soumissions individuelles | (append to submissions) |
| Glassdoor Vancouver | HAUTE | ❌ À collecter | Soumissions individuelles | (append to submissions) |
| Glassdoor Canada | HAUTE | ❌ À collecter | Statistiques nationales | `stat_real_data_glassdoor.csv` |
| Levels.fyi | HAUTE | ❌ À collecter | Salaires par entreprise+niveau | `stat_real_data_levelsfyi.csv` |
| LinkedIn | MOYENNE | ❌ À collecter | Salaires par entreprise | `stat_real_data_linkedin.csv` |
| Payscale | MOYENNE | ❌ À collecter | Salaires par skills | `stat_real_data_payscale.csv` |
| Job Bank | BASSE | ✅ Collecté | Baseline minimum | `stat_real_data_scraped_jobs.csv` |

---

## 🎯 Objectif de Collecte

**Minimum requis pour dashboard crédible:**
- ✅ 1 source principale (Glassdoor) - FAIT
- ❌ 2-3 villes supplémentaires Glassdoor (Toronto, Vancouver, Canada)
- ❌ 1 source enterprise (Levels.fyi)
- ❌ 1 source alternative (LinkedIn ou Payscale)

**Total submissions visé**: 200-300 (actuellement: 80)

---

## 🚀 Ordre de Collecte Recommandé

1. **Phase 1** (30 min): Glassdoor Toronto + Vancouver + Canada
   - 3 villes × 3-5 pages = 9-15 HTMLs
   - +150-200 soumissions

2. **Phase 2** (20 min): Levels.fyi
   - Export CSV des top companies
   - ~50-100 data points

3. **Phase 3** (optionnel): LinkedIn ou Payscale
   - Données complémentaires

---

## 📝 Notes de Collecte

- **Glassdoor**: Scroll pour charger toutes soumissions, sauvegarder chaque page
- **Levels.fyi**: Besoin d'account, possibilité d'export direct
- **LinkedIn**: Premium utile mais pas obligatoire
- **Toujours noter**: Date de collecte, URL source, méthode

---

## 🔧 Scripts Disponibles

```bash
# Extract Glassdoor submissions
python3 scripts/scrapers/extract_glassdoor_submissions.py --html-dir data/glassdoor_pages

# Extract Glassdoor companies
python3 scripts/scrapers/extract_glassdoor_companies.py [html_file] --location [city]

# Process all Glassdoor pages
python3 scripts/scrapers/process_all_glassdoor_pages.py --html-dir data/glassdoor_pages
```

---

**Prochaine étape**: Collecte Glassdoor Toronto/Vancouver/Canada
