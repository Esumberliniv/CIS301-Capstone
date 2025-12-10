"""
Google Cloud Storage Restore Script
CIS 301 Capstone Project - Clark Atlanta CIS301

Run this script to restore your IGS data from Google Cloud Storage
"""

import sys
from pathlib import Path

# Add src to path (parent directory since we're now in cloud/)
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from backend.cloud.gcs_manager import restore_data_from_gcs

# Configuration
BUCKET_NAME = "igs-data-backup-ccis301"  # Your GCS bucket name
CREDENTIALS_PATH = "credentials/gcs-key.json"  # Path to your service account JSON key

def main():
    print("=" * 60)
    print("GCS RESTORE SCRIPT")
    print("CIS 301 Capstone - Clark Atlanta CIS301")
    print("=" * 60)
    print(f"\nBucket: {BUCKET_NAME}")
    print(f"Credentials: {CREDENTIALS_PATH}")
    
    # Confirm restore
    print("\n[WARNING] This will overwrite local data files!")
    response = input("Are you sure you want to restore? (yes/no): ")
    
    if response.lower() != 'yes':
        print("\nRestore cancelled.")
        return 0
    
    print("\nStarting restore...")
    print("-" * 60)
    
    # Check if credentials file exists
    cred_path = Path(__file__).parent.parent / CREDENTIALS_PATH
    if not cred_path.exists():
        print(f"\n[ERROR] Credentials file not found: {CREDENTIALS_PATH}")
        return 1
    
    # Run restore
    success = restore_data_from_gcs(BUCKET_NAME, str(cred_path))
    
    if success:
        print("\n" + "=" * 60)
        print("[SUCCESS] Restore completed!")
        print("=" * 60)
        return 0
    else:
        print("\n" + "=" * 60)
        print("[ERROR] Restore failed!")
        print("=" * 60)
        return 1


if __name__ == "__main__":
    exit(main())

