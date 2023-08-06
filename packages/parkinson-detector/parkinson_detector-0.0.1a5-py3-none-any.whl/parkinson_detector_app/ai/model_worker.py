import os
import re
from PyQt5.QtCore import Qt, QObject, QThread
from PyQt5.QtCore import pyqtSlot, pyqtSignal

from tensorflow.keras.models import load_model
from tensorflow.keras import backend as K

import numpy as np
import cv2

from parkinson_detector_app.common.files import model_full_path
from parkinson_detector_app.common.settings import XRaySettings
from parkinson_detector_app.util.gdrive import download_file_from_google_drive
import parkinson_detector_app.ai.ensemble_rules as er


class LocalNeuralProcessor(QObject):
    """The class for the asynchronous image processor."""
    onError = pyqtSignal(str)
    finished = pyqtSignal()
    image_processed = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        print("LocalNeuralProcessor")
        self._models = None

    def close_connection(self):
        self.onClose.emit()

    def _process_image(self, image_np: np.ndarray):
        print("_process_image")
        print(image_np.shape)
        if self._models is None:
            self._models = self.load_models()

        if len(image_np.shape) != 4:
            image_np = cv2.resize(image_np, (224, 224),
                                  interpolation=cv2.INTER_CUBIC)
        if len(image_np.shape) == 2:
            img = cv2.cvtColor(image_np, cv2.COLOR_GRAY2RGB)
        else:
            img = image_np
        img = img.reshape(1, 224, 224, 3)
        img = img/255.0
        # prediction
        # The StackCovNet model takes 3 same CXR image inputs (for DenseNet201, ResNet50 and VGG19)
        print("Start predict")
        conf = {}
        rank = {}
        clp = {}
        for m_name, model in self._models.items():
            result = model.predict(img)[0]
            print("result", result)
            conf[m_name] = result
            rank[m_name] = er.rank_cal(result)
            if result[0] > result[1]:
                clp[m_name] = 0
            else:
                clp[m_name] = 1
        print(conf, rank, clp)

        vote_result = np.zeros([4, ])
        vote_result[0] = er.method_FRLF(clp, rank, conf)
        vote_result[1] = er.sum_rule(conf)
        vote_result[2] = er.product_rule(conf)
        vote_result[3] = er.majority_voting(clp)
        self.image_processed.emit(vote_result)

    def run(self):
        """The function is called when the thread starts, can be used as a constructor"""
        print("LocalNeuralProcessor Start")

    def _load_single_model(self, model_url, model_path):
        model_path = model_full_path(model_path)
        if not os.path.exists(model_path):
            os.makedirs(os.path.dirname(model_path), exist_ok=True)
            download_file_from_google_drive(model_url, model_path)
        return load_model(model_path)

    def load_models(self):
        print("Load model")
        models_names = ['vgg16', 'xcep', 'res50', 'incv3']
        models_paths = ["model_1_path", "model_2_path",
                        "model_3_path", "model_4_path"]
        models_uris = ["model_1_uri", "model_2_uri",
                       "model_3_uri", "model_4_uri"]
        self._models = {}
        for models_name, path, uri in zip(models_names, models_paths, models_uris):
            m = self._load_single_model(XRaySettings().getParam(uri),
                                        XRaySettings().getParam(path))
            self._models[models_name] = m
        return self._models

    @pyqtSlot(np.ndarray)
    def process_image(self, image_np):
        print("processImage(self, image_np)")
        self._process_image(image_np)

    def close(self):
        """
        Strictly synchronous (in the stream) method, we call when we request the completion
        of the stream in this method you need to free resources if necessary
        """
        self._video_processor.close()
        # self.close_connection()

    @pyqtSlot()
    def stopRequest(self):
        self.close()
        QThread.currentThread().exit()


class NeuralProcessor(QObject):
    """ Plugin for video processing"""

    requestImageProcess = pyqtSignal(np.ndarray)
    stopRemoteNeuralProcessor = pyqtSignal()

    end_of_process = pyqtSignal(str)

    def __init__(self, result_listner, parent=None):
        super().__init__(parent)
        self._image_processor = LocalNeuralProcessor()

        self._processorThread = QThread()

        self._image_processor.finished.connect(self._processorThread.quit)
        self._image_processor.image_processed.connect(result_listner)

        self._image_processor.moveToThread(self._processorThread)

        self.requestImageProcess.connect(self._image_processor.process_image)
        self.stopRemoteNeuralProcessor.connect(
            self._image_processor.stopRequest)

        self._processorThread.started.connect(self._image_processor.run)
        self._processorThread.finished.connect(
            self._processorThread.deleteLater)
        self._processorThread.start()

        self.is_bisy = False

    @pyqtSlot(np.ndarray)
    def process_file(self, image: np.ndarray):
        """
        start processing the video inside the filename
        Setting the GUI for the file processing

        :param filename: full path of file
        """
        print("process_file")
        self.requestImageProcess.emit(image)

    def close(self):
        pass
