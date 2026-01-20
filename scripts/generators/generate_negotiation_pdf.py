#!/usr/bin/env python3
"""Generate a professional negotiation speech PDF based on market data and contributions"""
import os

try:
    from weasyprint import HTML, CSS
except ImportError:
    print("Installing weasyprint...")
    os.system("pip install weasyprint -q")
    from weasyprint import HTML, CSS

# Professional negotiation speech based on market data and contributions
negotiation_speech = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Salary Negotiation Speech</title>
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
        <h1>AI Salary Negotiation Speech</h1>
        <p>Data-Driven Approach to Career Advancement & Compensation</p>
    </div>

    <div class="section">
        <h2>Opening Statement</h2>
        <p>
            Thank you for this opportunity to discuss my compensation and role at [Company]. 
            I'm excited about the work we're doing in AI, and I want to ensure that my compensation 
            reflects both my contributions to the organization and my market value as an AI professional.
        </p>
        <p>
            I've prepared this conversation based on objective market data, my demonstrated impact, 
            and my commitment to driving value for [Company]. I'd like to walk through what I bring to 
            the table and discuss a compensation package that recognizes that value.
        </p>
    </div>

    <div class="section">
        <h2>Part 1: Market Context & Position</h2>
        
        <h3>The AI Market Today</h3>
        <p>
            Before we discuss my specific situation, let's start with market context. According to 2026 
            data from O*NET, BLS, and industry analysis, AI engineers with 2–3 years of experience in 
            Montreal are positioned at a critical inflection point. The market for AI talent is competitive, 
            with demand growing at 2x the rate of software development roles generally.
        </p>
        
        <div class="highlight">
            <strong>Market Reality:</strong> AI engineers with proven expertise across multiple domains—
            particularly GenAI, ML Ops, and system design—command a 15–25% premium over general software engineers.
        </div>
        
        <h3>Geographic & Experience Context</h3>
        <p>
            For Montreal, the baseline salary range for 2–3 years of experience is:
        </p>
        <ul>
            <li><strong>Conservative (25th percentile):</strong> $85,000</li>
            <li><strong>Market median (50th percentile):</strong> $95,000</li>
            <li><strong>High performance (75th percentile):</strong> $110,000</li>
            <li><strong>With equity & bonus:</strong> $115,000–$125,000 total compensation</li>
        </ul>
        <p>
            This data comes from standardized market analysis tools and aligns with Toronto (+5–10%) 
            and Vancouver (+3–7%) markets.
        </p>
    </div>

    <div class="section">
        <h2>Part 2: My Demonstrated Value</h2>
        
        <h3>Technical Breadth & Depth</h3>
        <p>
            I've developed expertise across 24 technical skills, with mastery in 8 critical AI domains:
        </p>
        <ul>
            <li><strong>GenAI & LLMs:</strong> LangChain, RAG, GraphRAG, Agentic AI, Prompt Engineering</li>
            <li><strong>Deep Learning:</strong> PyTorch, TensorFlow, Computer Vision, NLP architectures</li>
            <li><strong>ML Ops & Systems:</strong> Model deployment, monitoring, vector databases, orchestration</li>
            <li><strong>Cloud & Infrastructure:</strong> AWS services, containerization, CI/CD pipelines</li>
            <li><strong>Full-Stack Integration:</strong> FastAPI, Django, Gradio, Streamlit, API design</li>
        </ul>
        
        <p>
            This breadth positions me at the 90th percentile for my experience level—significantly 
            above market average. Most engineers at this stage specialize in 2–3 areas; I've built 
            competence across 5 distinct domains.
        </p>
        
        <h3>Proven Project Delivery</h3>
        <p>
            My impact is quantifiable:
        </p>
        <ul>
            <li><strong>1 Client Project:</strong> Delivered production AI solution for Synchrony (external revenue-generating work)</li>
            <li><strong>2 FinLabs Initiatives:</strong> High-impact experimental projects advancing company IP</li>
            <li><strong>5 Internal Tools:</strong> Built and deployed end-to-end systems that drive operational efficiency</li>
            <li><strong>100% Deployment Rate:</strong> Every project I've owned has shipped to production</li>
        </ul>
        
        <p>
            This isn't theoretical knowledge—this is hands-on shipping experience. I've owned architecture, 
            design, implementation, and monitoring end-to-end. That's rare at the mid-level.
        </p>
        
        <h3>Soft Skills & Leadership Growth</h3>
        <p>
            Beyond technical skills, my professional growth has been exceptional:
        </p>
        <ul>
            <li><strong>Communication:</strong> +80% growth (from technical presentations to stakeholder alignment)</li>
            <li><strong>Leadership:</strong> +100% growth (mentoring peers, driving project direction)</li>
            <li><strong>Problem-Solving:</strong> +53% growth (from implementation to architectural thinking)</li>
            <li><strong>Adaptability:</strong> +75% growth (working across FinLabs, internal, and client contexts)</li>
        </ul>
        
        <p>
            These aren't soft skills in the sense of being optional—they're core to delivering value 
            in a rapidly evolving AI landscape. The ability to communicate complex technical concepts 
            to non-technical stakeholders, drive decisions when requirements are ambiguous, and mentor 
            other engineers—these are leadership qualities that justify a leadership-track salary.
        </p>
    </div>

    <div class="section">
        <h2>Part 3: Compensation Alignment</h2>
        
        <h3>The Ask</h3>
        <p>
            Based on market data and my demonstrated impact, I'm proposing the following compensation:
        </p>
        
        <div class="stat-box">
            <div>
                <div class="stat-label">Base Salary Target</div>
                <div class="stat-value">$105,000</div>
            </div>
        </div>
        
        <p>
            This is above the median ($95K) but below the 75th percentile ($110K), reflecting:
        </p>
        <ul>
            <li>My above-market technical breadth (90th percentile skill coverage)</li>
            <li>Proven delivery track record (8 projects, 100% shipped)</li>
            <li>Growth trajectory and demonstrated leadership</li>
            <li>A reasonable middle ground that acknowledges where I sit in the competitive market</li>
        </ul>
        
        <h3>Total Compensation Package</h3>
        <p>
            Additionally, for a competitive total compensation package, I'd like to discuss:
        </p>
        <ul>
            <li><strong>Performance Bonus:</strong> 10–15% (standard for my level and impact)</li>
            <li><strong>Equity/Stock Options:</strong> Aligned with company growth and my long-term commitment</li>
            <li><strong>Professional Development:</strong> Budget for MBA programs or advanced AI certifications</li>
            <li><strong>Flexible Arrangement:</strong> Remote-friendly setup to maximize productivity</li>
        </ul>
        
        <p>
            This brings total compensation to approximately $120,000–$130,000 annually—fair, competitive, 
            and aligned with my market value.
        </p>
    </div>

    <div class="section">
        <h2>Part 4: Why This Matters for [Company]</h2>
        
        <h3>Retention Risk</h3>
        <p>
            Talent market dynamics are clear: AI engineers with my profile are in high demand. 
            Companies like Google, Microsoft, Shopify, and local firms are actively recruiting 
            engineers with this skill set and track record. If my compensation falls below market, 
            the risk is that I'll be actively recruited away—and the cost of replacing me exceeds 
            any salary negotiation.
        </p>
        
        <p>
            The cost to hire and train a replacement engineer at my level is 6–9 months of full cost burden 
            plus the operational impact of losing domain knowledge. It's economically rational for [Company] 
            to invest in competitive compensation now.
        </p>
        
        <h3>Scaling & Impact</h3>
        <p>
            I'm also proposing to take on expanded responsibilities:
        </p>
        <ul>
            <li>Lead AI architecture for [key project]</li>
            <li>Mentor 2–3 junior engineers on the team</li>
            <li>Contribute to hiring and technical interviewing for AI roles</li>
            <li>Own the technical roadmap for GenAI/ML initiatives</li>
        </ul>
        
        <p>
            These responsibilities multiply my impact and reduce the company's technical risk 
            by distributing knowledge and building team capability.
        </p>
    </div>

    <div class="section">
        <h2>Part 5: Long-Term Vision & Commitment</h2>
        
        <h3>My Path Forward</h3>
        <p>
            I'm not asking for a raise and moving on. I'm asking for fair compensation in exchange 
            for a long-term partnership and expanded impact. My goals over the next 24 months are:
        </p>
        <ul>
            <li><strong>2026:</strong> Apply to MBA programs while staying fully committed to [Company]—an MBA will deepen my business acumen and make me more valuable to the organization</li>
            <li><strong>2027:</strong> Explore international opportunities within [Company]'s network to broaden impact and market exposure</li>
            <li><strong>Long-term:</strong> Transition into a leadership role managing AI/ML teams and strategic initiatives</li>
        </ul>
        
        <p>
            [Company] benefits from each of these milestones because I'm growing and bringing that growth back to the organization.
        </p>
        
        <h3>Values Alignment</h3>
        <p>
            I want to work at a company that invests in its people and recognizes value fairly. 
            Fair compensation is the foundation of that trust. When I feel valued and rewarded proportionally 
            to my contribution, I'm motivated to take on more, ship better work, and stay long-term.
        </p>
    </div>

    <div class="section">
        <h2>Closing: The Ask</h2>
        
        <p>
            To summarize, I'm requesting:
        </p>
        <ul>
            <li><strong>Base Salary:</strong> $105,000 (above median, below 75th percentile)</li>
            <li><strong>Performance Bonus:</strong> 10–15%</li>
            <li><strong>Expanded Scope:</strong> Leadership in AI architecture, mentoring, and strategic roadmapping</li>
            <li><strong>Professional Development:</strong> Support for MBA or advanced certifications</li>
        </ul>
        
        <p style="margin-top: 30px;">
            I believe this is fair based on market data, my demonstrated impact, and the value I'll 
            continue to create. I'm excited to discuss how this aligns with [Company]'s compensation 
            philosophy and what success looks like for us over the next 12–24 months.
        </p>
        
        <p style="margin-top: 20px; font-style: italic;">
            I've brought objective market data, examples of shipped work, and a clear vision for growth. 
            I'm confident this conversation will be productive for both of us.
        </p>
    </div>

    <div class="closing">
        <p><strong>Thank you for considering my request.</strong></p>
        <p style="margin-top: 20px; color: #999; font-size: 0.9em;">
            Prepared: January 2026 | Based on O*NET, BLS, and market analysis
        </p>
    </div>
</body>
</html>
"""

# Write HTML to temp file
with open('/tmp/negotiation_speech.html', 'w') as f:
    f.write(negotiation_speech)

# Convert to PDF
print("Converting negotiation speech to PDF...")
HTML('/tmp/negotiation_speech.html').write_pdf('negotiation.pdf')
print("✓ Successfully created negotiation.pdf")

# Clean up
os.remove('/tmp/negotiation_speech.html')
