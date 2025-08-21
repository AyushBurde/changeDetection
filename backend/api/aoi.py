"""
AOI (Area of Interest) API endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Optional
from pydantic import BaseModel, Field
from geoalchemy2 import Geometry
from geoalchemy2.functions import ST_AsGeoJSON, ST_Area, ST_GeomFromGeoJSON
import json
import uuid
from datetime import datetime

# Import database dependencies
from config.database import get_db

# Import models
from models.aoi import AOI

router = APIRouter()

# Pydantic models for request/response
class AOIBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, description="Name of the AOI")
    description: Optional[str] = Field(None, description="Description of the AOI")
    created_by: str = Field(..., min_length=1, max_length=255, description="Creator of the AOI")
    monitoring_frequency: str = Field("weekly", description="Monitoring frequency (daily, weekly, monthly)")
    change_threshold: float = Field(0.15, ge=0.0, le=1.0, description="Change detection threshold (0-1)")
    alert_enabled: bool = Field(True, description="Whether alerts are enabled for this AOI")

class AOICreate(AOIBase):
    geometry: dict = Field(..., description="GeoJSON geometry (Polygon)")

class AOIUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    monitoring_frequency: Optional[str] = None
    change_threshold: Optional[float] = Field(None, ge=0.0, le=1.0)
    alert_enabled: Optional[bool] = None
    is_active: Optional[bool] = None

class AOIResponse(AOIBase):
    id: str
    area_hectares: float
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]
    geometry: dict  # GeoJSON
    bbox: dict      # GeoJSON

    class Config:
        from_attributes = True

# Helper functions
def calculate_area_hectares(db: Session, geometry_geojson: dict) -> float:
    """Calculate area in hectares from GeoJSON geometry"""
    try:
        # Convert GeoJSON to PostGIS geometry and calculate area
        result = db.execute(
            text("SELECT ST_Area(ST_Transform(ST_GeomFromGeoJSON(:geom), 3857)) / 10000 as area_hectares"),
            {"geom": json.dumps(geometry_geojson)}
        ).fetchone()
        return float(result[0]) if result else 0.0
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid geometry: {str(e)}")

def create_bbox(db: Session, geometry_geojson: dict) -> dict:
    """Create bounding box from GeoJSON geometry"""
    try:
        result = db.execute(
            text("SELECT ST_AsGeoJSON(ST_Envelope(ST_GeomFromGeoJSON(:geom))) as bbox"),
            {"geom": json.dumps(geometry_geojson)}
        ).fetchone()
        return json.loads(result[0]) if result else {}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error creating bbox: {str(e)}")

def geometry_to_geojson(db: Session, geometry) -> dict:
    """Convert PostGIS geometry to GeoJSON"""
    if not geometry:
        return {}
    try:
        result = db.execute(
            text("SELECT ST_AsGeoJSON(:geom)"),
            {"geom": geometry}
        ).fetchone()
        return json.loads(result[0]) if result else {}
    except Exception:
        return {}

# API Endpoints

@router.post("/", response_model=AOIResponse, status_code=status.HTTP_201_CREATED)
async def create_aoi(aoi: AOICreate, db: Session = Depends(get_db)):
    """Create a new Area of Interest"""
    try:
        # Validate GeoJSON geometry
        if not aoi.geometry or aoi.geometry.get("type") != "Polygon":
            raise HTTPException(status_code=400, detail="Geometry must be a valid GeoJSON Polygon")
        
        # Calculate area and create bbox
        area_hectares = calculate_area_hectares(db, aoi.geometry)
        bbox_geojson = create_bbox(db, aoi.geometry)
        
        # Create AOI instance
        db_aoi = AOI(
            id=str(uuid.uuid4()),
            name=aoi.name,
            description=aoi.description,
            created_by=aoi.created_by,
            monitoring_frequency=aoi.monitoring_frequency,
            change_threshold=aoi.change_threshold,
            alert_enabled=aoi.alert_enabled,
            area_hectares=area_hectares,
            geometry=text(f"ST_GeomFromGeoJSON('{json.dumps(aoi.geometry)}')"),
            bbox=text(f"ST_GeomFromGeoJSON('{json.dumps(bbox_geojson)}')")
        )
        
        db.add(db_aoi)
        db.commit()
        db.refresh(db_aoi)
        
        # Convert geometry to GeoJSON for response
        geometry_geojson = geometry_to_geojson(db, db_aoi.geometry)
        bbox_geojson = geometry_to_geojson(db, db_aoi.bbox)
        
        return AOIResponse(
            id=db_aoi.id,
            name=db_aoi.name,
            description=db_aoi.description,
            created_by=db_aoi.created_by,
            monitoring_frequency=db_aoi.monitoring_frequency,
            change_threshold=db_aoi.change_threshold,
            alert_enabled=db_aoi.alert_enabled,
            area_hectares=db_aoi.area_hectares,
            is_active=db_aoi.is_active,
            created_at=db_aoi.created_at,
            updated_at=db_aoi.updated_at,
            geometry=geometry_geojson,
            bbox=bbox_geojson
        )
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create AOI: {str(e)}")

@router.get("/", response_model=List[AOIResponse])
async def get_aois(
    skip: int = 0,
    limit: int = 100,
    active_only: bool = True,
    db: Session = Depends(get_db)
):
    """Get list of Areas of Interest"""
    try:
        query = db.query(AOI)
        if active_only:
            query = query.filter(AOI.is_active == True)
        
        aois = query.offset(skip).limit(limit).all()
        
        results = []
        for aoi in aois:
            geometry_geojson = geometry_to_geojson(db, aoi.geometry)
            bbox_geojson = geometry_to_geojson(db, aoi.bbox)
            
            results.append(AOIResponse(
                id=aoi.id,
                name=aoi.name,
                description=aoi.description,
                created_by=aoi.created_by,
                monitoring_frequency=aoi.monitoring_frequency,
                change_threshold=aoi.change_threshold,
                alert_enabled=aoi.alert_enabled,
                area_hectares=aoi.area_hectares,
                is_active=aoi.is_active,
                created_at=aoi.created_at,
                updated_at=aoi.updated_at,
                geometry=geometry_geojson,
                bbox=bbox_geojson
            ))
        
        return results
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve AOIs: {str(e)}")

@router.get("/{aoi_id}", response_model=AOIResponse)
async def get_aoi(aoi_id: str, db: Session = Depends(get_db)):
    """Get a specific Area of Interest by ID"""
    try:
        aoi = db.query(AOI).filter(AOI.id == aoi_id).first()
        if not aoi:
            raise HTTPException(status_code=404, detail="AOI not found")
        
        geometry_geojson = geometry_to_geojson(db, aoi.geometry)
        bbox_geojson = geometry_to_geojson(db, aoi.bbox)
        
        return AOIResponse(
            id=aoi.id,
            name=aoi.name,
            description=aoi.description,
            created_by=aoi.created_by,
            monitoring_frequency=aoi.monitoring_frequency,
            change_threshold=aoi.change_threshold,
            alert_enabled=aoi.alert_enabled,
            area_hectares=aoi.area_hectares,
            is_active=aoi.is_active,
            created_at=aoi.created_at,
            updated_at=aoi.updated_at,
            geometry=geometry_geojson,
            bbox=bbox_geojson
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve AOI: {str(e)}")

@router.put("/{aoi_id}", response_model=AOIResponse)
async def update_aoi(aoi_id: str, aoi_update: AOIUpdate, db: Session = Depends(get_db)):
    """Update an Area of Interest"""
    try:
        aoi = db.query(AOI).filter(AOI.id == aoi_id).first()
        if not aoi:
            raise HTTPException(status_code=404, detail="AOI not found")
        
        # Update fields if provided
        update_data = aoi_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(aoi, field, value)
        
        db.commit()
        db.refresh(aoi)
        
        geometry_geojson = geometry_to_geojson(db, aoi.geometry)
        bbox_geojson = geometry_to_geojson(db, aoi.bbox)
        
        return AOIResponse(
            id=aoi.id,
            name=aoi.name,
            description=aoi.description,
            created_by=aoi.created_by,
            monitoring_frequency=aoi.monitoring_frequency,
            change_threshold=aoi.change_threshold,
            alert_enabled=aoi.alert_enabled,
            area_hectares=aoi.area_hectares,
            is_active=aoi.is_active,
            created_at=aoi.created_at,
            updated_at=aoi.updated_at,
            geometry=geometry_geojson,
            bbox=bbox_geojson
        )
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update AOI: {str(e)}")

@router.delete("/{aoi_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_aoi(aoi_id: str, db: Session = Depends(get_db)):
    """Delete an Area of Interest (soft delete by setting is_active=False)"""
    try:
        aoi = db.query(AOI).filter(AOI.id == aoi_id).first()
        if not aoi:
            raise HTTPException(status_code=404, detail="AOI not found")
        
        # Soft delete
        aoi.is_active = False
        db.commit()
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete AOI: {str(e)}")

@router.get("/{aoi_id}/stats")
async def get_aoi_stats(aoi_id: str, db: Session = Depends(get_db)):
    """Get statistics for a specific AOI"""
    try:
        aoi = db.query(AOI).filter(AOI.id == aoi_id).first()
        if not aoi:
            raise HTTPException(status_code=404, detail="AOI not found")
        
        # Calculate additional statistics
        stats = {
            "aoi_id": aoi_id,
            "area_hectares": aoi.area_hectares,
            "area_km2": aoi.area_hectares / 100,
            "monitoring_frequency": aoi.monitoring_frequency,
            "change_threshold": aoi.change_threshold,
            "alert_enabled": aoi.alert_enabled,
            "created_at": aoi.created_at,
            "days_active": (datetime.utcnow() - aoi.created_at).days,
            # TODO: Add more statistics from related tables
            "total_detections": 0,  # Will be implemented later
            "total_alerts": 0,      # Will be implemented later
            "last_detection": None   # Will be implemented later
        }
        
        return stats
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get AOI stats: {str(e)}")

