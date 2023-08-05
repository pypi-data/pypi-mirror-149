"""A mock type that returns datetime data."""
import re
from typing import Optional, Union

import numpy as np
import pandas as pd

from facilyst.mocks import MockBase


class Dates(MockBase):
    """Class to manage mock data creation of datetime values.

    :param num_rows: The number of observations in the final dataset. Defaults to 100.
    :type num_rows: int, optional
    :param library: The library of which the final dataset should be, options are 'pandas' and 'numpy'. Defaults to 'pandas'.
    :type library: str, optional
    :param start_date: The start date for the datetime values. Defaults to January 1, 2001.
    :type start_date: str, optional
    :param frequency: Frequency for the datetime values. Defaults to a frequency of 1 day.
    :type frequency: str, optional
    :param missing: Flag that determines if datetime values will be randomly removed. Defaults to False. Will be set to False if chaos is 0.
    :type missing: bool, optional
    :param misaligned: Flag that determines if datetime values will be randomly misaligned. Defaults to False. Will be set to False if chaos is 0.
    :type misaligned: bool, optional
    :param duplicates: Flag that determines if duplicate datetime values will be randomly added. Defaults to False. Will be set to False if chaos is 0.
    :type duplicates: bool, optional
    :param chaos: Determines what percentage of the date range will be modified to be uninferable. Set on a scale
    of 0 (no duplicate, missing, or misaligned values in the date range, resulting in an inferable frequency) to 10.
    If parameters `duplicates`, `missing`, and `misaligned` are all set to False, then this parameter will be set to 0.
    Defaults to 1.
    :type chaos: int, optional
    :return: Mock datetime data.
    :rtype: pd.DateTimeIndex by default, can also return np.ndarray
    """

    name: str = "Dates"

    chaos_percentage: dict = {
        0: 0,
        1: 10,
        2: 15,
        3: 20,
        4: 25,
        5: 30,
        6: 40,
        7: 50,
        8: 60,
        9: 70,
        10: 80,
    }

    def __init__(
        self,
        num_rows: int = 100,
        library: Optional[str] = "pandas",
        start_date: Optional[str] = "1/1/2001",
        frequency: Optional[str] = "1D",
        missing: Optional[bool] = False,
        misaligned: Optional[bool] = False,
        duplicates: Optional[bool] = False,
        chaos: Optional[int] = 1,
    ) -> None:
        self.num_rows = num_rows
        self.start_date = start_date
        self.frequency = frequency
        self.missing = missing
        self.misaligned = misaligned
        self.duplicates = duplicates
        self.chaos = int(chaos)

        if self.num_rows < 3:
            raise ValueError("Parameter `num_rows` must be 3 or above!")

        if not (self.duplicates or self.missing or self.misaligned):
            self.chaos = 0

        Dates.validate_num_rows(self.chaos, self.num_rows)

        parameters = {
            "start": self.start_date,
            "freq": self.frequency,
            "missing": self.missing,
            "misaligned": self.misaligned,
            "duplicates": self.duplicates,
            "chaos": self.chaos,
        }

        super().__init__(library, num_rows, parameters)

    def create_data(self) -> Union[pd.DatetimeIndex, np.ndarray]:
        """Main function to be called to create datetime data.

        :return: The final datetime data created.
        :rtype: pd.DatetimeIndex or np.ndarray
        """
        data = pd.date_range(
            start=self.start_date, periods=self.num_rows, freq=self.frequency
        )
        if self.chaos:
            data = self.make_uninferrable(data)
        data = self.handle_library(data)
        return data

    @staticmethod
    def validate_num_rows(chaos: Optional[int], num_rows: Optional[int]) -> None:
        """Main function to be called to create datetime data.

        :param chaos: Determines what percentage of the date range will be modified to be uninferable. Set on a scale
        of 0 (no duplicate, missing, or misaligned values in the date range, resulting in an inferable frequency) to 10.
        :type chaos: int
        :param num_rows: The number of observations in the final dataset.
        :type num_rows: int
        :raises ValueError: If chaos has been set but the number of rows is under 30.
        """
        if chaos and (num_rows < 30):
            raise ValueError(
                f"The `num_rows` parameter must be a minimum of 30 if chaos is not 0."
            )

    def make_uninferrable(self, dates_: pd.DatetimeIndex) -> pd.Series:
        """Main function to be called to create datetime data.

        :param dates_: The clean datetime data.
        :type dates_: pd.DatetimeIndex
        :return: The final datetime data created.
        :rtype: pd.Series
        """
        chaos_percent = Dates.chaos_percentage[self.chaos] / 100
        num_chaos_rows = chaos_percent * self.num_rows
        num_of_each_issue = int(
            num_chaos_rows // sum([self.missing, self.misaligned, self.duplicates])
        )
        all_indices_to_consider = np.arange(self.num_rows)
        if self.missing:
            random_missing_indices = np.random.choice(
                all_indices_to_consider, num_of_each_issue, replace=False
            )
            all_indices_to_consider = np.setdiff1d(
                all_indices_to_consider, random_missing_indices
            )
            dates_ = Dates.remove_missing(dates_, random_missing_indices)
        if self.misaligned:
            random_misaligned_indices = np.random.choice(
                all_indices_to_consider, num_of_each_issue, replace=False
            )
            all_indices_to_consider = np.setdiff1d(
                all_indices_to_consider, random_misaligned_indices
            )
            dates_ = Dates.shift_misaligned(
                dates_, random_misaligned_indices, self.frequency
            )
        if self.duplicates:
            random_duplicate_indices = np.random.choice(
                all_indices_to_consider, num_of_each_issue, replace=False
            )
            dates_ = Dates.add_duplicates(dates_, random_duplicate_indices)
        return dates_

    @staticmethod
    def remove_missing(
        dates_: pd.DatetimeIndex, missing_indices: Union[np.ndarray, list]
    ) -> pd.Series:
        """Removes random datetime data.

        :param dates_: The datetime data.
        :type dates_: pd.DatetimeIndex
        :param missing_indices: The indices that will have datetime values set to None.
        :type missing_indices: np.ndarray or list
        :return: The modified datetime data.
        :rtype: pd.Series
        """
        datetime_series = pd.Series(dates_)
        datetime_series.iloc[missing_indices] = None
        return datetime_series

    @staticmethod
    def shift_misaligned(
        dates_: pd.DatetimeIndex, misaligned_indices: Union[np.ndarray, list], freq: str
    ) -> pd.Series:
        """Randomly misaligns the datetime data.

        :param dates_: The datetime data.
        :type dates_: pd.DatetimeIndex
        :param misaligned_indices: The indices that will have datetime values misaligned.
        :type misaligned_indices: np.ndarray or list
        :param freq: The frequency of the datetime data.
        :type freq: str
        :return: The modified datetime data.
        :rtype: pd.Series
        """
        try:
            num_freq = re.findall("\\d+", freq)[0]
        except IndexError:
            num_freq = 1
        num_freq = int(num_freq)
        str_freq = re.findall("\\D+", freq)[0]
        if str_freq == "A":
            num_freq *= 365
            str_freq = "D"
        elif str_freq == "MS":
            num_freq *= (
                28  # Because February is the shortest month, it's a limiting factor
            )
            str_freq = "D"
        current_td = pd.Timedelta(int(num_freq), str_freq)

        missing_values = []
        for missing_index in misaligned_indices:
            fraction_td = current_td / np.random.choice([2, 3, 4, 5], 1)[0]
            missing_values.append(dates_[missing_index] + fraction_td)
        datetime_series = pd.Series(dates_)
        datetime_series.iloc[misaligned_indices] = missing_values
        return datetime_series

    @staticmethod
    def add_duplicates(
        dates_: pd.DatetimeIndex, duplicate_indices: Union[np.ndarray, list]
    ) -> pd.Series:
        """Adds random duplicates to datetime data.

        :param dates_: The datetime data.
        :type dates_: pd.DatetimeIndex
        :param duplicate_indices: The indices that will have datetime values duplicated.
        :type duplicate_indices: np.ndarray or list
        :return: The modified datetime data.
        :rtype: pd.Series
        """
        # Currently adds values to entire Series, maybe change logic so num_rows doesn't change
        datetime_series = pd.Series(dates_)
        duplicate_values = pd.Series(datetime_series.iloc[duplicate_indices].values)
        datetime_series = datetime_series.append(duplicate_values)
        sorted_datetime_series = datetime_series.sort_values().reset_index(drop=True)
        return sorted_datetime_series

    def handle_library(
        self, dates_: Union[pd.Series, pd.DatetimeIndex, np.ndarray]
    ) -> Union[pd.DatetimeIndex, np.ndarray]:
        """Handles the library that was selected to determine the format in which the data will be returned.

        :param dates_: The final data to be returned.
        :type dates_: pd.Series, pd.DateTimeIndex, or np.ndarray
        :return: The final data created from the appropriate library as a pd.
        :rtype: pd.DatetimeIndex or np.ndarray
        """
        if self.library.lower() == "numpy":
            return dates_.to_numpy()
        else:
            return pd.DatetimeIndex(dates_)
