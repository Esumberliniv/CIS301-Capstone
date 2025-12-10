"""
Configuration for FastAPI Backend
CIS 301 Capstone Project - Clark Atlanta CIS301
"""

from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent.parent.parent

# Database configuration
DATABASE_PATH = BASE_DIR / "data" / "igs_data.db"
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

# API configuration
API_TITLE = "IGS Data API"
API_DESCRIPTION = """
Mastercard Inclusive Growth Score (IGS) API

This API provides access to economic inclusion data at the census tract level across the United States.

## Key Features:
- Query IGS data by geography (state, county, census tract)
- Filter by year (2017-2024)
- Access specific metrics (Internet Access, Minority/Women-Owned Businesses, etc.)
- Calculate state/county averages for comparison
- Analyze correlations between metrics

## Use Cases:
- Policy research and analysis
- Economic equity assessment
- Community investment planning
- DEI (Diversity, Equity, and Inclusion) initiatives
"""
API_VERSION = "1.0.0"

# CORS configuration
CORS_ORIGINS = [
    "http://localhost:8501",  # Streamlit default port
    "http://localhost:3000",  # React dev server (future)
    "http://127.0.0.1:8501",
]

# Server configuration
HOST = "0.0.0.0"
PORT = 8000
RELOAD = True  # Set to False in production


