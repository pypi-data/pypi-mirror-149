import os
import sys
import appdirs

from parkinson_detector_app.common.const import *


def config_file_path():
    return os.path.join(appdirs.user_config_dir(APP_NAME, False), "settings.json")


def model_full_path(model_path):
    return os.path.join(appdirs.user_config_dir(APP_NAME, False), model_path)


if __name__ == "__main__":
    sys.path.append(os.path.abspath(os.path.join(
        os.path.dirname(__file__), '..', '..')))

    print(config_file_path())
    print(model_full_path(DEFAULT_MODEL_1_PATH))
