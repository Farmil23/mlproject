import os
import sys

import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from src.exception import CustomException
from src.logger import logging

from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score

import dill
import pickle

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
        raise CustomException(e, sys)
    
# di dalam src/utils.py

def evaluate_models(X_train, y_train,X_test,y_test,models, param):
    try:
        report = {}
        # Buat dictionary baru untuk menyimpan model yang sudah dilatih
        trained_models = {}

        for i in range(len(list(models))):
            model_name = list(models.keys())[i]
            model = list(models.values())[i]
            para = param[model_name]
            
            gs = GridSearchCV(model, para, cv=3)
            gs.fit(X_train, y_train)
            
            # Ambil model terbaik dari hasil GridSearchCV
            best_estimator = gs.best_estimator_
            
            # Simpan model yang sudah dilatih ini
            trained_models[model_name] = best_estimator
            
            y_test_pred = best_estimator.predict(X_test)
            test_model_score = r2_score(y_test, y_test_pred)

            report[model_name] = test_model_score

        # Kembalikan laporan DAN kamus model yang sudah dilatih
        return report, trained_models

    except Exception as e:
        raise CustomException(e, sys)
    
def load_object(file_path):
    try:
        with open(file_path, "rb") as file_obj:
            return pickle.load(file_obj)

    except Exception as e:
        raise CustomException(e, sys)