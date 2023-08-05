"""Base class for Graph types."""
import collections.abc
from abc import ABC, abstractmethod
from typing import Any, Optional

import matplotlib
import numpy as np
import pandas as pd


class GraphBase(ABC):
    """Base initialization for all mock types.

    :param graph_obj: The graph object to be used.
    :type graph_obj: object
    :param parameters: Parameters specific to the object being passed.
    :type parameters: dict
    :param extra_parameters: Extra parameters provided by the child class.
    :type extra_parameters: dict
    """

    def __init__(
        self, graph_obj: Any, parameters: dict, extra_parameters: dict
    ) -> None:
        self.parameters = parameters
        self.extra_parameters = extra_parameters

        self.check_passed_data()
        self._initialize_x_y()

        self.graph_obj = graph_obj(**self.parameters)
        self.resize()
        self.show()

    @property
    @abstractmethod
    def name(self):
        """Name of the graph."""

    def get_figure(self) -> Any:
        """Returns the graph figure.

        :return: The Figure object.
        :rtype: matplotlib.figure.Figure
        """
        return self.graph_obj.figure.get_figure

    def get_size(self) -> np.ndarray:
        """Returns the size of the graph in inches.

        :return: The size of the graph in the format (width, height).
        :rtype: np.ndarray
        """
        return self.graph_obj.figure.get_size_inches()

    def resize(
        self, width: Optional[float] = 11.7, height: Optional[float] = 8.27
    ) -> None:
        """Resize the graph. Call .show() after to display the graph.

        :param width: The width of the graph.
        :type width: float
        :param height: The height of the graph.
        :type height: float
        """
        self.graph_obj.figure.set_size_inches(width, height)

    def show(self) -> Any:
        """Show the graph.

        :return: The graph.
        :rtype: matplotlib.figure.Figure
        """
        return self.graph_obj.figure

    def check_passed_data(self) -> None:
        """Checks if the appropriate parameters has been passed to the graph object."""
        dataset_ = self.parameters["data"]
        if dataset_ is None:
            self.check_x_y_without_dataset()
        else:
            self.check_x_y_with_dataset()

    def check_x_y_without_dataset(self) -> None:
        """Checks if x and y have been passed appropriately when dataset has not been passed.

        :raises ValueError: If dataset is None and x is not an accepted collection of data.
        :raises ValueError: If dataset is None and y is not an accepted collection of data.
        :raises ValueError: If dataset is None and x and y are not one dimensional data.
        """
        x_ = self.parameters["x"]
        y_ = self.parameters["y"]

        if not isinstance(x_, (pd.Series, np.ndarray)):
            raise ValueError(
                "If `dataset` is None, then `x` must be a collection of data of type pd.Series or np.ndarray!"
            )
        if not isinstance(y_, (pd.Series, np.ndarray)):
            raise ValueError(
                "If `dataset` is None, then `y` must be a collection of data of type pd.Series or np.ndarray!"
            )
        try:
            x_pd_ = pd.Series(x_)
            y_pd_ = pd.Series(y_)
        except ValueError:
            raise ValueError(
                "If `dataset` is None, both x and y must be one dimensional!"
            )

    def check_x_y_with_dataset(self) -> None:
        """Checks if x and y have been passed appropriately when dataset has not been passed.

        :raises ValueError: If dataset is not of an acceptable type.
        :raises ValueError: If dataset has been passed and x and y aren't hashable values referencing column names.
        :raises ValueError: If x or y is None.
        :raises ValueError: If x could not be found in the dataset.
        :raises ValueError: If y could not be found in the dataset.
        """
        dataset_ = self.parameters["data"]
        x_ = self.parameters["x"]
        y_ = self.parameters["y"]

        if not isinstance(dataset_, (pd.DataFrame, np.ndarray)):
            raise ValueError("`dataset` must be of type pd.DataFrame or np.ndarray!")

        if not (
            isinstance(x_, collections.abc.Hashable)
            and isinstance(y_, collections.abc.Hashable)
        ):
            raise ValueError(
                "If `dataset` is not None, then `x` and `y` need to be hashable values referring to column names in the dataset!"
            )
        elif x_ is None or y_ is None:
            raise ValueError("`x` and `y` cannot be None!")

        pd_dataset_ = pd.DataFrame(dataset_)

        error_text = (
            "Column `{col_}` could not be found in the `dataset` columns! If you passed in a "
            "dataset of type np.ndarray, use an integer to indicate the column number e.g. 0, 1, 2, etc. "
            "`dataset` has {num_cols} columns."
        )

        if x_ not in pd_dataset_.columns:
            raise ValueError(
                error_text.format(col_=x_, num_cols=len(pd_dataset_.columns))
            )
        elif y_ not in pd_dataset_.columns:
            raise ValueError(
                error_text.format(col_=y_, num_cols=len(pd_dataset_.columns))
            )

    def _initialize_x_y(self) -> None:
        if self.parameters["data"] is not None:
            data = self.parameters["data"]
            data = pd.DataFrame(data)
            data.ww.init()
            self.parameters["data"] = data
        else:
            if not isinstance(self.parameters["x"], pd.Series):
                x = pd.Series(self.parameters["x"])
                x.ww.init()
                self.parameters["x"] = x
            if not isinstance(self.parameters["y"], pd.Series):
                y = pd.Series(self.parameters["y"])
                y.ww.init()
                self.parameters["y"] = y
