"""
Insights API Routes
CIS 301 Capstone Project - Clark Atlanta CIS301

Advanced analytics and insights endpoints for IGS data
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, distinct
from typing import List, Optional
import statistics
import sys
from pathlib import Path

# Add backend directory to path
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

from database.connection import get_db
from database.schema import CensusTract
from models.responses import (
    TrendAnalysisResponse, TrendDataPoint,
    RankingsResponse, TractRankingItem,
    RegionalInsightsResponse, CategorySummary, DisparityMetric,
    EquityScorecard, YearOverYearComparison
)

router = APIRouter(prefix="/api/insights", tags=["insights"])

# Metric display names for insights
METRIC_DISPLAY_NAMES = {
    'inclusive_growth_score': 'Inclusive Growth Score',
    'internet_access_score': 'Internet Access',
    'affordable_housing_score': 'Affordable Housing',
    'minority_women_owned_businesses_score': 'Minority/Women-Owned Businesses',
    'personal_income_score': 'Personal Income',
    'small_business_loans_score': 'Small Business Loans',
    'new_businesses_score': 'New Businesses',
    'health_insurance_coverage_score': 'Health Insurance Coverage',
    'place': 'Place (Overall)',
    'economy': 'Economy (Overall)',
    'community': 'Community (Overall)',
    'growth': 'Growth',
    'inclusion': 'Inclusion',
    'net_occupancy_score': 'Net Occupancy',
    'residential_real_estate_value_score': 'Residential Real Estate Value',
    'acres_of_park_land_score': 'Park Land Access',
    'travel_time_to_work_score': 'Travel Time to Work',
    'spend_growth_score': 'Spending Growth',
    'labor_market_engagement_index_score': 'Labor Market Engagement',
    'commercial_diversity_score': 'Commercial Diversity',
    'spending_per_capita_score': 'Spending Per Capita',
    'female_above_poverty_score': 'Female Above Poverty',
    'gini_coefficient_score': 'Income Equality (Gini)',
    'early_education_enrollment_score': 'Early Education Enrollment',
}


def get_grade(score: Optional[float]) -> str:
    """Convert numeric score to letter grade"""
    if score is None:
        return "N/A"
    if score >= 80:
        return "A"
    elif score >= 70:
        return "B"
    elif score >= 60:
        return "C"
    elif score >= 50:
        return "D"
    else:
        return "F"


def get_trend_direction(change: Optional[float]) -> str:
    """Determine trend direction from change value"""
    if change is None:
        return "stable"
    if change > 2:
        return "improving"
    elif change < -2:
        return "declining"
    else:
        return "stable"


@router.get("/trends/{fips_code}", response_model=TrendAnalysisResponse)
def get_tract_trends(
    fips_code: str,
    metric: str = Query("inclusive_growth_score", description="Metric to analyze trends for"),
    db: Session = Depends(get_db)
):
    """
    Analyze trends for a specific census tract over time
    
    Returns year-over-year changes and overall trend direction
    """
    # Validate metric
    if not hasattr(CensusTract, metric):
        raise HTTPException(status_code=400, detail=f"Invalid metric: {metric}")
    
    # Get all years of data for this tract
    tracts = db.query(CensusTract).filter(
        CensusTract.census_tract_fips == fips_code
    ).order_by(CensusTract.year).all()
    
    if not tracts:
        raise HTTPException(status_code=404, detail="Census tract not found")
    
    # Build trend data
    data_points = []
    prev_value = None
    
    for tract in tracts:
        value = getattr(tract, metric)
        change = None
        change_pct = None
        
        if value is not None and prev_value is not None:
            change = value - prev_value
            if prev_value != 0:
                change_pct = (change / prev_value) * 100
        
        data_points.append(TrendDataPoint(
            year=tract.year,
            value=value,
            change=change,
            change_pct=change_pct
        ))
        
        if value is not None:
            prev_value = value
    
    # Calculate overall change
    values = [dp.value for dp in data_points if dp.value is not None]
    overall_change = None
    overall_change_pct = None
    avg_annual_change = None
    
    if len(values) >= 2:
        overall_change = values[-1] - values[0]
        if values[0] != 0:
            overall_change_pct = (overall_change / values[0]) * 100
        avg_annual_change = overall_change / (len(values) - 1)
    
    return TrendAnalysisResponse(
        census_tract_fips=fips_code,
        state=tracts[0].state,
        county=tracts[0].county,
        metric=metric,
        metric_display_name=METRIC_DISPLAY_NAMES.get(metric, metric),
        trend_direction=get_trend_direction(overall_change),
        data_points=data_points,
        overall_change=overall_change,
        overall_change_pct=overall_change_pct,
        avg_annual_change=avg_annual_change
    )


@router.get("/rankings", response_model=RankingsResponse)
def get_rankings(
    metric: str = Query("inclusive_growth_score", description="Metric to rank by"),
    state: Optional[str] = Query(None, description="Filter by state"),
    year: Optional[int] = Query(None, description="Filter by year"),
    limit: int = Query(10, le=50, description="Number of top/bottom performers"),
    db: Session = Depends(get_db)
):
    """
    Get top and bottom performing tracts for a specific metric
    
    Returns rankings with percentiles
    """
    if not hasattr(CensusTract, metric):
        raise HTTPException(status_code=400, detail=f"Invalid metric: {metric}")
    
    # Build query
    query = db.query(CensusTract)
    
    if state:
        query = query.filter(CensusTract.state == state)
    if year:
        query = query.filter(CensusTract.year == year)
    
    # Get all tracts with valid metric values
    tracts = query.all()
    valid_tracts = [(t, getattr(t, metric)) for t in tracts if getattr(t, metric) is not None]
    
    if not valid_tracts:
        raise HTTPException(status_code=404, detail="No data found for specified filters")
    
    # Sort by metric value
    sorted_tracts = sorted(valid_tracts, key=lambda x: x[1], reverse=True)
    total = len(sorted_tracts)
    
    # Build top performers
    top_performers = []
    for i, (tract, score) in enumerate(sorted_tracts[:limit]):
        percentile = ((total - i) / total) * 100
        top_performers.append(TractRankingItem(
            rank=i + 1,
            census_tract_fips=tract.census_tract_fips,
            state=tract.state,
            county=tract.county,
            score=score,
            percentile=percentile
        ))
    
    # Build bottom performers
    bottom_performers = []
    for i, (tract, score) in enumerate(reversed(sorted_tracts[-limit:])):
        percentile = ((i + 1) / total) * 100
        bottom_performers.append(TractRankingItem(
            rank=total - limit + i + 1,
            census_tract_fips=tract.census_tract_fips,
            state=tract.state,
            county=tract.county,
            score=score,
            percentile=percentile
        ))
    
    return RankingsResponse(
        metric=metric,
        metric_display_name=METRIC_DISPLAY_NAMES.get(metric, metric),
        year=year,
        state_filter=state,
        total_tracts=total,
        top_performers=top_performers,
        bottom_performers=bottom_performers
    )


@router.get("/regional", response_model=RegionalInsightsResponse)
def get_regional_insights(
    state: str = Query(..., description="State to analyze"),
    county: Optional[str] = Query(None, description="Optional county filter"),
    year: int = Query(2024, description="Year to analyze"),
    db: Session = Depends(get_db)
):
    """
    Get comprehensive regional insights for a state/county
    
    Returns category summaries, disparity analysis, and key insights
    """
    # Build query
    query = db.query(CensusTract).filter(
        CensusTract.state == state,
        CensusTract.year == year
    )
    
    if county:
        query = query.filter(CensusTract.county == county)
    
    tracts = query.all()
    
    if not tracts:
        raise HTTPException(status_code=404, detail="No data found for specified filters")
    
    total_tracts = len(tracts)
    
    # Helper to calculate category summary
    def calc_category_summary(category: str, metric_name: str) -> CategorySummary:
        values = [getattr(t, metric_name) for t in tracts if getattr(t, metric_name) is not None]
        
        if not values:
            return CategorySummary(
                category=category,
                avg_score=None,
                min_score=None,
                max_score=None,
                above_average_count=0,
                below_average_count=0,
                key_insight="Insufficient data"
            )
        
        avg = statistics.mean(values)
        above_avg = sum(1 for v in values if v >= 50)
        below_avg = sum(1 for v in values if v < 50)
        
        # Generate insight based on data
        if avg >= 60:
            insight = f"{category} metrics show strong performance with {above_avg}/{len(values)} tracts above state baseline"
        elif avg >= 50:
            insight = f"{category} metrics are near state average with room for improvement"
        else:
            insight = f"{category} metrics indicate opportunity for intervention - {below_avg}/{len(values)} tracts below baseline"
        
        return CategorySummary(
            category=category,
            avg_score=avg,
            min_score=min(values),
            max_score=max(values),
            above_average_count=above_avg,
            below_average_count=below_avg,
            key_insight=insight
        )
    
    # Calculate category summaries
    place_summary = calc_category_summary("Place", "place")
    economy_summary = calc_category_summary("Economy", "economy")
    community_summary = calc_category_summary("Community", "community")
    
    # Calculate disparities for key metrics
    disparity_metrics = [
        'internet_access_score',
        'affordable_housing_score',
        'minority_women_owned_businesses_score',
        'personal_income_score',
        'health_insurance_coverage_score'
    ]
    
    disparities = []
    for metric in disparity_metrics:
        values = [getattr(t, metric) for t in tracts if getattr(t, metric) is not None]
        
        if len(values) >= 2:
            disparity = max(values) - min(values)
            mean_val = statistics.mean(values)
            std_val = statistics.stdev(values) if len(values) > 1 else 0
            cv = (std_val / mean_val * 100) if mean_val != 0 else 0
            
            # Generate interpretation
            if disparity > 40:
                interpretation = "Severe disparity - significant intervention needed"
            elif disparity > 25:
                interpretation = "Moderate disparity - targeted programs recommended"
            else:
                interpretation = "Low disparity - relatively equitable distribution"
            
            disparities.append(DisparityMetric(
                metric=metric,
                metric_display_name=METRIC_DISPLAY_NAMES.get(metric, metric),
                disparity_score=disparity,
                coefficient_of_variation=cv,
                gap_interpretation=interpretation
            ))
    
    # Sort disparities by score (highest first)
    disparities.sort(key=lambda x: x.disparity_score, reverse=True)
    
    # Calculate overall IGS
    igs_values = [t.inclusive_growth_score for t in tracts if t.inclusive_growth_score is not None]
    avg_igs = statistics.mean(igs_values) if igs_values else None
    
    # Count opportunity vs high-performing tracts
    tracts_needing_attention = sum(1 for v in igs_values if v < 50)
    high_performing = sum(1 for v in igs_values if v >= 70)
    
    # Generate key insights
    key_insights = []
    
    if avg_igs:
        if avg_igs >= 60:
            key_insights.append(f"Region shows strong inclusive growth with average IGS of {avg_igs:.1f}")
        elif avg_igs >= 50:
            key_insights.append(f"Region has moderate inclusive growth (IGS: {avg_igs:.1f}) with potential for improvement")
        else:
            key_insights.append(f"Region shows below-average inclusive growth (IGS: {avg_igs:.1f}) - investment opportunities exist")
    
    if disparities:
        top_disparity = disparities[0]
        key_insights.append(f"Largest disparity in {top_disparity.metric_display_name} (gap: {top_disparity.disparity_score:.1f} points)")
    
    if tracts_needing_attention > 0:
        pct = (tracts_needing_attention / total_tracts) * 100
        key_insights.append(f"{tracts_needing_attention} tracts ({pct:.0f}%) have IGS below 50 and need targeted support")
    
    if high_performing > 0:
        key_insights.append(f"{high_performing} high-performing tracts (IGS ≥ 70) can serve as models for improvement")
    
    return RegionalInsightsResponse(
        state=state,
        county=county,
        year=year,
        total_tracts=total_tracts,
        avg_inclusive_growth_score=avg_igs,
        place_summary=place_summary,
        economy_summary=economy_summary,
        community_summary=community_summary,
        top_disparities=disparities[:5],
        key_insights=key_insights,
        tracts_needing_attention=tracts_needing_attention,
        high_performing_tracts=high_performing
    )


@router.get("/scorecard/{fips_code}", response_model=EquityScorecard)
def get_equity_scorecard(
    fips_code: str,
    year: int = Query(2024, description="Year for scorecard"),
    db: Session = Depends(get_db)
):
    """
    Generate an equity scorecard for a specific census tract
    
    Returns letter grades and comparison to state averages
    """
    # Get tract data
    tract = db.query(CensusTract).filter(
        CensusTract.census_tract_fips == fips_code,
        CensusTract.year == year
    ).first()
    
    if not tract:
        raise HTTPException(status_code=404, detail="Census tract not found for specified year")
    
    # Get state averages for comparison
    state_tracts = db.query(CensusTract).filter(
        CensusTract.state == tract.state,
        CensusTract.year == year
    ).all()
    
    # Calculate state percentile for IGS
    igs_values = sorted([t.inclusive_growth_score for t in state_tracts if t.inclusive_growth_score is not None])
    
    state_percentile = None
    state_avg = None
    vs_state_avg = None
    
    if igs_values:
        state_avg = statistics.mean(igs_values)
        if tract.inclusive_growth_score is not None:
            vs_state_avg = tract.inclusive_growth_score - state_avg
            # Calculate percentile
            below_count = sum(1 for v in igs_values if v < tract.inclusive_growth_score)
            state_percentile = (below_count / len(igs_values)) * 100
    
    # Identify strengths and weaknesses
    metrics_to_check = [
        ('internet_access_score', 'Internet Access'),
        ('affordable_housing_score', 'Affordable Housing'),
        ('minority_women_owned_businesses_score', 'Minority/Women-Owned Businesses'),
        ('personal_income_score', 'Personal Income'),
        ('health_insurance_coverage_score', 'Health Insurance Coverage'),
        ('new_businesses_score', 'New Business Formation'),
        ('early_education_enrollment_score', 'Early Education'),
    ]
    
    strengths = []
    weaknesses = []
    
    for metric, name in metrics_to_check:
        value = getattr(tract, metric)
        if value is not None:
            if value >= 60:
                strengths.append(f"{name}: {value:.0f}")
            elif value < 45:
                weaknesses.append(f"{name}: {value:.0f}")
    
    # Sort by score (highest strengths, lowest weaknesses)
    strengths.sort(key=lambda x: float(x.split(': ')[1]), reverse=True)
    weaknesses.sort(key=lambda x: float(x.split(': ')[1]))
    
    return EquityScorecard(
        census_tract_fips=fips_code,
        state=tract.state,
        county=tract.county,
        year=year,
        overall_grade=get_grade(tract.inclusive_growth_score),
        overall_score=tract.inclusive_growth_score,
        place_grade=get_grade(tract.place),
        place_score=tract.place,
        economy_grade=get_grade(tract.economy),
        economy_score=tract.economy,
        community_grade=get_grade(tract.community),
        community_score=tract.community,
        top_strengths=strengths[:3],
        areas_for_improvement=weaknesses[:3],
        vs_state_avg=vs_state_avg,
        state_percentile=state_percentile
    )


@router.get("/year-over-year", response_model=List[YearOverYearComparison])
def get_year_over_year(
    state: str = Query(..., description="State to analyze"),
    year_start: int = Query(2017, description="Starting year"),
    year_end: int = Query(2024, description="Ending year"),
    db: Session = Depends(get_db)
):
    """
    Calculate year-over-year changes for key metrics across a state
    
    Returns aggregated changes for all key DEI metrics
    """
    metrics = [
        'inclusive_growth_score',
        'internet_access_score',
        'affordable_housing_score',
        'minority_women_owned_businesses_score',
        'personal_income_score',
        'health_insurance_coverage_score'
    ]
    
    results = []
    
    for metric in metrics:
        if not hasattr(CensusTract, metric):
            continue
        
        # Get start year data
        start_tracts = db.query(CensusTract).filter(
            CensusTract.state == state,
            CensusTract.year == year_start
        ).all()
        
        # Get end year data
        end_tracts = db.query(CensusTract).filter(
            CensusTract.state == state,
            CensusTract.year == year_end
        ).all()
        
        start_values = [getattr(t, metric) for t in start_tracts if getattr(t, metric) is not None]
        end_values = [getattr(t, metric) for t in end_tracts if getattr(t, metric) is not None]
        
        start_avg = statistics.mean(start_values) if start_values else None
        end_avg = statistics.mean(end_values) if end_values else None
        
        abs_change = None
        pct_change = None
        trend = "stable"
        
        if start_avg is not None and end_avg is not None:
            abs_change = end_avg - start_avg
            if start_avg != 0:
                pct_change = (abs_change / start_avg) * 100
            
            if abs_change > 2:
                trend = "improved"
            elif abs_change < -2:
                trend = "declined"
        
        results.append(YearOverYearComparison(
            metric=metric,
            year_start=year_start,
            year_end=year_end,
            start_value=start_avg,
            end_value=end_avg,
            absolute_change=abs_change,
            percent_change=pct_change,
            trend=trend
        ))
    
    return results


@router.get("/dei-opportunity")
def get_dei_opportunity_rankings(
    year: Optional[int] = Query(None, description="Year to analyze (defaults to latest)"),
    db: Session = Depends(get_db)
):
    """
    Get DEI Opportunity rankings for all counties
    
    Calculates a weighted DEI Opportunity Score based on:
    - Minority/Women-Owned Businesses (25%)
    - Inclusive Growth Score (20%)
    - Internet Access (15%)
    - Affordable Housing (15%)
    - Personal Income (10%)
    - Health Insurance (10%)
    - New Businesses (5%)
    
    Returns counties ranked by DEI potential
    """
    # Get latest year if not specified
    if year is None:
        max_year = db.query(func.max(CensusTract.year)).scalar()
        year = max_year or 2024
    
    # Get all tracts for the specified year
    tracts = db.query(CensusTract).filter(CensusTract.year == year).all()
    
    if not tracts:
        raise HTTPException(status_code=404, detail="No data found for specified year")
    
    # Define weights for DEI calculation
    weights = {
        'minority_women_owned_businesses_score': 0.25,
        'inclusive_growth_score': 0.20,
        'internet_access_score': 0.15,
        'affordable_housing_score': 0.15,
        'personal_income_score': 0.10,
        'health_insurance_coverage_score': 0.10,
        'new_businesses_score': 0.05
    }
    
    # Calculate DEI score for each tract
    tract_scores = []
    for tract in tracts:
        total_weight = 0
        weighted_sum = 0
        
        for metric, weight in weights.items():
            value = getattr(tract, metric)
            if value is not None:
                weighted_sum += value * weight
                total_weight += weight
        
        dei_score = weighted_sum / total_weight if total_weight > 0 else None
        
        tract_scores.append({
            'census_tract_fips': tract.census_tract_fips,
            'county': tract.county,
            'state': tract.state,
            'dei_score': dei_score,
            'inclusive_growth_score': tract.inclusive_growth_score,
            'minority_women_owned_businesses_score': tract.minority_women_owned_businesses_score,
            'internet_access_score': tract.internet_access_score,
            'affordable_housing_score': tract.affordable_housing_score,
            'personal_income_score': tract.personal_income_score,
            'health_insurance_coverage_score': tract.health_insurance_coverage_score,
            'new_businesses_score': tract.new_businesses_score
        })
    
    # Aggregate by county
    county_data = {}
    for ts in tract_scores:
        key = (ts['county'], ts['state'])
        if key not in county_data:
            county_data[key] = {
                'county': ts['county'],
                'state': ts['state'],
                'scores': [],
                'metrics': {k: [] for k in weights.keys()}
            }
        
        if ts['dei_score'] is not None:
            county_data[key]['scores'].append(ts['dei_score'])
        
        for metric in weights.keys():
            if ts[metric] is not None:
                county_data[key]['metrics'][metric].append(ts[metric])
    
    # Calculate county averages
    county_rankings = []
    for key, data in county_data.items():
        if data['scores']:
            avg_dei = statistics.mean(data['scores'])
            
            # Determine category
            if avg_dei >= 65:
                category = "Excellent"
            elif avg_dei >= 50:
                category = "Good"
            elif avg_dei >= 40:
                category = "Moderate"
            else:
                category = "Developing"
            
            county_rankings.append({
                'county': data['county'],
                'state': data['state'],
                'dei_score': round(avg_dei, 1),
                'category': category,
                'tract_count': len(data['scores']),
                'metrics': {
                    metric: round(statistics.mean(values), 1) if values else None
                    for metric, values in data['metrics'].items()
                }
            })
    
    # Sort by DEI score (highest first)
    county_rankings.sort(key=lambda x: x['dei_score'], reverse=True)
    
    # Add ranks
    for i, county in enumerate(county_rankings):
        county['rank'] = i + 1
    
    return {
        'year': year,
        'total_counties': len(county_rankings),
        'rankings': county_rankings
    }

