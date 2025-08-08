import os
import sys

import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from src.exception import CustomException
from src.logger import logging

import dill

def save_object(file_path, obj):
    """
    Save the given object to a file using dill.
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, 'wb') as file:
            dill.dump(obj, file)
            
    except Exception as e:
        pass