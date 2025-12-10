"""
Pytest Configuration and Fixtures
CIS 301 Capstone Project - Clark Atlanta CIS301
"""

import pytest
import sys
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pandas as pd
import tempfile
import os

# Add src to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from backend.database.schema import Base, CensusTract
from backend.main import app
from fastapi.testclient import TestClient


# ============================================================
# Database Fixtures
# ============================================================

@pytest.fixture(scope="function")
def test_engine():
    """Create an in-memory SQLite database for testing"""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False}
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    engine.dispose()


@pytest.fixture(scope="function")
def test_session(test_engine):
    """Create a test database session"""
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    session = SessionLocal()
    yield session
    session.close()


@pytest.fixture(scope="function")
def sample_tract_data():
    """Sample census tract data for testing"""
    return {
        "is_opportunity_zone": "Yes",
        "census_tract_fips": "13121001100",
        "county": "Fulton County",
        "state": "Georgia",
        "year": 2023,
        "inclusive_growth_score": 75.5,
        "growth": 80.0,
        "inclusion": 70.0,
        "place": 72.5,
        "internet_access_score": 85.0,
        "affordable_housing_score": 65.0,
        "minority_women_owned_businesses_score": 55.0,
        "personal_income_score": 78.0
    }


@pytest.fixture(scope="function")
def populated_session(test_session, sample_tract_data):
    """Create a test session with sample data"""
    # Create multiple test records
    tracts = [
        CensusTract(**sample_tract_data),
        CensusTract(
            is_opportunity_zone="No",
            census_tract_fips="13121001200",
            county="Fulton County",
            state="Georgia",
            year=2023,
            inclusive_growth_score=82.0,
            growth=85.0,
            inclusion=78.0,
            internet_access_score=90.0,
            affordable_housing_score=70.0,
            personal_income_score=85.0
        ),
        CensusTract(
            is_opportunity_zone="Yes",
            census_tract_fips="48201001000",
            county="Harris County",
            state="Texas",
            year=2023,
            inclusive_growth_score=68.0,
            growth=72.0,
            inclusion=65.0,
            internet_access_score=75.0,
            affordable_housing_score=60.0,
            personal_income_score=70.0
        ),
        CensusTract(
            is_opportunity_zone="No",
            census_tract_fips="13121001100",
            county="Fulton County",
            state="Georgia",
            year=2022,
            inclusive_growth_score=72.0,
            growth=76.0,
            inclusion=68.0,
            internet_access_score=80.0,
            affordable_housing_score=62.0,
            personal_income_score=74.0
        ),
    ]
    
    for tract in tracts:
        test_session.add(tract)
    test_session.commit()
    
    yield test_session


# ============================================================
# API Client Fixtures
# ============================================================

@pytest.fixture(scope="function")
def client(populated_session):
    """Create a test client with database override"""
    from backend.database.connection import get_db
    
    def override_get_db():
        try:
            yield populated_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()


# ============================================================
# ETL Test Fixtures
# ============================================================

@pytest.fixture(scope="function")
def sample_csv_data():
    """Sample CSV data for ETL testing"""
    return """Category,Is an Opportunity Zone,Census Tract FIPS code,County,State,Year,Inclusive Growth Score,Growth,Inclusion
Subcategory,N/A,N/A,N/A,N/A,N/A,Score,Score,Score

Yes,13121001100,Fulton County,Georgia,2023,75.5,80.0,70.0
No,13121001200,Fulton County,Georgia,2023,82.0,N/A,78.0
Yes,48201001000,Harris County,Texas,2023,68.0,72.0,65.0
"""


@pytest.fixture(scope="function")
def temp_csv_file(sample_csv_data):
    """Create a temporary CSV file for testing"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write(sample_csv_data)
        temp_path = f.name
    
    yield temp_path
    
    # Cleanup
    if os.path.exists(temp_path):
        os.remove(temp_path)


@pytest.fixture(scope="function")
def temp_output_dir():
    """Create a temporary output directory"""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    
    # Cleanup
    import shutil
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)



