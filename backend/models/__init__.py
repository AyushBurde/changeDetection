"""
Database models for Change Detection System
"""

# Import from the correct database configuration
try:
    from ..config.database import Base, engine, SessionLocal
except ImportError:
    from config.database import Base, engine, SessionLocal

# Import all models
try:
    # Relative imports for package
    from .aoi import AOI
    # from .imagery import SatelliteImage
    # from .detection import ChangeDetectionJob, ChangeDetectionResult
    # from .alerts import Alert, NotificationRule
except ImportError:
    # Try absolute imports
    from models.aoi import AOI
    # from models.imagery import SatelliteImage
    # from models.detection import ChangeDetectionJob, ChangeDetectionResult
    # from models.alerts import Alert, NotificationRule

__all__ = [
    "Base",
    "engine", 
    "SessionLocal",
    "AOI",
    "SatelliteImage",
    "ChangeDetectionJob",
    "ChangeDetectionResult",
    "Alert",
    "NotificationRule"
]


