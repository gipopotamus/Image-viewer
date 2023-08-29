import sys
from PyQt6.QtWidgets import QApplication
from viewer_window import ImageViewer

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageViewer()
    window.show()
    sys.exit(app.exec())
