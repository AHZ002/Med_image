import pydicom
import numpy as np
import matplotlib.pyplot as plt
import cv2  # OpenCV for better resizing
from PyQt5.QtWidgets import QMessageBox

def load_dicom_image(file_path):
    """Loads a single slice from a DICOM file and normalizes it."""
    try:
        dicom_data = pydicom.dcmread(file_path)
        dicom_array = dicom_data.pixel_array.astype(np.float32)  # Keep intensity range
        return dicom_array
    except Exception as e:
        print(f"Error loading DICOM file: {e}")
        QMessageBox.critical(None, "DICOM Load Error", f"An error occurred while loading DICOM:\n{e}")
        return None

def zoom_image(image, zoom_factor):
    """Properly zooms into the DICOM image while preserving quality."""
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

def display_images(original, zoomed):
    """Displays the original and zoomed images side by side."""
    try:
        if original is None or zoomed is None:
            raise ValueError("Invalid images provided for display.")

        fig, axes = plt.subplots(1, 2, figsize=(10, 5))
        axes[0].imshow(original, cmap='gray')
        axes[0].set_title("Original DICOM Slice")
        axes[0].axis("off")

        axes[1].imshow(zoomed, cmap='gray')
        axes[1].set_title("Zoomed Image (No Hole)")
        axes[1].axis("off")

        plt.show()
    except Exception as e:
        print(f"Error displaying images: {e}")
        QMessageBox.critical(None, "Display Error", f"An error occurred while displaying images:\n{e}")

# Example Usage
dicom_path = "E:/AHZ/IIT Hyderabad/MR000000.dcm"  # Replace with actual file path
dicom_image = load_dicom_image(dicom_path)

if dicom_image is not None:
    zoom_factor = 1.5  # Adjust zoom level as needed
    zoomed_image = zoom_image(dicom_image, zoom_factor)
    display_images(dicom_image, zoomed_image)
