import os
import numpy as np
import pydicom
import nibabel as nib
from PyQt5.QtWidgets import QMessageBox

def load_image(file_path):
    if not file_path:
        QMessageBox.warning(None, "Warning", "No file selected!")
        return None

    try:
        if file_path.lower().endswith('.dcm'):
            # Read the selected DICOM file.
            dicom_data = pydicom.dcmread(file_path)
            if hasattr(dicom_data, 'NumberOfFrames'):
                # Multi-frame DICOM: use the pixel_array directly.
                image_array = dicom_data.pixel_array.astype(np.float32)
            else:
                # Single file DICOM. Assume it's part of a series.
                folder = os.path.dirname(file_path)
                dicom_files = [os.path.join(folder, f) for f in os.listdir(folder) if f.lower().endswith('.dcm')]
                
                # If only one DICOM file is found, use it.
                if len(dicom_files) == 1:
                    image_array = dicom_data.pixel_array.astype(np.float32)
                else:
                    # Load each file and sort by InstanceNumber (if available).
                    slices = []
                    for f in dicom_files:
                        ds = pydicom.dcmread(f)
                        try:
                            instance = int(ds.InstanceNumber)
                        except Exception:
                            instance = 0
                        slices.append((instance, ds))
                    slices.sort(key=lambda x: x[0])
                    
                    # Stack the pixel data from all slices along a new axis.
                    slice_arrays = [s[1].pixel_array for s in slices]
                    image_array = np.stack(slice_arrays, axis=-1).astype(np.float32)
        else:
            # NIfTI case: load the full volume.
            nifti_img = nib.load(file_path)
            nifti_data = nifti_img.get_fdata()
            if nifti_data.ndim >= 3:
                image_array = nifti_data.astype(np.float32)
            else:
                image_array = nifti_data.squeeze().astype(np.float32)

        return image_array

    except Exception as e:
        QMessageBox.critical(None, "Error", f"Failed to load image:\n{e}")
        return None
