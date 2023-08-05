"""A tree-based model for classification problems."""
from typing import Optional

from hyperopt import hp
from sklearn.tree import DecisionTreeClassifier as dt_classifier

from facilyst.models.model_base import ModelBase


class DecisionTreeClassifier(ModelBase):
    """The Decision Tree Classifier (via sklearn's implementation).

    :param max_depth: The maximum depth of the tree. Defaults to no maximum depth, nodes are expanded until all leaves
    are pure or until all leaves contain less than 2 samples.
    :type max_depth: int, optional
    :param criterion: The function to measure the quality of a split. Options are `gini`, `entropy`.
    Defaults to the `gini`.
    :type criterion: str, optional
    :param max_features: The number of features to consider when looking for the best split. Defaults to `auto`.
    :type max_features: str, optional
    :param ccp_alpha: Complexity parameter used for Minimal Cost-Complexity Pruning. Defaults to 0.0.
    :type ccp_alpha: float, optional
    :param splitter: The strategy used to choose the split at each node. Options are `best` and `random`. Defaults to `best`.
    :type splitter: str, optional
    :param n_jobs: The number of cores to be used, -1 uses all available cores.
    :type n_jobs: int, optional
    """

    name: str = "Decision Tree Classifier"

    primary_type: str = "classification"
    secondary_type: str = "None"
    tertiary_type: str = "tree"

    hyperparameters: dict = {
        "max_depth": hp.randint("max_depth", 2, 10),
        "criterion": hp.choice("criterion", ["gini", "entropy"]),
        "max_features": hp.choice("max_features", ["auto", "sqrt"]),
        "ccp_alpha": hp.uniform("ccp_alpha", 0.0, 1.0),
        "splitter": hp.choice("splitter", ["best", "random"]),
    }

    def __init__(
        self,
        max_depth: Optional[int] = None,
        criterion: Optional[str] = "gini",
        max_features: Optional[str] = "auto",
        ccp_alpha: Optional[float] = 0.0,
        splitter: Optional[str] = "best",
        **kwargs,
    ) -> None:
        parameters = {
            "max_depth": max_depth,
            "criterion": criterion,
            "max_features": max_features,
            "ccp_alpha": ccp_alpha,
            "splitter": splitter,
        }
        parameters.update(kwargs)

        decision_tree_model = dt_classifier(**parameters)

        super().__init__(model=decision_tree_model, parameters=parameters)
