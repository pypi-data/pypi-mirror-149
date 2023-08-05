"""Base class for all preprocessors."""
from abc import ABC, abstractmethod
from typing import Any, Optional, Tuple, Union

import numpy as np
import pandas as pd


class PreprocessorBase(ABC):
    """Base initialization for all preprocessors.

    :param preprocessor: The preprocessor to be used.
    :type preprocessor: object
    :param parameters: The model to be used.
    :type parameters: dict
    """

    def __init__(
        self, preprocessor: Optional[Any] = None, parameters: Optional[dict] = None
    ) -> None:
        self.preprocessor = preprocessor
        self.parameters = parameters

    @property
    @abstractmethod
    def name(self):
        """Name of the preprocessor."""

    @property
    @abstractmethod
    def primary_type(self):
        """Primary type of the preprocessor."""

    @property
    @abstractmethod
    def secondary_type(self):
        """Secondary type of the preprocessor."""

    @property
    @abstractmethod
    def tertiary_type(self):
        """Tertiary type of the preprocessor."""

    @property
    @abstractmethod
    def hyperparameters(self):
        """Hyperparameter space for the preprocessor."""

    def fit(
        self,
        x: Union[pd.DataFrame, np.ndarray],
        y: Union[pd.Series, np.ndarray],
    ) -> Any:
        """Fits preprocessor to the data.

        :param x: The training data for the preprocessor to be fitted on.
        :type x: pd.DataFrame or np.ndarray
        :param y: The training targets for the preprocessor to be fitted on.
        :type y: pd.Series or np.ndarray
        """
        self.preprocessor.fit(x, y)
        return self

    def transform(
        self,
        x: Union[pd.DataFrame, np.ndarray],
        y: Union[pd.Series, np.ndarray],
    ) -> Tuple[pd.DataFrame, pd.Series]:
        """Transforms the data using the preprocessor.

        :param x: The testing data for the preprocessor to transform.
        :type x: pd.DataFrame or np.ndarray
        :return: The transformed data.
        :rtype tuple:
        """
        preprocessed_x, preprocessed_y = self.preprocessor.transform(x, y)
        return preprocessed_x, preprocessed_y
