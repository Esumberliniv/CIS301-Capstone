"""
Backend Server Launcher
CIS 301 Capstone Project - Clark Atlanta CIS301

Starts the FastAPI backend server
"""

import uvicorn
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

if __name__ == "__main__":
    print("=" * 60)
    print("Starting IGS Data API Server")
    print("CIS 301 Capstone Project - Clark Atlanta CIS301")
    print("=" * 60)
    print("\n[INFO] Server starting...")
    print("[INFO] API will be available at: http://localhost:8000")
    print("[INFO] API documentation at: http://localhost:8000/docs")
    print("[INFO] Press CTRL+C to stop the server\n")
    
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )


