# Equity in Focus: Visualizing Economic Inclusion with Mastercard IGS

**CIS 301 Capstone Project**  
**Clark Atlanta CIS301**

## 📊 Project Overview

This capstone project develops a full-stack data application to analyze and visualize economic inclusion across U.S. communities using the **Mastercard Inclusive Growth Score (IGS)** dataset. The tool empowers policymakers, non-profits, and community leaders to identify economic opportunity gaps and support data-driven DEI (Diversity, Equity, and Inclusion) initiatives.

Unlike traditional GDP metrics, the IGS provides normalized scores (1-100) that reveal disparities within communities—highlighting "investment deserts" and opportunities for targeted interventions.

## 👤 Solo Developer

**Developer:** Emery  
**Responsibilities:** Full-stack development including:
- **Backend:** FastAPI REST API, SQLite database design, data ETL pipelines
- **Frontend:** Streamlit dashboard with interactive visualizations
- **DevOps:** Google Cloud Storage integration, CI/CD with GitHub Actions
- **Data Engineering:** Data cleaning, processing, and management

## 🎯 Project Goals

1. **Analyze Equity Across Communities:** Correlate key indicators (Minority/Women-Owned Businesses, Internet Access, Affordable Housing) to identify exclusion patterns
2. **Visualize Opportunity Gaps:** Create interactive choropleth maps and comparative analytics
3. **Drive Social Impact:** Provide actionable insights for policy interventions in underserved communities
4. **Deliver Production-Ready Application:** Build scalable, maintainable full-stack system

## 🔬 Research Questions

This project analyzes the Mastercard Inclusive Growth Score (IGS) data to answer:

1. **How do economic inclusion scores correlate with demographic and economic indicators?**
   - Is there a relationship between IGS scores and median household income?
   - Do communities with higher inclusion scores show better access to digital infrastructure?
   - How does affordable housing availability impact overall inclusion scores?

2. **What regional patterns exist in economic inclusion across the United States?**
   - How do IGS scores vary across different states and counties?
   - Are there geographic clusters of economically excluded communities?
   - What spatial patterns emerge when analyzing opportunity gaps?

3. **Which dimensions have the strongest impact on overall inclusion scores?**
   - What are the key drivers of high vs. low IGS performance?
   - How do different components (minority/women-owned businesses, internet access, housing, income) contribute to overall scores?
   - Which metrics show the strongest correlations with economic opportunity?

4. **How have economic inclusion scores evolved over time (2017-2024)?**
   - Are communities improving their inclusion metrics year-over-year?
   - What trends can be identified in economic opportunity gaps?
   - Which states or counties show the most significant progress?

5. **What factors predict successful economic inclusion implementation?**
   - Can we identify characteristics of high-performing census tracts?
   - What policy interventions might be most effective based on data patterns?
   - How can policymakers use this data to target "investment deserts"?

## 🗂️ Repository Structure

```
CIS301-Capstone/
├── README.md                    # This file
├── docs/
│   ├── proposal.md             # Comprehensive project proposal (500 words)
│   ├── peer-review-template.md # Template for reviewing other projects
│   └── data-dictionary.md      # Dataset documentation
├── diagrams/
│   ├── system-architecture.mmd # System components diagram
│   └── data-flow.mmd           # Data pipeline sequence diagram
├── data/
│   ├── raw/                    # Original IGS dataset
│   ├── processed/              # Cleaned, processed data
│   └── IGS-score.csv           # Mastercard Inclusive Growth Score data
├── src/
│   ├── backend/                # FastAPI application
│   └── frontend/               # Streamlit dashboard
└── .github/
    └── workflows/              # CI/CD pipelines (future)
```

## 📈 Key Features

### Data Analytics
- Temporal analysis (2017-2024) of economic inclusion trends
- Census tract-level granularity across U.S. states and counties
- Comparative scoring against state averages

### Interactive Dashboard
- **Equity Map:** Choropleth visualization of Inclusive Growth Scores by geography
- **Opportunity Gap Analysis:** Compare census tracts against state benchmarks
- **Correlation Explorer:** Analyze relationships between key metrics (e.g., Internet Access vs. Small Business Growth)

### Technical Stack
- **Backend:** FastAPI (Python)
- **Database:** SQLite (structured queries), Google Cloud Storage (data lake)
- **Frontend:** Streamlit (interactive Python-based dashboards)
- **DevOps:** GitHub Actions, pytest, linting tools

## 🚀 Milestones

- [x] **Phase 1: Planning** - Repository setup, proposal, architecture design
- [x] **Phase 2: Development** - Backend API, database, ETL pipelines
- [x] **Phase 3: Frontend** - Streamlit dashboard, visualizations
- [x] **Phase 4: Integration & Testing** - End-to-end testing, system validation
- [x] **Phase 5: Documentation** - Complete setup instructions and usage guide

