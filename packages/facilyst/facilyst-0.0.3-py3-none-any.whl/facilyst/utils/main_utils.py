"""Main utility functions."""
from typing import Optional, Union

import numpy as np
import pandas as pd

from facilyst.mocks import Dates, Features, Wave
from facilyst.mocks.mock_types import handle_mock_and_library_type


def create_data(
    mock_type: str,
    num_rows: Optional[int] = 100,
    library: Optional[str] = "pandas",
    **kwargs,
) -> Union[pd.DataFrame, pd.DatetimeIndex, np.ndarray]:
    """Function that creates data based on the mock_type requested.

    :param mock_type: The mock data type to create.
    :type mock_type: str
    :param num_rows: The number of observations in the final dataset. Defaults to 100.
    :type num_rows: int, optional
    :param library: The library of which the final dataset should be, options are 'pandas' and 'numpy'. Defaults to 'pandas'.
    :type library: str, optional
    :param kwargs: Additional key word arguments passed depending on the type of mock data requested.
    :type kwargs: dict
    :return: The created data.
    :rtype: pd or np.ndarray
    """
    mock_type, library = handle_mock_and_library_type(mock_type, library)

    class_options = {"features": Features, "dates": Dates, "wave": Wave}

    class_args = {
        "num_rows": num_rows,
        "library": library,
    }
    class_args.update(kwargs)

    data_class = class_options[mock_type](**class_args)
    return data_class.get_data()


def make_features(
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
) -> Union[pd.DataFrame, np.ndarray]:
    """Convenience function that allows for the creation of mock features data.

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
    kw_args = locals()
    return create_data("features", **kw_args)


def make_dates(
    num_rows: Optional[int] = 100,
    library: Optional[str] = "pandas",
    start_date: Optional[str] = "1/1/2001",
    frequency: Optional[str] = "1D",
    missing: Optional[bool] = False,
    misaligned: Optional[bool] = False,
    duplicates: Optional[bool] = False,
    chaos: Optional[int] = 1,
) -> Union[pd.DatetimeIndex, np.ndarray]:
    """Convenience function that allows for the creation of mock datetime data.

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
    kw_args = locals()
    return create_data("dates", **kw_args)


def make_wave(
    num_rows: Optional[int] = 100,
    library: Optional[str] = "numpy",
    wave_type: Optional[str] = "sine",
    amplitude: Optional[int] = 1,
    frequency: Optional[int] = 1,
    random_amplitudes: Optional[bool] = False,
    random_frequency: Optional[bool] = False,
    trend: Optional[float] = 0.0,
) -> Union[np.ndarray, pd.DataFrame]:
    """Convenience function that allows for the creation of mock wave data.

    :param num_rows: The number of observations in the final dataset. Defaults to 100.
    :type num_rows: int, optional
    :param library: The library of which the final dataset should be, options are 'pandas' and 'numpy'. Defaults to 'numpy'.
    :type library: str, optional
    :param wave_type: The function off of which the wave will be based. Options are `sine` and `cosine`. Defaults to `sine`.
    :type wave_type: str, optional
    :param amplitude: The amplitude (height) of the wave. Defaults to 1.
    :type amplitude: int, optional
    :param frequency: The frequency (thickness) of the wave. Defaults to 1.
    :type frequency: int, optional
    :param random_amplitudes: Flag that determines if different sections of the wave will have different amplitudes. Defaults to False.
    :type random_amplitudes: bool, optional
    :param random_frequency: Flag that determines if different sections of the wave will have different frequencies. Defaults to False.
    :type random_frequency: bool, optional
    :param trend: Determines what sort of trend the wave will have. Higher positive values will result in a larger upwards trend, and vice verse.
    Defaults to 0, which is no trend.
    :type trend: float, optional
    :return: Mock wave data.
    :rtype: np.ndarray by default, can also return pd.DataFrame
    """
    kw_args = locals()
    return create_data("wave", **kw_args)
