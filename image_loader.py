import pydicom
import numpy as np

def load_dicom(file_path):
    """
    Loads a DICOM file and returns the image array.
    Args:
        file_path (str): Path to the DICOM file.
    Returns:
        numpy.ndarray: Image data as a NumPy array.
    """
    try:
        dicom_data = pydicom.dcmread(file_path)
        image_array = dicom_data.pixel_array.astype(np.float32)
        return image_array
    except Exception as e:
        raise ValueError(f"Error loading DICOM file: {e}")
