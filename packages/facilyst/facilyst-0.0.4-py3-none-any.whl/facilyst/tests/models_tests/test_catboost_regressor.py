import pandas as pd
import pytest

from facilyst.models import CatBoostRegressor

pytestmark = pytest.mark.needs_extra_dependency


def test_catboost_classifier_class_variables():
    assert CatBoostRegressor.name == "Catboost Regressor"
    assert CatBoostRegressor.primary_type == "regression"
    assert CatBoostRegressor.secondary_type == "None"
    assert CatBoostRegressor.tertiary_type == "tree"
    assert list(CatBoostRegressor.hyperparameters.keys()) == [
        "n_estimators",
        "max_depth",
        "learning_rate",
    ]


def test_catboost_regressor(numeric_features_regression):
    x, y = numeric_features_regression

    catboost_regressor = CatBoostRegressor()
    catboost_regressor.fit(x, y)
    catboost_predictions = catboost_regressor.predict(x)

    assert isinstance(catboost_predictions, pd.Series)
    assert len(catboost_predictions) == 100

    score = catboost_regressor.score(x, y)
    assert isinstance(score, float)

    assert catboost_regressor.get_params() == {
        "loss_function": "RMSE",
        "n_estimators": 50,
    }
