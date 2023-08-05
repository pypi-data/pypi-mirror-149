"""An ensemble tree-based model for classification problems."""
from typing import Optional

from hyperopt import hp
from sklearn.ensemble import ExtraTreesClassifier as et_classifier

from facilyst.models.model_base import ModelBase


class ExtraTreesClassifier(ModelBase):
    """The Extra Trees Classifier (via sklearn's implementation).

     This is an ensemble classifier that fits randomized decision trees on the entire dataset each time.

    :param n_estimators: The number of trees in the forest. Defaults to 100.
    :type n_estimators: int, optional
    :param max_depth: The maximum depth of the tree. Defaults to no maximum depth, nodes are expanded until all leaves
    are pure or until all leaves contain less than 2 samples.
    :type max_depth: int, optional
    :param criterion: The function to measure the quality of a split. Defaults to `gini`.
    :type criterion: str, optional
    :param max_features: The number of features to consider when looking for the best split. Defaults to `auto`.
    :type max_features: str, optional
    :param ccp_alpha: Complexity parameter used for Minimal Cost-Complexity Pruning. Defaults to 0.0.
    :type ccp_alpha: float, optional
    :param n_jobs: The number of cores to be used, -1 uses all available cores.
    :type n_jobs: int, optional
    """

    name: str = "Extra Trees Classifier"

    primary_type: str = "classification"
    secondary_type: str = "ensemble"
    tertiary_type: str = "tree"

    hyperparameters: dict = {
        "n_estimators": hp.choice("n_estimators", [10, 50, 100, 200, 300]),
        "max_depth": hp.randint("max_depth", 2, 10),
        "criterion": hp.choice("criterion", ["gini", "entropy"]),
        "max_features": hp.choice("max_features", ["auto", "sqrt"]),
        "ccp_alpha": hp.uniform("ccp_alpha", 0.0, 1.0),
    }

    def __init__(
        self,
        n_estimators: Optional[int] = 100,
        max_depth: Optional[int] = None,
        criterion: Optional[str] = "gini",
        max_features: Optional[str] = "auto",
        ccp_alpha: Optional[float] = 0.0,
        n_jobs: Optional[int] = -1,
        **kwargs,
    ) -> None:
        parameters = {
            "n_estimators": n_estimators,
            "max_depth": max_depth,
            "criterion": criterion,
            "max_features": max_features,
            "ccp_alpha": ccp_alpha,
            "n_jobs": n_jobs,
        }
        parameters.update(kwargs)

        extra_trees_model = et_classifier(**parameters)

        super().__init__(model=extra_trees_model, parameters=parameters)
