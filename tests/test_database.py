"""
Database Unit Tests
CIS 301 Capstone Project - Clark Atlanta CIS301

Essential tests for database models and queries
"""

import pytest
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from backend.database.schema import Base, CensusTract


@pytest.fixture
def test_session():
    """Create an in-memory test database"""
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
    engine.dispose()


class TestDatabase:
    """Core database tests"""
    
    def test_create_census_tract(self, test_session):
        """Should create a CensusTract record"""
        tract = CensusTract(
            census_tract_fips="13121001100",
            county="Fulton County",
            state="Georgia",
            year=2023,
            inclusive_growth_score=75.5
        )
        test_session.add(tract)
        test_session.commit()
        
        assert tract.id is not None
        assert tract.state == "Georgia"
    
    def test_query_filter_by_state(self, test_session):
        """Should filter tracts by state"""
        # Add test data
        test_session.add(CensusTract(census_tract_fips="GA001", county="Fulton", state="Georgia", year=2023))
        test_session.add(CensusTract(census_tract_fips="TX001", county="Harris", state="Texas", year=2023))
        test_session.commit()
        
        georgia_tracts = test_session.query(CensusTract).filter(CensusTract.state == "Georgia").all()
        assert len(georgia_tracts) == 1
        assert georgia_tracts[0].state == "Georgia"
    
    def test_tract_to_dict(self, test_session):
        """Should convert model to dictionary"""
        tract = CensusTract(
            census_tract_fips="13121001100",
            county="Fulton County",
            state="Georgia",
            year=2023,
            inclusive_growth_score=75.5
        )
        test_session.add(tract)
        test_session.commit()
        
        tract_dict = tract.to_dict()
        assert isinstance(tract_dict, dict)
        assert tract_dict["state"] == "Georgia"
        assert tract_dict["inclusive_growth_score"] == 75.5
