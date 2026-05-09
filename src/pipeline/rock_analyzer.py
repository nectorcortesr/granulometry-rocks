import cv2
import numpy as np

# We import our highly cohesive modules
from src.preprocessing.clahe_filter import preprocess_frame
from src.preprocessing.canny_detector import auto_canny
from src.preprocessing.morphology import apply_closing
from src.analysis.contour_measurement import find_rock_contours
from src.analysis.calibration import convert_metrics_to_physical

class RockAnalyzer:
    """
    Vision pipeline orchestrator. Meets SRP: Only analyzes,
    does not draw UI or write to disk.
    """
    def __init__(self, scale_factor, min_area_px=50):
        self.scale_factor = scale_factor
        self.min_area_px = min_area_px

    def process_frame(self, frame_bgr):
        """
        It applies the mathematical function composition F(x).
        It returns the physical metrics of the detected rocks.
        """
        # 1. Preprocessing
        gray, clahe_out, float_out = preprocess_frame(frame_bgr)
        
        # 2. Edges and Morphology
        edges = auto_canny(clahe_out)
        closed_edges = apply_closing(edges)
        
        # 3. Geometric Extraction
        contours, metrics_px = find_rock_contours(closed_edges, self.min_area_px)
        
        # 4. Physical Conversion
        physical_metrics = []
        for m in metrics_px:
            # LEVEL 1 - MECHANICAL GAP
            physics = convert_metrics_to_physical(m, self.scale_factor)
            physical_metrics.append(physics)
            
        return physical_metrics