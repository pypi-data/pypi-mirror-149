"""An ensemble weighted model for regression problems."""
from typing import Optional

from hyperopt import hp
from sklearn.ensemble import AdaBoostRegressor as ada_regressor
from sklearn.tree import DecisionTreeRegressor

from facilyst.models.model_base import ModelBase


class ADABoostRegressor(ModelBase):
    """The ADA Boost Regressor (via sklearn's implementation).

    This is an ensemble regressor that fits differently weighted copies of the same regressor on the dataset repeatedly
    depending on the error of subsequent predictions.

    :param base_estimator: The base estimator from which the boosted ensemble is built. Defaults to DecisionTreeRegressor.
    :type base_estimator: object, optional
    :param n_estimators: The maximum number of estimators at which boosting is terminated. Defaults to 50.
    :type n_estimators: int, optional
    :param learning_rate: Weight applied to each regressor at each boosting iteration. A higher learning rate increases
    the contribution of each regressor. There is a trade-off between the learning_rate and n_estimators parameters.
    Defaults to 1.0.
    :type learning_rate: float, optional
    :param loss: The loss function to use when updating the weights after each boosting iteration. Options are `linear`,
    `square`, and `exponential`. Defaults to `linear`.
    :type loss: str, optional
    """

    name: str = "ADA Boost Regressor"

    primary_type: str = "regression"
    secondary_type: str = "ensemble"
    tertiary_type: str = "tree"

    hyperparameters: dict = {
        "n_estimators": hp.choice("n_estimators", [10, 50, 100, 200, 300]),
        "learning_rate": hp.uniform("learning_rate", 0, 1),
        "loss": hp.choice("loss", ["linear", "square", "exponential"]),
    }

    def __init__(
        self,
        base_estimator: Optional[object] = DecisionTreeRegressor(),
        n_estimators: Optional[int] = 50,
        learning_rate: Optional[float] = 1.0,
        loss: Optional[str] = "linear",
        **kwargs,
    ) -> None:
        parameters = {
            "base_estimator": base_estimator,
            "n_estimators": n_estimators,
            "learning_rate": learning_rate,
            "loss": loss,
        }
        parameters.update(kwargs)

        ada_regressor_model = ada_regressor(**parameters)

        super().__init__(model=ada_regressor_model, parameters=parameters)
