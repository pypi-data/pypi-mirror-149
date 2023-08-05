"""Base class for mock types."""
from abc import ABC, abstractmethod
from typing import Optional, Union

import numpy as np
import pandas as pd


class MockBase(ABC):
    """Base initialization for all mock types.

    :param library: The library that should be used for the type of data returned.
    :type library: str
    :param num_rows: The number of rows your returned data should have.
    :type num_rows: int
    :param parameters: All relevant parameters for the mock type.
    :type parameters: dict
    """

    def __init__(
        self,
        library: Optional[str] = None,
        num_rows: Optional[int] = 100,
        parameters: Optional[dict] = None,
    ) -> None:
        self.library = library
        self.num_rows = num_rows
        self.parameters = parameters

    @property
    @abstractmethod
    def name(self):
        """Name of the mock type."""

    @abstractmethod
    def create_data(self):
        """Abstract method to be called by child classes to create the final data."""

    def get_data(self) -> Union[pd.DataFrame, np.ndarray]:
        """Returns the final data.

        :rtype: pd.DataFrame or np.ndarray
        """
        return self.create_data()
