from unittest.mock import patch

import pytest

from facilyst.utils import create_data, make_dates, make_features, make_wave


@pytest.mark.parametrize("mock_type", ["features", "dates", "wave"])
@pytest.mark.parametrize("library", ["pandas", "numpy"])
@patch("facilyst.mocks.mock_types.features.Features.get_data")
@patch("facilyst.mocks.mock_types.dates.Dates.get_data")
@patch("facilyst.mocks.mock_types.wave.Wave.get_data")
def test_create_data(mock_wave, mock_dates, mock_features, mock_type, library):
    mock_data = create_data(mock_type=mock_type, library=library)
    if mock_type == "features":
        mock_features.assert_called_once()
    elif mock_type == "dates":
        mock_dates.assert_called_once()
    else:
        mock_wave.assert_called_once()


@patch("facilyst.utils.main_utils.create_data")
def test_make_features(mock_create_data):
    mock_features = make_features(
        num_rows=1000, library="numpy", booleans=True, floats_nullable=True
    )
    mock_create_data.assert_called_once_with(
        "features",
        num_rows=1000,
        library="numpy",
        ints=True,
        rand_ints=True,
        floats=True,
        rand_floats=True,
        booleans=True,
        categoricals=False,
        dates=False,
        texts=False,
        ints_nullable=False,
        floats_nullable=True,
        booleans_nullable=False,
        full_names=False,
        phone_numbers=False,
        addresses=False,
        countries=False,
        email_addresses=False,
        urls=False,
        currencies=False,
        file_paths=False,
        ipv4=False,
        ipv6=False,
        lat_longs=False,
        all_dtypes=False,
    )


@patch("facilyst.utils.main_utils.create_data")
def test_make_dates(mock_create_data):
    mock_features = make_dates(
        num_rows=500, library="numpy", start_date="05/13/1989", misaligned=True
    )
    mock_create_data.assert_called_once_with(
        "dates",
        num_rows=500,
        library="numpy",
        start_date="05/13/1989",
        frequency="1D",
        missing=False,
        misaligned=True,
        duplicates=False,
        chaos=1,
    )


@patch("facilyst.utils.main_utils.create_data")
def test_make_wave(mock_create_data):
    mock_features = make_wave(
        num_rows=2000, library="numpy", wave_type="cosine", random_amplitudes=True
    )
    mock_create_data.assert_called_once_with(
        "wave",
        num_rows=2000,
        library="numpy",
        wave_type="cosine",
        amplitude=1,
        frequency=1,
        random_amplitudes=True,
        random_frequency=False,
        trend=0.0,
    )
