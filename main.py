import sys
from PyQt5.QtWidgets import QApplication
from gui import MedicalImageViewer

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MedicalImageViewer()
    window.show()
    sys.exit(app.exec_())