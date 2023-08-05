import pandas as pd
import pytest

from facilyst.models import RandomForestClassifier


def test_random_forest_classifier_class_variables():
    assert RandomForestClassifier.name == "Random Forest Classifier"
    assert RandomForestClassifier.primary_type == "classification"
    assert RandomForestClassifier.secondary_type == "ensemble"
    assert RandomForestClassifier.tertiary_type == "tree"
    assert list(RandomForestClassifier.hyperparameters.keys()) == [
        "n_estimators",
        "max_depth",
        "criterion",
        "max_features",
        "ccp_alpha",
        "max_samples",
    ]


@pytest.mark.parametrize("classification_type", ["binary", "multiclass"])
def test_random_forest_classifier(
    classification_type,
    numeric_features_binary_classification,
    numeric_features_multi_classification,
):
    x, y = (
        numeric_features_binary_classification
        if classification_type == "binary"
        else numeric_features_multi_classification
    )

    rf_classifier = RandomForestClassifier()
    rf_classifier.fit(x, y)
    rf_predictions = rf_classifier.predict(x)

    assert isinstance(rf_predictions, pd.Series)
    assert len(rf_predictions) == 100

    score = rf_classifier.score(x, y)
    assert isinstance(score, float)

    assert rf_classifier.get_params() == {
        "bootstrap": True,
        "ccp_alpha": 0.0,
        "class_weight": None,
        "criterion": "gini",
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
