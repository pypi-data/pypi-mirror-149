from PyQt5.QtCore import Qt, QThread, QTimer, QEvent
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QSlider
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QSizePolicy, QSpacerItem
from PyQt5.QtGui import QImage, QPixmap, QFont
from PyQt5.QtWidgets import QMessageBox
import numpy as np

from parkinson_detector_app.common.const import PREDICTION_STRING_FORMAT, PREDICTION_CAPTIONS


class ResultPreviewWidget(QWidget):
    """The class represents the  GUI widget"""
    error = pyqtSignal(int, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._current_image = None
        self.initUI()

    def initUI(self):
        self._root_layout = QVBoxLayout()

        result_caption = QLabel("Prediction")
        f = QFont("Arial", 14, QFont.Bold)
        result_caption.setFont(f)
        self._root_layout.addWidget(result_caption)

        self._prediction_lbl = QLabel("")
        self._root_layout.addWidget(self._prediction_lbl)

        self._root_layout.addStretch()

        self.setLayout(self._root_layout)

        self.clear()

    @pyqtSlot()
    def clear(self):
        self._prediction_lbl.setText(PREDICTION_STRING_FORMAT.format(
            method_FRLF="Undefined",
            sum_rule="Undefined",
            majority_voting="Undefined",
            product_rule="Undefined"))

    @pyqtSlot(np.ndarray)
    def fill_results(self, rates):
        method_FRLF = int(rates[0])
        sum_rule = int(rates[1])
        product_rule = int(rates[2])
        majority_voting = int(rates[2])

        self._prediction_lbl.setText(PREDICTION_STRING_FORMAT.format(
            method_FRLF=PREDICTION_CAPTIONS[method_FRLF],
            sum_rule=PREDICTION_CAPTIONS[sum_rule],
            majority_voting=PREDICTION_CAPTIONS[product_rule],
            product_rule=PREDICTION_CAPTIONS[majority_voting]))
