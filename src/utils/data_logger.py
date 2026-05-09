import os
import time
from datetime import datetime
import numpy as np

class SCADALogger:
    def __init__(self, filepath="granulometry_log.csv", interval_sec=5.0):
        self.filepath = filepath
        self.interval_sec = interval_sec
        self.last_log_time = time.time()
        self.p80_buffer = []

        # Create file with SCADA-compatible headers if it does not exist
        if not os.path.exists(self.filepath):
            with open(self.filepath, 'w', encoding='utf-8') as f:
                # We use semicolon as the delimiter
                f.write("timestamp;avg_p80_cm;active_alert\n")

    def log_frame(self, current_p80, threshold_alert=15.0):
        """
        Ingests the calculation of a frame. If the time window has expired,
        writes the consolidated average to disk atomically.
        """
        current_time = time.time()
        elapsed_time = current_time - self.last_log_time
        
        # LEVEL 2 - DESIGN GAP
        elapsed_time = current_time - self.last_log_time
        # (Hint: Calculate the delta by subtracting self.last_log_time from current_time)

        if elapsed_time >= self.interval_sec:
            # LEVEL 1 - MECHANICAL GAP
            iso_timestamp = datetime.now().isoformat()
            # (Hint: Use datetime.now() or datetime.utcnow() and convert it to ISO 8601 string by calling its .isoformat() method)
            
            # If the buffer is empty, skip to avoid np.mean(empty)

            if self.p80_buffer:
                avg_p80 = float(np.mean(self.p80_buffer))
                alert = int(avg_p80 > threshold_alert)

                # LEVEL 3 - EDGE CASE GAP
                try:
                    with open(self.filepath, 'a', encoding='utf-8') as f:
                        f.write(f"{iso_timestamp};{avg_p80:.2f};{alert}\n")
                    # (Hint: Open self.filepath in append mode ('a'). Write the string f"{iso_timestamp};{avg_p80:.2f};{alerta}\n". The try/except block is MANDATORY because a mechanical failure of disk, permissions, or quota should not crash the entire vision pipeline)
                except IOError as e:
                    print(f"[ERROR NO FATAL] Could not write to log: {e}")
            

            # Reset the window
            self.p80_buffer = []
            self.last_log_time = current_time
        
        self.p80_buffer.append(current_p80)


if __name__ == "__main__":
    # Unit test for time window (Simulating 6 seconds of fast operation)
    logger = SCADALogger(filepath="test_log.csv", interval_sec=1.0)
    
    print("Simulating frame processing...")
    
    # Burst 1: simulate frames for 1.1 seconds
    logger.log_frame(10.0)
    logger.log_frame(12.0)
    time.sleep(1.1) 
    logger.log_frame(14.0) # This will trigger the writing of the previous buffer (average = 11.0)
    
    # Burst 2: frames with alert
    logger.log_frame(20.0)
    logger.log_frame(20.0)
    time.sleep(1.1)
    logger.log_frame(5.0) # This will trigger the writing of the previous buffer (average = 18.0, alert = 1)
    
    # Verify the results mathematically
    assert os.path.exists("test_log.csv"), "The CSV file was not created"
    
    with open("test_log.csv", "r") as f:
        lines = f.readlines()
        
    assert len(lines) == 3, f"Expected 3 lines (header + 2 logs). Found: {len(lines)}"
    
    # Verify average of Burst 1
    log_1 = lines[1].strip().split(';')
    assert float(log_1[1]) == 11.00, f"Error in Burst 1 Average. Expected 11.00, got {log_1[1]}"
    assert int(log_1[2]) == 0, "Incorrect alert in Burst 1"

    # Verify average of Burst 2
    log_2 = lines[2].strip().split(';')
    assert float(log_2[1]) == 18.00, f"Error in Burst 2 Average. Expected 18.00, got {log_2[1]}"
    assert int(log_2[2]) == 1, "Alert not triggered in Burst 2 despite exceeding the threshold"
    
    # Cleanup
    os.remove("test_log.csv")
    
    print("SUCCESS: Temporal aggregation and SCADA telemetry verified on disk.")
    print(f"Sample Log 1: {lines[1].strip()}")
    print(f"Sample Log 2: {lines[2].strip()}")