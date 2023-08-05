import pandas as pd

from facilyst.models import ADABoostRegressor


def test_ada_boost_regressor_class_variables():
    assert ADABoostRegressor.name == "ADA Boost Regressor"
    assert ADABoostRegressor.primary_type == "regression"
    assert ADABoostRegressor.secondary_type == "ensemble"
    assert ADABoostRegressor.tertiary_type == "tree"
    assert list(ADABoostRegressor.hyperparameters.keys()) == [
        "n_estimators",
        "learning_rate",
        "loss",
    ]


def test_ada_boost_regressor(numeric_features_regression):
    x, y = numeric_features_regression

    ada_regressor = ADABoostRegressor()
    ada_regressor.fit(x, y)
    ada_predictions = ada_regressor.predict(x)

    assert isinstance(ada_predictions, pd.Series)
    assert len(ada_predictions) == 100

    score = ada_regressor.score(x, y)
    assert isinstance(score, float)

    actual_params = ada_regressor.get_params()
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
        "learning_rate": 1.0,
        "loss": "linear",
        "n_estimators": 50,
        "random_state": None,
    }
