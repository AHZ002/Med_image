import numpy as np
from skimage.transform import rescale, rotate
from PyQt5.QtWidgets import QMessageBox
import cv2

def adjust_contrast(image, factor):
    contrast_image = image * factor
    contrast_image = np.clip(contrast_image, 0, 255).astype(np.uint8)
    return contrast_image

def rotate_image(image, angle):
    rotated_image = rotate(image, angle=angle, resize=True, preserve_range=True).astype(image.dtype)
    return rotated_image

def flip_image(image):
    flipped_image = np.flipud(image)
    return flipped_image

def zoom_image(image, zoom_factor):
    """Properly zooms into the image while preserving quality."""
    try:
        h, w = image.shape
        new_h, new_w = int(h / zoom_factor), int(w / zoom_factor)

        if new_h <= 0 or new_w <= 0:
            raise ValueError("Zoom factor too large, resulting in zero or negative dimensions.")

        # Compute cropping coordinates (center crop)
        start_x, start_y = (w - new_w) // 2, (h - new_h) // 2
        cropped_image = image[start_y:start_y+new_h, start_x:start_x+new_w]

        # Resize using OpenCV's bicubic interpolation to avoid artifacts
        zoomed_image = cv2.resize(cropped_image, (w, h), interpolation=cv2.INTER_CUBIC)

        return zoomed_image
    except Exception as e:
        print(f"Error zooming image: {e}")
        QMessageBox.critical(None, "Zoom Error", f"An error occurred while zooming:\n{e}")
        return None
