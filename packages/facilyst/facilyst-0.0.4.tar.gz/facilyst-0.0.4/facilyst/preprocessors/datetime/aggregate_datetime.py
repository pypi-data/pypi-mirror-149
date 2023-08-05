"""preprocessor that combines datetime-relevant fields into a datetime column."""
from typing import Any, Optional, Tuple, Union

import numpy as np
import pandas as pd

from facilyst.preprocessors.preprocessor_base import PreprocessorBase


class AggregateDatetime(PreprocessorBase):
    """A preprocessor that aggregates specified columns with partial datetime information into one datetime column.

    All parameters passed will have their respective columns dropped, and a new column named "Aggregated_Datetime" will
    be created. The name of the new column can be manually set with the parameter "name_aggregated".
    The format of the aggregated datetime column will be `%yyyy-%mm-%dd %HH:%MM:%SS±zz:zz`.

    :param year: The name of the column that contains the year. Years must have 4 digits e.g. 1934 instead of 34.
    If no column name is passed it will default to 2001.
    :type year: str, optional
    :param month: The name of the column that contains the month. If no column name is passed it will default to 01.
    :type month: str, optional
    :param day: The name of the column that contains the day. If no column name is passed it will default to 01.
    :type day: str, optional
    :param hour: The name of the column that contains the hour. If no column name is passed it will default to 00.
    :type hour: str, optional
    :param minute: The name of the column that contains the minute. If no column name is passed it will default to 00.
    :type minute: str, optional
    :param second: The name of the column that contains the second. If no column name is passed it will default to 00.
    :type second: str, optional
    :param time_zone: The name of the column that contains the time zone.  If no column name is passed it will default to +00:00 (UTC).
    :type time_zone: str, optional
    :param name_aggregated: The name of the new aggregated datetime column that will be created.
    Defaults to `Aggregated_Datetime`.
    :type name_aggregated: str, optional
    """

    name: str = "Aggregate DateTime"

    primary_type: str = "x"
    secondary_type: str = "aggregation"
    tertiary_type: str = "datetime"

    hyperparameters: dict = {}

    datetime_defaults: dict = {
        "year": "2001",
        "month": "01",
        "day": "01",
        "hour": "00",
        "minute": "00",
        "second": "00",
        "time_zone": "+00:00",
    }

    def __init__(
        self,
        year: Optional[str] = None,
        month: Optional[str] = None,
        day: Optional[str] = None,
        hour: Optional[str] = None,
        minute: Optional[str] = None,
        second: Optional[str] = None,
        time_zone: Optional[str] = None,
        name_aggregated: Optional[str] = "Aggregated_Datetime",
        **kwargs,
    ):
        name_aggregated = name_aggregated or "Aggregated_Datetime"
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.second = second
        self.time_zone = time_zone
        self.name_aggregated = name_aggregated

        parameters = {
            "year": year,
            "month": month,
            "day": day,
            "hour": hour,
            "minute": minute,
            "second": second,
            "time_zone": time_zone,
            "name_aggregated": name_aggregated,
        }
        parameters.update(kwargs)

        super().__init__(preprocessor=None, parameters=parameters)

    def fit(
        self,
        x: Union[pd.DataFrame, np.ndarray],
        y: Any = None,
    ) -> PreprocessorBase:
        """Fits on the data using the preprocessor.

        :param x: The testing data for the preprocessor to fit on.
        :type x: pd.DataFrame or np.ndarray
        :param y: The testing data for the preprocessor to fit on. Ignored.
        :type y: pd.Series or np.array
        :raises ValueError: If `name_aggregated` is set to a column name in the dataset that will not be dropped.
        """
        if self.name_aggregated in set(x.columns) - {
            col for col in self.parameters.values() if col != self.name_aggregated
        }:
            raise ValueError(
                f"The parameter `name_aggregated` is set to `{self.name_aggregated}` which is already a column in x. "
                f"Please drop that column or set `name_aggregated` to a different value. `name_aggregated` can be set "
                f"to a column name that is passed into one of the other parameters, as the original column will be dropped."
            )

        return self

    def transform(
        self,
        x: Union[pd.DataFrame],
        y: Any = None,
    ) -> Tuple[pd.DataFrame, pd.Series]:
        """Transforms the data using the preprocessor.

        :param x: The testing data for the preprocessor to transform.
        :type x: pd.DataFrame
        :param y: The testing data for the preprocessor to transform. Ignored.
        :type y: pd.Series or np.array
        :return: The transformed data.
        :rtype tuple:
        """
        df = x.copy()

        def _get_latest_col(col_name_: Optional[str]) -> Union[pd.Series, None]:
            if col_name_:
                return df.pop(col_name_)
            return None

        aggregated_datetime = pd.Series(
            ["" for _ in range(len(df))], name=self.name_aggregated
        )
        for col_name in [
            "year",
            "month",
            "day",
            "hour",
            "minute",
            "second",
            "time_zone",
        ]:
            new_col = _get_latest_col(self.parameters[col_name])
            if col_name not in ["time_zone"] and new_col is not None:
                new_col = new_col.astype(str)
                if col_name == "year":
                    new_col = new_col.apply(
                        lambda val: f"20{val}" if len(val) != 4 else val
                    )
                else:
                    new_col = new_col.apply(lambda val: str(val).rjust(2, "0"))
            if new_col is not None:
                if col_name == "time_zone":
                    aggregated_datetime = aggregated_datetime.reset_index()
                    aggregated_datetime = aggregated_datetime.apply(
                        lambda ind: ind[self.name_aggregated].tz_convert(
                            new_col[ind.name]
                        ),
                        axis=1,
                    )
                    aggregated_datetime = pd.Series(aggregated_datetime)
                    break
                aggregated_datetime += new_col
            else:
                if col_name == "time_zone":
                    break
                aggregated_datetime += AggregateDatetime.datetime_defaults[col_name]
            if col_name in ["year", "month"]:
                aggregated_datetime += "-"
            elif col_name in ["hour", "minute"]:
                aggregated_datetime += ":"
            elif col_name == "day":
                aggregated_datetime += " "
            else:
                aggregated_datetime = pd.to_datetime(
                    aggregated_datetime,
                    format="%Y-%m-%d %H:%M:%S",
                    exact=True,
                    utc=True,
                )

        df[self.name_aggregated] = aggregated_datetime

        return df, y
