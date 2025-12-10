"""
System Integration Test
CIS 301 Capstone Project - Clark Atlanta CIS301

Tests the complete data flow from ETL to API
"""

import sys
from pathlib import Path
import requests
import time

def print_section(title):
    """Print a formatted section header"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)

def test_etl_pipeline():
    """Test ETL data processing"""
    print_section("Testing ETL Pipeline")
    
    # Check if cleaned data exists
    cleaned_data = Path("data/processed/IGS-score-cleaned.csv")
    if cleaned_data.exists():
        print("[PASS] Cleaned data file exists")
    else:
        print("[FAIL] Cleaned data file not found")
        return False
    
    # Check if database exists
    database = Path("data/igs_data.db")
    if database.exists():
        print("[PASS] Database file exists")
    else:
        print("[FAIL] Database file not found")
        return False
    
    return True

def test_api_endpoints():
    """Test FastAPI endpoints"""
    print_section("Testing API Endpoints")
    
    base_url = "http://localhost:8000"
    
    # Wait for API to be available
    print("Checking if API is running...")
    for i in range(3):
        try:
            response = requests.get(f"{base_url}/")
            break
        except requests.exceptions.ConnectionError:
            if i < 2:
                print(f"  API not responding, waiting... ({i+1}/3)")
                time.sleep(2)
            else:
                print("[FAIL] API is not running. Please start it with: python run_backend.py")
                return False
    
    tests_passed = 0
    tests_total = 7
    
    # Test 1: Health check
    try:
        response = requests.get(f"{base_url}/api/health")
        if response.status_code == 200:
            data = response.json()
            print(f"[PASS] Health check endpoint")
            print(f"  - Status: {data.get('status')}")
            print(f"  - Total records: {data.get('total_records')}")
            print(f"  - States: {', '.join(data.get('states_available', []))}")
            tests_passed += 1
        else:
            print(f"[FAIL] Health check endpoint (status: {response.status_code})")
    except Exception as e:
        print(f"[FAIL] Health check endpoint: {str(e)}")
    
    # Test 2: Get tracts
    try:
        response = requests.get(f"{base_url}/api/tracts?limit=10")
        if response.status_code == 200:
            data = response.json()
            print(f"[PASS] Get tracts endpoint")
            print(f"  - Retrieved: {len(data.get('tracts', []))} tracts")
            tests_passed += 1
        else:
            print(f"[FAIL] Get tracts endpoint (status: {response.status_code})")
    except Exception as e:
        print(f"[FAIL] Get tracts endpoint: {str(e)}")
    
    # Test 3: Get tracts with filters
    try:
        response = requests.get(f"{base_url}/api/tracts?state=Texas&year=2024")
        if response.status_code == 200:
            print(f"[PASS] Get tracts with filters")
            tests_passed += 1
        else:
            print(f"[FAIL] Get tracts with filters")
    except Exception as e:
        print(f"[FAIL] Get tracts with filters: {str(e)}")
    
    # Test 4: Get states
    try:
        response = requests.get(f"{base_url}/api/states")
        if response.status_code == 200:
            states = response.json()
            print(f"[PASS] Get states endpoint")
            print(f"  - States found: {len(states)}")
            tests_passed += 1
        else:
            print(f"[FAIL] Get states endpoint")
    except Exception as e:
        print(f"[FAIL] Get states endpoint: {str(e)}")
    
    # Test 5: Get metrics
    try:
        response = requests.get(f"{base_url}/api/metrics?metric=internet_access_score&limit=5")
        if response.status_code == 200:
            print(f"[PASS] Get metrics endpoint")
            tests_passed += 1
        else:
            print(f"[FAIL] Get metrics endpoint")
    except Exception as e:
        print(f"[FAIL] Get metrics endpoint: {str(e)}")
    
    # Test 6: Get statistics
    try:
        response = requests.get(f"{base_url}/api/statistics?metric=inclusive_growth_score")
        if response.status_code == 200:
            data = response.json()
            print(f"[PASS] Get statistics endpoint")
            print(f"  - Mean: {data.get('mean', 'N/A')}")
            print(f"  - Median: {data.get('median', 'N/A')}")
            tests_passed += 1
        else:
            print(f"[FAIL] Get statistics endpoint")
    except Exception as e:
        print(f"[FAIL] Get statistics endpoint: {str(e)}")
    
    # Test 7: Get correlation
    try:
        response = requests.get(
            f"{base_url}/api/correlations?"
            f"metric_x=internet_access_score&metric_y=small_business_loans_score"
        )
        if response.status_code == 200:
            data = response.json()
            print(f"[PASS] Get correlation endpoint")
            print(f"  - Correlation: {data.get('correlation_coefficient', 'N/A')}")
            print(f"  - Sample size: {data.get('sample_size', 'N/A')}")
            tests_passed += 1
        else:
            print(f"[FAIL] Get correlation endpoint")
    except Exception as e:
        print(f"[FAIL] Get correlation endpoint: {str(e)}")
    
    print(f"\nAPI Tests: {tests_passed}/{tests_total} passed")
    return tests_passed == tests_total

def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("  SYSTEM INTEGRATION TEST")
    print("  CIS 301 Capstone Project - Clark Atlanta CIS301")
    print("=" * 60)
    
    all_passed = True
    
    # Test ETL
    if not test_etl_pipeline():
        all_passed = False
        print("\n[ERROR] ETL tests failed. Run: python src/backend/etl/run_etl.py")
    
    # Test API
    if not test_api_endpoints():
        all_passed = False
        print("\n[ERROR] API tests failed. Make sure backend is running: python run_backend.py")
    
    # Summary
    print_section("Test Summary")
    if all_passed:
        print("\n[SUCCESS] All integration tests passed!")
        print("\nNext steps:")
        print("  1. Start backend: python run_backend.py")
        print("  2. Start frontend: python run_frontend.py")
        print("  3. Open dashboard: http://localhost:8501")
        return 0
    else:
        print("\n[PARTIAL] Some tests failed. See details above.")
        return 1

if __name__ == "__main__":
    exit(main())


