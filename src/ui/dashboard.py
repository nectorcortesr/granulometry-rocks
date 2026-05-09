import cv2
import numpy as np

class GranulometryDashboard:
    def __init__(self, buffer_size=500):
        """
        It maintains a history of sizes to smooth the calculation of the P80.
        """
        self.history = []
        self.buffer_size = buffer_size
        self.current_p80 = 0.0

    def update_metrics(self, new_sizes_cm):
        """
        Updates the circular buffer with new physical diameters.
        """
        if not new_sizes_cm:
            return

        self.history.extend(new_sizes_cm)
        
        # We maintain the maximum buffer size (sliding)
        if len(self.history) > self.buffer_size:
            self.history = self.history[-self.buffer_size:]

        # LEVEL 3 - EDGE CASE GAP
        if not self.history:
            self.current_p80 = 0.0
            return
        # (Hint: Before using np.percentile, check if 'self.history' is empty to avoid errors if all rocks disappear and the buffer is empty or never filled. If invalid, set self.current_p80 = 0.0)
        
        # LEVEL 1 - MECHANICAL GAP
        self.current_p80 = np.percentile(self.history, 80)
        # (Hint: Implement the mathematical calculation of the 80th percentile on the list self.history using numpy. Remember that np.percentile receives the value as a percentage 0-100, not 0-1)
    
    def draw_dashboard(self, frame_bgr):
        """
        Draw the panel in the frame using ONLY OpenCV in-place primitives.
        """
        # Draw a semi-transparent background
        overlay = frame_bgr.copy()
        
        # LEVEL 2 - DESIGN GAP
        rect_dashboard = (10, 10, 350, 100)
        cv2.rectangle(overlay, (rect_dashboard[0], rect_dashboard[1]), (rect_dashboard[0] + rect_dashboard[2], rect_dashboard[1] + rect_dashboard[3]), (0, 0, 0), cv2.FILLED)
        # (Hint: Draw a dark rectangle on 'overlay' using cv2.rectangle in the top-left corner (e.g., from (10,10) to (350, 100)) filled using cv2.FILLED or -1 as thickness)
        
        # Blend to give transparency
        alpha = 0.6
        cv2.addWeighted(overlay, alpha, frame_bgr, 1 - alpha, 0, frame_bgr)
        
        # Text of P80
        texto_p80 = f"P80: {self.current_p80:.2f} cm"
        
        # If P80 is dangerous (> 15cm), paint text in RED, otherwise GREEN (BGR)
        color = (0, 0, 255) if self.current_p80 > 15.0 else (0, 255, 0)
        
        cv2.putText(frame_bgr, texto_p80, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 3)
        cv2.putText(frame_bgr, f"Buffer: {len(self.history)} rocks", (20, 85), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1)

        return frame_bgr

if __name__ == "__main__":
    import time
    # Synthetic performance and logic test
    dash = GranulometryDashboard(buffer_size=100)
    
    # Simulate size detections (cm)
    detected_sizes = [2.0, 4.0, 5.0, 8.0, 10.0]
    dash.update_metrics(detected_sizes)
    
    # Verify mathematical interpolation
    assert abs(dash.current_p80 - 8.4) < 1e-4, f"Incorrect P80 calculation: {dash.current_p80}"
    
    # Benchmark in-place drawing
    frame_test = np.zeros((720, 1280, 3), dtype=np.uint8)
    
    start_t = time.perf_counter()
    for _ in range(100):
        frame_out = dash.draw_dashboard(frame_test.copy())
    end_t = time.perf_counter()
    
    ms_per_frame = ((end_t - start_t) / 100) * 1000
    fps_equivalent = 1000 / ms_per_frame
    
    assert fps_equivalent > 25, f"Unacceptable UI performance: {fps_equivalent:.1f} FPS. Did you use Matplotlib?"
    
    print("SUCCESS: UI in-place and P80 calculated in real-time.")
    print(f"Current P80: {dash.current_p80:.2f} cm")
    print(f"UI rendering performance: {fps_equivalent:.1f} equivalent FPS (Budget OK).")