"""
Data Cleaning Module for Mastercard IGS Dataset
CIS 301 Capstone Project - Clark Atlanta CIS301

This module handles cleaning and preprocessing of the raw IGS CSV data:
- Removes metadata rows (1-3)
- Standardizes "N/A" values to proper nulls
- Converts score columns to numeric types
- Exports cleaned data for database loading
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class IGSDataCleaner:
    """Handles cleaning and preprocessing of IGS dataset"""
    
    def __init__(self, raw_data_path: str, processed_data_path: str):
        """
        Initialize the data cleaner
        
        Args:
            raw_data_path: Path to raw CSV file
            processed_data_path: Path to save cleaned CSV file
        """
        self.raw_data_path = Path(raw_data_path)
        self.processed_data_path = Path(processed_data_path)
        self.df = None
        
    def load_raw_data(self) -> pd.DataFrame:
        """
        Load raw CSV file, skipping metadata rows
        
        Returns:
            DataFrame with raw data
        """
        logger.info(f"Loading raw data from {self.raw_data_path}")
        
        # Skip first row (category headers), use second row as column names, skip third row (empty)
        self.df = pd.read_csv(
            self.raw_data_path,
            skiprows=[0, 2],  # Skip row 0 (categories) and row 2 (empty)
            header=0  # Use row 1 as header (becomes row 0 after skipping)
        )
        
        # Remove the first column which is just an index or N/A column
        if self.df.columns[0] in ['Unnamed: 0', '0', 'N/A'] or str(self.df.columns[0]).isdigit():
            self.df = self.df.drop(self.df.columns[0], axis=1)
            logger.info("Removed index/N/A column")
        
        logger.info(f"Loaded {len(self.df)} records with {len(self.df.columns)} columns")
        return self.df
    
    def handle_missing_values(self) -> pd.DataFrame:
        """
        Standardize missing values - convert 'N/A' strings to NaN
        
        Returns:
            DataFrame with standardized missing values
        """
        logger.info("Standardizing missing values")
        
        # Replace 'N/A' strings with numpy NaN
        self.df = self.df.replace('N/A', np.nan)
        
        # Count missing values per column
        missing_counts = self.df.isnull().sum()
        columns_with_missing = missing_counts[missing_counts > 0]
        
        if len(columns_with_missing) > 0:
            logger.info(f"Found missing values in {len(columns_with_missing)} columns")
            logger.debug(f"Columns with missing values:\n{columns_with_missing}")
        else:
            logger.info("No missing values found")
        
        return self.df
    
    def convert_data_types(self) -> pd.DataFrame:
        """
        Convert columns to appropriate data types
        
        Returns:
            DataFrame with proper data types
        """
        logger.info("Converting data types")
        
        # Define columns that should remain as strings
        string_columns = [
            'Is an Opportunity Zone',
            'Census Tract FIPS code',
            'County',
            'State'
        ]
        
        # Year should be integer
        if 'Year' in self.df.columns:
            self.df['Year'] = pd.to_numeric(self.df['Year'], errors='coerce').astype('Int64')
        
        # Convert all score and percentage columns to numeric (float)
        for col in self.df.columns:
            if col not in string_columns and col != 'Year':
                # Try to convert to numeric, keeping NaN for non-convertible values
                self.df[col] = pd.to_numeric(self.df[col], errors='coerce')
        
        logger.info("Data type conversion complete")
        return self.df
    
    def validate_data(self) -> bool:
        """
        Validate cleaned data for integrity
        
        Returns:
            True if validation passes, False otherwise
        """
        logger.info("Validating cleaned data")
        
        validation_passed = True
        
        # Check required columns exist
        required_columns = [
            'Census Tract FIPS code',
            'County',
            'State',
            'Year',
            'Inclusive Growth Score'
        ]
        
        for col in required_columns:
            if col not in self.df.columns:
                logger.error(f"Required column missing: {col}")
                validation_passed = False
        
        # Check Year range
        if 'Year' in self.df.columns:
            years = self.df['Year'].dropna()
            if len(years) > 0:
                year_min, year_max = years.min(), years.max()
                if year_min < 2017 or year_max > 2024:
                    logger.warning(f"Year range {year_min}-{year_max} outside expected 2017-2024")
        
        # Check for duplicate records (same FIPS code and year)
        if 'Census Tract FIPS code' in self.df.columns and 'Year' in self.df.columns:
            duplicates = self.df.duplicated(subset=['Census Tract FIPS code', 'Year'], keep=False)
            duplicate_count = duplicates.sum()
            if duplicate_count > 0:
                logger.warning(f"Found {duplicate_count} duplicate records")
        
        # Check if we have data
        if len(self.df) == 0:
            logger.error("No data records found")
            validation_passed = False
        
        if validation_passed:
            logger.info("Data validation passed")
        else:
            logger.error("Data validation failed")
        
        return validation_passed
    
    def save_cleaned_data(self) -> None:
        """Save cleaned data to processed directory"""
        logger.info(f"Saving cleaned data to {self.processed_data_path}")
        
        # Ensure processed directory exists
        self.processed_data_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Save to CSV with empty string for NA values to avoid multiple consecutive commas
        self.df.to_csv(self.processed_data_path, index=False, na_rep='')
        
        logger.info(f"Successfully saved {len(self.df)} records to {self.processed_data_path}")
    
    def clean(self) -> pd.DataFrame:
        """
        Execute complete cleaning pipeline
        
        Returns:
            Cleaned DataFrame
        """
        logger.info("Starting data cleaning pipeline")
        
        # Step 1: Load raw data
        self.load_raw_data()
        
        # Step 2: Handle missing values
        self.handle_missing_values()
        
        # Step 3: Convert data types
        self.convert_data_types()
        
        # Step 4: Validate data
        if not self.validate_data():
            logger.error("Data validation failed - check logs for details")
            raise ValueError("Data validation failed")
        
        # Step 5: Save cleaned data
        self.save_cleaned_data()
        
        logger.info("Data cleaning pipeline complete")
        return self.df


def main():
    """Main execution function"""
    # Define paths
    raw_data_path = "data/raw/IGS-score.csv"
    processed_data_path = "data/processed/IGS-score-cleaned.csv"
    
    # Create cleaner instance
    cleaner = IGSDataCleaner(raw_data_path, processed_data_path)
    
    # Run cleaning pipeline
    try:
        cleaned_df = cleaner.clean()
        print(f"\n[SUCCESS] Data cleaning successful!")
        print(f"  - Records: {len(cleaned_df)}")
        print(f"  - Columns: {len(cleaned_df.columns)}")
        print(f"  - Output: {processed_data_path}")
        return 0
    except Exception as e:
        logger.error(f"Data cleaning failed: {str(e)}")
        print(f"\n[ERROR] Data cleaning failed: {str(e)}")
        return 1


if __name__ == "__main__":
    exit(main())

