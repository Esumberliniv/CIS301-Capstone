# Source Code Directory

This directory contains the application source code for the Equity in Focus capstone project.

## Structure

```
src/
├── backend/          # FastAPI REST API application
│   ├── main.py      # API entry point
│   ├── models.py    # Database models
│   ├── routes.py    # API route handlers
│   ├── database.py  # Database connection
│   └── etl.py       # ETL pipeline
│
└── frontend/        # Streamlit dashboard
    ├── app.py       # Dashboard entry point
    ├── pages/       # Multi-page dashboard components
    ├── utils.py     # Helper functions
    └── config.py    # Configuration
```

## Technology Stack

### Backend (FastAPI)
- **Framework:** FastAPI
- **Database:** SQLite
- **Cloud Storage:** Google Cloud Storage
- **Testing:** pytest
- **Dependencies:** pandas, sqlalchemy, uvicorn

### Frontend (Streamlit)
- **Framework:** Streamlit
- **Visualization:** plotly, matplotlib, folium (for maps)
- **Data Processing:** pandas, numpy
- **API Client:** requests

## Development Workflow

### Phase 1: Backend Development
1. Design database schema for IGS data
2. Build ETL pipeline to load cleaned CSV into SQLite
3. Implement REST API endpoints
4. Write unit tests for API

### Phase 2: Frontend Development
1. Create Streamlit dashboard structure
2. Build visualization components
3. Integrate with backend API
4. Design user interface/UX

### Phase 3: Integration & Deployment
1. End-to-end testing
2. CI/CD pipeline setup (GitHub Actions)
3. Documentation
4. Deployment preparation

---

**Status:** Planning Phase Complete (Phase 1 starts next)  
**Last Updated:** November 19, 2025

