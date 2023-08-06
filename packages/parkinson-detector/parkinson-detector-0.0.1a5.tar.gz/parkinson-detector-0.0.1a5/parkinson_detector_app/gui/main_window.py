import os
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QApplication, QMainWindow
from PyQt5.QtWidgets import QSizePolicy, QGridLayout
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QProgressDialog
from PyQt5.QtWidgets import QSizePolicy, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.uic.properties import QtWidgets
import numpy as np

from parkinson_detector_app.gui.widgets.about_widget import AboutWidget
from parkinson_detector_app.gui.widgets.dicom_preview_widget import DicomPreviewWidget
from parkinson_detector_app.gui.widgets.result_preview_widget import ResultPreviewWidget
from parkinson_detector_app.common.settings import XRaySettings
from parkinson_detector_app.ai.dicom_processor import DicomProcessor
from parkinson_detector_app.common.const import *


class Main_GUI(QMainWindow):
    onClose = pyqtSignal()
    process_file = pyqtSignal(str)
    clear_all = pyqtSignal()

    def __init__(self, title: str, args):
        super().__init__()

        self._title = title
        self.initUI()
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.setAcceptDrops(True)

        self._dicom_processor = DicomProcessor()
        self._dicom_processor.file_opened.connect(self.on_file_opened)
        self._dicom_processor.error.connect(self.on_error)
        self._dicom_processor.preview_loaded.connect(
            self._dicom_preview_w.setPreview)
        self.process_file.connect(self._dicom_processor.process_file)

        self._dicom_processor.classification_result.connect(
            self._result_preview_w.fill_results)
        self._dicom_processor.classification_result.connect(
            self.on_classification_result)
        self.clear_all.connect(self._result_preview_w.clear)

    def initUI(self):
        """constructs the GUI  """
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

        self.setWindowTitle(self._title)

        ### creating the menu ###
        self._menu_bar = self.menuBar()

        self._menu_file = self._menu_bar.addMenu("File")

        action = self._menu_file.addAction("Open file")
        action.triggered.connect(self.open_file_clicked)

        self._menu_file.addSeparator()

        action = self._menu_file.addAction("Exit")
        action.triggered.connect(self.exit_clicked)

        self._menu_help = self._menu_bar.addMenu("Help")
        self._menu_help.addSeparator()
        action = self._menu_help.addAction("About")
        action.triggered.connect(self.about_clicked)

        ### create status bar ###

        self.status_bar = self.statusBar()
        self.status_bar.showMessage('Ready')

        ws = XRaySettings().getParam('window', {})
        q = QDesktopWidget().availableGeometry()  # Get screen size

        ### Widgets ###
        self._main_widget = QWidget()
        self._main_widget.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding)

        mainLayout = QGridLayout()
        mainLayout.setSpacing(5)

        self._dicom_preview_w = DicomPreviewWidget()
        mainLayout.addWidget(self._dicom_preview_w, 0, 0, -1, 5)

        self._result_preview_w = ResultPreviewWidget()
        mainLayout.addWidget(self._result_preview_w, 0, 6, -1, 1)

        self._main_widget.setLayout(mainLayout)
        self.setCentralWidget(self._main_widget)

        # Set main windows geometry
        width = ws.get('width') or max(q.width() // 2, GUI_MIN_WIDTH)
        height = ws.get('height') or max(q.height() // 2, GUI_MIN_HEIGHT)
        x = ws.get('x') or (q.width() - width) // 2
        y = ws.get('y') or (q.height() - height) // 2
        self.setGeometry(x, y, width, height)

        # Icon
        res_path = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), "resources")
        QApplication.instance().setWindowIcon(
            QIcon(os.path.join(res_path, "logo.ico")))

        # Show gui
        self.show()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        if len(files) > 0:
            f = files[0]
            self._open_dicom(f)

    def _open_dicom(self, path):
        self.progress_dlg = QProgressDialog("Analysing", "Cancel", 0, 0, self)
        self.progress_dlg.setWindowTitle('Please wait...')
        self.progress_dlg.setWindowModality(Qt.WindowModal)
        self.progress_dlg.setWindowFlag(Qt.WindowCloseButtonHint, False)
        self.progress_dlg.setCancelButton(None)
        self.progress_dlg.setAutoClose(True)
        self.progress_dlg.setValue(1)
        self.progress_dlg.show()

        print("Open file", path)
        self.clear_all.emit()
        self.process_file.emit(path)

    @pyqtSlot(np.ndarray)
    def on_classification_result(self, rates):
        self.progress_dlg.close()

    @ pyqtSlot()
    def open_file_clicked(self):
        """Handler clicking on open file"""
        file_name = QFileDialog.getOpenFileName(self, "Open X-Ray image",
                                                XRaySettings().getParam(
                                                    'last_open_dir', "./"),
                                                "All files (*.*)")[0]
        if file_name:
            XRaySettings().setParam(
                'last_open_dir', os.path.dirname(file_name), force=True)
            print("Opening project: {}".format(file_name))
            self._open_dicom(file_name)

    @pyqtSlot(str)
    def on_file_opened(self, file_name):
        self.status_bar.showMessage(file_name)

    @pyqtSlot(int, str)
    def on_error(self, code, message):
        dialog = QMessageBox()
        dialog.setWindowTitle("Error: {}".format(code))
        dialog.setText(message)
        dialog.setIcon(QMessageBox.Warning)
        dialog.exec_()
        self.progress_dlg.close()

    @pyqtSlot()
    def exit_clicked(self):
        self.onClose.emit()
        self.deleteLater()
        self.destroy(True, True)
        QApplication.closeAllWindows()
        QCoreApplication.instance().quit()

    @ pyqtSlot()
    def about_clicked(self):
        self.aboutWidget = AboutWidget()
        self.aboutWidget.show()
