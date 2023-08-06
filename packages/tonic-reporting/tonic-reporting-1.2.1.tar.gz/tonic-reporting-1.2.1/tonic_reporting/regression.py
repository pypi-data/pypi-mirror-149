from typing import Tuple, List
from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, RegressorMixin, TransformerMixin
from sklearn.preprocessing import (
    OneHotEncoder,
    OrdinalEncoder,
    MinMaxScaler,
    StandardScaler,
)
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.neural_network import MLPRegressor
from lightgbm import LGBMRegressor
from xgboost import XGBRegressor
from catboost import CatBoostRegressor
from sklearn.compose import ColumnTransformer
from sklearn.metrics import r2_score, mean_squared_error

from tonic_reporting.util import make_data_transformer
from tonic_reporting.styling import PlotsSizes, Colors, Labels

@dataclass
class RegressionModel:
    model_class: RegressorMixin
    model_kwargs: dict
    numeric_transformer: TransformerMixin
    categorical_transformer: TransformerMixin


class PassthroughTransformer(BaseEstimator, TransformerMixin):
    """Convenience class for passthrough (no-op) transformation"""

    def __init__(self):
        pass

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        return X


REGRESSION_MODELS = {
    "Ridge": RegressionModel(
        Ridge,
        {"random_state": 0},
        StandardScaler,
        OneHotEncoder,
    ),
    "MLPRegressor": RegressionModel(
        MLPRegressor,
        {"hidden_layer_sizes": (200, 200), "max_iter": 500, "random_state": 0},
        MinMaxScaler,
        OneHotEncoder,
    ),
    "RandomForest": RegressionModel(
        RandomForestRegressor,
        {"random_state": 0},
        "passthrough",
        OrdinalEncoder,
    ),
    "LGBM": RegressionModel(
        LGBMRegressor,
        {"random_state": 0},
        "passthrough",
        OrdinalEncoder,
    ),
    "XGB": RegressionModel(
        XGBRegressor,
        {"random_state": 0},
        "passthrough",
        OrdinalEncoder,
    ),
    "CatBoost": RegressionModel(
        CatBoostRegressor,
        {"silent": True, "random_state": 0},
        "passthrough",
        OrdinalEncoder,
    ),
}


def extract_X_y(Xy: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    return Xy[:, 1:], Xy[:, 0]


def transform_data(
    column_transformer: ColumnTransformer, data: pd.DataFrame
) -> Tuple[np.ndarray, np.ndarray]:
    """Utility wrapper for ColumnTransformer.transform method"""
    X, y = extract_X_y(column_transformer.transform(data))
    return X, y


def train_and_test(
    regression_model: RegressionModel,
    train: pd.DataFrame,
    test: pd.DataFrame,
    target_column: str,
    numeric_features: List[str],
    categorical_features: List[str],
) -> Tuple[dict, ColumnTransformer, RegressorMixin]:
    """Trains RegressionModel on train data and evaluates on test data"""
    column_transformer = make_data_transformer(
        train,
        [target_column] + numeric_features,
        categorical_features,
        numeric_transformer_cls=regression_model.numeric_transformer,
        categorical_transformer_cls=regression_model.categorical_transformer,
    )
    X_train, y_train = transform_data(column_transformer, train)
    X_test, y_test = transform_data(column_transformer, test)
    model = regression_model.model_class(**regression_model.model_kwargs)
    model.fit(X_train, y_train)
    y_hat = model.predict(X_test)
    metrics = {
        "rmse": np.sqrt(mean_squared_error(y_test, y_hat)),
        "r2": r2_score(y_test, y_hat),
    }
    return metrics, column_transformer, model


def plot_results(results, ax):  # TODO: clean up
    """Summarizes R2 scores for real and synthetic models"""
    model_names = [x for x in results.keys()]
    triples = [[x, results[x]["R2_real"], results[x]["R2_synth"]] for x in model_names]
    triples.sort(key=lambda x: x[1], reverse=True)

    names = [x[0] for x in triples]
    real_vals = [x[1] for x in triples]
    synth_vals = [x[2] for x in triples]
    N = len(real_vals)
    ind = np.arange(N)
    width = 0.35

    real_rects = ax.bar(ind, real_vals, width, color=Colors.REAL)
    synth_rects = ax.bar(ind + width, synth_vals, width, color=Colors.SYNTH)
    ax.set_ylabel("R2 Score", fontsize=16)
    yticks = [i / 5 for i in range(6)]
    ax.set_yticks(yticks)
    ax.set_yticklabels(yticks, fontsize=14)
    ax.set_title(f"{Labels.REAL} vs {Labels.SYNTH} R2 Scores", fontsize=18)
    ax.set_xticks(ind + width / 2)
    ax.set_xticklabels(names, fontsize=14)
    ax.legend((real_rects[0], synth_rects[0]), (Labels.REAL, Labels.SYNTH), fontsize=14)
    autolabel(real_rects, ax)
    autolabel(synth_rects, ax)


def autolabel(rects, ax):
    """
    Attach a text label above each bar displaying its height
    """
    for rect in rects:
        height = rect.get_height()
        ax.text(
            rect.get_x() + rect.get_width() / 2.0,
            1.0 * height,
            "%.2f" % height,
            ha="center",
            va="bottom",
            fontsize=14,
        )