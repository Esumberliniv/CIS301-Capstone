"""
Configuration for Streamlit Frontend
CIS 301 Capstone Project - Clark Atlanta CIS301
"""

# API Configuration
API_BASE_URL = "http://localhost:8000"

# Page Configuration
PAGE_TITLE = "IGS Data Dashboard"
PAGE_ICON = "📊"
LAYOUT = "wide"

# Dashboard Information
DASHBOARD_TITLE = "Equity in Focus: IGS Data Dashboard"
DASHBOARD_SUBTITLE = "Visualizing Economic Inclusion Across U.S. Communities"
PROJECT_INFO = "CIS 301 Capstone Project - Clark Atlanta CIS301"

# Color schemes for visualizations
COLOR_SCHEME = {
    'primary': '#1f77b4',
    'secondary': '#ff7f0e',
    'success': '#2ca02c',
    'danger': '#d62728',
    'warning': '#ff9933',
    'info': '#17becf'
}

# Metric display names
METRIC_NAMES = {
    # Summary Scores
    'inclusive_growth_score': 'Inclusive Growth Score',
    'growth': 'Growth',
    'inclusion': 'Inclusion',
    
    # Place Metrics
    'place': 'Place (Overall)',
    'place_growth': 'Place Growth',
    'place_inclusion': 'Place Inclusion',
    'net_occupancy_score': 'Net Occupancy',
    'residential_real_estate_value_score': 'Residential Real Estate Value',
    'acres_of_park_land_score': 'Park Land Access',
    'affordable_housing_score': 'Affordable Housing Score',
    'internet_access_score': 'Internet Access Score',
    'travel_time_to_work_score': 'Travel Time to Work',
    
    # Economy Metrics
    'economy': 'Economy (Overall)',
    'economy_growth': 'Economy Growth',
    'economy_inclusion': 'Economy Inclusion',
    'new_businesses_score': 'New Businesses Score',
    'spend_growth_score': 'Spending Growth',
    'small_business_loans_score': 'Small Business Loans Score',
    'minority_women_owned_businesses_score': 'Minority/Women-Owned Businesses Score',
    'labor_market_engagement_index_score': 'Labor Market Engagement',
    'commercial_diversity_score': 'Commercial Diversity',
    
    # Community Metrics
    'community': 'Community (Overall)',
    'community_growth': 'Community Growth',
    'community_inclusion': 'Community Inclusion',
    'personal_income_score': 'Personal Income Score',
    'spending_per_capita_score': 'Spending Per Capita',
    'female_above_poverty_score': 'Female Above Poverty',
    'gini_coefficient_score': 'Income Equality (Gini)',
    'early_education_enrollment_score': 'Early Education Enrollment',
    'health_insurance_coverage_score': 'Health Insurance Coverage Score',
}


