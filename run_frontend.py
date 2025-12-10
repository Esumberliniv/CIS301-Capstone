"""
Frontend Dashboard Launcher
CIS 301 Capstone Project - Clark Atlanta CIS301

Starts the Streamlit dashboard
"""

import subprocess
import sys
from pathlib import Path

if __name__ == "__main__":
    print("=" * 60)
    print("Starting IGS Data Dashboard")
    print("CIS 301 Capstone Project - Clark Atlanta CIS301")
    print("=" * 60)
    print("\n[INFO] Dashboard starting...")
    print("[INFO] Dashboard will be available at: http://localhost:8501")
    print("[INFO] Press CTRL+C to stop the dashboard\n")
    
    # Path to the main app
    app_path = Path(__file__).parent / "src" / "frontend" / "app.py"
    
    # Run Streamlit
    subprocess.run([
        sys.executable,
        "-m",
        "streamlit",
        "run",
        str(app_path),
        "--server.port=8501",
        "--server.address=localhost"
    ])


