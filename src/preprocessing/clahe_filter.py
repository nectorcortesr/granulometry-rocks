import cv2
import numpy as np

def preprocess_frame(img_bgr):
    """
    It takes a frame from an industrial camera, validates its integrity, 
    and applies CLAHE to reveal structure under mining dust. It returns a normalized image.
    """
    
    if img_bgr is None or img_bgr.size == 0 or np.var(img_bgr) == 0:
        raise ValueError("La imagen de entrada es inválida: vacía, None o sin variación de píxeles.")

    img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))

    img_clahe = clahe.apply(img_gray)
    img_float = img_clahe.astype(np.float32) / 255.0

    return img_gray, img_clahe, img_float

if __name__ == "__main__":
    img_test = np.ones((100, 100, 3), dtype=np.uint8) * 60
    cv2.circle(img_test, (50, 50), 30, (75, 75, 75), -1) 
    
    gray, clahe_out, float_out = preprocess_frame(img_test)

    std_original = np.std(gray)
    std_clahe = np.std(clahe_out)
    
    assert std_clahe > std_original, "El contraste no mejoró tras CLAHE"
    assert float_out.dtype == np.float32, "El tipo de salida es incorrecto para producción"
    assert np.max(float_out) <= 1.0, "La imagen float no está normalizada"
    
    print(f"Desviación estándar Original: {std_original:.2f}")
    print(f"Desviación estándar CLAHE: {std_clahe:.2f}")
    print("SUCCESS: Tests numéricos y de tipos pasados.")