"""A mock type that returns features data."""
from typing import Optional, Tuple, Union

import numpy as np
import pandas as pd
import woodwork as ww

from facilyst.mocks import MockBase
from facilyst.mocks.mock_types.utils import mock_features_dtypes


class Features(MockBase):
    """Class to manage mock data creation of features.

    :param num_rows: The number of observations in the final dataset. Defaults to 100.
    :type num_rows: int, optional
    :param library: The library of which the final dataset should be, options are 'pandas' and 'numpy'. Defaults to 'pandas'.
    :type library: str, optional
    :param ints: Flag that includes column with monotonically increasing incremental set of negative and positive integers. Defaults to True.
    :type ints: bool, optional
    :param rand_ints: Flag that includes column with randomly selected integers between -5 and 5. Defaults to True.
    :type rand_ints: bool, optional
    :param floats: Flag that includes column which is the float version of the 'ints' column. Defaults to True.
    :type floats: bool, optional
    :param rand_floats: Flag that includes column with randomly selected floats between -5 and 5. Defaults to True.
    :type rand_floats: bool, optional
    :param booleans: Flag that includes column with randomly selected boolean values. Defaults to False.
    :type booleans: bool, optional
    :param categoricals: Flag that includes column with four categoriesL 'First', 'Second', 'Third', and 'Fourth'. Defaults to False.
    :type categoricals: bool, optional
    :param dates: Flag that includes column with monotonically increasing dates from 01/01/2001 with a daily frequency. Defaults to False.
    :type dates: bool, optional
    :param texts: Flag that includes column with different text on each line. Defaults to False.
    :type texts: bool, optional
    :param ints_nullable: Flag that includes column which is the same as the 'ints' column with pd.NA included. Defaults to False.
    :type ints_nullable: bool, optional
    :param floats_nullable: Flag that includes column which is the same as the 'floats' column with pd.NA included. Defaults to False.
    :type floats_nullable: bool, optional
    :param booleans_nullable: Flag that includes column which is a randomly selected column with boolean values and pd.NA included. Defaults to False.
    :type booleans_nullable: bool, optional
    :param full_names: Flag that includes column with first and last names. Defaults to False.
    :type full_names: bool, optional
    :param phone_numbers: Flag that includes column with US-based phone numbers. Defaults to True.
    :type phone_numbers: bool, optional
    :param addresses: Flag that includes column with addresses. Defaults to True.
    :type addresses: bool, optional
    :param countries: Flag that includes column with country names. Defaults to False.
    :type countries: bool, optional
    :param email_addresses: Flag that includes column with email addresses. Defaults to True.
    :type email_addresses: bool, optional
    :param urls: Flag that includes column with URLs. Defaults to True.
    :type urls: bool, optional
    :param currencies: Flag that includes column with US dollar based amounts. Defaults to False.
    :type currencies: bool, optional
    :param file_paths: Flag that includes column with file paths at a depth of 3. Defaults to False.
    :type file_paths: bool, optional
    :param ipv4: Flag that includes column with different IPv4 addresses. Defaults to False.
    :type ipv4: bool, optional
    :param ipv6: Flag that includes column with different IPv6 addresses. Defaults to False.
    :type ipv6: bool, optional
    :param lat_longs: Flag that includes column with latitude and longitude values in a tuple. Defaults to False.
    :type lat_longs: bool, optional
    :param all_dtypes: Flag that includes all columns. Defaults to False.
    :type all_dtypes: bool, optional
    :return: Mock features data.
    :rtype: pd.DataFrame by default, can also return np.ndarray
    """

    name = "Features"

    def __init__(
        self,
        num_rows: Optional[int] = 100,
        library: Optional[str] = "pandas",
        ints: Optional[bool] = True,
        rand_ints: Optional[bool] = True,
        floats: Optional[bool] = True,
        rand_floats: Optional[bool] = True,
        booleans: Optional[bool] = False,
        categoricals: Optional[bool] = False,
        dates: Optional[bool] = False,
        texts: Optional[bool] = False,
        ints_nullable: Optional[bool] = False,
        floats_nullable: Optional[bool] = False,
        booleans_nullable: Optional[bool] = False,
        full_names: Optional[bool] = False,
        phone_numbers: Optional[bool] = False,
        addresses: Optional[bool] = False,
        countries: Optional[bool] = False,
        email_addresses: Optional[bool] = False,
        urls: Optional[bool] = False,
        currencies: Optional[bool] = False,
        file_paths: Optional[bool] = False,
        ipv4: Optional[bool] = False,
        ipv6: Optional[bool] = False,
        lat_longs: Optional[bool] = False,
        all_dtypes: Optional[bool] = False,
    ) -> None:
        kw_args = locals()

        if all_dtypes:
            parameters = {
                k: True
                for k, v in kw_args.items()
                if k not in ["self", "library", "num_rows", "__class__"]
            }
        else:
            parameters = {
                k: v
                for k, v in kw_args.items()
                if k not in ["self", "library", "num_rows", "__class__"] and v
            }
            if not any(
                parameters.values()
            ):  # All False flags results in all dtypes being included
                parameters = {k: True for k, v in kw_args.items()}

        super().__init__(library, num_rows, parameters)

    def create_data(self) -> Union[pd.DatetimeIndex, np.ndarray]:
        """Main function to be called to create features data.

        :return: The final features data created.
        :rtype: pd.DatetimeIndex or np.ndarray
        """
        data, dtypes_to_keep = self.get_data_from_dict()
        data = self.handle_library(data, dtypes_to_keep)
        return data

    def get_data_from_dict(self) -> Tuple[pd.DataFrame, list]:
        """Returns the data based on the dtypes specified during class instantiation.

        :return: The final data created from the appropriate library.
        :rtype: pd.DataFrame, list
        """
        dtypes_to_keep = list(self.parameters.keys())
        mocked = Features._refine_dtypes(dtypes_to_keep, self.num_rows)

        mocked_df = pd.DataFrame.from_dict(mocked)
        return mocked_df, dtypes_to_keep

    def handle_library(
        self, data: pd.DataFrame, dtypes_to_keep: list
    ) -> Union[pd.DataFrame, np.ndarray]:
        """Handles the library that was selected to determine the format in which the data will be returned.

        :param data: The final data to be returned.
        :type data: pd.DataFrame
        :param dtypes_to_keep: All data format options from the class initialization. Defaults to returning the full dataset.
        :type dtypes_to_keep: list
        :return: The final data created from the appropriate library.
        :rtype: pd.DataFrame or np.ndarray
        """
        if self.library == "numpy":
            return data.to_numpy()
        else:
            if "ints_nullable" in dtypes_to_keep:
                data["ints_nullable"] = data["ints_nullable"].astype("Int64")
            if "floats_nullable" in dtypes_to_keep:
                data["floats_nullable"] = data["floats_nullable"].astype("Float64")
            data.ww.init()
            return data

    @staticmethod
    def _refine_dtypes(dtypes: list, num_rows: Optional[int] = 100) -> dict:
        """Internal function that selects the dtypes to be kept from the full dataset.

        :param dtypes: All data format options from the class initialization. Defaults to returning the full dataset.
        :type dtypes: list
        :param num_rows : The number of observations in the final dataset. Defaults to 100.
        :type num_rows: int
        :return: A refined form of the full set of columns available.
        :rtype: dict
        """
        full_mock = mock_features_dtypes(num_rows)
        return {k: v for k, v in full_mock.items() if k in dtypes}
