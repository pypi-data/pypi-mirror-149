import pandas as pd

from facilyst.models import MultiLayerPerceptronRegressor


def test_mlp_regressor_class_variables():
    assert MultiLayerPerceptronRegressor.name == "Multilayer Perceptron Regressor"
    assert MultiLayerPerceptronRegressor.primary_type == "regression"
    assert MultiLayerPerceptronRegressor.secondary_type == "neural"
    assert MultiLayerPerceptronRegressor.tertiary_type == "perceptron"
    assert MultiLayerPerceptronRegressor.hyperparameters == {}


def test_mlp_regressor(numeric_features_regression):
    x, y = numeric_features_regression

    mlp_regressor = MultiLayerPerceptronRegressor()
    mlp_regressor.fit(x[:80], y[:80])
    predictions = mlp_regressor.predict(x[80:])

    assert isinstance(predictions, pd.Series)
    assert len(predictions) == 20

    score = mlp_regressor.score(x[80:], y[80:])
    assert isinstance(score, float)

    assert mlp_regressor.get_params() == {
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
