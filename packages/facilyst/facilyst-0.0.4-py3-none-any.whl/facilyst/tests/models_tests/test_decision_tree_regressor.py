import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeRegressor as sk_DecisionTreeRegressor

from facilyst.models import DecisionTreeRegressor


def test_decision_tree_regressor_class_variables():
    assert DecisionTreeRegressor.name == "Decision Tree Regressor"
    assert DecisionTreeRegressor.primary_type == "regression"
    assert DecisionTreeRegressor.secondary_type == "None"
    assert DecisionTreeRegressor.tertiary_type == "tree"
    assert list(DecisionTreeRegressor.hyperparameters.keys()) == [
        "max_depth",
        "criterion",
        "max_features",
        "ccp_alpha",
        "splitter",
    ]


def test_decision_tree_regressor(numeric_features_regression):
    x, y = numeric_features_regression

    dt_regressor = DecisionTreeRegressor()
    dt_regressor.fit(x, y)
    dt_predictions = dt_regressor.predict(x)

    sk_dt_regressor = sk_DecisionTreeRegressor()
    sk_dt_regressor.fit(x, y)
    sk_dt_predictions = sk_dt_regressor.predict(x)

    np.testing.assert_array_equal(dt_predictions.values, sk_dt_predictions)

    assert isinstance(dt_predictions, pd.Series)
    assert len(dt_predictions) == 100

    score = dt_regressor.score(x, y)
    assert isinstance(score, float)

    assert dt_regressor.get_params() == {
        "ccp_alpha": 0.0,
        "criterion": "squared_error",
        "max_depth": None,
        "max_features": "auto",
        "max_leaf_nodes": None,
        "min_impurity_decrease": 0.0,
        "min_samples_leaf": 1,
        "min_samples_split": 2,
        "min_weight_fraction_leaf": 0.0,
        "random_state": None,
        "splitter": "best",
    }
