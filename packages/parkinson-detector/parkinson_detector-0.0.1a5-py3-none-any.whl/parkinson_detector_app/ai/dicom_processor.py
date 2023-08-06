
import os

from PyQt5.QtCore import Qt, QObject, QThread, QTimer
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtGui import QImage
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.preprocessing.image import img_to_array
from pydicom import dcmread
from pydicom.fileset import FileSet
import numpy as np
import PIL

from parkinson_detector_app.ai.model_worker import NeuralProcessor


def load_image(filename):
    """# load and prepare the image

    Parameters
    ----------
    filename : [type]
        [description]

    Returns
    -------
    [type]
        [description]
    """
    # load the image
    img = load_img(filename, target_size=(224, 224))
    orig_img = load_img(filename)
    # convert to array
    img = img_to_array(img)
    orig_img = img_to_array(orig_img)
    # reshape into a single sample with 3 channels
    img = img.reshape(1, 224, 224, 3)
    # center pixel data
    img = img.astype('float32')
    return orig_img.astype(np.uint8), img


class DicomProcessor(QObject):
    file_opened = pyqtSignal(str)
    error = pyqtSignal(int, str)
    preview_loaded = pyqtSignal(QImage)
    classification_result = pyqtSignal(np.ndarray)
    process_image = pyqtSignal(np.ndarray)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._current_dicom_path = None
        self._neural_processor = NeuralProcessor(self.classification_result)
        self.process_image.connect(self._neural_processor.process_file)

    def _open_dicom_file(self, file_path):
        self._current_dicom_path = file_path
        self._current_dicom_ds = dcmread(self._current_dicom_path)
        self._current_dicom_ds.decompress()
        arr = self._current_dicom_ds.pixel_array
        self.file_opened.emit(file_path)
        arr = arr.astype(np.float32)
        arr = arr / arr.max() * 255
        arr = arr.astype(np.uint8)
        dicom_preview_image = QImage(
            arr.data, arr.shape[1], arr.shape[0], arr.shape[1], QImage.Format_Grayscale8)
        self.load_preview(dicom_preview_image, arr)

    def _open_image_file(self, file_path):
        print("_open_image_file", file_path)
        orig_img, img = load_image(file_path)
        self.file_opened.emit(file_path)
        dicom_preview_image = QImage(file_path)
        self.load_preview(dicom_preview_image, img)

    def load_preview(self, dicom_preview_image, frame):
        raw_img = frame.copy()
        self.preview_loaded.emit(dicom_preview_image)
        print("Call process_image")
        self.process_image.emit(raw_img)

    @pyqtSlot(str)
    def process_file(self, file_path: str):
        print("process_file", file_path)
        filename, file_extension = os.path.splitext(file_path)
        if file_extension == '.dcm':
            self._open_dicom_file(file_path)
        else:
            try:
                self._open_image_file(file_path)
            except PIL.UnidentifiedImageError:
                self.error.emit(-1, "Only Dicom or image files are accepted")
