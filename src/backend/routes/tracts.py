"""
Census Tract API Routes
CIS 301 Capstone Project - Clark Atlanta CIS301
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, distinct
from typing import List, Optional
import sys
from pathlib import Path

# Add backend directory to path
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

from database.connection import get_db
from database.schema import CensusTract
from models.responses import (
    TractResponse, TractListResponse, StateResponse,
    MetricResponse, StatisticsResponse, CorrelationResponse, HealthResponse
)

router = APIRouter(prefix="/api", tags=["tracts"])


@router.get("/health", response_model=HealthResponse)
def health_check(db: Session = Depends(get_db)):
    """
    Health check endpoint
    
    Returns API status and database connection information
    """
    try:
        total_records = db.query(CensusTract).count()
        states = db.query(distinct(CensusTract.state)).all()
        state_list = [s[0] for s in states if s[0]]
        
        return HealthResponse(
            status="healthy",
            database_connected=True,
            total_records=total_records,
            states_available=sorted(state_list)
        )
    except Exception as e:
        return HealthResponse(
            status="unhealthy",
            database_connected=False,
            total_records=0,
            states_available=[]
        )


@router.get("/tracts", response_model=TractListResponse)
def get_tracts(
    state: Optional[str] = Query(None, description="Filter by state name"),
    county: Optional[str] = Query(None, description="Filter by county name"),
    year: Optional[int] = Query(None, description="Filter by year (2017-2024)"),
    limit: int = Query(100, le=500, description="Maximum number of results"),
    offset: int = Query(0, ge=0, description="Offset for pagination"),
    db: Session = Depends(get_db)
):
    """
    Get census tracts with optional filters
    
    Returns a list of census tracts matching the specified criteria
    """
    query = db.query(CensusTract)
    
    # Apply filters
    if state:
        query = query.filter(CensusTract.state == state)
    if county:
        query = query.filter(CensusTract.county == county)
    if year:
        query = query.filter(CensusTract.year == year)
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    tracts = query.offset(offset).limit(limit).all()
    
    return TractListResponse(
        total=total,
        tracts=tracts
    )


@router.get("/tracts/{fips_code}", response_model=List[TractResponse])
def get_tract_by_fips(
    fips_code: str,
    year: Optional[int] = Query(None, description="Filter by specific year"),
    db: Session = Depends(get_db)
):
    """
    Get census tract by FIPS code
    
    Returns all years of data for a specific census tract, or a single year if specified
    """
    query = db.query(CensusTract).filter(CensusTract.census_tract_fips == fips_code)
    
    if year:
        query = query.filter(CensusTract.year == year)
    
    tracts = query.all()
    
    if not tracts:
        raise HTTPException(status_code=404, detail="Census tract not found")
    
    return tracts


@router.get("/states", response_model=List[StateResponse])
def get_states(db: Session = Depends(get_db)):
    """
    Get list of all available states
    
    Returns states with their census tract counts
    """
    states = db.query(
        CensusTract.state,
        func.count(distinct(CensusTract.census_tract_fips)).label('count')
    ).group_by(CensusTract.state).all()
    
    return [
        StateResponse(state=state, count=count)
        for state, count in states if state
    ]


@router.get("/metrics", response_model=List[MetricResponse])
def get_metrics(
    metric: str = Query(..., description="Metric name (e.g., 'internet_access_score')"),
    state: Optional[str] = Query(None, description="Filter by state"),
    county: Optional[str] = Query(None, description="Filter by county"),
    year: Optional[int] = Query(None, description="Filter by year"),
    limit: int = Query(100, le=500),
    db: Session = Depends(get_db)
):
    """
    Get specific metric values with filters
    
    Returns metric values for specified geography and time filters
    """
    # Validate metric exists
    if not hasattr(CensusTract, metric):
        raise HTTPException(status_code=400, detail=f"Invalid metric: {metric}")
    
    query = db.query(CensusTract)
    
    # Apply filters
    if state:
        query = query.filter(CensusTract.state == state)
    if county:
        query = query.filter(CensusTract.county == county)
    if year:
        query = query.filter(CensusTract.year == year)
    
    tracts = query.limit(limit).all()
    
    results = []
    for tract in tracts:
        metric_value = getattr(tract, metric)
        results.append(MetricResponse(
            census_tract_fips=tract.census_tract_fips,
            state=tract.state,
            county=tract.county,
            year=tract.year,
            metric_name=metric,
            metric_value=metric_value
        ))
    
    return results


@router.get("/statistics", response_model=StatisticsResponse)
def get_statistics(
    metric: str = Query(..., description="Metric to analyze"),
    state: Optional[str] = Query(None, description="Filter by state"),
    county: Optional[str] = Query(None, description="Filter by county"),
    year: Optional[int] = Query(None, description="Filter by year"),
    db: Session = Depends(get_db)
):
    """
    Calculate statistical aggregations for a metric
    
    Returns mean, median, min, max, and standard deviation for the specified metric
    """
    # Validate metric exists
    if not hasattr(CensusTract, metric):
        raise HTTPException(status_code=400, detail=f"Invalid metric: {metric}")
    
    query = db.query(CensusTract)
    
    # Apply filters
    if state:
        query = query.filter(CensusTract.state == state)
    if county:
        query = query.filter(CensusTract.county == county)
    if year:
        query = query.filter(CensusTract.year == year)
    
    # Get all values for the metric
    tracts = query.all()
    values = [getattr(tract, metric) for tract in tracts if getattr(tract, metric) is not None]
    
    if not values:
        raise HTTPException(status_code=404, detail="No data found for specified filters")
    
    # Calculate statistics
    import statistics
    
    return StatisticsResponse(
        state=state,
        county=county,
        year=year,
        metric=metric,
        count=len(values),
        mean=statistics.mean(values),
        median=statistics.median(values),
        min=min(values),
        max=max(values),
        std_dev=statistics.stdev(values) if len(values) > 1 else 0.0
    )


@router.get("/correlations", response_model=CorrelationResponse)
def get_correlation(
    metric_x: str = Query(..., description="First metric for correlation"),
    metric_y: str = Query(..., description="Second metric for correlation"),
    state: Optional[str] = Query(None, description="Filter by state"),
    year: Optional[int] = Query(None, description="Filter by year"),
    db: Session = Depends(get_db)
):
    """
    Calculate correlation coefficient between two metrics
    
    Returns Pearson correlation coefficient for the specified metrics
    """
    # Validate metrics exist
    if not hasattr(CensusTract, metric_x):
        raise HTTPException(status_code=400, detail=f"Invalid metric: {metric_x}")
    if not hasattr(CensusTract, metric_y):
        raise HTTPException(status_code=400, detail=f"Invalid metric: {metric_y}")
    
    query = db.query(CensusTract)
    
    # Apply filters
    if state:
        query = query.filter(CensusTract.state == state)
    if year:
        query = query.filter(CensusTract.year == year)
    
    # Get all tracts
    tracts = query.all()
    
    # Extract values where both metrics are not None
    pairs = []
    for tract in tracts:
        x_val = getattr(tract, metric_x)
        y_val = getattr(tract, metric_y)
        if x_val is not None and y_val is not None:
            pairs.append((x_val, y_val))
    
    if len(pairs) < 2:
        raise HTTPException(status_code=404, detail="Insufficient data for correlation analysis")
    
    # Calculate Pearson correlation
    import statistics
    
    x_values = [p[0] for p in pairs]
    y_values = [p[1] for p in pairs]
    
    # Pearson correlation formula
    n = len(pairs)
    mean_x = statistics.mean(x_values)
    mean_y = statistics.mean(y_values)
    
    numerator = sum((x - mean_x) * (y - mean_y) for x, y in pairs)
    denominator_x = sum((x - mean_x) ** 2 for x in x_values)
    denominator_y = sum((y - mean_y) ** 2 for y in y_values)
    
    if denominator_x == 0 or denominator_y == 0:
        correlation = 0.0
    else:
        correlation = numerator / (denominator_x * denominator_y) ** 0.5
    
    return CorrelationResponse(
        metric_x=metric_x,
        metric_y=metric_y,
        correlation_coefficient=correlation,
        sample_size=n,
        state_filter=state,
        year_filter=year
    )


