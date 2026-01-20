# AI Salary Dashboard

A comprehensive salary negotiation and market analysis handout for AI Engineers in Canada. This dashboard provides data-driven insights into salary ranges, career progression, market demand, and skill evolution.

**Created by:** Nouhayla Benhammou  
**Date:** January 2026

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Data Sources](#data-sources)
3. [Dashboard Tabs](#dashboard-tabs)
4. [Chart-by-Chart Breakdown](#chart-by-chart-breakdown)
5. [Running the Dashboard](#running-the-dashboard)

---

## Project Overview

This dashboard is designed as a **salary negotiation reference handout** for AI Engineers. It provides:
- Market benchmark data for AI engineer salaries
- Career progression pathways
- Key performance indicators (KPIs)
- Visualization of salary distributions, demand trends, and investment opportunities

The dashboard consists of three main tabs:
1. **Benchmark AI Market** — Market overview and salary analytics
2. **Contribution Dashboard** — Personal project contributions and skill evolution
3. **Negotiation Summary** — Negotiation reference guide (placeholder)

---

## Data Sources

### Role Evolution & Career Progression Data

**Sources:** O*NET, BLS, Wikipedia (Retrieved: January 11, 2026)

- **O*NET (Occupational Information Network)**  
  URL: https://www.onetonline.org/link/summary/15-1252.00  
  Description: US Department of Labor's comprehensive occupational database. Provides standard job titles, responsibilities, and typical career progression for software developers and related roles.

- **BLS (Bureau of Labor Statistics) - Occupational Outlook Handbook**  
  URL: https://www.bls.gov/ooh/computer-and-information-technology/software-developers.htm  
  Description: US government labor statistics providing employment trends, job growth projections, and typical career paths for software developers.

- **Wikipedia - Software Engineering**  
  URL: https://en.wikipedia.org/wiki/Software_engineering  
  Description: General software engineering discipline reference including SWEBOK (Software Engineering Body of Knowledge) notes on staff engineer roles.

### Salary Data

**Basis:** Research-based estimates for Montreal/Canada AI Engineer roles  
**Data Type:** Sample/Representative data for market analysis  
**Geography:** Montreal, Toronto, Vancouver, Remote  
**Experience Levels:** Intern to Executive (0–30 years)

**Files:**
- `data/ai_geo.csv` — Salary by geography (Min/Avg/Max)
- `data/exp_23.csv` — Detailed salary table for 2–3 years experience
- `data/industry.csv` — Salary by industry sector
- `data/exp_position_sector.csv` — Salary by experience, position, and sector

### Skill Evolution Data

**File:** `data/technical_skills_evolution.csv`  
**Description:** Proficiency progression (0–9 scale) across 8 key AI/ML skills over time  
**Skills Tracked:**
- Python
- Machine Learning
- Deep Learning
- MLOps
- Data Engineering
- Cloud AWS
- Natural Language Processing (NLP)
- Computer Vision

### Market Trend Data

**File:** `data/timeline.csv`  
**Description:** AI job market trends and salary projections (2020–2030)

---

## Dashboard Tabs

### Tab 1: Benchmark AI Market

Market overview with 15+ visualizations showing salary ranges, demand, and career progression.

### Tab 2: Contribution Dashboard

Personal profile evolution featuring:
- Project contribution breakdown
- Technical skills evolution timeline
- Skills by stream (client/internal/FinLabs)

### Tab 3: Negotiation Summary

(Placeholder for future content)

---

## Chart-by-Chart Breakdown

### **KPI Strip** (Top of Tab 1)
**Type:** KPI Indicators  
**Data Source:** Aggregated salary data  
**Purpose:** Quick snapshot of key salary metrics (CAD) including median, percentiles, and salary ranges for Montreal AI Engineers  
**Use Case:** Dashboard header reference for quick lookups

---

### **Industry Share**
**Type:** Pie Chart  
**Data Source:** `data/industry.csv`  
**Purpose:** Shows the composition of AI Engineer roles by industry sector in the dataset  
**Insight:** Identifies which industries dominate the AI job market  
**Use Case:** Understand industry distribution when comparing salary benchmarks

---

### **AI Investment by Industry**
**Type:** Bar Chart  
**Data Source:** `data/timeline.csv` / Research data  
**Purpose:** Displays AI investment levels (Billion USD) by industry sector  
**Insight:** Shows where AI funding and opportunities are concentrated globally  
**Use Case:** Identify growth sectors and potential career opportunities

---

### **Career Progression by Years** ⭐
**Type:** Horizontal Timeline Bar Chart  
**Data Source:** `data/role_evolution_sourced.csv` (O*NET, BLS, Wikipedia)  
**Purpose:** Maps 6 career levels to years of experience:
  - **Intern:** 0–0.5 years
  - **Entry/Junior:** 0.5–3 years
  - **Mid:** 3–5 years
  - **Senior:** 5–8 years
  - **Principal/Lead:** 8–12 years
  - **Executive:** 12–30 years

**Titles Included:**
- Intern; Research Intern; Co-op
- Junior Software Engineer; Associate ML Engineer; ML Engineer I
- Software Engineer; ML Engineer; Applied ML Engineer
- Senior Software Engineer; Senior ML Engineer; Staff Engineer
- Principal Engineer; Lead ML Engineer; Engineering Manager
- Director of Engineering; VP of Engineering; Head of ML

**Insight:** Typical corporate ladder for AI professionals  
**Use Case:** Determine appropriate role title based on experience level

---

### **Avg Salary by Geography**
**Type:** Interactive Map/Choropleth  
**Data Source:** `data/ai_geo.csv`  
**Locations:** Montreal, Toronto, Vancouver, Remote  
**Purpose:** Compare average AI Engineer salaries across Canadian geographies  
**Insight:** Geographic salary premium/discount (Toronto/Vancouver higher, Remote lower)  
**Use Case:** Negotiate salary based on location; understand cost-of-living adjustments

---

### **Min/Avg/Max Salary Distribution**
**Type:** Grouped Bar Chart  
**Data Source:** `data/ai_geo.csv`  
**Purpose:** Shows salary range (minimum, average, maximum) for each geography  
**Insight:** Visualizes salary spread and variability by location  
**Use Case:** Understand realistic salary floors and ceilings for each region

---

### **Experience Progression**
**Type:** Line/Area Chart  
**Data Source:** `data/exp_position_sector.csv`  
**Purpose:** Salary progression trajectory by years of experience and location  
**Insight:** Expected salary growth curve for AI engineers  
**Use Case:** Forecast your career earnings and identify underperformance

---

### **Salary vs Experience**
**Type:** Scatter Plot with Trendline  
**Data Source:** `data/exp_position_sector.csv`  
**Purpose:** Individual salary points plotted against experience, with regression line  
**Insight:** Shows where you sit relative to peers  
**Use Case:** Identify outliers (over/under-compensated) and benchmark your salary

---

### **Salary Percentiles**
**Type:** Box Plot / Percentile Chart  
**Data Source:** Aggregated salary data  
**Percentiles:** 10th, 25th (Q1), 50th (Median), 75th (Q3), 90th  
**Purpose:** Understand your salary position within the distribution  
**Insight:** Where does your salary rank among peers?  
**Use Case:** Salary negotiation anchor — aim for 75th percentile or higher

---

### **Total Compensation (2–3 yrs)**
**Type:** Violin Plot  
**Data Source:** `data/exp_23.csv`  
**Purpose:** Shows distribution of total compensation (salary + bonuses + equity) for 2–3 year experience level  
**Insight:** Account for non-salary components in total package  
**Use Case:** Negotiate equity and bonus structure, not just base salary

---

### **Salary Details (2–3 yrs)**
**Type:** Data Table  
**Data Source:** `data/exp_23.csv`  
**Purpose:** Detailed breakdown of salary components for early-career AI engineers  
**Columns:** Base Salary, Bonus, Equity, Total Compensation, Percentile  
**Use Case:** Detailed reference for 2–3 year salary negotiations

---

### **AI Demand Timeline**
**Type:** Line Chart (2020–2030)  
**Data Source:** `data/timeline.csv`  
**Purpose:** AI job posting growth index from 2020 to 2030  
**Insight:** Market demand trajectory and future opportunities  
**Use Case:** Understand long-term market trends; validate career choice

---

### **AI Salary Projection**
**Type:** Line Chart (2020–2030)  
**Data Source:** `data/timeline.csv`  
**Purpose:** Forecasted average AI engineer salary growth (CAD) over 10 years  
**Insight:** Expected salary appreciation year-over-year  
**Use Case:** Plan long-term career compensation and negotiate future increases

---

### **Role Evolution — Titles by Years**
**Type:** Horizontal Bar Chart  
**Data Source:** `data/role_evolution_sourced.csv`  
**Purpose:** Same as "Career Progression by Years" but focused on job titles  
**Titles:** Lists typical corporate titles for each role level  
**Hover Data:** Shows exact year range for each position  
**Use Case:** Understand title progression; ensure you're tracking career level appropriately

---

### **Technical Skills Evolution** (Tab 2)
**Type:** Multi-line Plotly Chart  
**Data Source:** `data/technical_skills_evolution.csv`  
**Skills Tracked (8):**
1. Python
2. Machine Learning
3. Deep Learning
4. MLOps
5. Data Engineering
6. Cloud AWS
7. Natural Language Processing
8. Computer Vision

**Proficiency Scale:** 0–9 (Novice to Expert)  
**Time Period:** June 2019 – January 2025  
**Purpose:** Visualize skill progression over time  
**Insight:** Identify fastest-growing and most important skills  
**Use Case:** Skill development planning; identify gaps in profile

---

### **Project Contributions** (Tab 2)
**Type:** Histogram (Chart.js Canvas)  
**Data Source:** Hardcoded contribution counts  
**Purpose:** Breakdown of project contributions by stream:
  - **Client Projects:** External client work
  - **FinLabs:** Internal financial/experimental labs
  - **Internal Builds:** Internal company projects

**Total:** 8 projects (1 client, 2 FinLabs, 5 internal)  
**Use Case:** Personal portfolio summary; demonstrate breadth of experience

---

### **Skills by Stream** (Tab 2)
**Type:** Histogram with Skill Pills  
**Data Source:** Custom skill list by stream  
**Purpose:** Categorize and display skills by project type  
**Use Case:** Showcase specialized skills for different contexts

---

## Running the Dashboard

### Prerequisites
- Python 3.8+
- Required packages: pandas, plotly, matplotlib, seaborn, nbconvert

### Installation

```bash
cd /home/nouhayla/AI_Salary_Dashboard
pip install pandas plotly matplotlib seaborn nbconvert
```

### Start the Server

```bash
python3 -m http.server 8000
```

Then open your browser to: **http://localhost:8000/salary_handout_tabs.html**

### Generate/Regenerate Charts

```bash
# Generate role evolution chart
python3 scripts/generate_role_evolution.py

# Generate position progression chart
python3 scripts/generate_position_progression.py

# Generate technical skills evolution
python3 scripts/generate_tech_skills.py

# Run full Jupyter notebook (all charts)
jupyter notebook dashboard.ipynb
```

---

## File Structure

```
AI_Salary_Dashboard/
├── README.md                           (This file)
├── salary_handout_tabs.html            (Main dashboard HTML)
├── dashboard.ipynb                     (Jupyter notebook with analysis)
├── data/
│   ├── role_evolution_sourced.csv      (Role titles by years - sourced)
│   ├── ai_geo.csv                      (Salary by geography)
│   ├── exp_23.csv                      (2-3 years salary details)
│   ├── industry.csv                    (Salary by industry)
│   ├── exp_position_sector.csv         (Experience vs position vs sector)
│   ├── technical_skills_evolution.csv  (Skill proficiency over time)
│   ├── timeline.csv                    (Market trends 2020-2030)
│   └── role_evolution_ai_roles.csv     (Legacy mock data)
├── scripts/
│   ├── generate_role_evolution.py      (Role titles chart)
│   ├── generate_position_progression.py (Career progression chart)
│   ├── generate_tech_skills.py         (Technical skills evolution)
│   └── generate_visuals.py             (Other chart generators)
└── handout/
    ├── kpis.html                       (KPI strip)
    ├── geo.html                        (Geography salary map)
    ├── industry_share.html             (Industry pie chart)
    ├── vis3_salary_distribution.html   (Min/Avg/Max bars)
    ├── exp_progression.html            (Experience progression line)
    ├── salary_vs_exp.html              (Salary vs experience scatter)
    ├── percentiles.html                (Salary percentiles)
    ├── total_comp.html                 (Total compensation violin)
    ├── vis5_2_3_years_table.html       (2-3 years detailed table)
    ├── vis6_ai_demand_timeline.html    (Job posting growth)
    ├── vis7_salary_projection.html     (Salary forecast)
    ├── vis8_investment_by_industry.html (AI investment by industry)
    ├── role_evolution.html             (Role titles by years)
    ├── position_progression.html       (Career progression timeline)
    └── technical_skills_evolution.html (Technical skills line chart)
```

---

## Data Attribution & Disclaimer

**Real Data Sources:**
- Role evolution titles and career levels sourced from O*NET, BLS, and Wikipedia
- Career progression milestones based on industry standards

**Sample Data:**
- Salary figures are representative estimates for Montreal/Canada AI Engineer roles
- Used for demonstration and analysis purposes
- Should be validated with current market data (Levels.fyi, Blind, Glassdoor) before actual negotiations

---

## Author & Contact

**Created by:** Nouhayla Benhammou  
**Purpose:** Salary negotiation reference handout for AI Engineers  
**Last Updated:** January 12, 2026

---

## License

This dashboard and its source code are provided for educational and personal use.

