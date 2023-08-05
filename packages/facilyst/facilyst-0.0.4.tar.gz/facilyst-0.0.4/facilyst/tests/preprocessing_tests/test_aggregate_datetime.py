import numpy as np
import pandas as pd
import pytest

from facilyst.preprocessors import AggregateDatetime


def test_aggregate_datetime_class_variables():
    assert AggregateDatetime.name == "Aggregate DateTime"
    assert AggregateDatetime.primary_type == "x"
    assert AggregateDatetime.secondary_type == "aggregation"
    assert AggregateDatetime.tertiary_type == "datetime"
    assert AggregateDatetime.hyperparameters == {}


@pytest.mark.parametrize("name_agg", ("time_zones", "dates"))
def test_aggregate_datetime_naming_errors(name_agg):
    df = pd.DataFrame()
    df["dates"] = pd.date_range("1/1/21", periods=100)
    df["yr"] = [str(i) for i in range(1925, 2025)]
    df["mon"] = np.random.choice([str(i) for i in range(1, 13)], 100)
    df["time_zones"] = ["time zones"] * 100
    df["random"] = [i for i in range(100)]

    agg = AggregateDatetime(
        year="yr", month="mon", time_zone="time_zones", name_aggregated=name_agg
    )
    with pytest.raises(
        ValueError, match=f"The parameter `name_aggregated` is set to `{name_agg}`"
    ):
        agg.fit(df, None)


@pytest.mark.parametrize(
    "year, month, day, hour, min, sec, tz, name_agg",
    [
        (None, None, None, None, None, None, None, None),
        ("yr", "mon", "d", None, None, None, "tz", ""),
        (None, None, None, "hr", "min", "sec", None, "Aggregated_Datetime"),
        ("yr", False, "d", None, "min", None, "tz", "Another name"),
        (None, "mon", None, "hr", None, "sec", "tz", "Date"),
        ("yr", "mon", "d", "hr", "min", "sec", "tz", None),
    ],
)
def test_aggregate_datetime(year, month, day, hour, min, sec, tz, name_agg):
    df = pd.DataFrame()
    df["ints"] = [i for i in range(100)]
    df["cats"] = np.random.choice(["First", "Second", "Third"], 100)
    df["dates"] = pd.date_range("1/1/21", periods=100)
    df["yr"] = [str(i) for i in range(1925, 2025)]
    df["mon"] = np.random.choice([str(i) for i in range(1, 13)], 100)
    df["d"] = np.random.choice([str(i) for i in range(1, 29)], 100)
    df["hr"] = np.random.choice([str(i) for i in range(24)], 100)
    df["min"] = np.random.choice([str(i) for i in range(60)], 100)
    df["sec"] = np.random.choice([str(i) for i in range(60)], 100)
    df["tz"] = np.random.choice(
        [
            "UTC",
            "US/Central",
            "US/Eastern",
            "Africa/Douala",
            "Asia/Baghdad",
            "Europe/Lisbon",
        ],
        100,
    )
    y = pd.Series([i for i in range(100)])

    agg = AggregateDatetime(
        year=year,
        month=month,
        day=day,
        hour=hour,
        minute=min,
        second=sec,
        time_zone=tz,
        name_aggregated=name_agg,
    )
    agg.fit(df, y)
    results_x, results_y = agg.transform(df, y)

    assert len(results_x) == len(df)
    pd.testing.assert_series_equal(results_y, y)
    expected_agg_column = "Aggregated_Datetime" if not name_agg else name_agg
    assert expected_agg_column in results_x.columns
    assert (
        results_x[expected_agg_column].dtype == "object"
        if tz
        else "datetime64[ns, UTC]"
    )
    assert all(
        [
            isinstance(agg_datetime, pd.Timestamp)
            for agg_datetime in results_x[expected_agg_column]
        ]
    )
    assert "ints" in results_x.columns
    assert "cats" in results_x.columns
    assert "dates" in results_x.columns

    inputs_ = {year, month, day, hour, min, sec, tz}
    expected_dropped = {col for col in inputs_ if col}
    expected_kept = {"yr", "mon", "d", "hr", "min", "sec", "tz"} - expected_dropped
    assert set(results_x.columns).intersection(expected_dropped) == set()
    assert set(results_x.columns).intersection(expected_kept) == expected_kept

    # Validate 10 times that the aggregate datetime values matches their components
    for ind_ in np.random.choice(range(len(df)), 10):
        expected_components = df.iloc[ind_, 3:]
        actual_aggregated = results_x.iloc[ind_][expected_agg_column]
        actual_aggregated_utc = actual_aggregated.tz_convert(
            tz="UTC"
        )  # Cannot test UTC against non-UTC TimeStamps
        actual_components = {
            "yr": actual_aggregated_utc.year,
            "mon": actual_aggregated_utc.month,
            "d": actual_aggregated_utc.day,
            "hr": actual_aggregated_utc.hour,
            "min": actual_aggregated_utc.minute,
            "sec": actual_aggregated_utc.second,
            "tz": str(actual_aggregated.tzinfo),
        }
        for used_col in expected_dropped:
            assert str(actual_components[used_col]) == expected_components[used_col]
