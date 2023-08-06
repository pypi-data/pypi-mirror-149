# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['parkinson_detector_app',
 'parkinson_detector_app.ai',
 'parkinson_detector_app.common',
 'parkinson_detector_app.gui',
 'parkinson_detector_app.gui.widgets',
 'parkinson_detector_app.util']

package_data = \
{'': ['*'], 'parkinson_detector_app.gui': ['resources/*']}

install_requires = \
['PyQt5',
 'appdirs',
 'numpy>=1.20.1,<2.0.0',
 'opencv-python',
 'pillow',
 'pydicom',
 'pylibjpeg',
 'pylibjpeg-libjpeg',
 'pylibjpeg-openjpeg',
 'requests',
 'tensorflow>=2.3.1,<3.0.0']

entry_points = \
{'console_scripts': ['parkinson-detector-app = '
                     'parkinson_detector_app.parkinson_detector_app:main']}

setup_kwargs = {
    'name': 'parkinson-detector',
    'version': '0.0.1a5',
    'description': 'An Ensemble of CNN Models for Parkinsons Disease Detection',
    'long_description': '# Parkinson detector\n\nAn Ensemble of CNN Models for Parkinson’s Disease Detection\n\nMedical support tool for fast preliminary diagnosis can be used by any medical personnel.  Parkinson detector is written in Python and runs in a normal Windows and Linux environment. The user interface was implemented using the Qt library. \n\nOur application can work directly with Dicom files (.dcm) from a digital CRT machine or with any image files (jpg, png, etc.). We make a simple user interface with drag-and-drop support.\n\n**Note:** prediction from the application cannot be used as a medical diagnosis.\n## Application requirements: \n\n* Operational system: \n    * Windows 7 or later\n    * Ubuntu 16.04 or later\n    * Mac OS 10.12.6 (Sierra) or later (64-bit) (no GPU support)\n* Python 3.6 or later\n* Hard Drive: 4Gb of free space,\n* Processor: Intel Core i3,\n* Memory (RAM): 3Gb or above free.\n* Internet connection: wideband connection for first use (for neural network model downloading)\n* Admin privileges are not a requirement\n\n## Run without instalation\n\n### Requirements instalation\n```\ngit clone https://gitlab.com/digiratory/biomedimaging/parkinson-detector.git\ncd parkinson-detector\npip install -r requirements.txt\n```\n\n### Application starting\n```\ncd parkinson-detector\npython run.pyw\n```\n\n## Instalation over pip\n\n```\npip install parkinson-detector\n```\n\nFor starting application run the follow command:\n\n```\nparkinson-detector-app\n```\n',
    'author': 'Aleksandr Sinitca',
    'author_email': 'amsinitca@etu.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/digiratory/biomedimaging/parkinson-detector',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
