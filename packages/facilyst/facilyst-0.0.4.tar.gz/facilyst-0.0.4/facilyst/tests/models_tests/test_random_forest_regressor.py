import pandas as pd

from facilyst.models import RandomForestRegressor


def test_random_forest_regressor_class_variables():
    assert RandomForestRegressor.name == "Random Forest Regressor"
    assert RandomForestRegressor.primary_type == "regression"
    assert RandomForestRegressor.secondary_type == "ensemble"
    assert RandomForestRegressor.tertiary_type == "tree"
    assert list(RandomForestRegressor.hyperparameters.keys()) == [
        "n_estimators",
        "max_depth",
        "criterion",
        "max_features",
        "ccp_alpha",
        "max_samples",
    ]


def test_random_forest_regressor(numeric_features_regression):
    x, y = numeric_features_regression

    rf_regressor = RandomForestRegressor()
    rf_regressor.fit(x, y)
    rf_predictions = rf_regressor.predict(x)

    assert isinstance(rf_predictions, pd.Series)
    assert len(rf_predictions) == 100

    score = rf_regressor.score(x, y)
    assert isinstance(score, float)

    assert rf_regressor.get_params() == {
        "bootstrap": True,
        "ccp_alpha": 0.0,
        "criterion": "squared_error",
        "max_depth": None,
        "max_features": "auto",
        "max_leaf_nodes": None,
        "max_samples": None,
        "min_impurity_decrease": 0.0,
        "min_samples_leaf": 1,
        "min_samples_split": 2,
        "min_weight_fraction_leaf": 0.0,
        "n_estimators": 100,
        "n_jobs": -1,
        "oob_score": False,
        "random_state": None,
        "verbose": 0,
        "warm_start": False,
    }
