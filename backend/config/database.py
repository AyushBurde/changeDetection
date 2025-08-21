"""
Database configuration and connection management
"""

import os
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
from loguru import logger

# Database configuration
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "name": "changeDetection",  # Updated to match your actual database name
    "user": "postgres",
    "password": "ayu121",  # Your actual password
    "pool_size": 20,
    "max_overflow": 30
}

# Build database URL
DATABASE_URL = f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['name']}"

logger.info(f"Database URL: {DATABASE_URL.replace(DB_CONFIG['password'], '***')}")

# Create engine with connection pooling
engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=DB_CONFIG['pool_size'],
    max_overflow=DB_CONFIG['max_overflow'],
    pool_pre_ping=True,
    echo=False  # Set to True for SQL debugging
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()

def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Initialize database tables"""
    try:
        # Import all models to ensure they're registered
        try:
            from ..models import AOI, SatelliteImage, ChangeDetectionJob, ChangeDetectionResult, Alert, NotificationRule
        except ImportError:
            from models import AOI, SatelliteImage, ChangeDetectionJob, ChangeDetectionResult, Alert, NotificationRule
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
        logger.info("Available tables:")
        for table_name in Base.metadata.tables.keys():
            logger.info(f"  - {table_name}")
        
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise

def check_db_connection():
    """Check database connectivity"""
    try:
        logger.info("🔍 Testing database connection...")
        with engine.connect() as conn:
            logger.info("✅ Engine connection successful")
            result = conn.execute(text("SELECT 1"))
            logger.info("✅ Query execution successful")
            return True
    except Exception as e:
        logger.error(f"❌ Database connection failed: {e}")
        logger.error(f"Error type: {type(e).__name__}")
        return False

def test_postgis():
    """Test PostGIS functionality"""
    try:
        logger.info("🔍 Testing PostGIS functionality...")
        with engine.connect() as conn:
            # Test PostGIS version
            result = conn.execute(text("SELECT PostGIS_Version()"))
            version = result.fetchone()[0]
            logger.info(f"✅ PostGIS version: {version}")
            
            # Test basic spatial functions
            result = conn.execute(text("SELECT ST_AsText(ST_GeomFromText('POINT(0 0)'))"))
            point = result.fetchone()[0]
            logger.info(f"✅ PostGIS spatial test: {point}")
            
            return True
    except Exception as e:
        logger.error(f"❌ PostGIS test failed: {e}")
        logger.error(f"Error type: {type(e).__name__}")
        return False
