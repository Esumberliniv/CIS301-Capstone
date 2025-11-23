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

- [x] **Phase 1: Planning** (Week 1) - Repository setup, proposal, architecture design
- [ ] **Phase 2: Development** (Weeks 2-3) - Backend API, database, ETL pipelines
- [ ] **Phase 3: Frontend** (Week 4) - Streamlit dashboard, visualizations
- [ ] **Phase 4: Integration & Testing** (Week 5) - End-to-end testing, deployment
- [ ] **Phase 5: Finalization** (Week 6) - Documentation, presentation, submission

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

## 🛠️ Setup Instructions (Development)

### Prerequisites
```bash
Python 3.9+
pip (Python package manager)
Git
```

### Installation (Coming Soon)
```bash
# Clone repository
git clone https://github.com/yourusername/CIS301-Capstone.git
cd CIS301-Capstone

# Install dependencies
pip install -r requirements.txt

# Run ETL pipeline
python src/backend/etl.py

# Start FastAPI backend
uvicorn src.backend.main:app --reload

# Start Streamlit dashboard (new terminal)
streamlit run src/frontend/app.py
```

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

**Last Updated:** November 19, 2025

