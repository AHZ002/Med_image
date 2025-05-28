# 🩺 Medical Imaging Viewer and Segmentation Tool

An open-source Python-based desktop application for loading, visualizing, and manipulating medical images in DICOM and NIfTI formats. Built with a user-friendly GUI for clinicians and researchers.

## 🚀 Features

* 📂 Load and display 2D/3D medical images (DICOM & NIfTI)
* 🔧 Basic image manipulations:

  * Zoom
  * Contrast adjustment (real-time slider)
  * Rotation (90° increments)
  * Vertical flip
* 💾 Save processed images in PNG or JPEG format
* 🖥️ Navigate multi-slice datasets with ease
* 🧑‍💻 GUI built using **PyQt5**

## 🛠️ Project Structure

* `main.py`: Entry point for the application; initializes and runs the GUI
* `gui.py`: Manages the PyQt5-based graphical user interface
* `image_loader.py`: Loads and preprocesses DICOM/NIfTI images
* `image_processor.py`: Provides manipulation tools (zoom, rotate, contrast, flip)
* `requirements.txt`: Lists all Python dependencies

## 📦 Installation & Usage

### ✅ Requirements

* Python 3.8 or higher
* Install dependencies:

```bash
pip install -r requirements.txt
```

### ▶️ Run the Application

Make sure all Python files are in the same directory. Then run:

```bash
python main.py
```

## 📁 File Format Support

* DICOM (.dcm)
* NIfTI (.nii, .nii.gz)

Supports both single-slice and multi-slice volumes, with slice navigation for 3D datasets.

## 🔍 Notes

* **Segmentation functionality using MedSAM** is provided separately in a Jupyter Notebook (`medsam_segmentation.ipynb`).
* This notebook can be used independently to perform deep learning-based medical image segmentation.

## 🧩 Future Enhancements

* 3D volumetric rendering
* Modular plugin system for extending tools
* Natural language support via large language models

---

## 👨‍⚕️ Acknowledgment

Developed as part of an internship project to create a foundation for advanced medical imaging tools.

