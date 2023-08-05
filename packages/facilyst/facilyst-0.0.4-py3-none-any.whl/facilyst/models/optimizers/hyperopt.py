"""An optimizer used for hyperparameter tuning via Bayesian optimization."""
from typing import Optional, Tuple, Union

import numpy as np
import pandas as pd
from hyperopt import STATUS_OK, Trials, fmin, space_eval, tpe
from sklearn.model_selection import train_test_split

from facilyst.models import ModelBase
from facilyst.models.utils import get_models


class HyperoptOptimizer:
    """The Multilayer Perceptron regressor is a feedforward neural network made of hidden layers.

    For either the `classifier` or `regressor` parameters, the name of the model can be passed or a type of model
    can be specified, which will use all models belonging to that type. For example, `Random Forest Classifier` will
    result in only that model being used, while `tree` will result in all tree-based models being used during optimization.
    If `any` is passed, then every model belonging to that problem type will be used during optimization.
    Either the classifier OR the `regressor` parameter must be set.

    :param classifier: The classifier model(s) to use.
    :type classifier: str, optional
    :param regressor: The regressor model(s) to use.
    :type regressor: str, optional
    :param split: The percentage of the data passed to be kept aside for training. 1 - the value set for this parameter
    will be used for testing.
    :type split: float, optional
    :param split: The number of iterations that should be performed per model. If a dict is passed, keys should represent
    the name of the model and values should be the number of iterations. If more models are selected than those specified
    in the dict, then they will be set to a default number of iterations of 50.
    :type split: int or dict, optional
    """

    name: str = "Hyperopt Optimizer"

    def __init__(
        self,
        classifier: Optional[str] = None,
        regressor: Optional[str] = None,
        split: Optional[float] = 0.8,
        iterations_per_model: Optional[int] = 50,
    ) -> None:
        self.classifier = classifier
        self.regressor = regressor
        self.split = split
        self.iterations_per_model = iterations_per_model
        self.results = {}

        if not (self.classifier or self.regressor):
            raise ValueError("Either classifier or regressor must be set.")
        elif self.classifier and self.regressor:
            raise ValueError("Either classifier or regressor must be set, not both.")

        if not isinstance(self.iterations_per_model, (int, dict)):
            raise ValueError(
                "The parameter `iterations_per_model` must be either an int or a dict specifying the "
                "number of iterations per model."
            )

        self.collected_models = self.collect_models()

        self.space = self.hyperparameter_space()

    def collect_models(self) -> list:
        """Collect all models requested for the optimizer.

        :rtype list:
        """
        return (
            get_models(self.classifier)
            if self.classifier
            else get_models(self.regressor)
        )

    def hyperparameter_space(self) -> list:
        """The collected hyperparameter space for all models selected to search through.

        :rtype list:
        """
        space = []
        for each_model in self.collected_models:
            model_space = {each_model.name: each_model.hyperparameters}
            space.append(model_space)
        return space

    def optimize(
        self, x: Union[pd.DataFrame, np.ndarray], y: Union[pd.Series, np.ndarray]
    ) -> Tuple[ModelBase, float]:
        """Convenience function to start optimization job and iterate over collected models.

        :param x: All feature data.
        :type x: pd.DataFrame or np.ndarray
        :param y: All target data.
        :type y: pd.Series or np.ndarray
        :return: The best model selected with the corresponding best hyperparameters, and the score achieved.
        :rtype tuple: object, float
        """
        for model in self.collected_models:
            self.results[model.name] = self._optimize(
                x, y, model, model.hyperparameters
            )

        best_score = np.Inf
        best_model_name = None
        best_model_hyp = None
        for model_name, model_data in self.results.items():
            if model_data["best_score"] < best_score:
                best_model_name = model_name
                best_score = model_data["best_score"]
                best_model_hyp = model_data["best_hyperparameters"]

        best_model = get_models(best_model_name)[0]
        return best_model(**best_model_hyp), best_score

    def _optimize(
        self,
        x: Union[pd.DataFrame, np.ndarray],
        y: Union[pd.Series, np.ndarray],
        model: ModelBase,
        space: dict,
    ) -> dict:
        """Optimization per model over hyperparameter space."""

        def cost_function(parameters: dict) -> dict:
            """Cost function definition."""
            parameters = {hyp: parameters[hyp] for hyp in parameters.keys()}

            x_train, x_test, y_train, y_test = train_test_split(
                x, y, train_size=self.split
            )
            model_ = model(**parameters)  # pytype: disable=not-callable
            model_.fit(x_train, y_train)
            score = model_.score(x_test, y_test)
            return {"loss": -score, "status": STATUS_OK}

        trials = Trials()

        model_iter = None
        if isinstance(self.iterations_per_model, dict):
            model_iter = self.iterations_per_model.get(model.name, 50)

        best_hyp = fmin(
            fn=cost_function,
            space=space,
            algo=tpe.suggest,
            max_evals=model_iter or 50,
            trials=trials,
        )

        best_trial = trials.best_trial
        best_dict = {
            "best_hyperparameters": space_eval(model.hyperparameters, best_hyp),
            "best_score": round(best_trial["result"]["loss"], 3),
        }

        return best_dict
