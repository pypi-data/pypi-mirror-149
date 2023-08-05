"""General utility functions."""
import importlib
from types import ModuleType
from typing import Optional


def _get_subclasses(base_class: object) -> list:
    """Returns all subclasses to the base class passed.

    :param base_class:
    :type base_class: object
    :return: The list of child classes.
    :rtype: list
    """
    classes_to_check = base_class.__subclasses__()

    subclasses = []

    while classes_to_check:
        subclass = classes_to_check.pop()
        subclasses.append(subclass)

    return subclasses


error_str = (
    "{name} is not installed. Please install {name} using pip install {name} or install facilyst with extra "
    "dependencies using pip install facilyst[extra]."
)
import_errors_dict = {
    "catboost": error_str.format(name="catboost"),
    "xgboost": error_str.format(name="xgboost"),
    "torch": error_str.format(name="torch"),
    "transformers": error_str.format(name="transformers"),
    "sentencepiece": error_str.format(name="sentencepiece"),
    "keras_preprocessing": error_str.format(name="keras_preprocessing"),
}


def import_or_raise(library: str, error_msg: Optional[str] = None) -> ModuleType:
    """Import the requested library.

    :param library: The name of the library.
    :type library: str
    :param error_msg: The error message to return if the import fails.
    :type error_msg: str
    :return: The imported library.
    :rtype: ModuleType
    :raises ImportError: If the library is not installed.
    :raises Exception: A general exception to not being able to import the library.
    """
    try:
        return importlib.import_module(library)
    except ImportError:
        if error_msg is None:
            error_msg = ""
        msg = f"Missing extra dependency '{library}'. {error_msg}"
        raise ImportError(msg)


def handle_problem_type(problem_type: str) -> str:
    """Handles the problem type passed to be returned in a consistent way.

    :param problem_type: The problem type to match.
    :type problem_type: str
    :return: The standardized problem type.
    :rtype: str
    """
    if problem_type.lower() in ["regression", "regressor"]:
        problem_type_ = "regression"
    elif problem_type.lower() in ["classification", "classifier"]:
        problem_type_ = "classification"
    elif problem_type.lower() in ["binary"]:
        problem_type_ = "binary"
    elif problem_type.lower() in ["multiclass", "multi", "multi class"]:
        problem_type_ = "multiclass"
    elif problem_type.lower() in [
        "time series regression",
        "timeseries regression",
        "ts regression",
    ]:
        problem_type_ = "time series regression"
    else:
        raise ValueError("That problem type isn't recognized!")

    return problem_type_
