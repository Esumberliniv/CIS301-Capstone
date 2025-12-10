"""
Google Cloud Storage Backup Script
CIS 301 Capstone Project - Clark Atlanta CIS301

Run this script to backup your IGS data to Google Cloud Storage
"""

import sys
from pathlib import Path

# Add src to path (parent directory since we're now in cloud/)
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from backend.cloud.gcs_manager import backup_data_to_gcs

# Configuration
BUCKET_NAME = "igs-data-backup-ccis301"  # Your GCS bucket name
CREDENTIALS_PATH = "credentials/gcs-key.json"  # Path to your service account JSON key

def main():
    print("=" * 60)
    print("GCS BACKUP SCRIPT")
    print("CIS 301 Capstone - Clark Atlanta CIS301")
    print("=" * 60)
    print(f"\nBucket: {BUCKET_NAME}")
    print(f"Credentials: {CREDENTIALS_PATH}")
    print("\nStarting backup...")
    print("-" * 60)
    
    # Check if credentials file exists
    cred_path = Path(__file__).parent.parent / CREDENTIALS_PATH
    if not cred_path.exists():
        print(f"\n[ERROR] Credentials file not found: {CREDENTIALS_PATH}")
        print("\nPlease:")
        print("1. Download your service account JSON key from Google Cloud")
        print(f"2. Save it as: {CREDENTIALS_PATH}")
        print("3. Run this script again")
        return 1
    
    # Run backup
    success = backup_data_to_gcs(BUCKET_NAME, str(cred_path))
    
    if success:
        print("\n" + "=" * 60)
        print("[SUCCESS] Backup completed!")
        print("=" * 60)
        print("\nYour data has been backed up to:")
        print(f"  gs://{BUCKET_NAME}/backup/")
        print("\nBacked up files:")
        print("  - Raw data: backup/raw/")
        print("  - Processed data: backup/processed/")
        print("  - Database: backup/igs_data.db")
        return 0
    else:
        print("\n" + "=" * 60)
        print("[ERROR] Backup failed!")
        print("=" * 60)
        print("\nPlease check:")
        print("1. Your credentials are valid")
        print("2. The bucket name is correct")
        print("3. You have write permissions to the bucket")
        return 1


if __name__ == "__main__":
    exit(main())

