import pandas as pd
import pytest

from facilyst.models import MultiLayerPerceptronClassifier


def test_mlp_classifier_class_variables():
    assert MultiLayerPerceptronClassifier.name == "Multilayer Perceptron Classifier"
    assert MultiLayerPerceptronClassifier.primary_type == "classification"
    assert MultiLayerPerceptronClassifier.secondary_type == "neural"
    assert MultiLayerPerceptronClassifier.tertiary_type == "perceptron"
    assert MultiLayerPerceptronClassifier.hyperparameters == {}


@pytest.mark.parametrize("classification_type", ["binary", "multiclass"])
def test_mlp_classifier(
    classification_type,
    numeric_features_binary_classification,
    numeric_features_multi_classification,
):
    x, y = (
        numeric_features_binary_classification
        if classification_type == "binary"
        else numeric_features_multi_classification
    )

    mlp_classifier = MultiLayerPerceptronClassifier()
    mlp_classifier.fit(x[:80], y[:80])
    predictions = mlp_classifier.predict(x[80:])

    assert isinstance(predictions, pd.Series)
    assert len(predictions) == 20

    score = mlp_classifier.score(x[80:], y[80:])
    assert isinstance(score, float)

    assert mlp_classifier.get_params() == {
        "activation": "relu",
        "alpha": 0.0001,
        "batch_size": "auto",
        "beta_1": 0.9,
        "beta_2": 0.999,
        "early_stopping": False,
        "epsilon": 1e-08,
        "hidden_layer_sizes": (100,),
        "learning_rate": "constant",
        "learning_rate_init": 0.001,
        "max_fun": 15000,
        "max_iter": 200,
        "momentum": 0.9,
        "n_iter_no_change": 10,
        "nesterovs_momentum": True,
        "power_t": 0.5,
        "random_state": None,
        "shuffle": True,
        "solver": "adam",
        "tol": 0.0001,
        "validation_fraction": 0.1,
        "verbose": False,
        "warm_start": False,
    }
