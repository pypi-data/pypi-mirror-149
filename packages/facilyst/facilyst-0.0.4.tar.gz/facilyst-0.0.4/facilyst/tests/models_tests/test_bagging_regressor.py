import pandas as pd

from facilyst.models import BaggingRegressor


def test_bagging_regressor_class_variables():
    assert BaggingRegressor.name == "Bagging Regressor"
    assert BaggingRegressor.primary_type == "regression"
    assert BaggingRegressor.secondary_type == "ensemble"
    assert BaggingRegressor.tertiary_type == "tree"
    assert list(BaggingRegressor.hyperparameters.keys()) == [
        "n_estimators",
        "max_samples",
        "oob_score",
    ]


def test_bagging_regressor(numeric_features_regression):
    x, y = numeric_features_regression

    bagging_regressor = BaggingRegressor()
    bagging_regressor.fit(x, y)
    bagging_predictions = bagging_regressor.predict(x)

    assert isinstance(bagging_predictions, pd.Series)
    assert len(bagging_predictions) == 100

    score = bagging_regressor.score(x, y)
    assert isinstance(score, float)

    actual_params = bagging_regressor.get_params()
    actual_params.pop("base_estimator")

    assert actual_params == {
        "base_estimator__ccp_alpha": 0.0,
        "base_estimator__criterion": "squared_error",
        "base_estimator__max_depth": None,
        "base_estimator__max_features": None,
        "base_estimator__max_leaf_nodes": None,
        "base_estimator__min_impurity_decrease": 0.0,
        "base_estimator__min_samples_leaf": 1,
        "base_estimator__min_samples_split": 2,
        "base_estimator__min_weight_fraction_leaf": 0.0,
        "base_estimator__random_state": None,
        "base_estimator__splitter": "best",
        "bootstrap": True,
        "bootstrap_features": False,
        "max_features": 1.0,
        "max_samples": 1.0,
        "n_estimators": 50,
        "n_jobs": -1,
        "oob_score": False,
        "random_state": None,
        "verbose": 0,
        "warm_start": False,
    }
