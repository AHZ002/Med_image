import sys
from PyQt5.QtWidgets import QApplication
from gui import MedicalImageViewer

if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = MedicalImageViewer()
    viewer.show()
    sys.exit(app.exec_())
