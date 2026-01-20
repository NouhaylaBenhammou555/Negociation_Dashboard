# Guide : Sauvegarder et Utiliser les Dashboards en Local

## 🎯 Objectif
Ce guide explique comment sauvegarder et utiliser les dashboards avec leurs charts interactifs **sans connexion internet**.

## ✅ Configuration Effectuée

Tous les fichiers HTML générés incluent maintenant la bibliothèque Plotly.js **complète** au lieu d'utiliser un CDN. Cela permet de :
- ✨ Conserver l'interactivité (zoom, hover, etc.)
- 📂 Ouvrir les fichiers localement sans internet
- 💾 Partager les fichiers facilement

## 📦 Fichiers Disponibles

### Dashboards Individuels
- `outputs/handout/salary_handout_benchmark.html` (24 MB)
- `outputs/handout/salary_handout_contribution.html` (4.7 MB)
- `outputs/handout/salary_handout_negotiation.html` (35 KB)

### Dashboard Complet (Tous en Un)
- `outputs/handout/salary_handout_complete.html` (28 MB)

### Charts Individuels
Tous les charts dans `outputs/handout/` :
- `kpis.html`, `geo.html`, `industry_share.html`
- `exp_progression.html`, `salary_vs_exp.html`, etc.

## 💾 Comment Sauvegarder en Local

### Méthode 1 : Copier le Dossier Complet
```bash
# Copier tout le dossier outputs/handout
cp -r outputs/handout ~/Documents/Salary_Dashboards/
```

### Méthode 2 : Télécharger via le Navigateur
1. Ouvrez le dashboard dans votre navigateur
2. Cliquez sur "📋 Print All Dashboards"
3. Dans la nouvelle fenêtre : `Fichier` → `Enregistrer sous...`
4. Choisissez `Page Web, complète` ou `HTML complet`
5. Sauvegardez où vous voulez

### Méthode 3 : Créer une Archive
```bash
# Créer un fichier ZIP
cd outputs
zip -r dashboards_interactive.zip handout/

# Ou créer un tar.gz
tar -czf dashboards_interactive.tar.gz handout/
```

## 🚀 Utilisation Hors Ligne

### Ouvrir les Fichiers
1. **Double-cliquez** sur le fichier HTML
2. Ou cliquez-droit → `Ouvrir avec` → `Navigateur web`
3. Tous les charts seront **interactifs** même sans internet !

### Fonctionnalités Interactives Disponibles
- ✨ **Zoom** : Cliquez-glissez sur le chart
- 🔍 **Hover** : Survolez pour voir les détails
- 👁️ **Légendes** : Cliquez pour masquer/afficher des séries
- 📸 **Export** : Bouton appareil photo pour sauvegarder en PNG
- 🔄 **Reset** : Bouton maison pour réinitialiser la vue

## 📊 Avantages et Inconvénients

### ✅ Avantages
- Fonctionne **sans connexion internet**
- Charts **100% interactifs**
- Peut être **partagé facilement** (USB, email, cloud)
- Pas de dépendance externe
- Ouverture **instantanée**

### ⚠️ Inconvénients
- Fichiers plus **volumineux** (~3-5 MB par chart au lieu de ~50 KB)
- Le dashboard complet fait **28 MB** au lieu de quelques KB
- Temps de chargement légèrement plus long (1-2 secondes)

## 🔧 Pour Régénérer les Charts

Si vous modifiez les données et voulez régénérer les charts :

```bash
# Depuis le notebook Jupyter
# Les nouveaux fichiers incluront automatiquement Plotly.js

# Ou exécuter les scripts
python3 scripts/generate_benchmark_charts.py
python3 scripts/generators/generate_negotiation_visuals.py
python3 scripts/generate_montreal_2_3_years.py
```

## 💡 Conseils

### Pour Partager
- **Email** : Utilisez les fichiers individuels (plus petits)
- **Présentation** : Utilisez `salary_handout_complete.html` (tout en un)
- **Archive** : Créez un ZIP si vous partagez plusieurs fichiers

### Pour Imprimer
- Utilisez le bouton "📋 Print All Dashboards"
- Les charts s'imprimeront avec leurs données interactives

### Pour le Web
Si vous voulez héberger sur un serveur web, vous pouvez :
- Garder `include_plotlyjs=True` (autonome, plus gros)
- Ou revenir à `include_plotlyjs='cdn'` (plus léger, besoin d'internet)

## 📧 Compatibilité

Les fichiers HTML fonctionnent avec :
- ✅ Chrome, Firefox, Safari, Edge (tous les navigateurs modernes)
- ✅ Windows, macOS, Linux
- ✅ Même sans connexion internet
- ✅ Depuis USB, réseau local, ou cloud

## 🎓 Note Technique

La différence entre les deux modes :

```python
# Mode CDN (besoin d'internet)
fig.write_html('chart.html', include_plotlyjs='cdn')
# Fichier léger (~50 KB) mais nécessite internet

# Mode Autonome (fonctionne hors ligne) ✅ ACTUEL
fig.write_html('chart.html', include_plotlyjs=True)
# Fichier plus gros (~3 MB) mais totalement autonome
```

---

**Résumé** : Tous vos dashboards sont maintenant 100% autonomes et interactifs, même sans internet ! 🎉
