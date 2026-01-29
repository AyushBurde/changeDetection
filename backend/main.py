"""
Main FastAPI application for Change Detection System
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from loguru import logger
import os

# Import database configuration - Fixed import path
try:
    from config.database import check_db_connection, test_postgis, init_db
    logger.info("✅ Database configuration imported successfully")
except ImportError as e:
    logger.error(f"❌ Failed to import database configuration: {e}")
    # Fallback functions if import fails
    def check_db_connection():
        logger.error("Database configuration not available")
        return False
    
    def test_postgis():
        logger.error("Database configuration not available")
        return False
    
    def init_db():
        logger.error("Database configuration not available")
        raise Exception("Database configuration not available")

# Import routers
from api.aoi import router as aoi_router

app = FastAPI(
    title="Change Detection & Monitoring System",
    description="Robust change detection using multi-temporal satellite imagery",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    try:
        db_status = check_db_connection()
        postgis_status = test_postgis() if db_status else False
        
        return {
            "status": "healthy" if db_status else "degraded",
            "service": "Change Detection System",
            "version": "1.0.0",
            "database": {
                "status": "connected" if db_status else "disconnected",
                "postgis": "available" if postgis_status else "unavailable"
            }
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "error",
            "service": "Change Detection System",
            "version": "1.0.0",
            "database": {
                "status": "error",
                "postgis": "error",
                "error": str(e)
            }
        }

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with system information"""
    return {
        "message": "Change Detection & Monitoring System API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

# Demo endpoint for testing
@app.get("/demo")
async def demo():
    """Demo endpoint to test the system"""
    try:
        db_status = check_db_connection()
        postgis_status = test_postgis() if db_status else False
        
        return {
            "message": "🎉 Backend is running successfully!",
            "features": [
                "FastAPI framework working",
                "CORS middleware enabled",
                "Health check available",
                "API documentation ready",
                f"Database: {'Connected' if db_status else 'Disconnected'}",
                f"PostGIS: {'Available' if postgis_status else 'Unavailable'}"
            ],
            "next_steps": [
                "Test database connection",
                "Run database initialization",
                "Create API endpoints",
                "Connect frontend"
            ]
        }
    except Exception as e:
        logger.error(f"Demo endpoint failed: {e}")
        return {
            "message": "Backend is running but database connection failed",
            "error": str(e),
            "features": [
                "FastAPI framework working",
                "CORS middleware enabled",
                "Health check available",
                "API documentation ready"
            ]
        }

# Database initialization endpoint
@app.post("/init-db")
async def initialize_database():
    """Initialize database tables"""
    try:
        init_db()
        return {
            "message": "Database initialized successfully",
            "status": "success"
        }
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise HTTPException(status_code=500, detail=f"Database initialization failed: {str(e)}")

# Include routers
app.include_router(aoi_router, prefix="/api/v1/aoi", tags=["AOI Management"])
from api.detection import router as detection_router
app.include_router(detection_router, prefix="/api/v1/detection", tags=["Change Detection"])
# app.include_router(alerts.router, prefix="/api/v1/alerts", tags=["Alerts & Notifications"])

if __name__ == "__main__":
    logger.info("Starting Change Detection System API...")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )


