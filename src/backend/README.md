# Backend - FastAPI REST API

This directory will contain the FastAPI backend for serving IGS data to the dashboard.

## Planned Architecture

```
backend/
├── main.py              # FastAPI application entry point
├── models.py            # SQLAlchemy database models
├── routes.py            # API route handlers
├── database.py          # Database connection and session management
├── etl.py               # ETL pipeline (CSV → SQLite)
├── schemas.py           # Pydantic schemas for request/response validation
├── config.py            # Configuration (database URL, GCS credentials)
├── requirements.txt     # Python dependencies
└── tests/
    ├── test_api.py      # API endpoint tests
    └── test_etl.py      # ETL pipeline tests
```

## Planned API Endpoints

### Core Data Endpoints

```
GET /api/health
- Description: Health check endpoint
- Response: {"status": "healthy"}

GET /api/tracts
- Description: Get all census tracts with optional filters
- Query Params:
  - state: Filter by state (e.g., "Georgia")
  - county: Filter by county
  - year: Filter by year (2017-2024)
  - min_score: Minimum Inclusive Growth Score
- Response: List of census tract records

GET /api/tracts/{fips_code}
- Description: Get specific census tract by FIPS code
- Path Param: fips_code (11-digit FIPS code)
- Response: Single tract record with all metrics

GET /api/metrics
- Description: Get specific metric across tracts
- Query Params:
  - metric: Metric name (e.g., "internet_access_score")
  - state: Optional state filter
  - year: Optional year filter
- Response: List of {fips_code, metric_value}

GET /api/states
- Description: List all states in dataset
- Response: List of state names

GET /api/counties
- Description: List counties by state
- Query Param: state (required)
- Response: List of county names
```

### Analysis Endpoints

```
GET /api/correlations
- Description: Calculate correlation between two metrics
- Query Params:
  - metric1: First metric name
  - metric2: Second metric name
  - state: Optional state filter
- Response: Correlation coefficient and scatter plot data

GET /api/trends/{fips_code}
- Description: Get time-series trends for a census tract
- Path Param: fips_code
- Response: Year-over-year data for all metrics

GET /api/compare
- Description: Compare tract against state average
- Query Params:
  - fips_code: Census tract FIPS code
  - metrics: Comma-separated metric names
- Response: {metric: {tract_value, state_value, difference}}
```

## Database Schema (Planned)

### Table: `census_tracts`

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER PRIMARY KEY | Auto-increment ID |
| fips_code | TEXT UNIQUE | 11-digit FIPS code |
| county | TEXT | County name |
| state | TEXT | State name |
| year | INTEGER | Data year (2017-2024) |
| is_opportunity_zone | TEXT | Opportunity zone designation |
| inclusive_growth_score | INTEGER | Primary IGS score |
| growth_score | INTEGER | Growth dimension score |
| inclusion_score | INTEGER | Inclusion dimension score |
| internet_access_score | INTEGER | Digital inclusion metric |
| minority_women_business_score | INTEGER | Entrepreneurial equity metric |
| affordable_housing_score | INTEGER | Housing cost burden metric |
| personal_income_score | INTEGER | Income opportunity metric |
| ... | ... | (Additional 60+ metric columns) |

**Indexes:**
- `idx_state` on `state`
- `idx_county` on `county`
- `idx_year` on `year`
- `idx_fips_year` on `(fips_code, year)` (composite)

## ETL Pipeline Overview

```python
# Pseudocode for etl.py

1. Load cleaned CSV from data/processed/
2. Connect to SQLite database
3. Create table if not exists
4. Transform data:
   - Normalize column names (remove spaces, lowercase)
   - Handle null values
   - Validate FIPS codes
5. Insert records (bulk insert for performance)
6. Create indexes
7. Verify record count
```

## Development Commands (Future)

```bash
# Install dependencies
pip install -r requirements.txt

# Run ETL pipeline
python etl.py

# Start development server
uvicorn main:app --reload --port 8000

# Run tests
pytest tests/ -v

# Check API documentation
# Visit: http://localhost:8000/docs
```

## Dependencies (requirements.txt - planned)

```
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
pandas==2.1.3
pydantic==2.5.0
python-dotenv==1.0.0
google-cloud-storage==2.10.0
pytest==7.4.3
httpx==0.25.1
```

---

**Status:** Planning Phase  
**Next Steps:** Implement database schema and ETL pipeline  
**Developer:** Emery

