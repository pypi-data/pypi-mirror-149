import pandas as pd

from facilyst.models import ExtraTreesRegressor


def test_extra_trees_regressor_class_variables():
    assert ExtraTreesRegressor.name == "Extra Trees Regressor"
    assert ExtraTreesRegressor.primary_type == "regression"
    assert ExtraTreesRegressor.secondary_type == "ensemble"
    assert ExtraTreesRegressor.tertiary_type == "tree"
    assert list(ExtraTreesRegressor.hyperparameters.keys()) == [
        "n_estimators",
        "max_depth",
        "criterion",
        "max_features",
        "ccp_alpha",
    ]


def test_extra_trees_regressor(numeric_features_regression):
    x, y = numeric_features_regression

    et_regressor = ExtraTreesRegressor()
    et_regressor.fit(x, y)
    et_predictions = et_regressor.predict(x)

    assert isinstance(et_predictions, pd.Series)
    assert len(et_predictions) == 100

    score = et_regressor.score(x, y)
    assert isinstance(score, float)

    assert et_regressor.get_params() == {
        "bootstrap": False,
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
