"""
FastAPI Main Application
CIS 301 Capstone Project - Clark Atlanta CIS301

Main entry point for the IGS Data API
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys
from pathlib import Path

# Add backend directory to path
backend_path = Path(__file__).parent
sys.path.insert(0, str(backend_path))

from config import API_TITLE, API_DESCRIPTION, API_VERSION, CORS_ORIGINS
from routes.tracts import router as tracts_router
from routes.insights import router as insights_router
from database.connection import init_db

# Create FastAPI application
app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(tracts_router)
app.include_router(insights_router)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    init_db()
    print("[INFO] Database initialized")
    print(f"[INFO] API running at http://localhost:8000")
    print(f"[INFO] API documentation at http://localhost:8000/docs")


@app.on_event("shutdown")
async def shutdown_event():
    """Clean up on shutdown"""
    print("[INFO] Shutting down API")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "IGS Data API",
        "version": API_VERSION,
        "documentation": "/docs",
        "health_check": "/api/health"
    }


if __name__ == "__main__":
    import uvicorn
    from config import HOST, PORT, RELOAD
    
    uvicorn.run(
        "main:app",
        host=HOST,
        port=PORT,
        reload=RELOAD
    )


