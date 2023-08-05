import matplotlib
import numpy as np
import pytest

from facilyst.graphs import Scatter


@pytest.mark.parametrize("x_type", ["pandas", "numpy", "list", "None"])
@pytest.mark.parametrize("y_type", ["pandas", "numpy", "list", "None"])
def test_warnings_without_dataset(x_type, y_type, one_dim_data):
    if x_type not in ["pandas", "numpy"]:
        with pytest.raises(
            ValueError,
            match="If `dataset` is None, then `x` must be a collection of data of type pd.Series or np.ndarray!",
        ):
            _ = Scatter(dataset=None, x=one_dim_data[x_type], y=one_dim_data[y_type])
    elif y_type not in ["pandas", "numpy"]:
        with pytest.raises(
            ValueError,
            match="If `dataset` is None, then `y` must be a collection of data of type pd.Series or np.ndarray!",
        ):
            _ = Scatter(dataset=None, x=one_dim_data[x_type], y=one_dim_data[y_type])
    else:
        _ = Scatter(dataset=None, x=one_dim_data[x_type], y=one_dim_data[y_type])


@pytest.mark.parametrize("dataset_type", ["pandas", "numpy", "list"])
@pytest.mark.parametrize("x_type", ["pandas", "numpy", "list", "str", "None"])
@pytest.mark.parametrize("y_type", ["pandas", "numpy", "list", "str", "None"])
def test_warnings_with_dataset(
    dataset_type, x_type, y_type, multi_dim_data, one_dim_data
):
    if dataset_type not in ["pandas", "numpy"]:
        with pytest.raises(
            ValueError, match="`dataset` must be of type pd.DataFrame or np.ndarray!"
        ):
            _ = Scatter(
                dataset=multi_dim_data[dataset_type],
                x=one_dim_data[x_type],
                y=one_dim_data[y_type],
            )
    elif x_type not in ["str", "None"] or y_type not in ["str", "None"]:
        with pytest.raises(
            ValueError,
            match="If `dataset` is not None, then `x` and `y` need to be hashable values referring to column names in the dataset!",
        ):
            _ = Scatter(
                dataset=multi_dim_data[dataset_type],
                x=one_dim_data[x_type],
                y=one_dim_data[y_type],
            )
    elif x_type == "None" or y_type == "None":
        with pytest.raises(ValueError, match="`x` and `y` cannot be None!"):
            _ = Scatter(
                dataset=multi_dim_data[dataset_type],
                x=one_dim_data[x_type],
                y=one_dim_data[y_type],
            )
    else:
        _ = Scatter(
            dataset=multi_dim_data[dataset_type],
            x=one_dim_data[x_type],
            y=one_dim_data[y_type],
        )


def test_multidim_x_y_without_dataset(multi_dim_data):
    with pytest.raises(
        ValueError,
        match="If `dataset` is None, both x and y must be one dimensional!",
    ):
        _ = Scatter(
            dataset=None,
            x=multi_dim_data["numpy"],
            y=multi_dim_data["numpy"],
        )


@pytest.mark.parametrize("dataset_type", ["pandas", "numpy"])
@pytest.mark.parametrize("x_name", [0, 11])
@pytest.mark.parametrize("y_name", [0, 11])
def test_column_not_in_dataset(dataset_type, x_name, y_name, multi_dim_data):
    if x_name == 11 or y_name == 11:
        with pytest.raises(
            ValueError,
            match="Column `11` could not be found in the `dataset` columns! If you passed in a "
            "dataset of type np.ndarray, use an integer to indicate the column number e.g. 0, 1, 2, etc. "
            "`dataset` has 10 columns.",
        ):
            _ = Scatter(dataset=multi_dim_data[dataset_type], x=x_name, y=y_name)
    else:
        _ = Scatter(dataset=multi_dim_data[dataset_type], x=x_name, y=y_name)


def test_default_size_and_resize(multi_dim_data):
    dataset = multi_dim_data["pandas"]

    scatter = Scatter(x=0, y=1, dataset=dataset)
    assert np.array_equal(scatter.get_size(), np.array([11.7, 8.27]))

    scatter.resize(20, 10)
    assert np.array_equal(scatter.get_size(), np.array([20, 10]))


def test_get_figure(multi_dim_data):
    dataset = multi_dim_data["pandas"]

    scatter = Scatter(x=0, y=1, dataset=dataset)
    assert isinstance(scatter.get_figure()(), matplotlib.figure.Figure)
