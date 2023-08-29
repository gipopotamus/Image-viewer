from PyQt6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QPushButton, QFileDialog, QWidget
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt, QPoint
from config import SCALE_STEP, MAX_SCALE, MIN_SCALE


class ImageViewer(QMainWindow):
    """
    Главное окно приложения для просмотра изображений.
    """

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        """
        Инициализация пользовательского интерфейса.
        """
        self.setWindowTitle("Image Viewer")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.image_label)

        self.open_button = QPushButton("Открыть изображение", self)
        self.open_button.clicked.connect(self.openImage)
        self.layout.addWidget(self.open_button)

        self.scale_factor = 1.0
        self.max_scale = 3.0
        self.min_scale = 0.2

        self.origin = QPoint()
        self.last_pos = QPoint()

        self.coordinates = []

    def openImage(self):
        """
        Открывает и отображает выбранное изображение.
        """
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Открыть изображение", "", "Изображения (*.jpg *.png *.bmp *.jpeg)")

        if file_name:
            image = QImage(file_name)
            if image.isNull():
                return

            self.pixmap = QPixmap.fromImage(image)
            self.image_label.setPixmap(self.pixmap.scaled(
                self.pixmap.size() * self.scale_factor, Qt.AspectRatioMode.KeepAspectRatio))
            self.image_label.adjustSize()

    def wheelEvent(self, event):
        """
        Обрабатывает событие прокрутки колеса мыши для масштабирования.
        """
        if self.pixmap:
            delta = event.angleDelta().y() / 120.0
            factor = 1.0 + SCALE_STEP if delta > 0 else 1.0 - SCALE_STEP
            new_scale = self.scale_factor * factor

            if MIN_SCALE <= new_scale <= MAX_SCALE:
                self.scale_factor = new_scale

                self.image_label.setPixmap(self.pixmap.scaled(
                    self.pixmap.size() * self.scale_factor, Qt.AspectRatioMode.KeepAspectRatio))
                self.image_label.adjustSize()

    def mousePressEvent(self, event):
        """
        Обрабатывает события нажатия кнопок мыши.
        """
        if event.button() == Qt.MouseButton.RightButton:
            self.origin = QPoint(event.pos())
        elif event.button() == Qt.MouseButton.LeftButton:
            x = round(event.pos().x() / self.scale_factor, 1)
            y = round(event.pos().y() / self.scale_factor, 1)
            self.coordinates.append((len(self.coordinates) + 1, x, y))
            print("Координаты:", self.coordinates)

    def mouseMoveEvent(self, event):
        """
        Обрабатывает события перемещения мыши для перетаскивания изображения.
        """
        if event.buttons() & Qt.MouseButton.RightButton:
            delta = event.pos() - self.origin
            self.image_label.move(self.image_label.pos() + delta)
            self.origin = QPoint(event.pos())
