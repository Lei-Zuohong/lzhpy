# -*- coding: UTF-8 -*-
# Public package
import tqdm
import xgboost as xgb
# Private package
# Internal package


class CallbackTqdm(xgb.callback.TrainingCallback):
    def __init__(self, rounds):
        self.pbar = tqdm.tqdm(total=rounds, desc='Training XGBoost')

    def after_iteration(self, model, epoch, evals_log):
        self.pbar.update(1)
        return False

    def after_training(self, model):
        self.pbar.close()
        return model
