"""
AOI (Area of Interest) model for user-defined monitoring areas
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

class AOI(Base):
    """Area of Interest model"""
    
    __tablename__ = "aois"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    
    # Geometry (PostGIS)
    geometry = Column(Geometry('POLYGON', srid=4326), nullable=False, index=True)
    
    # Bounding box for quick spatial queries
    bbox = Column(Geometry('POLYGON', srid=4326), nullable=False, index=True)
    
    # AOI properties
    area_hectares = Column(Float, nullable=False)
    created_by = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, index=True)
    
    # Monitoring settings
    monitoring_frequency = Column(String(50), default="weekly")  # daily, weekly, monthly
    change_threshold = Column(Float, default=0.15)  # 15% change threshold
    alert_enabled = Column(Boolean, default=True)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Additional properties as JSON
    properties = Column(JSONB, default={})
    
    def __repr__(self):
        return f"<AOI(id='{self.id}', name='{self.name}', area={self.area_hectares:.2f}ha)>"
    
    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "geometry": self.geometry,
            "bbox": self.bbox,
            "area_hectares": self.area_hectares,
            "created_by": self.created_by,
            "is_active": self.is_active,
            "monitoring_frequency": self.monitoring_frequency,
            "change_threshold": self.change_threshold,
            "alert_enabled": self.alert_enabled,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "properties": self.properties
        }


