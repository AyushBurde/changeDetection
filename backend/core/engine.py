
import numpy as np
import rasterio
from rasterio.warp import reproject, Resampling
from loguru import logger
import cv2

class ChangeDetectionEngine:
    """
    Core engine for performing change detection on satellite imagery.
    Implements NDVI-based differencing and simple thresholding.
    """

    def __init__(self):
        pass

    def calculate_ndvi(self, red_band: np.ndarray, nir_band: np.ndarray) -> np.ndarray:
        """
        Calculate Normalized Difference Vegetation Index (NDVI).
        NDVI = (NIR - Red) / (NIR + Red)
        """
        # Allow division by zero
        np.seterr(divide='ignore', invalid='ignore')
        
        ndvi = (nir_band.astype(float) - red_band.astype(float)) / (nir_band.astype(float) + red_band.astype(float))
        
        # Fill NaN values with 0
        ndvi = np.nan_to_num(ndvi, nan=0.0)
        
        return ndvi

    def mask_clouds(self, image: np.ndarray, threshold: int = 200) -> np.ndarray:
        """
        Simple cloud masking based on brightness threshold.
        Assumes higher values in visible bands correspond to clouds.
        Returns a binary mask (0 for cloud, 1 for clear).
        """
        # Simple assumption: Clouds are bright in RGB
        # If image has 3 bands (RGB), take mean. if single band, take it directly.
        if len(image.shape) == 3:
            brightness = np.mean(image, axis=0)
        else:
            brightness = image
            
        mask = brightness < threshold
        return mask.astype(np.uint8)

    def detect_changes(self, before_path: str, after_path: str, threshold: float = 0.2) -> dict:
        """
        Perform change detection between two images.
        """
        try:
            with rasterio.open(before_path) as src_before, rasterio.open(after_path) as src_after:
                # Read Red and NIR bands (Assuming Band 3=Red, Band 4=NIR for Sentinel-2, adjust as needed)
                # NOTE: This implies the input images are multi-spectral.
                # For demo purposes, we will safely try to read the first few bands.
                
                # Check band counts
                if src_before.count < 3 or src_after.count < 3:
                     raise ValueError("Input images need at least 3 bands (RGB/NIR) for accurate analysis")

                # Reading bands (0-indexed read)
                # Custom mapping: 0:Blue, 1:Green, 2:Red, 3:NIR (Example)
                # Let's assume standard 4-band ordering or usage of kwargs to specify indices
                
                # Simplify: Using Red (idx 2) and Green (idx 1) for a basic vegetation index helper
                # Ideally, we need NIR. Let's assume the user provides suitable GeoTIFFs.
                
                before_red = src_before.read(3) if src_before.count >= 3 else src_before.read(1)
                before_nir = src_before.read(4) if src_before.count >= 4 else src_before.read(1) # Fallback to 1 if not 4
                
                after_red = src_after.read(3) if src_after.count >= 3 else src_after.read(1)
                after_nir = src_after.read(4) if src_after.count >= 4 else src_after.read(1)

                # Ensure dimensions match
                if before_red.shape != after_red.shape:
                    logger.warning("Dimensions mismatch, resizing after_image to match before_image")
                    # In a real scenario, we should reproject/resample. 
                    # For prototype, cv2 resize (lossy but fast)
                    after_red = cv2.resize(after_red, (before_red.shape[1], before_red.shape[0]))
                    after_nir = cv2.resize(after_nir, (before_nir.shape[1], before_nir.shape[0]))

                # Calculate NDVI
                ndvi_before = self.calculate_ndvi(before_red, before_nir)
                ndvi_after = self.calculate_ndvi(after_red, after_nir)

                # Diff
                diff = ndvi_after - ndvi_before
                
                # Thresholding for change
                # Positive change (growth) vs Negative change (loss)
                # We care about magnitude
                change_mask = np.abs(diff) > threshold
                
                change_pixels = np.count_nonzero(change_mask)
                total_pixels = change_mask.size
                change_percentage = (change_pixels / total_pixels) * 100

                return {
                    "status": "success",
                    "change_percentage": change_percentage,
                    "change_mask_shape": change_mask.shape,
                    "ndvi_before_mean": float(np.mean(ndvi_before)),
                    "ndvi_after_mean": float(np.mean(ndvi_after))
                }

        except Exception as e:
            logger.error(f"Error in change detection: {e}")
            return {"status": "error", "message": str(e)}

engine = ChangeDetectionEngine()
