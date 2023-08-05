import pytest

from facilyst.utils import (
    get_dataset,
    get_dataset_metadata_by_name,
    ts_regression_datasets,
)


@pytest.mark.parametrize("dataset_name", ts_regression_datasets)
def test_regression_datasets(dataset_name):
    x, y = get_dataset(dataset_name)
    metadata = get_dataset_metadata_by_name(dataset_name)[dataset_name]

    expected_num_of_features = metadata["num_of_features"]
    expected_num_of_rows = metadata["num_of_rows"]
    expected_target_type = metadata["target_type"]
    expected_time_index = metadata["time_index"]
    expected_features = set(metadata["features"].keys())
    expected_target = list(metadata["target"].keys())[0]

    assert x.shape[1] == expected_num_of_features
    assert len(x) == expected_num_of_rows
    assert "time series regression" == expected_target_type
    assert x.ww.select(include=["datetime"]).columns[0] == expected_time_index
    assert set(x.columns) == expected_features
    assert y.name == expected_target

    expected_features_logical_types = metadata["features"]
    expected_target_logical_type = metadata["target"][expected_target]
    actual_features_logical_types = {
        col_: type_.__str__() for col_, type_ in x.ww.logical_types.items()
    }
    actual_target_logical_type = y.ww.logical_type.__str__()

    assert actual_features_logical_types == expected_features_logical_types
    assert actual_target_logical_type == expected_target_logical_type
