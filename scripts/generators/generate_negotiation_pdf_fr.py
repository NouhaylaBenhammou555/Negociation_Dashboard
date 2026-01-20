#!/usr/bin/env python3
"""Generate a professional negotiation speech PDF in French based on market data and contributions"""
import os

try:
    from weasyprint import HTML, CSS
except ImportError:
    print("Installing weasyprint...")
    os.system("pip install weasyprint -q")
    from weasyprint import HTML, CSS

# Professional negotiation speech in French
negotiation_speech_fr = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Discours de Négociation Salariale IA</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Georgia', 'Times New Roman', serif;
            line-height: 1.9;
            color: #2c3e50;
            background-color: #fff;
            padding: 50px 60px;
            max-width: 900px;
            margin: 0 auto;
        }
        
        .header {
            text-align: center;
            margin-bottom: 50px;
            border-bottom: 3px solid #2563eb;
            padding-bottom: 30px;
        }
        
        .header h1 {
            color: #2563eb;
            font-size: 2.5em;
            margin-bottom: 10px;
            font-weight: 700;
        }
        
        .header p {
            color: #666;
            font-size: 1.1em;
            font-style: italic;
        }
        
        .section {
            margin-bottom: 40px;
            page-break-inside: avoid;
        }
        
        .section h2 {
            color: #2563eb;
            font-size: 1.8em;
            margin-bottom: 20px;
            border-left: 4px solid #2563eb;
            padding-left: 15px;
            font-weight: 700;
        }
        
        .section h3 {
            color: #34495e;
            font-size: 1.3em;
            margin-top: 25px;
            margin-bottom: 12px;
            font-weight: 600;
        }
        
        p {
            margin-bottom: 16px;
            text-align: justify;
            color: #444;
            line-height: 2;
        }
        
        .highlight {
            background-color: #f0f7ff;
            padding: 20px;
            border-left: 4px solid #2563eb;
            margin-bottom: 20px;
            border-radius: 4px;
        }
        
        .highlight strong {
            color: #2563eb;
        }
        
        ul, ol {
            margin-left: 30px;
            margin-bottom: 20px;
            color: #444;
        }
        
        li {
            margin-bottom: 12px;
            line-height: 1.8;
        }
        
        .stat-box {
            background-color: #f8fafc;
            border: 2px solid #e2e8f0;
            padding: 16px;
            margin: 15px 0;
            border-radius: 6px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .stat-value {
            font-size: 1.8em;
            font-weight: 700;
            color: #2563eb;
        }
        
        .stat-label {
            color: #666;
            font-size: 0.95em;
        }
        
        .quote {
            font-style: italic;
            color: #555;
            border-left: 4px solid #8b5cf6;
            padding-left: 20px;
            margin: 20px 0;
            line-height: 1.8;
        }
        
        strong {
            color: #2c3e50;
            font-weight: 600;
        }
        
        .closing {
            margin-top: 50px;
            text-align: center;
            padding-top: 30px;
            border-top: 2px solid #e2e8f0;
            color: #666;
        }
        
        .page-break {
            page-break-after: always;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>Discours de Négociation Salariale</h1>
        <p>Approche Basée sur les Données pour l'Avancement Professionnel et la Rémunération</p>
    </div>

    <div class="section">
        <h2>Déclaration d'Ouverture</h2>
        <p>
            Merci de cette opportunité de discuter de ma rémunération et de mon rôle chez [Entreprise]. 
            Je suis enthousiaste à propos du travail que nous faisons en IA, et je veux m'assurer que ma 
            rémunération reflète à la fois ma contribution à l'organisation et ma valeur marchande en tant 
            que professionnel IA.
        </p>
        <p>
            J'ai préparé cette conversation en me basant sur des données de marché objectives, mon impact 
            démontré et mon engagement envers la création de valeur pour [Entreprise]. Je voudrais vous 
            présenter ce que j'apporte et discuter d'un package de rémunération qui reconnaît cette valeur.
        </p>
    </div>

    <div class="section">
        <h2>Partie 1 : Contexte du Marché et Position</h2>
        
        <h3>Le Marché de l'IA Aujourd'hui</h3>
        <p>
            Avant de discuter de ma situation spécifique, commençons par le contexte du marché. Selon les 
            données 2026 d'O*NET, du BLS et de l'analyse industrielle, les ingénieurs IA avec 2-3 ans 
            d'expérience à Montréal sont positionnés à un point d'inflexion critique. Le marché du talent 
            IA est compétitif, avec une demande croissante à 2x le taux des rôles de développement logiciel 
            en général.
        </p>
        
        <div class="highlight">
            <strong>Réalité du Marché :</strong> Les ingénieurs IA ayant une expertise éprouvée dans plusieurs 
            domaines—particulièrement GenAI, ML Ops et conception de systèmes—commandent une prime de 15-25% 
            par rapport aux ingénieurs logiciel généraux.
        </div>
        
        <h3>Contexte Géographique et d'Expérience</h3>
        <p>
            Pour Montréal, la gamme de salaire de base pour 2-3 ans d'expérience est :
        </p>
        <ul>
            <li><strong>Conservateur (25e percentile) :</strong> 85 000 $</li>
            <li><strong>Médiane du marché (50e percentile) :</strong> 95 000 $</li>
            <li><strong>Haute performance (75e percentile) :</strong> 110 000 $</li>
            <li><strong>Avec actions et bonus :</strong> 115 000 $–125 000 $ rémunération totale</li>
        </ul>
        <p>
            Ces données proviennent d'outils d'analyse de marché standardisés et s'alignent avec les marchés 
            de Toronto (+5-10%) et Vancouver (+3-7%).
        </p>
    </div>

    <div class="section">
        <h2>Partie 2 : Ma Valeur Démontrée</h2>
        
        <h3>Breadth and Depth Techniques</h3>
        <p>
            J'ai développé une expertise dans 24 compétences techniques, avec maîtrise dans 8 domaines 
            critiques de l'IA :
        </p>
        <ul>
            <li><strong>GenAI & LLMs :</strong> LangChain, RAG, GraphRAG, Agentic AI, Prompt Engineering</li>
            <li><strong>Deep Learning :</strong> PyTorch, TensorFlow, Computer Vision, architectures NLP</li>
            <li><strong>ML Ops & Systèmes :</strong> Déploiement de modèles, monitoring, bases de données vectorielles, orchestration</li>
            <li><strong>Cloud & Infrastructure :</strong> Services AWS, containerisation, pipelines CI/CD</li>
            <li><strong>Intégration Full-Stack :</strong> FastAPI, Django, Gradio, Streamlit, conception d'API</li>
        </ul>
        
        <p>
            Cette ampleur me positionne au 90e percentile pour mon niveau d'expérience—significativement 
            au-dessus de la moyenne du marché. La plupart des ingénieurs à ce stade se spécialisent dans 
            2-3 domaines ; j'ai construit une compétence dans 5 domaines distincts.
        </p>
        
        <h3>Livraison de Projets Prouvée</h3>
        <p>
            Mon impact est quantifiable :
        </p>
        <ul>
            <li><strong>1 Projet Client :</strong> Solution IA en production livrée pour Synchrony (travail externe générant des revenus)</li>
            <li><strong>2 Initiatives FinLabs :</strong> Projets expérimentaux à fort impact avançant la propriété intellectuelle de l'entreprise</li>
            <li><strong>5 Outils Internes :</strong> Construit et déployé des systèmes end-to-end qui améliorent l'efficacité opérationnelle</li>
            <li><strong>100% Taux de Déploiement :</strong> Chaque projet que j'ai dirigé a été mis en production</li>
        </ul>
        
        <p>
            Ce n'est pas une connaissance théorique—c'est une expérience pratique de livraison. J'ai dirigé 
            l'architecture, la conception, l'implémentation et le monitoring end-to-end. C'est rare au niveau 
            intermédiaire.
        </p>
        
        <h3>Croissance des Soft Skills et Leadership</h3>
        <p>
            Au-delà des compétences techniques, ma croissance professionnelle a été exceptionnelle :
        </p>
        <ul>
            <li><strong>Communication :</strong> +80% de croissance (des présentations techniques à l'alignement des stakeholders)</li>
            <li><strong>Leadership :</strong> +100% de croissance (mentorat des pairs, direction des projets)</li>
            <li><strong>Résolution de Problèmes :</strong> +53% de croissance (de l'implémentation à la pensée architecturale)</li>
            <li><strong>Adaptabilité :</strong> +75% de croissance (travail à travers FinLabs, interne et contextes client)</li>
        </ul>
        
        <p>
            Ce ne sont pas des soft skills au sens où ils seraient optionnels—ils sont essentiels pour 
            livrer de la valeur dans un paysage IA en évolution rapide. La capacité à communiquer des 
            concepts techniques complexes aux stakeholders non-techniques, à prendre des décisions quand 
            les exigences sont ambiguës, et à mentorer d'autres ingénieurs—ce sont des qualités de 
            leadership qui justifient un salaire de voie leadership.
        </p>
    </div>

    <div class="section">
        <h2>Partie 3 : Alignement de la Rémunération</h2>
        
        <h3>La Demande</h3>
        <p>
            En me basant sur les données de marché et mon impact démontré, je propose la rémunération suivante :
        </p>
        
        <div class="stat-box">
            <div>
                <div class="stat-label">Objectif de Salaire de Base</div>
                <div class="stat-value">105 000 $</div>
            </div>
        </div>
        
        <p>
            C'est au-dessus de la médiane (95 K$) mais en dessous du 75e percentile (110 K$), reflétant :
        </p>
        <ul>
            <li>Ma breadth technique au-dessus du marché (couverture des compétences au 90e percentile)</li>
            <li>Un track record de livraison éprouvé (8 projets, 100% livrés)</li>
            <li>Une trajectoire de croissance et un leadership démontré</li>
            <li>Un juste milieu raisonnable qui reconnaît où je me situe sur le marché compétitif</li>
        </ul>
        
        <h3>Package de Rémunération Totale</h3>
        <p>
            De plus, pour un package de rémunération totale compétitif, j'aimerais discuter de :
        </p>
        <ul>
            <li><strong>Bonus de Performance :</strong> 10-15% (standard pour mon niveau et mon impact)</li>
            <li><strong>Actions/Options d'Achat :</strong> Alignées avec la croissance de l'entreprise et mon engagement à long terme</li>
            <li><strong>Développement Professionnel :</strong> Budget pour les programmes MBA ou certifications IA avancées</li>
            <li><strong>Arrangement Flexible :</strong> Configuration favorable au télétravail pour maximiser la productivité</li>
        </ul>
        
        <p>
            Cela porte la rémunération totale à environ 120 000 $–130 000 $ par an—juste, compétitif et 
            aligné avec ma valeur marchande.
        </p>
    </div>

    <div class="section">
        <h2>Partie 4 : Pourquoi C'est Important pour [Entreprise]</h2>
        
        <h3>Risque de Rétention</h3>
        <p>
            La dynamique du marché du talent est claire : les ingénieurs IA avec mon profil sont très 
            demandés. Des entreprises comme Google, Microsoft, Shopify et des firmes locales recrutent 
            activement des ingénieurs avec cet ensemble de compétences et ce track record. Si ma rémunération 
            se situe en dessous du marché, le risque est que je sois activement recruté ailleurs—et le coût 
            de me remplacer dépasse celui de toute négociation salariale.
        </p>
        
        <p>
            Le coût pour embaucher et former un ingénieur de remplacement à mon niveau est 6-9 mois de 
            charge complète plus l'impact opérationnel de perdre la connaissance du domaine. C'est 
            économiquement rationnel pour [Entreprise] d'investir dans une rémunération compétitive 
            maintenant.
        </p>
        
        <h3>Mise à l'Échelle & Impact</h3>
        <p>
            Je propose également de prendre des responsabilités élargies :
        </p>
        <ul>
            <li>Diriger l'architecture IA pour [projet clé]</li>
            <li>Mentorer 2-3 ingénieurs juniors dans l'équipe</li>
            <li>Contribuer à l'embauche et aux entrevues techniques pour les rôles IA</li>
            <li>Posséder la feuille de route technique pour les initiatives GenAI/ML</li>
        </ul>
        
        <p>
            Ces responsabilités multiplient mon impact et réduisent le risque technique de l'entreprise 
            en distribuant la connaissance et en construisant la capacité de l'équipe.
        </p>
    </div>

    <div class="section">
        <h2>Partie 5 : Vision à Long Terme et Engagement</h2>
        
        <h3>Mon Chemin en Avant</h3>
        <p>
            Je ne demande pas une augmentation et je m'en vais. Je demande une rémunération juste en 
            échange d'un partenariat à long terme et d'un impact étendu. Mes objectifs pour les 24 
            prochains mois sont :
        </p>
        <ul>
            <li><strong>2026 :</strong> Postuler pour des programmes MBA tout en restant pleinement engagé envers [Entreprise]—un MBA approfondira ma compréhension commerciale et me rendra plus précieux pour l'organisation</li>
            <li><strong>2027 :</strong> Explorer les opportunités internationales au sein du réseau de [Entreprise] pour élargir l'impact et l'exposition au marché</li>
            <li><strong>Long Terme :</strong> Transitionner vers un rôle de leadership gérant les équipes IA/ML et les initiatives stratégiques</li>
        </ul>
        
        <p>
            [Entreprise] bénéficie de chacun de ces jalons car je croîs et je ramène cette croissance à 
            l'organisation.
        </p>
        
        <h3>Alignement des Valeurs</h3>
        <p>
            Je veux travailler pour une entreprise qui investit dans ses gens et reconnaît la valeur 
            équitablement. Une rémunération juste est la fondation de cette confiance. Quand je me sens 
            apprécié et récompensé proportionnellement à ma contribution, je suis motivé à prendre plus 
            de responsabilités, à livrer un meilleur travail et à rester à long terme.
        </p>
    </div>

    <div class="section">
        <h2>Conclusion : La Demande</h2>
        
        <p>
            Pour résumer, je demande :
        </p>
        <ul>
            <li><strong>Salaire de Base :</strong> 105 000 $ (au-dessus de la médiane, en dessous du 75e percentile)</li>
            <li><strong>Bonus de Performance :</strong> 10-15%</li>
            <li><strong>Périmètre Étendu :</strong> Leadership en architecture IA, mentorat et feuille de route stratégique</li>
            <li><strong>Développement Professionnel :</strong> Soutien pour MBA ou certifications avancées</li>
        </ul>
        
        <p style="margin-top: 30px;">
            Je crois que c'est juste en me basant sur les données de marché, mon impact démontré et la 
            valeur que je continuerai à créer. Je suis enthousiaste de discuter de la façon dont cela 
            s'aligne avec la philosophie de rémunération de [Entreprise] et ce que le succès ressemble 
            pour nous au cours des 12-24 prochains mois.
        </p>
        
        <p style="margin-top: 20px; font-style: italic;">
            J'ai apporté des données de marché objectives, des exemples de travail livré et une vision 
            claire de croissance. Je suis confiant que cette conversation sera productive pour nous deux.
        </p>
    </div>

    <div class="closing">
        <p><strong>Merci de considérer ma demande.</strong></p>
        <p style="margin-top: 20px; color: #999; font-size: 0.9em;">
            Préparé : Janvier 2026 | Basé sur O*NET, BLS et analyse de marché
        </p>
    </div>
</body>
</html>
"""

# Write HTML to temp file
with open('/tmp/negotiation_speech_fr.html', 'w', encoding='utf-8') as f:
    f.write(negotiation_speech_fr)

# Convert to PDF
print("Conversion du discours de négociation en PDF (Français)...")
HTML('/tmp/negotiation_speech_fr.html').write_pdf('negotiation.pdf')
print("✓ PDF negotiation.pdf créé avec succès en français")

# Clean up
os.remove('/tmp/negotiation_speech_fr.html')
