"""
ETL Pipeline Orchestrator for Mastercard IGS Dataset
CIS 301 Capstone Project - Clark Atlanta CIS301

Orchestrates the complete ETL process:
1. Clean raw CSV data
2. Load cleaned data into SQLite database
3. Validate data integrity
"""

import sys
from pathlib import Path
import logging
from datetime import datetime

# Add backend directory to path
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

from etl.data_cleaning import IGSDataCleaner
from etl.load_database import IGSDatabaseLoader
from database.schema import Base, CensusTract
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ETLPipeline:
    """Orchestrates the complete ETL pipeline"""
    
    def __init__(
        self,
        raw_data_path: str = "data/raw/IGS-score.csv",
        processed_data_path: str = "data/processed/IGS-score-cleaned.csv",
        database_path: str = "data/igs_data.db"
    ):
        """
        Initialize the ETL pipeline
        
        Args:
            raw_data_path: Path to raw CSV file
            processed_data_path: Path to save cleaned CSV file
            database_path: Path to SQLite database file
        """
        self.raw_data_path = raw_data_path
        self.processed_data_path = processed_data_path
        self.database_path = database_path
        
        self.cleaner = None
        self.loader = None
        self.stats = {
            'start_time': None,
            'end_time': None,
            'records_cleaned': 0,
            'records_loaded': 0,
            'status': 'pending'
        }
    
    def run_cleaning(self) -> bool:
        """
        Run data cleaning step
        
        Returns:
            True if successful, False otherwise
        """
        logger.info("=" * 60)
        logger.info("STEP 1: DATA CLEANING")
        logger.info("=" * 60)
        
        try:
            self.cleaner = IGSDataCleaner(self.raw_data_path, self.processed_data_path)
            cleaned_df = self.cleaner.clean()
            self.stats['records_cleaned'] = len(cleaned_df)
            logger.info(f"Data cleaning successful - {self.stats['records_cleaned']} records")
            return True
        except Exception as e:
            logger.error(f"Data cleaning failed: {str(e)}")
            self.stats['status'] = 'failed_cleaning'
            return False
    
    def run_loading(self) -> bool:
        """
        Run database loading step
        
        Returns:
            True if successful, False otherwise
        """
        logger.info("=" * 60)
        logger.info("STEP 2: DATABASE LOADING")
        logger.info("=" * 60)
        
        try:
            self.loader = IGSDatabaseLoader(self.processed_data_path, self.database_path)
            records_count = self.loader.load()
            self.stats['records_loaded'] = records_count
            logger.info(f"Database loading successful - {self.stats['records_loaded']} records")
            return True
        except Exception as e:
            logger.error(f"Database loading failed: {str(e)}")
            self.stats['status'] = 'failed_loading'
            return False
    
    def validate_pipeline(self) -> bool:
        """
        Validate the complete ETL pipeline
        
        Returns:
            True if validation passes, False otherwise
        """
        logger.info("=" * 60)
        logger.info("STEP 3: VALIDATION")
        logger.info("=" * 60)
        
        try:
            # Connect to database
            engine = create_engine(f'sqlite:///{self.database_path}')
            Session = sessionmaker(bind=engine)
            session = Session()
            
            # Check record count
            db_count = session.query(CensusTract).count()
            logger.info(f"Database contains {db_count} records")
            
            # Check for required states
            states = session.query(CensusTract.state).distinct().all()
            state_list = [s[0] for s in states]
            logger.info(f"States in database: {', '.join(state_list)}")
            
            # Check year range
            min_year = session.query(CensusTract.year).filter(CensusTract.year.isnot(None)).order_by(CensusTract.year).first()
            max_year = session.query(CensusTract.year).filter(CensusTract.year.isnot(None)).order_by(CensusTract.year.desc()).first()
            
            if min_year and max_year:
                logger.info(f"Year range: {min_year[0]} - {max_year[0]}")
            
            # Verify data matches
            if db_count != self.stats['records_cleaned']:
                logger.warning(f"Record count mismatch: cleaned={self.stats['records_cleaned']}, loaded={db_count}")
            else:
                logger.info("Record counts match - validation successful")
            
            session.close()
            return True
            
        except Exception as e:
            logger.error(f"Validation failed: {str(e)}")
            self.stats['status'] = 'failed_validation'
            return False
    
    def run(self) -> bool:
        """
        Execute complete ETL pipeline
        
        Returns:
            True if successful, False otherwise
        """
        self.stats['start_time'] = datetime.now()
        
        logger.info("\n" + "=" * 60)
        logger.info("STARTING ETL PIPELINE")
        logger.info("=" * 60)
        logger.info(f"Raw Data: {self.raw_data_path}")
        logger.info(f"Processed Data: {self.processed_data_path}")
        logger.info(f"Database: {self.database_path}")
        logger.info("")
        
        # Step 1: Clean data
        if not self.run_cleaning():
            return False
        
        # Step 2: Load into database
        if not self.run_loading():
            return False
        
        # Step 3: Validate
        if not self.validate_pipeline():
            return False
        
        # Calculate duration
        self.stats['end_time'] = datetime.now()
        duration = (self.stats['end_time'] - self.stats['start_time']).total_seconds()
        self.stats['status'] = 'success'
        
        # Print summary
        logger.info("\n" + "=" * 60)
        logger.info("ETL PIPELINE COMPLETE")
        logger.info("=" * 60)
        logger.info(f"Status: {self.stats['status']}")
        logger.info(f"Records Cleaned: {self.stats['records_cleaned']}")
        logger.info(f"Records Loaded: {self.stats['records_loaded']}")
        logger.info(f"Duration: {duration:.2f} seconds")
        logger.info("=" * 60)
        
        return True
    
    def get_stats(self) -> dict:
        """Get pipeline statistics"""
        return self.stats


def main():
    """Main execution function"""
    print("\n" + "=" * 60)
    print("IGS DATA ETL PIPELINE")
    print("CIS 301 Capstone Project - Clark Atlanta CIS301")
    print("=" * 60 + "\n")
    
    # Create and run pipeline
    pipeline = ETLPipeline()
    
    try:
        success = pipeline.run()
        
        if success:
            print("\n[SUCCESS] ETL Pipeline completed successfully!")
            print(f"  - Records processed: {pipeline.stats['records_cleaned']}")
            print(f"  - Database: data/igs_data.db")
            return 0
        else:
            print(f"\n[ERROR] ETL Pipeline failed at: {pipeline.stats['status']}")
            return 1
            
    except Exception as e:
        logger.error(f"ETL Pipeline error: {str(e)}")
        print(f"\n[ERROR] ETL Pipeline failed: {str(e)}")
        return 1


if __name__ == "__main__":
    exit(main())


