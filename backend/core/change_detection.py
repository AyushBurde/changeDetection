"""
Core change detection algorithms for satellite imagery analysis
"""

import numpy as np
import rasterio
from rasterio.mask import mask
from rasterio.warp import calculate_default_transform, reproject, Resampling
from scipy import ndimage
from skimage import filters, morphology, segmentation
from sklearn.cluster import KMeans
from sklearn.ensemble import IsolationForest
import cv2
from loguru import logger
from typing import Tuple, Dict, List, Optional
import geopandas as gpd
from shapely.geometry import Polygon, box
import json

class ChangeDetector:
    """Main change detection class for satellite imagery analysis"""
    
    def __init__(self, config: Dict):
        """
        Initialize change detector with configuration
        
        Args:
            config: Configuration dictionary with detection parameters
        """
        self.config = config
        self.bands = config.get('detection', {}).get('bands', ['red', 'green', 'nir'])
        self.cloud_thresholds = config.get('detection', {}).get('cloud', {})
        self.change_thresholds = config.get('detection', {}).get('change', {})
        
        logger.info(f"Initialized ChangeDetector with bands: {self.bands}")
    
    def preprocess_imagery(self, image_path: str, aoi_geometry: Polygon) -> np.ndarray:
        """
        Preprocess satellite imagery for analysis
        
        Args:
            image_path: Path to satellite imagery file
            aoi_geometry: AOI geometry for masking
            
        Returns:
            Preprocessed image array
        """
        try:
            with rasterio.open(image_path) as src:
                # Reproject to consistent CRS if needed
                if src.crs != 'EPSG:4326':
                    transform, width, height = calculate_default_transform(
                        src.crs, 'EPSG:4326', src.width, src.height, *src.bounds
                    )
                    image = np.empty((src.count, height, width))
                    reproject(
                        source=rasterio.band(src, 1),
                        destination=image[0],
                        src_transform=src.transform,
                        src_crs=src.crs,
                        dst_transform=transform,
                        dst_crs='EPSG:4326',
                        resampling=Resampling.bilinear
                    )
                else:
                    image = src.read()
                
                # Mask to AOI
                masked_image, _ = mask(src, [aoi_geometry], crop=True, nodata=0)
                
                # Normalize to 0-1 range
                normalized_image = self._normalize_image(masked_image)
                
                logger.info(f"Preprocessed image: {normalized_image.shape}")
                return normalized_image
                
        except Exception as e:
            logger.error(f"Error preprocessing imagery: {e}")
            raise
    
    def detect_clouds_and_shadows(self, image: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Detect clouds and shadows in satellite imagery
        
        Args:
            image: Input image array (bands, height, width)
            
        Returns:
            Tuple of (cloud_mask, shadow_mask)
        """
        try:
            # Calculate NDVI for vegetation detection
            if len(image) >= 3:  # Need at least Red and NIR bands
                red_band = image[0]  # Assuming first band is red
                nir_band = image[2]  # Assuming third band is NIR
                
                ndvi = (nir_band - red_band) / (nir_band + red_band + 1e-8)
                
                # Cloud detection using brightness and NDVI
                brightness = np.mean(image[:3], axis=0)  # Average of RGB bands
                
                cloud_mask = (
                    (brightness > self.cloud_thresholds.get('brightness_threshold', 0.7)) |
                    (ndvi < self.cloud_thresholds.get('ndvi_threshold', 0.1))
                )
                
                # Shadow detection (dark areas near clouds)
                shadow_mask = self._detect_shadows(image, cloud_mask)
                
                # Morphological operations to clean up masks
                cloud_mask = morphology.binary_closing(cloud_mask, morphology.disk(3))
                shadow_mask = morphology.binary_closing(shadow_mask, morphology.disk(2))
                
                logger.info(f"Cloud coverage: {np.sum(cloud_mask) / cloud_mask.size:.2%}")
                logger.info(f"Shadow coverage: {np.sum(shadow_mask) / shadow_mask.size:.2%}")
                
                return cloud_mask, shadow_mask
            else:
                logger.warning("Insufficient bands for cloud/shadow detection")
                return np.zeros(image.shape[1:], dtype=bool), np.zeros(image.shape[1:], dtype=bool)
                
        except Exception as e:
            logger.error(f"Error in cloud/shadow detection: {e}")
            raise
    
    def _detect_shadows(self, image: np.ndarray, cloud_mask: np.ndarray) -> np.ndarray:
        """Detect shadows based on dark areas near clouds"""
        # Simple shadow detection: dark areas with low NDVI
        if len(image) >= 3:
            red_band = image[0]
            nir_band = image[2]
            ndvi = (nir_band - red_band) / (nir_band + red_band + 1e-8)
            
            # Dark areas with low NDVI near clouds
            dark_areas = np.mean(image[:3], axis=0) < self.cloud_thresholds.get('shadow_threshold', 0.3)
            low_ndvi = ndvi < 0.1
            
            # Dilate cloud mask to find areas near clouds
            dilated_clouds = morphology.binary_dilation(cloud_mask, morphology.disk(5))
            
            shadow_mask = dark_areas & low_ndvi & dilated_clouds
            return shadow_mask
        
        return np.zeros(image.shape[1:], dtype=bool)
    
    def detect_changes(self, 
                      image1: np.ndarray, 
                      image2: np.ndarray,
                      cloud_mask1: np.ndarray,
                      cloud_mask2: np.ndarray) -> Dict:
        """
        Detect changes between two temporal images
        
        Args:
            image1: First temporal image
            image2: Second temporal image
            cloud_mask1: Cloud mask for first image
            cloud_mask2: Cloud mask for second image
            
        Returns:
            Dictionary containing change detection results
        """
        try:
            # Create valid pixel mask (no clouds in either image)
            valid_pixels = ~(cloud_mask1 | cloud_mask2)
            
            if np.sum(valid_pixels) < 100:  # Need minimum valid pixels
                logger.warning("Insufficient valid pixels for change detection")
                return self._empty_change_result()
            
            # Calculate spectral differences
            spectral_diff = self._calculate_spectral_differences(image1, image2, valid_pixels)
            
            # Apply change detection algorithms
            change_magnitude = self._calculate_change_magnitude(spectral_diff)
            change_direction = self._calculate_change_direction(spectral_diff)
            
            # Filter changes based on thresholds
            significant_changes = self._filter_significant_changes(
                change_magnitude, 
                self.change_thresholds.get('min_change_threshold', 0.15)
            )
            
            # Classify change types
            change_types = self._classify_changes(
                image1, image2, change_magnitude, change_direction, valid_pixels
            )
            
            # Calculate change statistics
            change_stats = self._calculate_change_statistics(
                change_magnitude, significant_changes, valid_pixels
            )
            
            result = {
                'change_magnitude': change_magnitude.tolist(),
                'change_direction': change_direction.tolist(),
                'significant_changes': significant_changes.tolist(),
                'change_types': change_types,
                'statistics': change_stats,
                'valid_pixels': valid_pixels.tolist(),
                'metadata': {
                    'algorithm': 'multi-spectral_change_detection',
                    'thresholds': self.change_thresholds,
                    'bands_used': self.bands
                }
            }
            
            logger.info(f"Change detection completed. Significant changes: {change_stats['significant_change_percentage']:.2%}")
            return result
            
        except Exception as e:
            logger.error(f"Error in change detection: {e}")
            raise
    
    def _calculate_spectral_differences(self, image1: np.ndarray, image2: np.ndarray, 
                                      valid_pixels: np.ndarray) -> np.ndarray:
        """Calculate spectral differences between two images"""
        # Normalized difference for each band
        differences = []
        
        for i in range(min(len(image1), len(image2))):
            band1 = image1[i]
            band2 = image2[i]
            
            # Normalized difference
            diff = (band2 - band1) / (band1 + 1e-8)
            differences.append(diff)
        
        # Combine differences (weighted average)
        combined_diff = np.mean(differences, axis=0)
        
        # Apply valid pixel mask
        combined_diff[~valid_pixels] = 0
        
        return combined_diff
    
    def _calculate_change_magnitude(self, spectral_diff: np.ndarray) -> np.ndarray:
        """Calculate magnitude of changes"""
        return np.abs(spectral_diff)
    
    def _calculate_change_direction(self, spectral_diff: np.ndarray) -> np.ndarray:
        """Calculate direction of changes (positive/negative)"""
        return np.sign(spectral_diff)
    
    def _filter_significant_changes(self, change_magnitude: np.ndarray, threshold: float) -> np.ndarray:
        """Filter changes based on magnitude threshold"""
        return change_magnitude > threshold
    
    def _classify_changes(self, image1: np.ndarray, image2: np.ndarray, 
                         change_magnitude: np.ndarray, change_direction: np.ndarray,
                         valid_pixels: np.ndarray) -> Dict:
        """Classify types of changes"""
        # Simple classification based on spectral characteristics
        changes = {
            'vegetation_loss': 0,
            'vegetation_gain': 0,
            'urban_expansion': 0,
            'water_changes': 0,
            'other': 0
        }
        
        # This is a simplified classification - in practice, you'd use more sophisticated methods
        # like machine learning models trained on labeled data
        
        return changes
    
    def _calculate_change_statistics(self, change_magnitude: np.ndarray, 
                                   significant_changes: np.ndarray,
                                   valid_pixels: np.ndarray) -> Dict:
        """Calculate comprehensive change statistics"""
        total_valid_pixels = np.sum(valid_pixels)
        total_changes = np.sum(significant_changes)
        
        stats = {
            'total_pixels': int(change_magnitude.size),
            'valid_pixels': int(total_valid_pixels),
            'changed_pixels': int(total_changes),
            'change_percentage': float(total_changes / total_valid_pixels * 100) if total_valid_pixels > 0 else 0,
            'significant_change_percentage': float(total_changes / total_valid_pixels * 100) if total_valid_pixels > 0 else 0,
            'mean_change_magnitude': float(np.mean(change_magnitude[valid_pixels])),
            'max_change_magnitude': float(np.max(change_magnitude[valid_pixels])),
            'std_change_magnitude': float(np.std(change_magnitude[valid_pixels]))
        }
        
        return stats
    
    def _normalize_image(self, image: np.ndarray) -> np.ndarray:
        """Normalize image to 0-1 range"""
        if image.dtype != np.float32:
            image = image.astype(np.float32)
        
        # Handle different data types (uint8, uint16, etc.)
        if image.max() > 1.0:
            image = image / image.max()
        
        return image
    
    def _empty_change_result(self) -> Dict:
        """Return empty change detection result"""
        return {
            'change_magnitude': [],
            'change_direction': [],
            'significant_changes': [],
            'change_types': {},
            'statistics': {
                'total_pixels': 0,
                'valid_pixels': 0,
                'changed_pixels': 0,
                'change_percentage': 0.0,
                'significant_change_percentage': 0.0,
                'mean_change_magnitude': 0.0,
                'max_change_magnitude': 0.0,
                'std_change_magnitude': 0.0
            },
            'valid_pixels': [],
            'metadata': {
                'algorithm': 'multi-spectral_change_detection',
                'thresholds': self.change_thresholds,
                'bands_used': self.bands,
                'error': 'insufficient_valid_pixels'
            }
        }

