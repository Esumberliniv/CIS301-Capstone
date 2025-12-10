"""
Google Cloud Storage Manager
CIS 301 Capstone Project - Clark Atlanta CIS301

Handles backup and storage of IGS data to Google Cloud Storage
"""

import os
from pathlib import Path
from google.cloud import storage
from google.oauth2 import service_account
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GCSManager:
    """Manages interactions with Google Cloud Storage"""
    
    def __init__(self, bucket_name: str, credentials_path: str = None):
        """
        Initialize GCS Manager
        
        Args:
            bucket_name: Name of your GCS bucket
            credentials_path: Path to service account JSON key file
        """
        self.bucket_name = bucket_name
        
        # Set up credentials
        if credentials_path:
            credentials = service_account.Credentials.from_service_account_file(
                credentials_path
            )
            self.client = storage.Client(credentials=credentials)
        else:
            # Uses GOOGLE_APPLICATION_CREDENTIALS environment variable
            self.client = storage.Client()
        
        self.bucket = self.client.bucket(bucket_name)
        logger.info(f"Connected to GCS bucket: {bucket_name}")
    
    def upload_file(self, local_file_path: str, gcs_file_path: str = None) -> str:
        """
        Upload a file to GCS
        
        Args:
            local_file_path: Path to local file
            gcs_file_path: Destination path in GCS (optional, uses local filename if not provided)
            
        Returns:
            GCS path of uploaded file
        """
        local_path = Path(local_file_path)
        
        if not local_path.exists():
            raise FileNotFoundError(f"File not found: {local_file_path}")
        
        # Use local filename if GCS path not specified
        if gcs_file_path is None:
            gcs_file_path = local_path.name
        
        blob = self.bucket.blob(gcs_file_path)
        blob.upload_from_filename(str(local_path))
        
        logger.info(f"Uploaded {local_file_path} to gs://{self.bucket_name}/{gcs_file_path}")
        return f"gs://{self.bucket_name}/{gcs_file_path}"
    
    def download_file(self, gcs_file_path: str, local_file_path: str) -> str:
        """
        Download a file from GCS
        
        Args:
            gcs_file_path: Path to file in GCS
            local_file_path: Destination path for downloaded file
            
        Returns:
            Local path of downloaded file
        """
        local_path = Path(local_file_path)
        local_path.parent.mkdir(parents=True, exist_ok=True)
        
        blob = self.bucket.blob(gcs_file_path)
        blob.download_to_filename(str(local_path))
        
        logger.info(f"Downloaded gs://{self.bucket_name}/{gcs_file_path} to {local_file_path}")
        return str(local_path)
    
    def upload_directory(self, local_dir: str, gcs_prefix: str = "") -> list:
        """
        Upload all files in a directory to GCS
        
        Args:
            local_dir: Path to local directory
            gcs_prefix: Prefix for GCS paths (like a folder)
            
        Returns:
            List of uploaded file paths
        """
        local_path = Path(local_dir)
        uploaded_files = []
        
        for file_path in local_path.rglob('*'):
            if file_path.is_file():
                # Create relative path for GCS
                relative_path = file_path.relative_to(local_path)
                gcs_path = f"{gcs_prefix}/{relative_path}" if gcs_prefix else str(relative_path)
                
                # Upload file
                gcs_url = self.upload_file(str(file_path), gcs_path)
                uploaded_files.append(gcs_url)
        
        logger.info(f"Uploaded {len(uploaded_files)} files from {local_dir}")
        return uploaded_files
    
    def list_files(self, prefix: str = "") -> list:
        """
        List files in GCS bucket
        
        Args:
            prefix: Filter files by prefix
            
        Returns:
            List of file names
        """
        blobs = self.client.list_blobs(self.bucket_name, prefix=prefix)
        files = [blob.name for blob in blobs]
        
        logger.info(f"Found {len(files)} files with prefix '{prefix}'")
        return files
    
    def delete_file(self, gcs_file_path: str) -> None:
        """
        Delete a file from GCS
        
        Args:
            gcs_file_path: Path to file in GCS
        """
        blob = self.bucket.blob(gcs_file_path)
        blob.delete()
        
        logger.info(f"Deleted gs://{self.bucket_name}/{gcs_file_path}")
    
    def file_exists(self, gcs_file_path: str) -> bool:
        """
        Check if a file exists in GCS
        
        Args:
            gcs_file_path: Path to file in GCS
            
        Returns:
            True if file exists, False otherwise
        """
        blob = self.bucket.blob(gcs_file_path)
        return blob.exists()


def backup_data_to_gcs(bucket_name: str, credentials_path: str = None):
    """
    Backup all IGS data files to Google Cloud Storage
    
    Args:
        bucket_name: GCS bucket name
        credentials_path: Path to service account JSON key
    """
    try:
        gcs = GCSManager(bucket_name, credentials_path)
        
        # Backup raw data
        logger.info("Backing up raw data...")
        gcs.upload_directory("data/raw", "backup/raw")
        
        # Backup processed data
        logger.info("Backing up processed data...")
        gcs.upload_directory("data/processed", "backup/processed")
        
        # Backup database
        logger.info("Backing up database...")
        if Path("data/igs_data.db").exists():
            gcs.upload_file("data/igs_data.db", "backup/igs_data.db")
        
        logger.info("✓ Backup completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"Backup failed: {str(e)}")
        return False


def restore_data_from_gcs(bucket_name: str, credentials_path: str = None):
    """
    Restore IGS data files from Google Cloud Storage
    
    Args:
        bucket_name: GCS bucket name
        credentials_path: Path to service account JSON key
    """
    try:
        gcs = GCSManager(bucket_name, credentials_path)
        
        # List available backups
        files = gcs.list_files("backup/")
        logger.info(f"Found {len(files)} backup files")
        
        # Download database
        if gcs.file_exists("backup/igs_data.db"):
            logger.info("Restoring database...")
            gcs.download_file("backup/igs_data.db", "data/igs_data.db")
        
        logger.info("✓ Restore completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"Restore failed: {str(e)}")
        return False


