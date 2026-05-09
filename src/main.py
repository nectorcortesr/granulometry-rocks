import cv2
import numpy as np
import time

from src.pipeline.rock_analyzer import RockAnalyzer
from src.ui.dashboard import GranulometryDashboard
from src.utils.data_logger import SCADALogger

def main():
    # Industrial parameters
    SCALE_CM_PER_PX = 0.1  # Calibration from Day 20
    
    # Dependency Injection
    analyzer = RockAnalyzer(scale_factor=SCALE_CM_PER_PX)
    dashboard = GranulometryDashboard(buffer_size=100)
    
    # LEVEL 2 - DESIGN GAP
    logger = SCADALogger(filepath="produccion_scada.csv", interval_sec=2.0)

    # We simulated a noisy video stream
    print("Iniciando planta procesadora...")
    for frame_idx in range(50):
        # We generated a synthetic noisy frame
        frame = np.ones((480, 640, 3), dtype=np.uint8) * 50
        # We drew some random rocks
        num_rocks = np.random.randint(1, 5)
        for _ in range(num_rocks):
            cx, cy = np.random.randint(50, 600), np.random.randint(50, 400)
            r = np.random.randint(20, 60)
            cv2.circle(frame, (cx, cy), r, (150, 150, 150), -1)
            
        # LEVEL 3 - EDGE CASE GAP
        if frame is None or frame.size == 0:
            continue

        # 1. Analysis (Vision)
        rocks = analyzer.process_frame(frame)
        
        # Extract only the diameters for the KPI
        diameters_cm = [r["equiv_diameter_cm"] for r in rocks]
        
        # 2. Aggregation and UI
        dashboard.update_metrics(diameters_cm)
        frame_ui = dashboard.draw_dashboard(frame)
        
        # 3. Telemetry
        logger.log_frame(dashboard.current_p80)
        
        # We simulated the camera FPS
        time.sleep(0.033) 
        
    print(f"Shift ended. Final P80: {dashboard.current_p80:.2f} cm")

if __name__ == "__main__":
    main()