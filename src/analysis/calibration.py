import math

def calibrate_scale(reference_length_px, reference_length_cm):
    """
    Calculate the linear scale factor (cm per pixel).
    """
    # LEVEL 3 - EDGE CASE GAP
    # (Hint: Protect against ZeroDivisionError and absurd negative values. If reference_length_px <= 0, raise explicit ValueError)

    if reference_length_px <= 0:
        raise ValueError("Reference length in pixels must be greater than zero.")
    if reference_length_cm <= 0:
        raise ValueError("Reference length in cm must be greater than zero.")
    
    return reference_length_cm / reference_length_px

def convert_metrics_to_physical(metrics_px, scale_factor_cm_per_px):
    """
    Converts the dictionary of metrics in pixels (Day 19) to physical metrics.
    """
    k = scale_factor_cm_per_px
    
    # LEVEL 1 - MECHANICAL GAP
    area_cm2 = metrics_px["area_px"] * (k ** 2)
    # (Hint: Multiply the area_px by the scale factor SQUARED, according to theory)
    
    equiv_diameter_cm = metrics_px["equiv_diameter_px"] * k
    
    metrics_physical = {
        "area_cm2": area_cm2,
        "equiv_diameter_cm": equiv_diameter_cm,
        "circularity": metrics_px["circularity"]
    }
    return metrics_physical

def classify_rock(equiv_diameter_cm, threshold_medium, threshold_large):
    """
    Classify the rock as Fine, Medium, or Coarse.
    """
    # LEVEL 2 - DESIGN GAP
    if equiv_diameter_cm < threshold_medium:
        clasificacion = "Fine"
    elif equiv_diameter_cm >= threshold_large:
        clasificacion = "Coarse"
    else:
        clasificacion = "Medium"
    # (Hint: Implement conditional logic using if/elif/else. Strictly less than threshold_medium is 'Fine'. Greater than or equal to threshold_large is 'Coarse'. Between both is 'Medium'.)
    
    return clasificacion

if __name__ == "__main__":
    # Test: Reference ball of 10 cm measures 100 pixels.
    ref_px = 100.0
    ref_cm = 10.0
    k_factor = calibrate_scale(ref_px, ref_cm)
    
    assert k_factor == 0.1, "Error in scale factor calculation"
    
    # Simulate the output from Day 19 for a rock
    rock_mock = {
        "area_px": 5000, 
        "equiv_diameter_px": math.sqrt(4 * 5000 / math.pi),
        "circularity": 0.8
    }
    
    physics = convert_metrics_to_physical(rock_mock, k_factor)
    
    # The area of ​​5000 px * (0.1)^2 should be 50 cm^2
    assert abs(physics["area_cm2"] - 50.0) < 1e-5, f"Area conversion failed. Got {physics['area_cm2']}"
    
    diam_cm = physics["equiv_diameter_cm"]
    clase = classify_rock(diam_cm, threshold_medium=5.0, threshold_large=10.0)
    
    # The equivalent diameter should be ~7.97 cm, which falls into the 'Medium' category
    assert clase == "Medium", f"Incorrect classification: {clase} for diameter {diam_cm:.2f} cm"
    
    print("SUCCESS: Physical calibration and classification tested successfully.")
    print(f"Calculated physical diameter: {diam_cm:.2f} cm -> Class: {clase}")