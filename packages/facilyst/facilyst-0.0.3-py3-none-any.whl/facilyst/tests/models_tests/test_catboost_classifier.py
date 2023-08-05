import pandas as pd
import pytest

from facilyst.models import CatBoostClassifier

pytestmark = pytest.mark.needs_extra_dependency


def test_catboost_classifier_class_variables():
    assert CatBoostClassifier.name == "Catboost Classifier"
    assert CatBoostClassifier.primary_type == "classification"
    assert CatBoostClassifier.secondary_type == "None"
    assert CatBoostClassifier.tertiary_type == "tree"
    assert list(CatBoostClassifier.hyperparameters.keys()) == [
        "n_estimators",
        "max_depth",
        "learning_rate",
    ]


@pytest.mark.parametrize("classification_type", ["binary", "multiclass"])
def test_catboost_classifier(
    classification_type,
    numeric_features_binary_classification,
    numeric_features_multi_classification,
):
    x, y = (
        numeric_features_binary_classification
        if classification_type == "binary"
        else numeric_features_multi_classification
    )

    catboost_classifier = CatBoostClassifier()
    catboost_classifier.fit(x, y)
    catboost_predictions = catboost_classifier.predict(x)

    assert isinstance(catboost_predictions, pd.Series)
    assert len(catboost_predictions) == 100

    score = catboost_classifier.score(x, y)
    assert isinstance(score, float)

    assert catboost_classifier.get_params() == {
        "n_estimators": 50,
    }
