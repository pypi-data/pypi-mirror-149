from facilyst.models import RandomForestRegressor


def test_equals():
    rf_regressor = RandomForestRegressor()

    assert isinstance(rf_regressor.__eq__(4), NotImplemented.__class__)
