import pandas as pd
import pytest
from hyperopt import hp

from facilyst.models import ADABoostClassifier


def test_ada_boost_classifier_class_variables():
    assert ADABoostClassifier.name == "ADA Boost Classifier"
    assert ADABoostClassifier.primary_type == "classification"
    assert ADABoostClassifier.secondary_type == "ensemble"
    assert ADABoostClassifier.tertiary_type == "tree"
    assert list(ADABoostClassifier.hyperparameters.keys()) == [
        "n_estimators",
        "learning_rate",
        "algorithm",
    ]


@pytest.mark.parametrize("classification_type", ["binary", "multiclass"])
def test_ada_boost_classifier(
    classification_type,
    numeric_features_binary_classification,
    numeric_features_multi_classification,
):

    x, y = (
        numeric_features_binary_classification
        if classification_type == "binary"
        else numeric_features_multi_classification
    )

    ada_classifier = ADABoostClassifier()
    ada_classifier.fit(x, y)
    ada_predictions = ada_classifier.predict(x)

    assert isinstance(ada_predictions, pd.Series)
    assert len(ada_predictions) == 100

    score = ada_classifier.score(x, y)
    assert isinstance(score, float)

    actual_params = ada_classifier.get_params()
    actual_params.pop("base_estimator")

    assert actual_params == {
        "algorithm": "SAMME.R",
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
        "learning_rate": 1.0,
        "n_estimators": 50,
        "random_state": None,
    }
