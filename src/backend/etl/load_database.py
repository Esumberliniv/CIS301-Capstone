"""
Database Loader for Mastercard IGS Dataset
CIS 301 Capstone Project - Clark Atlanta CIS301

Loads cleaned CSV data into SQLite database using SQLAlchemy ORM
"""

import pandas as pd
import sys
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import logging

# Add backend directory to path to import database module
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

from database.schema import Base, CensusTract

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class IGSDatabaseLoader:
    """Handles loading cleaned IGS data into SQLite database"""
    
    def __init__(self, cleaned_csv_path: str, database_path: str):
        """
        Initialize the database loader
        
        Args:
            cleaned_csv_path: Path to cleaned CSV file
            database_path: Path to SQLite database file
        """
        self.cleaned_csv_path = Path(cleaned_csv_path)
        self.database_path = Path(database_path)
        self.engine = None
        self.Session = None
        
    def create_database(self) -> None:
        """Create database and tables"""
        logger.info(f"Creating database at {self.database_path}")
        
        # Ensure directory exists
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Create engine
        self.engine = create_engine(f'sqlite:///{self.database_path}')
        
        # Create all tables
        Base.metadata.create_all(self.engine)
        
        # Create session factory
        self.Session = sessionmaker(bind=self.engine)
        
        logger.info("Database and tables created successfully")
    
    def load_csv_data(self) -> pd.DataFrame:
        """Load cleaned CSV data"""
        logger.info(f"Loading cleaned data from {self.cleaned_csv_path}")
        
        df = pd.read_csv(self.cleaned_csv_path)
        
        # Drop the first unnamed column if it exists (index column from cleaning)
        if df.columns[0] in ['Unnamed: 0', 'N/A'] or str(df.columns[0]).startswith('Unnamed'):
            df = df.drop(df.columns[0], axis=1)
            logger.info("Dropped unnamed index column")
        
        logger.info(f"Loaded {len(df)} records from CSV")
        return df
    
    def map_column_names(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Map CSV column names to database column names
        
        Args:
            df: DataFrame with CSV column names
            
        Returns:
            DataFrame with database column names
        """
        # Define column name mapping from CSV to database
        column_mapping = {
            'Is an Opportunity Zone': 'is_opportunity_zone',
            'Census Tract FIPS code': 'census_tract_fips',
            'County': 'county',
            'State': 'state',
            'Year': 'year',
            'Inclusive Growth Score': 'inclusive_growth_score',
            'Growth': 'growth',
            'Inclusion': 'inclusion',
            'Place': 'place',
            'Place Growth': 'place_growth',
            'Place Inclusion': 'place_inclusion',
            'Net Occupancy Score': 'net_occupancy_score',
            'Net Occupancy Base, %': 'net_occupancy_base_pct',
            'Net Occupancy Tract, %': 'net_occupancy_tract_pct',
            'Residential Real Estate Value Score': 'residential_real_estate_value_score',
            'Residential Real Estate Value Base, %': 'residential_real_estate_value_base_pct',
            'Residential Real Estate Value Tract, %': 'residential_real_estate_value_tract_pct',
            'Acres of Park Land Score': 'acres_of_park_land_score',
            'Acres of Park Land Base, %': 'acres_of_park_land_base_pct',
            'Acres of Park Land Tract, %': 'acres_of_park_land_tract_pct',
            'Affordable Housing Score': 'affordable_housing_score',
            'Affordable Housing Base, %': 'affordable_housing_base_pct',
            'Affordable Housing Tract, %': 'affordable_housing_tract_pct',
            'Internet Access Score': 'internet_access_score',
            'Internet Access Base, %': 'internet_access_base_pct',
            'Internet Access Tract, %': 'internet_access_tract_pct',
            'Travel Time to Work Score': 'travel_time_to_work_score',
            'Travel Time to Work Base, %': 'travel_time_to_work_base_pct',
            'Travel Time to Work Tract, %': 'travel_time_to_work_tract_pct',
            'Economy': 'economy',
            'Economy Growth': 'economy_growth',
            'Economy Inclusion': 'economy_inclusion',
            'New Businesses Score': 'new_businesses_score',
            'New Businesses Base, %': 'new_businesses_base_pct',
            'New Businesses Tract, %': 'new_businesses_tract_pct',
            'Spend Growth Score': 'spend_growth_score',
            'Spend Growth Base, %': 'spend_growth_base_pct',
            'Spend Growth Tract, %': 'spend_growth_tract_pct',
            'Small Business Loans Score': 'small_business_loans_score',
            'Small Business Loans Base, %': 'small_business_loans_base_pct',
            'Small Business Loans Tract, %': 'small_business_loans_tract_pct',
            'Minority/Women Owned Businesses Score': 'minority_women_owned_businesses_score',
            'Minority/Women Owned Businesses Base, %': 'minority_women_owned_businesses_base_pct',
            'Minority/Women Owned Businesses Tract, %': 'minority_women_owned_businesses_tract_pct',
            'Labor Market Engagement Index Score': 'labor_market_engagement_index_score',
            'Labor Market Engagement Index Base': 'labor_market_engagement_index_base',
            'Labor Market Engagement Index Tract': 'labor_market_engagement_index_tract',
            'Commercial Diversity Score': 'commercial_diversity_score',
            'Commercial Diversity Base, %': 'commercial_diversity_base_pct',
            'Commercial Diversity Tract, %': 'commercial_diversity_tract_pct',
            'Community': 'community',
            'Community Growth': 'community_growth',
            'Community Inclusion': 'community_inclusion',
            'Personal Income Score': 'personal_income_score',
            'Personal Income Base, %': 'personal_income_base_pct',
            'Personal Income Tract, %': 'personal_income_tract_pct',
            'Spending per Capita Score': 'spending_per_capita_score',
            'Spending per Capita Base, %': 'spending_per_capita_base_pct',
            'Spending per Capita Tract, %': 'spending_per_capita_tract_pct',
            'Female Above Poverty Score': 'female_above_poverty_score',
            'Female Above Poverty Base, %': 'female_above_poverty_base_pct',
            'Female Above Poverty Tract, %': 'female_above_poverty_tract_pct',
            'Gini Coefficient Score': 'gini_coefficient_score',
            'Gini Coefficient Base': 'gini_coefficient_base',
            'Gini Coefficient Tract': 'gini_coefficient_tract',
            'Early Education Enrollment Score': 'early_education_enrollment_score',
            'Early Education Enrollment Base, %': 'early_education_enrollment_base_pct',
            'Early Education Enrollment Tract, %': 'early_education_enrollment_tract_pct',
            'Health Insurance Coverage Score': 'health_insurance_coverage_score',
            'Health Insurance Coverage Base, %': 'health_insurance_coverage_base_pct',
            'Health Insurance Coverage Tract, %': 'health_insurance_coverage_tract_pct',
        }
        
        # Rename columns
        df = df.rename(columns=column_mapping)
        
        logger.info("Column names mapped successfully")
        return df
    
    def insert_records(self, df: pd.DataFrame) -> int:
        """
        Insert DataFrame records into database
        
        Args:
            df: DataFrame with database column names
            
        Returns:
            Number of records inserted
        """
        logger.info("Inserting records into database")
        
        session = self.Session()
        records_inserted = 0
        
        try:
            # Convert DataFrame rows to CensusTract objects
            for _, row in df.iterrows():
                # Create tract object
                tract = CensusTract(
                    is_opportunity_zone=row.get('is_opportunity_zone'),
                    census_tract_fips=row.get('census_tract_fips'),
                    county=row.get('county'),
                    state=row.get('state'),
                    year=int(row.get('year')) if pd.notna(row.get('year')) else None,
                    inclusive_growth_score=row.get('inclusive_growth_score'),
                    growth=row.get('growth'),
                    inclusion=row.get('inclusion'),
                    place=row.get('place'),
                    place_growth=row.get('place_growth'),
                    place_inclusion=row.get('place_inclusion'),
                    net_occupancy_score=row.get('net_occupancy_score'),
                    net_occupancy_base_pct=row.get('net_occupancy_base_pct'),
                    net_occupancy_tract_pct=row.get('net_occupancy_tract_pct'),
                    residential_real_estate_value_score=row.get('residential_real_estate_value_score'),
                    residential_real_estate_value_base_pct=row.get('residential_real_estate_value_base_pct'),
                    residential_real_estate_value_tract_pct=row.get('residential_real_estate_value_tract_pct'),
                    acres_of_park_land_score=row.get('acres_of_park_land_score'),
                    acres_of_park_land_base_pct=row.get('acres_of_park_land_base_pct'),
                    acres_of_park_land_tract_pct=row.get('acres_of_park_land_tract_pct'),
                    affordable_housing_score=row.get('affordable_housing_score'),
                    affordable_housing_base_pct=row.get('affordable_housing_base_pct'),
                    affordable_housing_tract_pct=row.get('affordable_housing_tract_pct'),
                    internet_access_score=row.get('internet_access_score'),
                    internet_access_base_pct=row.get('internet_access_base_pct'),
                    internet_access_tract_pct=row.get('internet_access_tract_pct'),
                    travel_time_to_work_score=row.get('travel_time_to_work_score'),
                    travel_time_to_work_base_pct=row.get('travel_time_to_work_base_pct'),
                    travel_time_to_work_tract_pct=row.get('travel_time_to_work_tract_pct'),
                    economy=row.get('economy'),
                    economy_growth=row.get('economy_growth'),
                    economy_inclusion=row.get('economy_inclusion'),
                    new_businesses_score=row.get('new_businesses_score'),
                    new_businesses_base_pct=row.get('new_businesses_base_pct'),
                    new_businesses_tract_pct=row.get('new_businesses_tract_pct'),
                    spend_growth_score=row.get('spend_growth_score'),
                    spend_growth_base_pct=row.get('spend_growth_base_pct'),
                    spend_growth_tract_pct=row.get('spend_growth_tract_pct'),
                    small_business_loans_score=row.get('small_business_loans_score'),
                    small_business_loans_base_pct=row.get('small_business_loans_base_pct'),
                    small_business_loans_tract_pct=row.get('small_business_loans_tract_pct'),
                    minority_women_owned_businesses_score=row.get('minority_women_owned_businesses_score'),
                    minority_women_owned_businesses_base_pct=row.get('minority_women_owned_businesses_base_pct'),
                    minority_women_owned_businesses_tract_pct=row.get('minority_women_owned_businesses_tract_pct'),
                    labor_market_engagement_index_score=row.get('labor_market_engagement_index_score'),
                    labor_market_engagement_index_base=row.get('labor_market_engagement_index_base'),
                    labor_market_engagement_index_tract=row.get('labor_market_engagement_index_tract'),
                    commercial_diversity_score=row.get('commercial_diversity_score'),
                    commercial_diversity_base_pct=row.get('commercial_diversity_base_pct'),
                    commercial_diversity_tract_pct=row.get('commercial_diversity_tract_pct'),
                    community=row.get('community'),
                    community_growth=row.get('community_growth'),
                    community_inclusion=row.get('community_inclusion'),
                    personal_income_score=row.get('personal_income_score'),
                    personal_income_base_pct=row.get('personal_income_base_pct'),
                    personal_income_tract_pct=row.get('personal_income_tract_pct'),
                    spending_per_capita_score=row.get('spending_per_capita_score'),
                    spending_per_capita_base_pct=row.get('spending_per_capita_base_pct'),
                    spending_per_capita_tract_pct=row.get('spending_per_capita_tract_pct'),
                    female_above_poverty_score=row.get('female_above_poverty_score'),
                    female_above_poverty_base_pct=row.get('female_above_poverty_base_pct'),
                    female_above_poverty_tract_pct=row.get('female_above_poverty_tract_pct'),
                    gini_coefficient_score=row.get('gini_coefficient_score'),
                    gini_coefficient_base=row.get('gini_coefficient_base'),
                    gini_coefficient_tract=row.get('gini_coefficient_tract'),
                    early_education_enrollment_score=row.get('early_education_enrollment_score'),
                    early_education_enrollment_base_pct=row.get('early_education_enrollment_base_pct'),
                    early_education_enrollment_tract_pct=row.get('early_education_enrollment_tract_pct'),
                    health_insurance_coverage_score=row.get('health_insurance_coverage_score'),
                    health_insurance_coverage_base_pct=row.get('health_insurance_coverage_base_pct'),
                    health_insurance_coverage_tract_pct=row.get('health_insurance_coverage_tract_pct'),
                )
                
                session.add(tract)
                records_inserted += 1
            
            # Commit all records
            session.commit()
            logger.info(f"Successfully inserted {records_inserted} records")
            
        except Exception as e:
            session.rollback()
            logger.error(f"Error inserting records: {str(e)}")
            raise
        finally:
            session.close()
        
        return records_inserted
    
    def load(self) -> int:
        """
        Execute complete database loading pipeline
        
        Returns:
            Number of records loaded
        """
        logger.info("Starting database loading pipeline")
        
        # Step 1: Create database
        self.create_database()
        
        # Step 2: Load CSV data
        df = self.load_csv_data()
        
        # Step 3: Map column names
        df = self.map_column_names(df)
        
        # Step 4: Insert records
        records_count = self.insert_records(df)
        
        logger.info("Database loading pipeline complete")
        return records_count


def main():
    """Main execution function"""
    # Define paths
    cleaned_csv_path = "data/processed/IGS-score-cleaned.csv"
    database_path = "data/igs_data.db"
    
    # Create loader instance
    loader = IGSDatabaseLoader(cleaned_csv_path, database_path)
    
    # Run loading pipeline
    try:
        records_count = loader.load()
        print(f"\n[SUCCESS] Database loading successful!")
        print(f"  - Records inserted: {records_count}")
        print(f"  - Database location: {database_path}")
        return 0
    except Exception as e:
        logger.error(f"Database loading failed: {str(e)}")
        print(f"\n[ERROR] Database loading failed: {str(e)}")
        return 1


if __name__ == "__main__":
    exit(main())

