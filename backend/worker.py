
import os
from celery import Celery
from loguru import logger
from core.engine import engine

# Celery Configuration
# In production, use environment variables
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

celery_app = Celery("change_detection_worker", broker=REDIS_URL, backend=REDIS_URL)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

@celery_app.task(name="tasks.detect_changes")
def perform_change_detection_task(before_image_path: str, after_image_path: str, aoi_id: str):
    """
    Background task to run the heavy change detection algo.
    """
    logger.info(f"Starting change detection for AOI: {aoi_id}")
    try:
        # Run the engine
        result = engine.detect_changes(before_image_path, after_image_path)
        
        # In a real app, you would save 'result' to the Database here
        # db.save_result(aoi_id, result)
        
        logger.info(f"Completed change detection for AOI: {aoi_id}. Result: {result}")
        return result
    except Exception as e:
        logger.error(f"Task failed: {e}")
        return {"status": "failed", "error": str(e)}
