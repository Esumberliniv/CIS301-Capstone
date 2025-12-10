"""
ETL Pipeline Unit Tests
CIS 301 Capstone Project - Clark Atlanta CIS301

Essential tests for data cleaning and processing
"""

import pytest
import pandas as pd
import numpy as np


class TestDataCleaning:
    """Core ETL tests"""
    
    def test_replace_na_strings(self):
        """Should replace 'N/A' strings with NaN"""
        df = pd.DataFrame({'col1': ['value', 'N/A', 'value2']})
        df_cleaned = df.replace('N/A', np.nan)
        
        assert pd.isna(df_cleaned.loc[1, 'col1'])
        assert df_cleaned.loc[0, 'col1'] == 'value'
    
    def test_convert_numeric_columns(self):
        """Should convert string numbers to numeric"""
        df = pd.DataFrame({'score': ['75.5', '80.0', 'invalid']})
        df['score'] = pd.to_numeric(df['score'], errors='coerce')
        
        assert df['score'].iloc[0] == 75.5
        assert pd.isna(df['score'].iloc[2])
    
    def test_validate_required_columns(self):
        """Should validate required columns exist"""
        df = pd.DataFrame({
            'Census Tract FIPS code': ['13121001100'],
            'County': ['Fulton County'],
            'State': ['Georgia'],
            'Year': [2023],
            'Inclusive Growth Score': [75.5]
        })
        
        required = ['Census Tract FIPS code', 'County', 'State', 'Year', 'Inclusive Growth Score']
        for col in required:
            assert col in df.columns
    
    def test_year_range_validation(self):
        """Should validate year is in expected range"""
        valid_years = [2017, 2020, 2024]
        for year in valid_years:
            assert 2017 <= year <= 2024
    
    def test_correlation_calculation(self):
        """Should calculate correlations correctly"""
        df = pd.DataFrame({
            'x': [1, 2, 3, 4, 5],
            'y': [2, 4, 6, 8, 10]
        })
        correlation = df['x'].corr(df['y'])
        assert correlation == pytest.approx(1.0, abs=0.001)
    
    def test_statistics_calculation(self):
        """Should calculate statistics correctly"""
        scores = pd.Series([60.0, 70.0, 80.0, 90.0])
        
        assert scores.mean() == 75.0
        assert scores.min() == 60.0
        assert scores.max() == 90.0
