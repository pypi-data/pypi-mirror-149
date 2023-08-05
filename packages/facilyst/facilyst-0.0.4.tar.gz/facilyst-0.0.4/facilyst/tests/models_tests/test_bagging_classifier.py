import pandas as pd
import pytest

from facilyst.models import BaggingClassifier


def test_bagging_regressor_class_variables():
    assert BaggingClassifier.name == "Bagging Classifier"
    assert BaggingClassifier.primary_type == "classification"
    assert BaggingClassifier.secondary_type == "ensemble"
    assert BaggingClassifier.tertiary_type == "tree"
    assert list(BaggingClassifier.hyperparameters.keys()) == [
        "n_estimators",
        "max_samples",
        "oob_score",
    ]


@pytest.mark.parametrize("classification_type", ["binary", "multiclass"])
def test_bagging_classifier(
    classification_type,
    numeric_features_binary_classification,
    numeric_features_multi_classification,
):
    x, y = (
        numeric_features_binary_classification
        if classification_type == "binary"
        else numeric_features_multi_classification
    )

    bagging_classifier = BaggingClassifier()
    bagging_classifier.fit(x, y)
    bagging_predictions = bagging_classifier.predict(x)

    assert isinstance(bagging_predictions, pd.Series)
    assert len(bagging_predictions) == 100

    score = bagging_classifier.score(x, y)
    assert isinstance(score, float)

    actual_params = bagging_classifier.get_params()
    actual_params.pop("base_estimator")

    assert actual_params == {
        "base_estimator__ccp_alpha": 0.0,
        "base_estimator__class_weight": None,
        "base_estimator__criterion": "gini",
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
