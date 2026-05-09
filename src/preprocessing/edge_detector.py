import cv2
import numpy as np

def compute_gradients(img_float, sigma=1.0):
    """
    It takes an image in float32 format and returns the spatial edge components.
    Returns: gx, gy, magnitude, orientation.
    """
    # LEVEL 3 - EDGE CASE GAP
    if img_float is None or img_float.size == 0 or np.var(img_float) == 0:
        raise ValueError("Input image is invalid: empty, None, or no pixel variation.")

    # LEVEL 2 - DESIGN GAP
    ksize = int(np.ceil(3 * sigma) * 2 + 1)
    
    # Separable Gaussian smoothing O(N*k)
    img_smoothed = cv2.GaussianBlur(img_float, (ksize, ksize), sigmaX=sigma)

    # Sobel gradients in float32 to retain negative signs of the derivative
    gx = cv2.Sobel(img_smoothed, cv2.CV_32F, 1, 0, ksize=3)
    gy = cv2.Sobel(img_smoothed, cv2.CV_32F, 0, 1, ksize=3)

    # LEVEL 1 - MECHANICAL GAP
    magnitude = np.sqrt(np.square(gx) + np.square(gy))
    # (Hint: Apply the M(x,y) equation from the theory, combining np.square and np.sqrt over gx and gy)
    
    # Orientation in radians (-pi to pi)
    orientation = np.arctan2(gy, gx)

    return gx, gy, magnitude, orientation

if __name__ == "__main__":
    # Geometric regression test: Hard and predictable vertical edge
    # Black image with a pure white rectangle in the center
    img_test = np.zeros((100, 100), dtype=np.float32)
    img_test[:, 50:] = 1.0

    gx, gy, mag, ori = compute_gradients(img_test, sigma=0.5)

    # The gradient on the X-axis MUST react to the change in columns 49-50
    assert np.max(np.abs(gx[:, 49:51])) > 0.5, "Gradient X failed to detect the left vertical edge"
    
    # In a pure vertical edge (change in X, constant in Y), the gradient in Y is ~0
    assert np.max(np.abs(gy[:, 49:51])) < 0.2 * np.max(np.abs(gx[:, 49:51])), "Gradient leakage in Y over a purely vertical edge"
    
    print("max gx:", np.max(np.abs(gx)))
    print("max gy:", np.max(np.abs(gy)))
    print("SUCCESS: Directional derivative tests passed.")
    print(f"Maximum magnitude detected: {np.max(mag):.4f}")

    