import cv2
import numpy as np

def measure_contour(contour):
    """
    It takes a raw outline from OpenCV and calculates its basic geometric properties.
    It returns a dictionary with the metrics.
    """
    area = cv2.contourArea(contour)
    perimeter = cv2.arcLength(contour, True)  # True = closed contour
    x, y, w, h = cv2.boundingRect(contour)
    
    # LEVEL 3 - EDGE CASE GAP
    circularity = 0.0
    if perimeter > 0:
        circularity = 4 * np.pi * area / (perimeter ** 2)
    # (Hint: Protect the division in the equation C = 4*pi*A / P^2. If the perimeter is 0 (e.g., an anomalous point), the circularity should be explicitly 0.0 to avoid ZeroDivisionError)

    # LEVEL 1 - MECHANICAL GAP
    equivalent_diameter = np.sqrt(4 * area / np.pi)
    # (Hint: Implement the D_eq equation shown in the theory using np.sqrt and np.pi on the 'area' variable)
    metrics = {
        "area_px": area,
        "perimeter_px": perimeter,
        "bbox": (x, y, w, h),
        "circularity": circularity,
        "equiv_diameter_px": equivalent_diameter
    }
    return metrics

def find_rock_contours(img_bin, min_area_px):
    """
    Finds contours in a binary image (rocks=255, background=0) and filters them.
    """
    # LEVEL 2 - DESIGN GAP
    mode = cv2.RETR_EXTERNAL
    # (Hint: In cv2.findContours, which retrieval mode extracts ONLY the extreme outer boundary of the rock and ignores internal "holes" in case the Closing partially failed? Options: cv2.RETR_TREE, cv2.RETR_LIST, cv2.RETR_EXTERNAL)
    
    contours, _ = cv2.findContours(img_bin, mode, cv2.CHAIN_APPROX_SIMPLE)
    
    valid_contours = []
    valid_metrics = []
    
    for cnt in contours:
        metrics = measure_contour(cnt)
        if metrics["area_px"] >= min_area_px:
            valid_contours.append(cnt)
            valid_metrics.append(metrics)
            
    return valid_contours, valid_metrics

if __name__ == "__main__":
    # Synthetic test: A perfect 10x10 square
    test_img = np.zeros((50, 50), dtype=np.uint8)
    test_img[20:30, 20:30] = 255
    
    contours, metrics_list = find_rock_contours(test_img, min_area_px=10)
    
    assert len(contours) == 1, "The figure was not detected."
    
    m = metrics_list[0]
    # A 10x10 square has an area of 100
    assert m["area_px"] == 81, f"Incorrect area: {m['area_px']}"
    # Perimeter of a 10x10 square is 40
    assert m["perimeter_px"] == 36, f"Incorrect perimeter: {m['perimeter_px']}"
    # Circularity of a square is pi/4 (approx 0.785)
    assert 0.78 < m["circularity"] < 0.79, f"Incorrect circularity: {m['circularity']}"
    
    print("SUCCESS: Geometric metrics (Area, Perimeter, D_eq, Circularity) calculated correctly.")
    print(f"Synthetic square metrics: {m}")