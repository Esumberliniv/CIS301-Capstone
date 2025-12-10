"""
API Endpoint Unit Tests
CIS 301 Capstone Project - Clark Atlanta CIS301

Essential tests for FastAPI REST API endpoints
"""

import pytest
from fastapi import status
from fastapi.testclient import TestClient
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from backend.main import app

client = TestClient(app)


class TestAPIEndpoints:
    """Core API endpoint tests"""
    
    def test_health_check(self):
        """Health endpoint returns correct structure and status"""
        response = client.get("/api/health")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == "healthy"
        assert data["database_connected"] is True
        assert data["total_records"] > 0
    
    def test_get_tracts(self):
        """Tracts endpoint returns data with correct structure"""
        response = client.get("/api/tracts?limit=5")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "total" in data
        assert "tracts" in data
        assert len(data["tracts"]) <= 5
    
    def test_get_tracts_filter_by_year(self):
        """Tracts endpoint filters by year correctly"""
        response = client.get("/api/tracts?year=2023")
        data = response.json()
        for tract in data["tracts"]:
            assert tract["year"] == 2023
    
    def test_get_states(self):
        """States endpoint returns list with counts"""
        response = client.get("/api/states")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        assert "state" in data[0]
        assert "count" in data[0]
    
    def test_get_statistics(self):
        """Statistics endpoint calculates metrics correctly"""
        response = client.get("/api/statistics?metric=inclusive_growth_score")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["count"] > 0
        assert data["min"] <= data["mean"] <= data["max"]
    
    def test_invalid_metric_returns_400(self):
        """Invalid metric returns 400 error"""
        response = client.get("/api/statistics?metric=fake_metric")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
