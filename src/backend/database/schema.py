"""
Database Schema for Mastercard IGS Dataset
CIS 301 Capstone Project - Clark Atlanta CIS301

Defines SQLAlchemy ORM models for the IGS database
"""

from sqlalchemy import Column, Integer, Float, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class CensusTract(Base):
    """
    Census Tract model representing IGS data for a specific tract and year
    
    Primary Key: Composite of census_tract_fips and year
    """
    __tablename__ = 'tracts'
    
    # Composite primary key
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Core Identification Fields
    is_opportunity_zone = Column(String(10), nullable=True)
    census_tract_fips = Column(String(20), nullable=False, index=True)
    county = Column(String(100), nullable=False, index=True)
    state = Column(String(50), nullable=False, index=True)
    year = Column(Integer, nullable=False, index=True)
    
    # Summary Scores
    inclusive_growth_score = Column(Float, nullable=True)
    growth = Column(Float, nullable=True)
    inclusion = Column(Float, nullable=True)
    
    # Place Metrics
    place = Column(Float, nullable=True)
    place_growth = Column(Float, nullable=True)
    place_inclusion = Column(Float, nullable=True)
    
    # Net Occupancy
    net_occupancy_score = Column(Float, nullable=True)
    net_occupancy_base_pct = Column(Float, nullable=True)
    net_occupancy_tract_pct = Column(Float, nullable=True)
    
    # Residential Real Estate Value
    residential_real_estate_value_score = Column(Float, nullable=True)
    residential_real_estate_value_base_pct = Column(Float, nullable=True)
    residential_real_estate_value_tract_pct = Column(Float, nullable=True)
    
    # Acres of Park Land
    acres_of_park_land_score = Column(Float, nullable=True)
    acres_of_park_land_base_pct = Column(Float, nullable=True)
    acres_of_park_land_tract_pct = Column(Float, nullable=True)
    
    # Affordable Housing
    affordable_housing_score = Column(Float, nullable=True)
    affordable_housing_base_pct = Column(Float, nullable=True)
    affordable_housing_tract_pct = Column(Float, nullable=True)
    
    # Internet Access
    internet_access_score = Column(Float, nullable=True)
    internet_access_base_pct = Column(Float, nullable=True)
    internet_access_tract_pct = Column(Float, nullable=True)
    
    # Travel Time to Work
    travel_time_to_work_score = Column(Float, nullable=True)
    travel_time_to_work_base_pct = Column(Float, nullable=True)
    travel_time_to_work_tract_pct = Column(Float, nullable=True)
    
    # Economy Metrics
    economy = Column(Float, nullable=True)
    economy_growth = Column(Float, nullable=True)
    economy_inclusion = Column(Float, nullable=True)
    
    # New Businesses
    new_businesses_score = Column(Float, nullable=True)
    new_businesses_base_pct = Column(Float, nullable=True)
    new_businesses_tract_pct = Column(Float, nullable=True)
    
    # Spend Growth
    spend_growth_score = Column(Float, nullable=True)
    spend_growth_base_pct = Column(Float, nullable=True)
    spend_growth_tract_pct = Column(Float, nullable=True)
    
    # Small Business Loans
    small_business_loans_score = Column(Float, nullable=True)
    small_business_loans_base_pct = Column(Float, nullable=True)
    small_business_loans_tract_pct = Column(Float, nullable=True)
    
    # Minority/Women Owned Businesses
    minority_women_owned_businesses_score = Column(Float, nullable=True)
    minority_women_owned_businesses_base_pct = Column(Float, nullable=True)
    minority_women_owned_businesses_tract_pct = Column(Float, nullable=True)
    
    # Labor Market Engagement
    labor_market_engagement_index_score = Column(Float, nullable=True)
    labor_market_engagement_index_base = Column(Float, nullable=True)
    labor_market_engagement_index_tract = Column(Float, nullable=True)
    
    # Commercial Diversity
    commercial_diversity_score = Column(Float, nullable=True)
    commercial_diversity_base_pct = Column(Float, nullable=True)
    commercial_diversity_tract_pct = Column(Float, nullable=True)
    
    # Community Metrics
    community = Column(Float, nullable=True)
    community_growth = Column(Float, nullable=True)
    community_inclusion = Column(Float, nullable=True)
    
    # Personal Income
    personal_income_score = Column(Float, nullable=True)
    personal_income_base_pct = Column(Float, nullable=True)
    personal_income_tract_pct = Column(Float, nullable=True)
    
    # Spending per Capita
    spending_per_capita_score = Column(Float, nullable=True)
    spending_per_capita_base_pct = Column(Float, nullable=True)
    spending_per_capita_tract_pct = Column(Float, nullable=True)
    
    # Female Above Poverty
    female_above_poverty_score = Column(Float, nullable=True)
    female_above_poverty_base_pct = Column(Float, nullable=True)
    female_above_poverty_tract_pct = Column(Float, nullable=True)
    
    # Gini Coefficient
    gini_coefficient_score = Column(Float, nullable=True)
    gini_coefficient_base = Column(Float, nullable=True)
    gini_coefficient_tract = Column(Float, nullable=True)
    
    # Early Education Enrollment
    early_education_enrollment_score = Column(Float, nullable=True)
    early_education_enrollment_base_pct = Column(Float, nullable=True)
    early_education_enrollment_tract_pct = Column(Float, nullable=True)
    
    # Health Insurance Coverage
    health_insurance_coverage_score = Column(Float, nullable=True)
    health_insurance_coverage_base_pct = Column(Float, nullable=True)
    health_insurance_coverage_tract_pct = Column(Float, nullable=True)
    
    def __repr__(self):
        return f"<CensusTract(fips={self.census_tract_fips}, year={self.year}, state={self.state})>"
    
    def to_dict(self):
        """Convert model instance to dictionary"""
        return {
            'id': self.id,
            'is_opportunity_zone': self.is_opportunity_zone,
            'census_tract_fips': self.census_tract_fips,
            'county': self.county,
            'state': self.state,
            'year': self.year,
            'inclusive_growth_score': self.inclusive_growth_score,
            'growth': self.growth,
            'inclusion': self.inclusion,
            'place': self.place,
            'place_growth': self.place_growth,
            'place_inclusion': self.place_inclusion,
            'net_occupancy_score': self.net_occupancy_score,
            'net_occupancy_base_pct': self.net_occupancy_base_pct,
            'net_occupancy_tract_pct': self.net_occupancy_tract_pct,
            'residential_real_estate_value_score': self.residential_real_estate_value_score,
            'residential_real_estate_value_base_pct': self.residential_real_estate_value_base_pct,
            'residential_real_estate_value_tract_pct': self.residential_real_estate_value_tract_pct,
            'acres_of_park_land_score': self.acres_of_park_land_score,
            'acres_of_park_land_base_pct': self.acres_of_park_land_base_pct,
            'acres_of_park_land_tract_pct': self.acres_of_park_land_tract_pct,
            'affordable_housing_score': self.affordable_housing_score,
            'affordable_housing_base_pct': self.affordable_housing_base_pct,
            'affordable_housing_tract_pct': self.affordable_housing_tract_pct,
            'internet_access_score': self.internet_access_score,
            'internet_access_base_pct': self.internet_access_base_pct,
            'internet_access_tract_pct': self.internet_access_tract_pct,
            'travel_time_to_work_score': self.travel_time_to_work_score,
            'travel_time_to_work_base_pct': self.travel_time_to_work_base_pct,
            'travel_time_to_work_tract_pct': self.travel_time_to_work_tract_pct,
            'economy': self.economy,
            'economy_growth': self.economy_growth,
            'economy_inclusion': self.economy_inclusion,
            'new_businesses_score': self.new_businesses_score,
            'new_businesses_base_pct': self.new_businesses_base_pct,
            'new_businesses_tract_pct': self.new_businesses_tract_pct,
            'spend_growth_score': self.spend_growth_score,
            'spend_growth_base_pct': self.spend_growth_base_pct,
            'spend_growth_tract_pct': self.spend_growth_tract_pct,
            'small_business_loans_score': self.small_business_loans_score,
            'small_business_loans_base_pct': self.small_business_loans_base_pct,
            'small_business_loans_tract_pct': self.small_business_loans_tract_pct,
            'minority_women_owned_businesses_score': self.minority_women_owned_businesses_score,
            'minority_women_owned_businesses_base_pct': self.minority_women_owned_businesses_base_pct,
            'minority_women_owned_businesses_tract_pct': self.minority_women_owned_businesses_tract_pct,
            'labor_market_engagement_index_score': self.labor_market_engagement_index_score,
            'labor_market_engagement_index_base': self.labor_market_engagement_index_base,
            'labor_market_engagement_index_tract': self.labor_market_engagement_index_tract,
            'commercial_diversity_score': self.commercial_diversity_score,
            'commercial_diversity_base_pct': self.commercial_diversity_base_pct,
            'commercial_diversity_tract_pct': self.commercial_diversity_tract_pct,
            'community': self.community,
            'community_growth': self.community_growth,
            'community_inclusion': self.community_inclusion,
            'personal_income_score': self.personal_income_score,
            'personal_income_base_pct': self.personal_income_base_pct,
            'personal_income_tract_pct': self.personal_income_tract_pct,
            'spending_per_capita_score': self.spending_per_capita_score,
            'spending_per_capita_base_pct': self.spending_per_capita_base_pct,
            'spending_per_capita_tract_pct': self.spending_per_capita_tract_pct,
            'female_above_poverty_score': self.female_above_poverty_score,
            'female_above_poverty_base_pct': self.female_above_poverty_base_pct,
            'female_above_poverty_tract_pct': self.female_above_poverty_tract_pct,
            'gini_coefficient_score': self.gini_coefficient_score,
            'gini_coefficient_base': self.gini_coefficient_base,
            'gini_coefficient_tract': self.gini_coefficient_tract,
            'early_education_enrollment_score': self.early_education_enrollment_score,
            'early_education_enrollment_base_pct': self.early_education_enrollment_base_pct,
            'early_education_enrollment_tract_pct': self.early_education_enrollment_tract_pct,
            'health_insurance_coverage_score': self.health_insurance_coverage_score,
            'health_insurance_coverage_base_pct': self.health_insurance_coverage_base_pct,
            'health_insurance_coverage_tract_pct': self.health_insurance_coverage_tract_pct,
        }


