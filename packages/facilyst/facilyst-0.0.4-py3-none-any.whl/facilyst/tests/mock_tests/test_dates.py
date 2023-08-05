import numpy as np
import pandas as pd
import pytest

from facilyst.mocks import Dates


@pytest.mark.parametrize("library", ["Pandas", "numpy", "third_option"])
def test_library(library):
    dates_class = Dates(library=library)
    dates_data = dates_class.get_data()
    if library.lower() in ["pandas", "third_option"]:
        assert isinstance(dates_data, pd.DatetimeIndex)
    else:
        assert isinstance(dates_data, np.ndarray)


@pytest.mark.parametrize("chaos", [0, 2])
@pytest.mark.parametrize("misaligned", [True, False])
@pytest.mark.parametrize("num_rows", [2, 29, 30])
def test_warning(num_rows, misaligned, chaos):
    if num_rows < 3:
        with pytest.raises(
            ValueError,
            match="Parameter `num_rows` must be 3 or above!",
        ):
            dates_class = Dates(num_rows=num_rows, misaligned=misaligned, chaos=chaos)
    elif misaligned and chaos != 0 and num_rows < 30:
        with pytest.raises(
            ValueError,
            match="The `num_rows` parameter must be a minimum of 30 if chaos is not 0.",
        ):
            dates_class = Dates(num_rows=num_rows, misaligned=misaligned, chaos=chaos)
    else:
        dates_class = Dates(num_rows=num_rows, misaligned=misaligned, chaos=chaos)
        if misaligned:
            assert dates_class.chaos == chaos
        else:
            assert dates_class.chaos == 0


def test_dates_default():
    dates_class = Dates()
    assert dates_class.library == "pandas"
    assert dates_class.num_rows == 100
    assert dates_class.start_date == "1/1/2001"
    assert dates_class.frequency == "1D"
    assert dates_class.missing is False
    assert dates_class.misaligned is False
    assert dates_class.duplicates is False
    assert dates_class.chaos == 0

    dates_data = dates_class.get_data()
    assert isinstance(dates_data, pd.DatetimeIndex)
    assert dates_data.shape == (100,)
    assert pd.infer_freq(dates_data) == "D"


@pytest.mark.parametrize("num_rows", [30, 100])
@pytest.mark.parametrize("start_date", ["1/1/2001", "3/5/2001"])
@pytest.mark.parametrize("num_freq", ["", "2"])
@pytest.mark.parametrize("str_freq", ["S", "D", "W", "MS", "A"])
@pytest.mark.parametrize(
    "missing, misaligned, duplicates",
    [
        [False, False, True],
        [False, False, True],
        [True, True, False],
        [False, True, True],
        [True, False, True],
        [True, True, False],
        [True, True, True],
    ],
)
@pytest.mark.parametrize("chaos", [0, 1, 3, 7, 10])
def test_dates_variations(
    num_rows, start_date, num_freq, str_freq, missing, misaligned, duplicates, chaos
):
    dates_class = Dates(
        num_rows=num_rows,
        start_date=start_date,
        frequency=num_freq + str_freq,
        missing=missing,
        misaligned=misaligned,
        duplicates=duplicates,
        chaos=chaos,
    )
    dates_data = dates_class.get_data()

    if duplicates:
        chaos_percent = Dates.chaos_percentage[chaos] / 100
        num_chaos_rows = chaos_percent * num_rows
        num_of_each_issue = int(num_chaos_rows) // sum(
            [missing, misaligned, duplicates]
        )
        assert dates_data.shape == (num_rows + num_of_each_issue,)
    else:
        assert dates_data.shape == (num_rows,)

    if chaos:
        if missing:
            assert not dates_data.is_monotonic
        else:
            assert dates_data.is_monotonic
