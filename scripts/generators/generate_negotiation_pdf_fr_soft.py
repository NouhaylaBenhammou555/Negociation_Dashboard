#!/usr/bin/env python3
"""Generate a softer, collaborative French negotiation speech PDF"""
import os

try:
    from weasyprint import HTML
except ImportError:
    os.system("pip install weasyprint -q")
    from weasyprint import HTML

html = """
<!DOCTYPE html>
<html lang=\"fr\">
<head>
  <meta charset=\"UTF-8\" />
  <title>Discours de Négociation (Version Collaborative)</title>
  <style>
    body{font-family:Georgia, 'Times New Roman', serif; color:#2c3e50; line-height:1.9; margin:50px 60px}
    h1{color:#2563eb; border-bottom:3px solid #2563eb; padding-bottom:12px}
    h2{color:#2563eb; border-left:4px solid #2563eb; padding-left:12px; margin-top:28px}
    h3{color:#34495e; margin-top:18px}
    p{margin:12px 0; text-align:justify}
    ul{margin:8px 0 16px 24px}
    li{margin:6px 0}
    .note{background:#f0f7ff; border-left:4px solid #2563eb; padding:10px 14px; border-radius:4px; margin:12px 0}
    .stat{display:flex; justify-content:space-between; border:1px solid #e2e8f0; padding:10px 12px; border-radius:6px; margin:8px 0}
    .val{color:#2563eb; font-weight:700}
    .closing{margin-top:28px; border-top:1px solid #e2e8f0; padding-top:14px; color:#666; text-align:center}
  </style>
</head>
<body>
  <h1>Négociation Salariale — Version Collaborative</h1>
  <p>Merci de prendre le temps d'échanger. Mon objectif est de trouver, ensemble, un équilibre juste entre la valeur que j'apporte et les cadres internes de rémunération. Je reste pleinement ouvert à vos contraintes et aux fourchettes de l'entreprise.</p>

  <h2>1) Contexte marché (synthèse)</h2>
  <p>D'après nos analyses 2026 (Montréal, profils IA 2–3 ans), la fourchette de référence est :</p>
  <div class=\"stat\"><span>Conservateur (P25)</span><span class=\"val\">85 000 $</span></div>
  <div class=\"stat\"><span>Médiane (P50)</span><span class=\"val\">95 000 $</span></div>
  <div class=\"stat\"><span>Ambition (P75)</span><span class=\"val\">110 000 $</span></div>
  <div class=\"stat\"><span>Avec bonus/équité</span><span class=\"val\">115–125 000 $</span></div>
  <p class=\"note\"><strong>Lecture :</strong> Mon profil est au-dessus de la moyenne du marché sur plusieurs axes (expertise IA full‑stack, livraison, technologies avancées), ce qui justifie une cible dans la partie haute de la fourchette, tout en restant raisonnable.</p>

  <h2>2) Apport et impact (très bref)</h2>
  <ul>
    <li>8 projets livrés (client, FinLabs, interne) avec mise en production</li>
    <li>Compétences couvrant GenAI/LLM, MLOps, DL, intégration et cloud</li>
    <li>Progression notable des soft skills (communication, leadership, résolution)</li>
  </ul>

  <h2>3) Proposition collaborative</h2>
  <h3>Base salariale (cible)</h3>
  <p>Je proposerais une base à <strong>105 000 $</strong>, qui se situe entre la médiane et le P75, cohérente avec mon périmètre actuel et l'impact visé.</p>
  <h3>Flexibilités</h3>
  <ul>
    <li>Équilibrage base/bonus (plage 10–15%) selon vos pratiques</li>
    <li>Revue à 6 mois avec objectifs mesurables (livrables, ownership, mentoring)</li>
    <li>Possibilité d'une part d'équité alignée sur la trajectoire</li>
  </ul>

  <h2>4) Alignement & prochaines étapes</h2>
  <p>Je souhaite rester parfaitement aligné avec vos grilles internes. Si nécessaire, nous pouvons partir sur une rampe (ex. palier initial + re‑calibrage à 6 mois) afin de matérialiser la progression attendue.</p>

  <h2>Formulation courte à l'oral</h2>
  <p>« Compte tenu du marché à Montréal pour 2–3 ans d'expérience et de mon périmètre (8 livraisons, GenAI/MLOps, intégration), viser <strong>105 000 $</strong> me paraît juste, avec un bonus 10–15% selon vos standards. Je suis ouvert à un ajustement progressif et à des objectifs clairs à 6 mois pour sécuriser l'alignement. »</p>

  <div class=\"closing\">Préparé en janvier 2026 · Basé sur analyses marché & réalisations</div>
</body>
</html>
"""

with open('/tmp/negotiation_soft_fr.html','w',encoding='utf-8') as f:
    f.write(html)

print('Conversion en PDF (version collaborative FR)...')
HTML('/tmp/negotiation_soft_fr.html').write_pdf('negotiation_soft.pdf')
print('✓ negotiation_soft.pdf créé')
