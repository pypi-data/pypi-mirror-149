

APP_NAME = "Parkinson detector"
DEFAULT_MODEL_1_URI = "https://drive.google.com/file/d/1hMbL6_W8TPTMwWQ-35mwkcAh1lDSZrlm/view"
DEFAULT_MODEL_2_URI = "https://drive.google.com/file/d/1N7P0IVdfBd2QW1K63gtz8nx7mHAq414t/view"
DEFAULT_MODEL_3_URI = "https://drive.google.com/file/d/1BjQjZ5z79J8Qn2s-UdfrH_u9OOheVQKD/view"
DEFAULT_MODEL_4_URI = "https://drive.google.com/file/d/1VqMV-7PUXwhOUBc-8CR1K6ZapSLkDZw5/view"
DEFAULT_MODEL_1_PATH = "models/vgg16_500.h5"
DEFAULT_MODEL_2_PATH = "models/xcep_500.h5"
DEFAULT_MODEL_3_PATH = "models/res50_500.h5"
DEFAULT_MODEL_4_PATH = "models/incv3_500.h5"
GUI_MIN_WIDTH = 320
GUI_MIN_HEIGHT = 280


PREDICTION_STRING_FORMAT = "Most likely diagnosis: \n\n \
    FRLF method(~98% Accuracy): {method_FRLF} \n\n\n \
    Other methods: \
    \n sum_rule (~96% Accuracy): {sum_rule} \
    \n majority_voting (~96% Accuracy): {majority_voting} \
    \n product_rule (~92% Accuracy): {product_rule}"

PREDICTION_CAPTIONS = ["Normal", "Parkinson detected"]
