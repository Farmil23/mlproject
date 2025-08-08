import os
import sys
from dataclasses import dataclass

from catboost import CatBoostRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, AdaBoostRegressor

from src.exception import CustomException
from src.logger import logging

from sklearn.linear_model import LinearRegression
from src.utils import save_object, evaluate_models

from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor

from sklearn.metrics import r2_score
from xgboost import XGBRegressor

@dataclass
class ModelTrainerConfig:
    trained_model_file_path = os.path.join('artifacts', 'model.pkl')
    
class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()
        
    def initiate_model_trainer(self, train_array, test_array):
        try:
            logging.info("Splitting training and testing data")
            
            X_train, y_train, X_test, y_test = (
                train_array[:,:-1], train_array[:,-1],
                test_array[:,:-1], test_array[:,-1]
            )
            
            models = {
                "Random Forest": RandomForestRegressor(),
                "Decision Tree": DecisionTreeRegressor(),
                "Gradient Boosting" : GradientBoostingRegressor(),
                "Linear Regression": LinearRegression(),
                "K-neighbors Reggresion" : KNeighborsRegressor(),
                "XGBRegressor" : XGBRegressor(),
                "Catboosting Regressor" : CatBoostRegressor(),
                "AdaBoost Regressor": AdaBoostRegressor(),
            }

            params={
                "Decision Tree": {
                    'criterion':['squared_error', 'friedman_mse', 'absolute_error', 'poisson'],
                    # 'splitter':['best','random'],
                    # 'max_features':['sqrt','log2'],
                },
                "Random Forest":{
                    # 'criterion':['squared_error', 'friedman_mse', 'absolute_error', 'poisson'],
                 
                    # 'max_features':['sqrt','log2',None],
                    'n_estimators': [8,16,32,64,128,256]
                },
                "Gradient Boosting":{
                    # 'loss':['squared_error', 'huber', 'absolute_error', 'quantile'],
                    'learning_rate':[.1,.01,.05,.001],
                    'subsample':[0.6,0.7,0.75,0.8,0.85,0.9],
                    # 'criterion':['squared_error', 'friedman_mse'],
                    # 'max_features':['auto','sqrt','log2'],
                    'n_estimators': [8,16,32,64,128,256]
                },
                "Linear Regression":{},
                 "K-neighbors Reggresion" : {}, 
                "XGBRegressor":{
                    'learning_rate':[.1,.01,.05,.001],
                    'n_estimators': [8,16,32,64,128,256]
                },
                "Catboosting Regressor":{
                    'depth': [6,8,10],
                    'learning_rate': [0.01, 0.05, 0.1],
                    'iterations': [30, 50, 100]
                },
                "AdaBoost Regressor":{
                    'learning_rate':[.1,.01,0.5,.001],
                    # 'loss':['linear','square','exponential'],
                    'n_estimators': [8,16,32,64,128,256]
                }
            }
            
            model_report, trained_models = evaluate_models(
            X_train=X_train, y_train=y_train, X_test=X_test, y_test=y_test, 
            models=models, param=params
        )
                    
            # Cari skor dan nama model terbaik (logika ini tetap sama)
            best_model_score = max(model_report.values())
            best_model_name = max(model_report, key=model_report.get)
                    
            # AMBIL MODEL TERBAIK DARI DICTIONARY 'trained_models', BUKAN 'models'
            best_model = trained_models[best_model_name]
                    
            if best_model_score < 0.6:
                raise CustomException("No base model found")
            
            logging.info(f"Best model found on both training an testing datasets: {best_model_name}")
                    
            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=best_model # Sekarang 'best_model' adalah objek yang sudah dilatih
            )
                    
            predicted = best_model.predict(X_test)
            final_r2_score = r2_score(y_test, predicted)
            return final_r2_score# Gunakan nama variabel baru
                
        except Exception as e:
            raise CustomException(e, sys)

