import os

UTILS_DIR = os.path.dirname(os.path.realpath(__file__))
SRC_DIR = os.path.dirname(UTILS_DIR)
ROOT_DIR = os.path.dirname(SRC_DIR)
CONFIG_DIR = f'{ROOT_DIR}/config'
DATASET_DIR = f'{ROOT_DIR}/dataset'