from PyQt5.QtWidgets import (
    QMainWindow, QVBoxLayout, QLabel, QPushButton,
    QSlider, QFileDialog, QHBoxLayout, QWidget, QMessageBox
)
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
from image_loader import load_dicom
from image_processor import normalize_image, adjust_contrast, rotate_image, flip_image, zoom_image

class MedicalImageViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Medical Image Viewer")
        self.setGeometry(100, 100, 1000, 800)

        self.image_array = None
        self.current_image = None

        # Main Layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Image Display
        self.image_label = QLabel("No image loaded")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setScaledContents(True)
        self.layout.addWidget(self.image_label)

        # Buttons Layout
        buttons_layout = QHBoxLayout()

        # Load Button
        self.load_button = QPushButton("Load DICOM Image")
        self.load_button.clicked.connect(self.load_dicom_image)
        buttons_layout.addWidget(self.load_button)

        # Contrast Slider
        self.contrast_slider = QSlider(Qt.Horizontal)
        self.contrast_slider.setRange(1, 300)
        self.contrast_slider.setValue(100)
        self.contrast_slider.valueChanged.connect(self.update_contrast)
        buttons_layout.addWidget(QLabel("Contrast:"))
        buttons_layout.addWidget(self.contrast_slider)

        # Rotate Button
        self.rotate_button = QPushButton("Rotate 90°")
        self.rotate_button.clicked.connect(self.rotate_image)
        buttons_layout.addWidget(self.rotate_button)

        # Flip Button
        self.flip_button = QPushButton("Flip Vertically")
        self.flip_button.clicked.connect(self.flip_image)
        buttons_layout.addWidget(self.flip_button)

        # Zoom Slider
        self.zoom_slider = QSlider(Qt.Horizontal)
        self.zoom_slider.setRange(1, 300)
        self.zoom_slider.setValue(100)
        self.zoom_slider.valueChanged.connect(self.zoom_image)
        buttons_layout.addWidget(QLabel("Zoom:"))
        buttons_layout.addWidget(self.zoom_slider)

        self.layout.addLayout(buttons_layout)

    def load_dicom_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open DICOM File", "", "DICOM Files (*.dcm)")
        if file_path:
            try:
                self.image_array = load_dicom(file_path)
                self.current_image = self.image_array.copy()
                self.display_image(self.current_image)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load DICOM file:\n{e}")

    def display_image(self, image):
        try:
            normalized = normalize_image(image)
            height, width = normalized.shape
            byte_array = normalized.tobytes()
            qt_image = QImage(byte_array, width, height, QImage.Format_Grayscale8)
            pixmap = QPixmap.fromImage(qt_image)
            self.image_label.setPixmap(pixmap)
        except Exception as e:
            QMessageBox.critical(self, "Display Error", f"Failed to display image:\n{e}")

    def update_contrast(self):
        if self.image_array is not None:
            factor = self.contrast_slider.value() / 100.0
            self.current_image = adjust_contrast(self.image_array, factor)
            self.display_image(self.current_image)

    def rotate_image(self):
        if self.image_array is not None:
            self.current_image = rotate_image(self.current_image, 90)
            self.display_image(self.current_image)

    def flip_image(self):
        if self.image_array is not None:
            self.current_image = flip_image(self.current_image)
            self.display_image(self.current_image)

    def zoom_image(self):
        if self.image_array is not None:
            factor = self.zoom_slider.value() / 100.0
            try:
                self.current_image = zoom_image(self.current_image, factor)
                self.display_image(self.current_image)
            except Exception as e:
                QMessageBox.critical(self, "Zoom Error", f"An error occurred during zoom:\n{e}")
