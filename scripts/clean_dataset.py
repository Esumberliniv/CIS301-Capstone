"""
Data Cleaning Script for Mastercard IGS Dataset
Author: Emery
Course: CIS 301 Capstone
Date: November 19, 2025

This script cleans the raw IGS dataset by:
1. Removing metadata rows (rows 1-3)
2. Setting proper column headers
3. Handling N/A values
4. Type conversions
5. Saving cleaned data to processed/ directory
"""

import pandas as pd
import os

# File paths
RAW_DATA_PATH = os.path.join('data', 'raw', 'IGS-score.csv')
PROCESSED_DATA_PATH = os.path.join('data', 'processed', 'IGS-score-cleaned.csv')

def clean_igs_dataset():
    """Clean the IGS dataset and save to processed directory."""
    
    print("=" * 60)
    print("Mastercard IGS Dataset Cleaning Pipeline")
    print("=" * 60)
    
    # Read the raw CSV, skipping first row (category headers) and row 3 (empty)
    print("\n[1/5] Reading raw dataset...")
    df = pd.read_csv(RAW_DATA_PATH, skiprows=[0, 2])
    print(f"   ✓ Loaded {len(df)} rows and {len(df.columns)} columns")
    
    # Display basic info
    print(f"\n[2/5] Dataset Overview:")
    print(f"   • Years covered: {df['Year'].min()} - {df['Year'].max()}")
    print(f"   • Unique states: {df['State'].nunique()}")
    print(f"   • Unique counties: {df['County'].nunique()}")
    print(f"   • Unique census tracts: {df['Census Tract FIPS code'].nunique()}")
    
    # Handle missing values
    print(f"\n[3/5] Handling missing values...")
    # Replace 'N/A' strings with actual NaN
    df = df.replace('N/A', pd.NA)
    
    missing_counts = df.isna().sum()
    columns_with_missing = missing_counts[missing_counts > 0]
    print(f"   • Found {len(columns_with_missing)} columns with missing values")
    print(f"   • Most missing: {columns_with_missing.nlargest(5).to_dict()}")
    
    # Convert numeric columns
    print(f"\n[4/5] Converting data types...")
    numeric_columns = df.columns[6:]  # All columns from 'Inclusive Growth Score' onward
    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    print(f"   ✓ Converted {len(numeric_columns)} columns to numeric types")
    
    # Remove the first unnamed column if it exists (row index column)
    if 'N/A' in df.columns or df.columns[0].startswith('Unnamed'):
        df = df.iloc[:, 1:]
        print(f"   ✓ Removed index column")
    
    # Save cleaned dataset
    print(f"\n[5/5] Saving cleaned dataset...")
    os.makedirs(os.path.dirname(PROCESSED_DATA_PATH), exist_ok=True)
    df.to_csv(PROCESSED_DATA_PATH, index=False)
    print(f"   ✓ Saved to: {PROCESSED_DATA_PATH}")
    
    # Summary statistics
    print(f"\n" + "=" * 60)
    print(f"CLEANING COMPLETE")
    print(f"=" * 60)
    print(f"Original rows: {len(df) + 3} (including metadata)")
    print(f"Cleaned rows: {len(df)}")
    print(f"Columns: {len(df.columns)}")
    print(f"Output file size: {os.path.getsize(PROCESSED_DATA_PATH) / 1024:.2f} KB")
    print("=" * 60)
    
    return df

if __name__ == "__main__":
    cleaned_df = clean_igs_dataset()
    print("\n✅ Dataset cleaning complete!")

