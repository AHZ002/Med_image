import sys
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QLabel, QPushButton,
    QSlider, QFileDialog, QHBoxLayout, QWidget, QMessageBox
)
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
from image_loader import load_image
from image_processor import adjust_contrast, rotate_image, flip_image, zoom_image

class MedicalImageViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Medical Image Viewer")
        self.setGeometry(100, 100, 1000, 800)

        self.image_array = None       # Currently active 2D slice
        self.image_volume = None      # Full volume if multi-slice
        self.current_image = None     # Processed image for display
        self.zoom_factor = 1.0
        self.rotation_angle = 0

        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        self.image_label = QLabel("No image loaded")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setScaledContents(True)
        main_layout.addWidget(self.image_label, stretch=1)

        controls_layout = QHBoxLayout()
        load_button = QPushButton("Load DICOM/NIfTI Image")
        load_button.clicked.connect(self.load_image)
        controls_layout.addWidget(load_button)

        save_button = QPushButton("Save Image")
        save_button.clicked.connect(self.save_image)
        controls_layout.addWidget(save_button)

        controls_layout.addWidget(QLabel("Contrast:"))
        self.contrast_slider = QSlider(Qt.Horizontal)
        self.contrast_slider.setRange(1, 300)
        self.contrast_slider.setValue(100)
        self.contrast_slider.valueChanged.connect(self.adjust_contrast)
        controls_layout.addWidget(self.contrast_slider)

        rotate_button = QPushButton("Rotate 90°")
        rotate_button.clicked.connect(self.rotate_image)
        controls_layout.addWidget(rotate_button)

        flip_button = QPushButton("Flip Vertically")
        flip_button.clicked.connect(self.flip_image)
        controls_layout.addWidget(flip_button)

        controls_layout.addWidget(QLabel("Zoom:"))
        self.zoom_slider = QSlider(Qt.Horizontal)
        self.zoom_slider.setRange(100, 300)
        self.zoom_slider.setValue(100)
        self.zoom_slider.valueChanged.connect(self.zoom_image)
        controls_layout.addWidget(self.zoom_slider)

        main_layout.addLayout(controls_layout)

        slice_layout = QHBoxLayout()
        self.slice_label = QLabel("Slice:")
        slice_layout.addWidget(self.slice_label)
        self.slice_slider = QSlider(Qt.Horizontal)
        self.slice_slider.setRange(0, 0)
        self.slice_slider.valueChanged.connect(self.change_slice)
        self.slice_slider.setMinimumWidth(200)
        slice_layout.addWidget(self.slice_slider)
        main_layout.addLayout(slice_layout)

        self.slice_slider.setVisible(False)
        self.slice_label.setVisible(False)

    def load_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            None, "Open Medical Image", "",
            "Medical Images (*.dcm *.nii *.nii.gz)"
        )
        
        loaded = load_image(file_path)
        if loaded is not None:
            self.contrast_slider.setValue(100)
            self.zoom_slider.setValue(100)
            self.rotation_angle = 0

            if loaded.ndim == 2:
                self.image_array = loaded
                self.image_volume = None
                self.slice_slider.setVisible(False)
                self.slice_label.setVisible(False)
            elif loaded.ndim == 3:
                self.image_volume = loaded
                total_slices = loaded.shape[2]
                default_idx = total_slices // 2
                self.image_array = loaded[:, :, default_idx]
                self.slice_slider.setRange(0, total_slices - 1)
                self.slice_slider.setValue(default_idx)
                self.slice_slider.setVisible(True)
                self.slice_label.setVisible(True)
                print("Number of slices:", total_slices)
            elif loaded.ndim == 4:
                self.image_volume = loaded
                total_slices = loaded.shape[2]
                default_idx = total_slices // 2
                self.image_array = loaded[:, :, default_idx, 0]
                self.slice_slider.setRange(0, total_slices - 1)
                self.slice_slider.setValue(default_idx)
                self.slice_slider.setVisible(True)
                self.slice_label.setVisible(True)
                print("Number of slices:", total_slices)

            self.current_image = self.image_array.copy()
            self.display_image(self.current_image)

    def change_slice(self):
        if self.image_volume is None:
            return
        
        idx = self.slice_slider.value()
        if self.image_volume.ndim == 3:
            self.image_array = self.image_volume[:, :, idx]
        elif self.image_volume.ndim == 4:
            self.image_array = self.image_volume[:, :, idx, 0]
        
        self.contrast_slider.setValue(100)
        self.zoom_slider.setValue(100)
        self.rotation_angle = 0

        self.current_image = self.image_array.copy()
        self.display_image(self.current_image)

    def save_image(self):
        if self.current_image is None:
            QMessageBox.warning(None, "Warning", "No image to save!")
            return

        file_path, selected_filter = QFileDialog.getSaveFileName(
            None, "Save Image", "",
            "PNG Image (*.png);;JPEG Image (*.jpg *.jpeg)"
        )

        if not file_path:
            return

        try:
            normalized_image = ((self.current_image - np.min(self.current_image)) /
                               (np.max(self.current_image) - np.min(self.current_image)) * 255).astype(np.uint8)
            height, width = normalized_image.shape
            byte_array = normalized_image.tobytes()
            qt_image = QImage(byte_array, width, height, QImage.Format_Grayscale8)

            if selected_filter.startswith("PNG"):
                success = qt_image.save(file_path, "PNG")
            else:
                success = qt_image.save(file_path, "JPEG", quality=90)

            if not success:
                QMessageBox.critical(None, "Error", "Failed to save image!")
            else:
                QMessageBox.information(None, "Success", "Image saved successfully!")

        except Exception as e:
            QMessageBox.critical(None, "Error", f"Failed to save image:\n{e}")

    def display_image(self, image):
        normalized_image = ((image - np.min(image)) / (np.max(image) - np.min(image)) * 255).astype(np.uint8)
        height, width = normalized_image.shape
        byte_array = normalized_image.tobytes()
        qt_image = QImage(byte_array, width, height, QImage.Format_Grayscale8)
        pixmap = QPixmap.fromImage(qt_image)
        self.image_label.setPixmap(pixmap)

    def adjust_contrast(self):
        if self.image_array is None:
            return
        factor = self.contrast_slider.value() / 100.0
        self.current_image = adjust_contrast(self.image_array, factor)
        self.display_image(self.current_image)

    def rotate_image(self):
        if self.current_image is None:
            return
        self.rotation_angle = (self.rotation_angle + 90) % 360
        self.current_image = rotate_image(self.current_image, 90)
        self.display_image(self.current_image)

    def flip_image(self):
        if self.current_image is None:
            return
        self.current_image = flip_image(self.current_image)
        self.display_image(self.current_image)

    def zoom_image(self):
        if self.image_array is None:
            return
        self.zoom_factor = max(1.0, self.zoom_slider.value() / 100.0)
        self.current_image = zoom_image(self.image_array, self.zoom_factor)
        self.display_image(self.current_image)
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MedicalImageViewer()
    window.show()
    sys.exit(app.exec_())
