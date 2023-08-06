
import sys
import os
import argparse
import ctypes
from PyQt5.QtWidgets import QApplication
from parkinson_detector_app.gui.main_window import Main_GUI
from parkinson_detector_app.common.const import APP_NAME


def main():
    if os.name == 'nt':
        myappid = 'digiratory.parkinson_detector_app'  # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    """Application entry point"""
    parser = argparse.ArgumentParser(description="Data analysis client")

    parser.add_argument('input_file', nargs='?', help="Input file")
    args = vars(parser.parse_args())
    app = QApplication(sys.argv)
    gui = Main_GUI(APP_NAME, args)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
