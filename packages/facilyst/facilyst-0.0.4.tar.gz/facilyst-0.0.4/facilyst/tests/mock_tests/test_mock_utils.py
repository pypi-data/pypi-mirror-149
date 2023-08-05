from facilyst.mocks import Dates, Features, Wave, _all_mock_data_types

all_mock_data_types = [Dates, Features, Wave]


def test_mock_data_children():
    all_mock_types = {mock_type.__name__ for mock_type in all_mock_data_types}
    all_subclasses = {subclass.__name__ for subclass in _all_mock_data_types()}
    assert all_mock_types == all_subclasses
