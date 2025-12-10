# Google Cloud Storage Setup Guide

**CIS 301 Capstone Project - Clark Atlanta CIS301**

---

## 📋 **Prerequisites**

- Google Cloud account (free tier available)
- Credit card (required for GCP, but free tier covers this project)
- Project administrator access

---

## 🚀 **Step-by-Step Setup**

### **Step 1: Create Google Cloud Project**

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Select a project" → "New Project"
3. **Project Name:** `igs-data-project`
4. Click "Create"

### **Step 2: Enable Cloud Storage API**

1. In the left menu: **APIs & Services** → **Library**
2. Search for "Cloud Storage API"
3. Click **Enable**

### **Step 3: Create Storage Bucket**

1. In the left menu: **Storage** → **Buckets**
2. Click **Create Bucket**
3. Configure:
   - **Name:** `igs-data-backup-<your-unique-id>` (globally unique)
   - **Location type:** Region
   - **Region:** `us-central1` (or closest to you)
   - **Storage class:** Standard
   - **Access control:** Uniform
   - **Protection tools:** None (for now)
4. Click **Create**

### **Step 4: Create Service Account**

1. Go to **IAM & Admin** → **Service Accounts**
2. Click **Create Service Account**
3. **Service account details:**
   - Name: `igs-data-service`
   - Description: "Service account for IGS data backup"
   - Click **Create and Continue**
4. **Grant permissions:**
   - Role: **Storage Object Admin**
   - Click **Continue** → **Done**

### **Step 5: Generate & Download Credentials**

1. Click on your new service account (`igs-data-service`)
2. Go to **Keys** tab
3. Click **Add Key** → **Create new key**
4. Choose **JSON** format
5. Click **Create** (file downloads automatically)

### **Step 6: Save Credentials to Project**

1. In your project directory, create folder:
   ```bash
   mkdir credentials
   ```

2. Move the downloaded JSON file:
   ```bash
   # Rename and move to: credentials/gcs-key.json
   ```

3. **IMPORTANT:** Verify `.gitignore` excludes credentials:
   ```
   credentials/
   *.json
   gcs-key.json
   ```

---

## 🔧 **Update Configuration**

### Edit `cloud/backup.py` and `cloud/restore.py`:

Replace the bucket name with yours:

```python
BUCKET_NAME = "igs-data-backup-<your-unique-id>"  # Your actual bucket name
```

---

## ✅ **Test Your Setup**

### 1. Verify credentials file exists:
```bash
ls credentials/gcs-key.json
```

### 2. Run test backup (from project root):
```bash
python cloud/backup.py
```

**Expected output:**
```
============================================================
GCS BACKUP SCRIPT
CIS 301 Capstone - Clark Atlanta CIS301
============================================================

Bucket: igs-data-backup-<your-id>
Credentials: credentials/gcs-key.json

Starting backup...
------------------------------------------------------------
[SUCCESS] Backup completed!
```

### 3. Verify in Google Cloud Console:
1. Go to **Storage** → **Buckets**
2. Click your bucket
3. You should see:
   - `backup/raw/` folder
   - `backup/processed/` folder
   - `backup/igs_data.db` file

---

## 📊 **Usage**

### **Backup Data:**
```bash
python cloud/backup.py
```

### **Restore Data:**
```bash
python cloud/restore.py
```

### **Integrate with ETL Pipeline:**
```python
from src.backend.cloud.gcs_manager import GCSManager

# Initialize
gcs = GCSManager("your-bucket-name", "credentials/gcs-key.json")

# Upload file
gcs.upload_file("data/raw/IGS-score.csv", "backup/raw/IGS-score.csv")

# Download file
gcs.download_file("backup/igs_data.db", "data/igs_data.db")

# List files
files = gcs.list_files("backup/")
```

---

## 🔒 **Security Best Practices**

1. **Never commit credentials to GitHub**
   - Already protected by `.gitignore`
   
2. **Limit service account permissions**
   - Only grant "Storage Object Admin" to specific bucket
   
3. **Rotate credentials regularly**
   - Create new key every 90 days
   - Delete old keys

4. **Use environment variables in production:**
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="credentials/gcs-key.json"
   ```

---

## 💰 **Cost Estimation**

**Google Cloud Free Tier includes:**
- 5 GB storage per month
- 5,000 Class A operations (uploads)
- 50,000 Class B operations (downloads)

**Your project usage:**
- IGS data: ~1 MB
- **Cost:** $0.00 per month (well within free tier)

---

## 🆘 **Troubleshooting**

### **Error: "Bucket not found"**
- Check bucket name in `cloud/backup.py`
- Verify bucket exists in Google Cloud Console

### **Error: "Permission denied"**
- Verify service account has "Storage Object Admin" role
- Check credentials file path is correct

### **Error: "File not found: credentials/gcs-key.json"**
- Ensure you downloaded the JSON key
- Move it to `credentials/gcs-key.json`

---

## 📚 **Additional Resources**

- [Google Cloud Storage Documentation](https://cloud.google.com/storage/docs)
- [Python Client Library](https://cloud.google.com/python/docs/reference/storage/latest)
- [Free Tier Details](https://cloud.google.com/free)

---

**Last Updated:** December 2025  
**Project:** IGS Data Visualization - CIS 301 Capstone

