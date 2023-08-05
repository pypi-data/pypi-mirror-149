"""Utility functions for all mock types."""
from facilyst.mocks import MockBase
from facilyst.utils.gen_utils import _get_subclasses


def _all_mock_data_types() -> list:
    return _get_subclasses(MockBase)