## ✅ Implementation Status

All core features have been implemented:
- ✅ ETL Pipeline (data cleaning, database loading, validation)
- ✅ FastAPI Backend (6+ REST endpoints with full documentation)
- ✅ SQLite Database (104 records across 4 states, 2017-2024)
- ✅ Streamlit Dashboard (3 interactive visualization pages)
- ✅ Integration Testing (automated test suite)
- ✅ Comprehensive Documentation

## 📊 Dataset: Mastercard Inclusive Growth Score

**Source:** Mastercard Center for Inclusive Growth  
**Temporal Coverage:** 2017-2024  
**Geographic Scope:** U.S. Census Tracts

### Key Variables
| Metric | Description | Social Impact |
|--------|-------------|---------------|
| **Minority/Women-Owned Businesses Score** | Measures entrepreneurship in marginalized groups | Assesses economic equity |
| **Internet Access Score** | Proxy for digital inclusion | Critical for education, remote work |
| **Affordable Housing Score** | Housing cost burden indicator | Community stability baseline |
| **Personal Income Score** | Median income normalized to state | Economic opportunity measure |
| **Inclusive Growth Score** | Composite score (1-100) | Overall community health |

### Why This Dataset?
- **Equity-Focused:** Designed to measure inclusion, not just aggregate growth
- **Normalized Scores:** Enables "apples-to-apples" comparisons across diverse geographies
- **Actionable Insights:** Identifies specific intervention points for policymakers

## 🔗 Quick Links

- [Project Proposal](docs/proposal.md)
- [Architecture Diagrams](diagrams/)
- [Data Dictionary](docs/data-dictionary.md)
- [Peer Review Template](docs/peer-review-template.md)

## 🛠️ Setup Instructions

### Prerequisites
- Python 3.9 or higher
- pip (Python package manager)
- Git

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/CIS301-Capstone.git
cd CIS301-Capstone
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run ETL Pipeline** (one-time setup)
```bash
# Option 1: Run complete ETL pipeline (recommended)
python src/backend/etl/run_etl.py

# Option 2: Run steps individually
python src/backend/etl/data_cleaning.py
python src/backend/etl/load_database.py
```

This will:
- Clean the raw IGS CSV data
- Create SQLite database at `data/igs_data.db`
- Load 104 census tract records

### Running the Application

#### Start the Backend API

In your first terminal:
```bash
python run_backend.py
```

The API will be available at:
- **API Endpoints:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs
- **Alternative Docs:** http://localhost:8000/redoc

#### Start the Dashboard

In a second terminal:
```bash
python run_frontend.py
```

The dashboard will open automatically at:
- **Dashboard:** http://localhost:8501

### Testing the System

Run integration tests to verify everything is working:
```bash
python test_system.py
```

## 📊 Using the Dashboard

### Available Pages

1. **📍 Equity Map**
   - Interactive visualizations of IGS scores by geography
   - Filter by state, county, and year
   - View bar charts and distribution plots
   - Download data as CSV

2. **📊 Opportunity Gap Analysis**
   - Compare specific census tracts against state/county averages
   - Identify opportunity gaps in key metrics
   - Visual gap analysis with color-coded indicators
   - See strongest and weakest areas for targeted interventions

3. **🔗 Correlation Explorer**
   - Analyze relationships between different metrics
   - Scatter plots with trendlines
   - Correlation heatmaps
   - Quadrant analysis for pattern identification

### Available API Endpoints

- `GET /api/health` - Health check and system status
- `GET /api/tracts` - Get census tracts with filters
- `GET /api/tracts/{fips_code}` - Get specific tract by FIPS code
- `GET /api/states` - List all available states
- `GET /api/metrics` - Get specific metric values
- `GET /api/statistics` - Calculate statistical aggregations
- `GET /api/correlations` - Compute correlations between metrics

Full API documentation available at http://localhost:8000/docs

## 📝 Ethical Considerations

1. **Representation Bias:** Spending data may underrepresent cash-based economies in lower-income areas
2. **Privacy Protection:** Data aggregated to census tract level to protect individual identities
3. **Framing:** Visualizations focus on "opportunity potential" rather than "deficits" to avoid stigmatization

## 📄 License

This project is developed for educational purposes as part of Clark Atlanta's CIS 301 course.

## 🙏 Acknowledgments

- **Clark Atlanta CIS301** for curriculum design
- **Mastercard Center for Inclusive Growth** for dataset access
- Course instructors and peer reviewers

---

**Last Updated:** November 29, 2025  
**Status:** ✅ Fully Implemented

