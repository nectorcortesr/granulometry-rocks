import cv2
import numpy as np

def non_maximum_suppression_vectorized(mag, theta):
    """
    NMS is implemented assuming a quantized angle of 0 degrees (horizontal) for simplicity.
    In a real Canny, quantization occurs in 4 directions.
    """
    M, N = mag.shape
    
    # LEVEL 3 - EDGE CASE GAP
    Z = np.zeros((M, N), dtype=np.float32)
    # (Hint: To avoid an IndexError when accessing neighbors [i-1] and [i+1] at the image borders,
    # initialize the output matrix Z with zeros of the same size as 'mag', and then iterate only over the interior of the image, e.g., range(1, M-1))
    
    for i in range(1, M-1):
        for j in range(1, N-1):
            # Simplification: we assume theta at this pixel is ~0 degrees (vertical edge, horizontal gradient)
            # In a real Canny, this depends on the value of theta[i,j]
            left_neighbor = mag[i, j-1]
            right_neighbor = mag[i, j+1]
            
            # LEVEL 1 - MECHANICAL GAP
            is_peak = mag[i, j] >= left_neighbor and mag[i, j] >= right_neighbor
            # (Hint: implement the mathematical condition of NMS. The current value mag[i,j] must be greater than or equal to left_neighbor AND right_neighbor)
            
            if is_peak:
                Z[i,j] = mag[i,j]
            else:
                Z[i,j] = 0.0
                
    return Z

def auto_canny(img_gray, sigma=0.33):
    """
    Dynamic Canny that adapts to industrial lighting conditions.
    """
    # LEVEL 2 - DESIGN GAP
    median_val = np.median(img_gray)
    lower = int(max(0, (1.0 - sigma) * median_val))
    upper = int(min(255, (1.0 + sigma) * median_val))
    # (Hint: Define lower as the maximum between 0 and (1.0 - sigma) * median_val. Define upper as the minimum between 255 and (1.0 + sigma) * median_val. Force cast to integer 'int()')
    
    edged = cv2.Canny(img_gray, lower, upper)
    return edged

if __name__ == "__main__":
    # Test NMS
    mag_test = np.array([
        [0,  0,  0,  0, 0],
        [0, 10, 50, 20, 0],
        [0, 30, 40, 60, 0],
        [0,  0,  0,  0, 0]
    ], dtype=np.float32)
    theta_test = np.zeros_like(mag_test) # We assume horizontal gradient
    
    nms_result = non_maximum_suppression_vectorized(mag_test, theta_test)
    
    print("\n--- 1. ORIGINAL MAGNITUDE (Thick gradient mountains) ---")
    print(mag_test)
    print("\n--- 2. NMS RESULT (Thinned edges) ---")
    print(nms_result)
    print("\nNOTE: The 50 in row 1 survived because it is greater than 10 and 20.")
    print("NOTE: The 40 in row 2 became 0.0 (black) because its neighbor 60 was higher!")

    # 50 is greater than 10 and 20 -> Should be kept
    assert nms_result[1, 2] == 50.0, "NMS failed to keep the local peak"
    # 40 is not greater than 60 -> Should be suppressed
    assert nms_result[2, 2] == 0.0, "NMS failed to suppress the non-maximum"
    
    # Test Auto Canny
    img_dark = np.ones((100, 100), dtype=np.uint8) * 30
    img_dark[25:75, 25:75] = 40 # Very low contrast
    
    edges = auto_canny(img_dark)
    assert np.max(edges) == 255, "Auto-Canny failed to detect edges in low contrast image"
    
    print("\n--- 3. THRESHOLD CALCULATION (Auto-Canny) ---")
    mediana = np.median(img_dark)
    lower = int(max(0, (1.0 - 0.33) * mediana))
    upper = int(min(255, (1.0 + 0.33) * mediana))
    print(f"Median light detected in the dark image: {mediana}")
    print(f"Lower Threshold (Noise) adjusted to: {lower}")
    print(f"Upper Threshold (Strong Edge) adjusted to: {upper}")
    print("NOTE: If we had used the classic fixed OpenCV Canny (50, 150), it would not have detected ANYTHING because the maximum color of our rock was only 40.")

    print("SUCCESS: Geometric NMS and Adaptive Auto-Canny passed the tests.")