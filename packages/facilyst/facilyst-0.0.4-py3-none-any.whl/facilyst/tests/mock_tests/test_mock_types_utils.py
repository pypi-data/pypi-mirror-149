import pytest

from facilyst.mocks.mock_types import handle_mock_and_library_type


@pytest.mark.parametrize(
    "mock_type",
    ["DataFrame", "features", "X", "some_features", "WAVES", "wave", "dates", "DATE"],
)
@pytest.mark.parametrize("library", ["PANDAS", "Numpy", "pd", "nP", "paddy_cake"])
def test_handle_mock_and_library_type(mock_type, library):
    handled_mock_type, handled_library = handle_mock_and_library_type(
        mock_type, library
    )
    if mock_type.lower() in ["dataframe", "features", "x", "some_features"]:
        assert handled_mock_type == "features"
    elif mock_type.lower() in ["WAVES", "wave"]:
        assert handled_mock_type == "wave"
    elif mock_type.lower() in ["dates", "DATE"]:
        assert handled_mock_type == "dates"
    if library.lower() in ["pandas", "pd", "paddy_cake"]:
        assert handled_library == "pandas"
    else:
        assert handled_library == "numpy"
