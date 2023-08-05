"""Utility functions for handling LFS stored datasets."""
import os
from typing import Tuple

import pandas as pd

from facilyst.tests.datasets.datasets_metadata import datasets_metadata_dict
from facilyst.utils.gen_utils import handle_problem_type


def get_dataset_metadata_by_problem_type(problem_type: str) -> dict:
    """Function that returns the metadata of locally stored datasets that match the passed problem type.

    :param problem_type: The problem type of the datasets to match.
    :type problem_type: str
    :return: All metadata corresponding to datasets matching the problem type.
    :rtype dict:
    """
    dataset_metadata_dict = {}
    for dataset_name, dataset_metadata in datasets_metadata_dict.items():
        if dataset_metadata["target_type"] == handle_problem_type(problem_type):
            dataset_metadata_dict[dataset_name] = dataset_metadata
    return dataset_metadata_dict


def get_dataset_metadata_by_name(dataset_name: str) -> dict:
    """Function that returns the metadata of locally stored datasets that match the passed name.

    :param dataset_name: The name of the datasets to match.
    :type dataset_name: str
    :return: A dictionary of the dataset name with the associated metadata.
    :rtype dict:
    """
    return {dataset_name: datasets_metadata_dict[dataset_name]}


def get_dataset(dataset_name: str) -> Tuple[pd.DataFrame, pd.Series]:
    """Function that returns the locally stored dataset that matches the passed problem type.

    :param dataset_name: The name of the dataset to match.
    :type dataset_name: str
    :return: The features and target of the dataset.
    :rtype tuple: (x, y)
    """
    if dataset_name not in datasets_metadata_dict:
        raise ValueError("That dataset doesn't exist in the datasets directory.")
    dataset_metadata = datasets_metadata_dict[dataset_name]

    assert isinstance(dataset_metadata["features"], dict)
    features = list(dataset_metadata["features"].keys())
    target = list(dataset_metadata["target"].keys())[0]
    assert isinstance(dataset_metadata["target_type"], str)
    type_ = dataset_metadata["target_type"]
    type_ = type_.replace(" ", "_")

    dataset = pd.read_csv(
        f"{os.path.dirname(os.getcwd())}/datasets/{type_}/{dataset_name}.csv"
    )

    x = pd.DataFrame(dataset[features], columns=features)
    y = pd.Series(dataset[target], name=target)

    x.ww.init()
    y.ww.init()

    return x, y


def regression_dataset_names() -> list:
    """Function that returns the names of all regression datasets.

    :return: A list of dataset names.
    :rtype list:
    """
    metadata = get_dataset_metadata_by_problem_type("regression")
    names = list(metadata.keys())
    return names


def binary_dataset_names() -> list:
    """Function that returns the names of all binary datasets.

    :return: A list of dataset names.
    :rtype list:
    """
    metadata = get_dataset_metadata_by_problem_type("binary")
    names = list(metadata.keys())
    return names


def multiclass_dataset_names() -> list:
    """Function that returns the names of all multiclass datasets.

    :return: A list of dataset names.
    :rtype list:
    """
    metadata = get_dataset_metadata_by_problem_type("multiclass")
    names = list(metadata.keys())
    return names


def ts_regression_dataset_names() -> list:
    """Function that returns the names of all time series regression datasets.

    :return: A list of dataset names.
    :rtype list:
    """
    metadata = get_dataset_metadata_by_problem_type("time series regression")
    names = list(metadata.keys())
    return names


regression_datasets = regression_dataset_names()
binary_datasets = binary_dataset_names()
multiclass_datasets = multiclass_dataset_names()
ts_regression_datasets = ts_regression_dataset_names()
