"""
API Client for IGS Dashboard
CIS 301 Capstone Project - Clark Atlanta CIS301

Handles all HTTP requests to the FastAPI backend
"""

import requests
from typing import Dict, List, Optional, Any
import sys
from pathlib import Path

# Add frontend directory to path
frontend_path = Path(__file__).parent.parent
sys.path.insert(0, str(frontend_path))

from config import API_BASE_URL


class APIClient:
    """Client for interacting with the IGS Data API"""
    
    def __init__(self, base_url: str = API_BASE_URL):
        """
        Initialize API client
        
        Args:
            base_url: Base URL of the API
        """
        self.base_url = base_url
        self.session = requests.Session()
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """
        Make HTTP request to API
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint
            **kwargs: Additional arguments for requests
            
        Returns:
            JSON response as dictionary
        """
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.ConnectionError:
            raise Exception(f"Could not connect to API at {self.base_url}. Make sure the backend is running.")
        except requests.exceptions.HTTPError as e:
            raise Exception(f"API request failed: {str(e)}")
        except Exception as e:
            raise Exception(f"Unexpected error: {str(e)}")
    
    def health_check(self) -> Dict[str, Any]:
        """Check API health status"""
        return self._make_request("GET", "/api/health")
    
    def get_tracts(
        self,
        state: Optional[str] = None,
        county: Optional[str] = None,
        year: Optional[int] = None,
        limit: int = 100,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        Get census tracts with filters
        
        Args:
            state: Filter by state
            county: Filter by county
            year: Filter by year
            limit: Maximum results
            offset: Pagination offset
            
        Returns:
            Dictionary with 'total' and 'tracts' keys
        """
        params = {'limit': limit, 'offset': offset}
        if state:
            params['state'] = state
        if county:
            params['county'] = county
        if year:
            params['year'] = year
        
        return self._make_request("GET", "/api/tracts", params=params)
    
    def get_tract_by_fips(self, fips_code: str, year: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get specific census tract by FIPS code
        
        Args:
            fips_code: Census tract FIPS code
            year: Optional year filter
            
        Returns:
            List of tract records
        """
        params = {}
        if year:
            params['year'] = year
        
        return self._make_request("GET", f"/api/tracts/{fips_code}", params=params)
    
    def get_states(self) -> List[Dict[str, Any]]:
        """
        Get list of available states
        
        Returns:
            List of state dictionaries with 'state' and 'count' keys
        """
        return self._make_request("GET", "/api/states")
    
    def get_metrics(
        self,
        metric: str,
        state: Optional[str] = None,
        county: Optional[str] = None,
        year: Optional[int] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Get specific metric values
        
        Args:
            metric: Metric name
            state: Filter by state
            county: Filter by county
            year: Filter by year
            limit: Maximum results
            
        Returns:
            List of metric value dictionaries
        """
        params = {'metric': metric, 'limit': limit}
        if state:
            params['state'] = state
        if county:
            params['county'] = county
        if year:
            params['year'] = year
        
        return self._make_request("GET", "/api/metrics", params=params)
    
    def get_statistics(
        self,
        metric: str,
        state: Optional[str] = None,
        county: Optional[str] = None,
        year: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Get statistical aggregations for a metric
        
        Args:
            metric: Metric name
            state: Filter by state
            county: Filter by county
            year: Filter by year
            
        Returns:
            Statistics dictionary with mean, median, min, max, std_dev
        """
        params = {'metric': metric}
        if state:
            params['state'] = state
        if county:
            params['county'] = county
        if year:
            params['year'] = year
        
        return self._make_request("GET", "/api/statistics", params=params)
    
    def get_correlation(
        self,
        metric_x: str,
        metric_y: str,
        state: Optional[str] = None,
        year: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Get correlation between two metrics
        
        Args:
            metric_x: First metric
            metric_y: Second metric
            state: Filter by state
            year: Filter by year
            
        Returns:
            Correlation dictionary with coefficient and sample size
        """
        params = {
            'metric_x': metric_x,
            'metric_y': metric_y
        }
        if state:
            params['state'] = state
        if year:
            params['year'] = year
        
        return self._make_request("GET", "/api/correlations", params=params)
    
    # ==================== INSIGHTS ENDPOINTS ====================
    
    def get_tract_trends(
        self,
        fips_code: str,
        metric: str = "inclusive_growth_score"
    ) -> Dict[str, Any]:
        """
        Get trend analysis for a census tract over time
        
        Args:
            fips_code: Census tract FIPS code
            metric: Metric to analyze
            
        Returns:
            Trend analysis with year-over-year changes
        """
        params = {'metric': metric}
        return self._make_request("GET", f"/api/insights/trends/{fips_code}", params=params)
    
    def get_rankings(
        self,
        metric: str = "inclusive_growth_score",
        state: Optional[str] = None,
        year: Optional[int] = None,
        limit: int = 10
    ) -> Dict[str, Any]:
        """
        Get top and bottom performing tracts
        
        Args:
            metric: Metric to rank by
            state: Filter by state
            year: Filter by year
            limit: Number of top/bottom performers
            
        Returns:
            Rankings with top and bottom performers
        """
        params = {'metric': metric, 'limit': limit}
        if state:
            params['state'] = state
        if year:
            params['year'] = year
        
        return self._make_request("GET", "/api/insights/rankings", params=params)
    
    def get_regional_insights(
        self,
        state: str,
        county: Optional[str] = None,
        year: int = 2024
    ) -> Dict[str, Any]:
        """
        Get comprehensive regional insights
        
        Args:
            state: State to analyze
            county: Optional county filter
            year: Year to analyze
            
        Returns:
            Regional insights with category summaries and disparities
        """
        params = {'state': state, 'year': year}
        if county:
            params['county'] = county
        
        return self._make_request("GET", "/api/insights/regional", params=params)
    
    def get_equity_scorecard(
        self,
        fips_code: str,
        year: int = 2024
    ) -> Dict[str, Any]:
        """
        Get equity scorecard for a census tract
        
        Args:
            fips_code: Census tract FIPS code
            year: Year for scorecard
            
        Returns:
            Scorecard with grades and comparisons
        """
        params = {'year': year}
        return self._make_request("GET", f"/api/insights/scorecard/{fips_code}", params=params)
    
    def get_year_over_year(
        self,
        state: str,
        year_start: int = 2017,
        year_end: int = 2024
    ) -> List[Dict[str, Any]]:
        """
        Get year-over-year changes for key metrics
        
        Args:
            state: State to analyze
            year_start: Starting year
            year_end: Ending year
            
        Returns:
            List of year-over-year changes by metric
        """
        params = {
            'state': state,
            'year_start': year_start,
            'year_end': year_end
        }
        return self._make_request("GET", "/api/insights/year-over-year", params=params)
    
    def get_dei_opportunity_rankings(
        self,
        year: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Get DEI Opportunity rankings for all counties
        
        Args:
            year: Year to analyze (defaults to latest available)
            
        Returns:
            County rankings by DEI Opportunity Score
        """
        params = {}
        if year:
            params['year'] = year
        return self._make_request("GET", "/api/insights/dei-opportunity", params=params)


# Global API client instance
api_client = APIClient()


