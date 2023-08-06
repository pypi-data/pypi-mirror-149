import os
import sys
import appdirs
import json

from parkinson_detector_app.common.singleton import Singleton
from parkinson_detector_app.common.files import config_file_path
from parkinson_detector_app.common.const import *


DEFAUL_SETTINGS = {
    "model_1_uri": DEFAULT_MODEL_1_URI,
    "model_2_uri": DEFAULT_MODEL_2_URI,
    "model_3_uri": DEFAULT_MODEL_3_URI,
    "model_4_uri": DEFAULT_MODEL_4_URI,
    "model_1_path": DEFAULT_MODEL_1_PATH,
    "model_2_path": DEFAULT_MODEL_2_PATH,
    "model_3_path": DEFAULT_MODEL_3_PATH,
    "model_4_path": DEFAULT_MODEL_4_PATH,
    "show_rate": True,
}


class XRaySettings(object, metaclass=Singleton):
    """
    Class for the application settings.
    """
    __settings = None

    def __init__(self):
        """
        Inits XRaySettings class.
        """
        pass

    def getParam(self, key: str, default_value=None):
        """
        Get parameter from setting dictionary based on given key.

        Parameters
        ----------
        key: Key of parameter.
        default_value: Default value of the parameter.

        Returns
        -------
        The requested parameter.

        """
        if self.__settings is None:
            self._load_setting()
        if key not in self.__settings.keys():
            self.setParam(key, default_value)
        print(key, self.__settings.get(key, default_value))
        return self.__settings.get(key, default_value)

    def setParam(self, key: str, value, force=True):
        """
        Set given parameter inside setting dictionary.

        Parameters
        ----------
        key: Key of parameter.
        value: Value of parameter.
        force: Flag to force the addition.

        Returns
        -------
        True if the parameter was set, false otherwise.

        """
        if self.__settings is None:
            self._load_setting()
        if key in self.__settings.keys() or force:
            self.__settings[key] = value
            self._save_setting()
            return True
        else:
            return False

    def _load_setting(self):
        """
        Loads a settings configurations from file.

        """
        settigs_filename = XRaySettings.get_settings_filename()
        if not os.path.exists(settigs_filename):
            self._create_default_settings_file()
        try:
            with open(settigs_filename, 'r', encoding='utf-8') as file:
                self.__settings = json.load(file)
        except:
            print("Error: some troubles with configuration")
        pass

    def _create_default_settings_file(self):
        """
        Creates a settings file, and saves the settings into it as json.

        """
        settigs_filename = XRaySettings.get_settings_filename()
        os.makedirs(os.path.dirname(settigs_filename), exist_ok=True)
        with open(settigs_filename, 'w', encoding='utf-8') as file:
            json.dump(DEFAUL_SETTINGS, file, indent=2, sort_keys=True)

    def _save_setting(self):
        """
        Saves the settings into a file.

        """
        settigs_filename = XRaySettings.get_settings_filename()
        os.makedirs(os.path.dirname(settigs_filename), exist_ok=True)
        with open(settigs_filename, 'w', encoding='utf-8') as file:
            json.dump(self.__settings, file, indent=2, sort_keys=True)

    @staticmethod
    def get_settings_filename():
        """
        Static method to get the file name of the settings file.

        """
        return config_file_path()


if __name__ == "__main__":
    sys.path.append(os.path.abspath(os.path.join(
        os.path.dirname(__file__), '..', '..')))
    print(XRaySettings.get_settings_filename())
    model_uri = XRaySettings().getParam("model_uri")
    print(model_uri)
