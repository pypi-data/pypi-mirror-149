"""A model that uses gradient boosting on decision trees alongside categorical encoding for classification problems."""
from typing import Optional, Union

import numpy as np
import pandas as pd
from hyperopt import hp

from facilyst.models.model_base import ModelBase
from facilyst.utils import import_errors_dict, import_or_raise


class CatBoostClassifier(ModelBase):
    """The CatBoost Classifier (via catboost's library).

     This is a classifier that uses gradient boosting on decision trees alongside categorical encoding.

    :param n_estimators: The maximum number of trees that can be built. Defaults to 50.
    :type n_estimators: int, optional
    :param max_depth: The maximum depth of the tree. Defaults to None.
    :type max_depth: int, optional
    :param learning_rate: The learning rate.
    :type learning_rate: float, optional
    """

    name: str = "Catboost Classifier"

    primary_type: str = "classification"
    secondary_type: str = "None"
    tertiary_type: str = "tree"

    hyperparameters: dict = {
        "n_estimators": hp.choice("n_estimators", [10, 50, 100, 200, 300]),
        "max_depth": hp.randint("max_depth", 2, 10),
        "learning_rate": hp.uniform("learning_rate", 0.001, 1.0),
    }

    def __init__(
        self,
        n_estimators: Optional[int] = 50,
        max_depth: Optional[int] = None,
        learning_rate: Optional[float] = None,
        **kwargs,
    ) -> None:
        parameters = {
            "n_estimators": n_estimators,
            "max_depth": max_depth,
            "learning_rate": learning_rate,
        }
        parameters.update(kwargs)

        cat_classifier = import_or_raise("catboost", import_errors_dict["catboost"])

        catboost_model = cat_classifier.CatBoostClassifier(**parameters)

        super().__init__(model=catboost_model, parameters=parameters)

    def predict(self, x_test: Union[pd.DataFrame, np.ndarray]) -> pd.Series:
        """Predicts on the data using the model. Catboost returns an n-dimension array and needs to be flattened.

        :param x_test: The testing data for the model to predict on.
        :type x_test: pd.DataFrame or np.ndarray
        :return: The predictions.
        :rtype pd.Series:
        """
        predictions = self.model.predict(x_test)
        if predictions.ndim == 2 and predictions.shape[1] == 1:
            predictions = predictions.flatten()
        return pd.Series(predictions)
