"""
Pydantic Response Models for FastAPI
CIS 301 Capstone Project - Clark Atlanta CIS301
"""

from pydantic import BaseModel, Field
from typing import Optional, List


class TractResponse(BaseModel):
    """Response model for a single census tract"""
    id: int
    is_opportunity_zone: Optional[str] = None
    census_tract_fips: str
    county: str
    state: str
    year: int
    inclusive_growth_score: Optional[float] = None
    growth: Optional[float] = None
    inclusion: Optional[float] = None
    
    # Place metrics
    place: Optional[float] = None
    place_growth: Optional[float] = None
    place_inclusion: Optional[float] = None
    
    # Key metrics for DEI analysis
    internet_access_score: Optional[float] = None
    internet_access_base_pct: Optional[float] = None
    internet_access_tract_pct: Optional[float] = None
    
    affordable_housing_score: Optional[float] = None
    affordable_housing_base_pct: Optional[float] = None
    affordable_housing_tract_pct: Optional[float] = None
    
    minority_women_owned_businesses_score: Optional[float] = None
    minority_women_owned_businesses_base_pct: Optional[float] = None
    minority_women_owned_businesses_tract_pct: Optional[float] = None
    
    personal_income_score: Optional[float] = None
    personal_income_base_pct: Optional[float] = None
    personal_income_tract_pct: Optional[float] = None
    
    small_business_loans_score: Optional[float] = None
    
    class Config:
        from_attributes = True


class TractListResponse(BaseModel):
    """Response model for list of census tracts"""
    total: int = Field(..., description="Total number of records")
    tracts: List[TractResponse] = Field(..., description="List of census tracts")


class StateResponse(BaseModel):
    """Response model for state information"""
    state: str
    count: int = Field(..., description="Number of tracts in state")


class MetricResponse(BaseModel):
    """Response model for specific metric data"""
    census_tract_fips: str
    state: str
    county: str
    year: int
    metric_name: str
    metric_value: Optional[float] = None


class StatisticsResponse(BaseModel):
    """Response model for statistical aggregations"""
    state: Optional[str] = None
    county: Optional[str] = None
    year: Optional[int] = None
    metric: str
    
    count: int
    mean: Optional[float] = None
    median: Optional[float] = None
    min: Optional[float] = None
    max: Optional[float] = None
    std_dev: Optional[float] = None


class CorrelationResponse(BaseModel):
    """Response model for correlation analysis"""
    metric_x: str
    metric_y: str
    correlation_coefficient: Optional[float] = None
    sample_size: int
    state_filter: Optional[str] = None
    year_filter: Optional[int] = None


class HealthResponse(BaseModel):
    """Response model for API health check"""
    status: str
    database_connected: bool
    total_records: int
    states_available: List[str]


# ==================== INSIGHTS RESPONSE MODELS ====================

class TrendDataPoint(BaseModel):
    """Single data point for trend analysis"""
    year: int
    value: Optional[float] = None
    change: Optional[float] = None
    change_pct: Optional[float] = None


class TrendAnalysisResponse(BaseModel):
    """Response model for tract trend analysis over time"""
    census_tract_fips: str
    state: str
    county: str
    metric: str
    metric_display_name: str
    trend_direction: str  # "improving", "declining", "stable"
    data_points: List[TrendDataPoint]
    overall_change: Optional[float] = None
    overall_change_pct: Optional[float] = None
    avg_annual_change: Optional[float] = None


class TractRankingItem(BaseModel):
    """Single tract in rankings"""
    rank: int
    census_tract_fips: str
    state: str
    county: str
    score: Optional[float] = None
    percentile: Optional[float] = None


class RankingsResponse(BaseModel):
    """Response model for tract rankings"""
    metric: str
    metric_display_name: str
    year: Optional[int] = None
    state_filter: Optional[str] = None
    total_tracts: int
    top_performers: List[TractRankingItem]
    bottom_performers: List[TractRankingItem]


class CategorySummary(BaseModel):
    """Summary for a metric category (Place, Economy, Community)"""
    category: str
    avg_score: Optional[float] = None
    min_score: Optional[float] = None
    max_score: Optional[float] = None
    above_average_count: int
    below_average_count: int
    key_insight: str


class DisparityMetric(BaseModel):
    """Disparity measurement for a metric"""
    metric: str
    metric_display_name: str
    disparity_score: float  # Difference between max and min
    coefficient_of_variation: Optional[float] = None  # Std dev / mean
    gap_interpretation: str


class RegionalInsightsResponse(BaseModel):
    """Comprehensive regional insights"""
    state: str
    county: Optional[str] = None
    year: int
    total_tracts: int
    
    # Overall scores
    avg_inclusive_growth_score: Optional[float] = None
    
    # Category breakdowns
    place_summary: CategorySummary
    economy_summary: CategorySummary
    community_summary: CategorySummary
    
    # Top disparities (areas with largest gaps)
    top_disparities: List[DisparityMetric]
    
    # Key findings
    key_insights: List[str]
    
    # Opportunity zones
    tracts_needing_attention: int  # Tracts with IGS < 50
    high_performing_tracts: int  # Tracts with IGS >= 70


class EquityScorecard(BaseModel):
    """Equity scorecard for a specific tract"""
    census_tract_fips: str
    state: str
    county: str
    year: int
    
    # Overall grade
    overall_grade: str  # A, B, C, D, F
    overall_score: Optional[float] = None
    
    # Category grades
    place_grade: str
    place_score: Optional[float] = None
    economy_grade: str
    economy_score: Optional[float] = None
    community_grade: str
    community_score: Optional[float] = None
    
    # Strengths and weaknesses
    top_strengths: List[str]
    areas_for_improvement: List[str]
    
    # Comparison to state
    vs_state_avg: Optional[float] = None
    state_percentile: Optional[float] = None


class YearOverYearComparison(BaseModel):
    """Year-over-year comparison data"""
    metric: str
    year_start: int
    year_end: int
    start_value: Optional[float] = None
    end_value: Optional[float] = None
    absolute_change: Optional[float] = None
    percent_change: Optional[float] = None
    trend: str  # "improved", "declined", "stable"


