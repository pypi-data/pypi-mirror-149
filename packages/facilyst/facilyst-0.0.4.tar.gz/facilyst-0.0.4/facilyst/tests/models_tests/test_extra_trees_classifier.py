import pandas as pd
import pytest

from facilyst.models import ExtraTreesClassifier


def test_extra_trees_classifier_class_variables():
    assert ExtraTreesClassifier.name == "Extra Trees Classifier"
    assert ExtraTreesClassifier.primary_type == "classification"
    assert ExtraTreesClassifier.secondary_type == "ensemble"
    assert ExtraTreesClassifier.tertiary_type == "tree"
    assert list(ExtraTreesClassifier.hyperparameters.keys()) == [
        "n_estimators",
        "max_depth",
        "criterion",
        "max_features",
        "ccp_alpha",
    ]


@pytest.mark.parametrize("classification_type", ["binary", "multiclass"])
def test_extra_trees_classifier(
    classification_type,
    numeric_features_binary_classification,
    numeric_features_multi_classification,
):
    x, y = (
        numeric_features_binary_classification
        if classification_type == "binary"
        else numeric_features_multi_classification
    )

    et_classifier = ExtraTreesClassifier()
    et_classifier.fit(x, y)
    et_predictions = et_classifier.predict(x)

    assert isinstance(et_predictions, pd.Series)
    assert len(et_predictions) == 100

    score = et_classifier.score(x, y)
    assert isinstance(score, float)

    assert et_classifier.get_params() == {
        "bootstrap": False,
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
