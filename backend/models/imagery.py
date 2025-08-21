"""
Satellite imagery model for storing imagery metadata and references
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, Float
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from geoalchemy2 import Geometry
try:
    from ..config.database import Base
except ImportError:
    from config.database import Base
import uuid

class SatelliteImage(Base):
    """Satellite imagery model"""
    
    __tablename__ = "satellite_images"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False, index=True)
    
    # Image metadata
    satellite = Column(String(100), nullable=False)  # e.g., "Landsat-8", "Sentinel-2"
    sensor = Column(String(100))  # e.g., "OLI", "MSI"
    acquisition_date = Column(DateTime(timezone=True), nullable=False, index=True)
    
    # Spatial information
    footprint = Column(Geometry('POLYGON', srid=4326), nullable=False, index=True)
    center_point = Column(Geometry('POINT', srid=4326))
    
    # Image properties
    cloud_coverage = Column(Float, default=0.0)  # 0-100%
    resolution_meters = Column(Float)  # spatial resolution in meters
    bands_available = Column(JSONB)  # list of available bands
    
    # File information
    file_path = Column(String(500))  # path to image file
    file_size_mb = Column(Float)
    format = Column(String(50))  # e.g., "GeoTIFF", "JP2"
    
    # Processing status
    is_processed = Column(Boolean, default=False)
    processing_status = Column(String(50), default="pending")  # pending, processing, completed, failed
    quality_score = Column(Float)  # 0-1 quality assessment
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Additional properties as JSON
    properties = Column(JSONB, default={})
    
    def __repr__(self):
        return f"<SatelliteImage(id='{self.id}', satellite='{self.satellite}', date='{self.acquisition_date}')>"
    
    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            "id": self.id,
            "name": self.name,
            "satellite": self.satellite,
            "sensor": self.sensor,
            "acquisition_date": self.acquisition_date.isoformat() if self.acquisition_date else None,
            "footprint": self.footprint,
            "center_point": self.center_point,
            "cloud_coverage": self.cloud_coverage,
            "resolution_meters": self.resolution_meters,
            "bands_available": self.bands_available,
            "file_path": self.file_path,
            "file_size_mb": self.file_size_mb,
            "format": self.format,
            "is_processed": self.is_processed,
            "processing_status": self.processing_status,
            "quality_score": self.quality_score,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "properties": self.properties
        }
