from PyQt5.QtCore import Qt, QThread, QTimer, QEvent
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QSlider
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QSizePolicy
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QMessageBox


class DicomPreviewWidget(QWidget):
    """The class represents the  GUI widget"""
    error = pyqtSignal(int, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._current_image = None

        self.initUI()

    def initUI(self):
        self._canvas = QLabel()
        self._canvas.setText("Drop file here")
        self._canvas.setAlignment(Qt.AlignCenter)
        self._canvas.setSizePolicy(
            QSizePolicy.Ignored, QSizePolicy.Ignored)
        self._canvas.installEventFilter(self)
        self._root_layout = QVBoxLayout()
        self._root_layout.addWidget(self._canvas)

        self.setLayout(self._root_layout)

    def eventFilter(self, source, event):
        if (source is self._canvas and event.type() == QEvent.Resize):
            # re-scale the pixmap when the label resizes
            if self._current_image is not None:
                self._canvas.setPixmap(self._current_image.scaled(
                    self._canvas.size()*0.95, Qt.KeepAspectRatio,
                    Qt.SmoothTransformation))
        return super().eventFilter(source, event)

    @pyqtSlot(QImage)
    def setPreview(self, image):
        """sets the image on the screen"""
        print(image)
        try:
            self._current_image = QPixmap.fromImage(image)
        except Exception as e:
            print(e.with_traceback)
        self._canvas.setPixmap(self._current_image.scaled(
            self._canvas.size(), Qt.KeepAspectRatio,
            Qt.SmoothTransformation))
