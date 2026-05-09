import cv2
import numpy as np

def dilate_scratch(img_bin, kernel):
    """
    Morphological dilation from zero (Spatial Max Filter)
    img_bin and kernel contain 0s and 1s.
    """
    # LEVEL 3 - EDGE CASE GAP
    if not (np.array_equal(img_bin, img_bin.astype(bool)) and np.array_equal(kernel, kernel.astype(bool))):
        raise ValueError("Both image and kernel must be binary (0 and 1).")

    k_h, k_w = kernel.shape
    pad_h, pad_w = k_h // 2, k_w // 2
    
    img_padded = np.pad(img_bin, ((pad_h, pad_h), (pad_w, pad_w)), mode='constant', constant_values=0)
    out = np.zeros_like(img_bin)
    
    for i in range(img_bin.shape[0]):
        for j in range(img_bin.shape[1]):
            region = img_padded[i:i+k_h, j:j+k_w]
            # LEVEL 2 - DESIGN GAP
            out[i, j] = np.max(region * kernel)
            # (Hint: In dilation, if there is overlap between the 1s of the kernel and the region, the center becomes 1. Which numpy function evaluates the maximum of the element-wise multiplication?)
            
    return out

def erode_scratch(img_bin, kernel):
    """
    Morphological erosion from zero (Spatial Min Filter)
    img_bin and kernel contain 0s and 1s.
    """
    k_h, k_w = kernel.shape
    pad_h, pad_w = k_h // 2, k_w // 2
    
    img_padded = np.pad(img_bin, ((pad_h, pad_h), (pad_w, pad_w)), mode='constant', constant_values=0)
    out = np.zeros_like(img_bin)
    
    # We precalculate the kernel weight sum
    k_sum = np.sum(kernel)
    
    for i in range(img_bin.shape[0]):
        for j in range(img_bin.shape[1]):
            region = img_padded[i:i+k_h, j:j+k_w]
            # For erosion, the kernel MUST be completely contained within the region
            match = np.sum(region * kernel)
            if match == k_sum:
                out[i, j] = 1
            else:
                out[i, j] = 0
                
    return out

def apply_closing(img_edges, ksize=5):
    """
    Apply closing to close Canny edges.
    """
    kernel = np.ones((ksize, ksize), np.uint8)
    
    # We normalize to pure binary 0s and 1s for our scratch function
    img_bin = (img_edges > 0).astype(np.uint8)
    
    # LEVEL 1 - MECHANICAL GAP
    dilated = dilate_scratch(img_bin, kernel)
    closed = erode_scratch(dilated, kernel)
    # (Hint: Implement mathematically the Closing by calling the scratch functions we just created in the correct order)
    
    return closed * 255 # Return to 0-255

if __name__ == "__main__":
    # Test: Rock edge with a 1 pixel "gap" (noise)
    edges_test = np.array([
        [0, 0, 0, 0, 0, 0],
        [0, 1, 1, 0, 1, 0], # Gap in column 3
        [0, 0, 0, 0, 0, 0]
    ], dtype=np.uint8)
    
    kernel_1d = np.array([[1, 1, 1]], dtype=np.uint8)
    
    dilated_res = dilate_scratch(edges_test, kernel_1d)
    eroded_res = erode_scratch(dilated_res, kernel_1d)
    
    print("--- 1. Original Broken Edge ---")
    print(edges_test)
    print("--- 2. Dilation (Max) ---")
    print(dilated_res)
    print("--- 3. Final Closing (Gap closed without expanding the ends) ---")
    print(eroded_res)

    # We verify that the Closing repaired the gap (index 1,3)
    assert eroded_res[1, 3] == 1, "Closing failed to fill the internal gap."
    # We verify that it did not artificially expand
    assert eroded_res[1, 0] == 0 and eroded_res[1, 5] == 0, "Closing expandió falsamente los límites."
    
    print("SUCCESS: Mathematical Morphology manual verified against set logic")