import numpy as np
import pandas as pd
import pytest
from sklearn.tree import DecisionTreeClassifier as sk_DecisionTreeClassifier

from facilyst.models import DecisionTreeClassifier


def test_decision_tree_classifier_class_variables():
    assert DecisionTreeClassifier.name == "Decision Tree Classifier"
    assert DecisionTreeClassifier.primary_type == "classification"
    assert DecisionTreeClassifier.secondary_type == "None"
    assert DecisionTreeClassifier.tertiary_type == "tree"
    assert list(DecisionTreeClassifier.hyperparameters.keys()) == [
        "max_depth",
        "criterion",
        "max_features",
        "ccp_alpha",
        "splitter",
    ]


@pytest.mark.parametrize("classification_type", ["binary", "multiclass"])
def test_decision_tree_classifier(
    classification_type,
    numeric_features_binary_classification,
    numeric_features_multi_classification,
):
    x, y = (
        numeric_features_binary_classification
        if classification_type == "binary"
        else numeric_features_multi_classification
    )

    dt_classifier = DecisionTreeClassifier()
    dt_classifier.fit(x, y)
    dt_predictions = dt_classifier.predict(x)

    sk_dt_classifier = sk_DecisionTreeClassifier()
    sk_dt_classifier.fit(x, y)
    sk_dt_predictions = sk_dt_classifier.predict(x)

    np.testing.assert_array_equal(dt_predictions.values, sk_dt_predictions)

    assert isinstance(dt_predictions, pd.Series)
    assert len(dt_predictions) == 100

    score = dt_classifier.score(x, y)
    assert isinstance(score, float)

    assert dt_classifier.get_params() == {
        "ccp_alpha": 0.0,
        "class_weight": None,
        "criterion": "gini",
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
