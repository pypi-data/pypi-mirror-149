"""An ensemble bagging model for classification problems."""
from typing import Optional

from hyperopt import hp
from sklearn.ensemble import BaggingClassifier as bagging_classifier
from sklearn.tree import DecisionTreeClassifier

from facilyst.models.model_base import ModelBase


class BaggingClassifier(ModelBase):
    """The Bagging Classifier (via sklearn's implementation).

    This is an ensemble classifier that fits base classifier on random subsets of the dataset (wuth replacement) and then
    aggregates predictions.

    :param base_estimator: The base estimator from which the boosted ensemble is built. Defaults to DecisionTreeClassifier.
    :type base_estimator: object, optional
    :param n_estimators: The maximum number of estimators at which boosting is terminated. Defaults to 50.
    :type n_estimators: int, optional
    :param max_samples: The number of samples to draw from x to train each base estimator. If an int has been passed,
    it will draw `max_samples` samples. If a float has been passed, it will draw that percentage of samples. Defaults to 1.0.
    :type max_samples: float, optional
    :param oob_score: Whether to use out-of-bag samples to estimate the generalization error. Defaults to False.
    :type oob_score: bool, optional
    """

    name: str = "Bagging Classifier"

    primary_type: str = "classification"
    secondary_type: str = "ensemble"
    tertiary_type: str = "tree"

    hyperparameters: dict = {
        "n_estimators": hp.choice("n_estimators", [10, 50, 100, 200, 300]),
        "max_samples": hp.uniform("max_samples", 0.5, 1.0),
        "oob_score": hp.choice("oob_score", [True, False]),
    }

    def __init__(
        self,
        base_estimator: Optional[object] = DecisionTreeClassifier(),
        n_estimators: Optional[int] = 50,
        max_samples: Optional[float] = 1.0,
        oob_score: Optional[bool] = False,
        n_jobs: Optional[int] = -1,
        **kwargs,
    ) -> None:
        parameters = {
            "base_estimator": base_estimator,
            "n_estimators": n_estimators,
            "max_samples": max_samples,
            "oob_score": oob_score,
            "n_jobs": n_jobs,
        }
        parameters.update(kwargs)

        bag_classifier = bagging_classifier(**parameters)

        super().__init__(model=bag_classifier, parameters=parameters)
