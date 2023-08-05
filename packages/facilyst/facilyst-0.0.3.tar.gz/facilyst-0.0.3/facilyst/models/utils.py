"""Utility functions for all model types."""
from typing import Optional

from facilyst.models.model_base import ModelBase
from facilyst.utils import _get_subclasses
from facilyst.utils.gen_utils import handle_problem_type


def get_models(model: str, problem_type: Optional[str] = None) -> list:
    """Return all models that correspond to either the name or type passed.

    A model can be selected either by its name, or by its primary, secondary, or tertiary type. If problem type is passed,
    then only models belonging to that type will be returned. If the name of a model is passed that conflicts with the
    problem type passed, then an error will be raised.

    :param model: The name or type of model(s) to return.
    :type model: str
    :param problem_type: The problem type to which the models should belong, `regression` or `classification`.
    :type problem_type: str, optional
    :return: A list of all models found.
    :rtype list:
    """
    if not model:
        raise ValueError("No model name passed.")

    all_models = _get_subclasses(ModelBase)
    if " " not in model:
        if model.lower() in ["all", "any"]:
            return all_models
        subset_models_primary = [
            each_model
            for each_model in all_models
            if model.lower() in each_model.primary_type.lower()
        ]
        subset_models_secondary = [
            each_model
            for each_model in all_models
            if model.lower() in each_model.secondary_type.lower()
        ]
        subset_models_tertiary = [
            each_model
            for each_model in all_models
            if model.lower() in each_model.tertiary_type.lower()
        ]
        subset_models = (
            subset_models_primary or subset_models_secondary or subset_models_tertiary
        )

        if not subset_models:
            raise ValueError(
                f"That model type doesn't exist. Available model types are: \n"
                f"Primary types: {set(each_model.primary_type for each_model in all_models)} \n"
                f"Secondary types: {set(each_model.secondary_type for each_model in all_models)} \n"
                f"Tertiary types: {set(each_model.tertiary_type for each_model in all_models)}"
            )
        else:
            if problem_type:
                subset_models = _get_models_by_problem_type(subset_models, problem_type)
                if not subset_models:
                    raise ValueError(
                        f"There are no {model} models belong to the {problem_type} problem type available."
                    )
            return subset_models

    model_name_found = []
    for each_model in all_models:
        if each_model.name.lower() == model.lower():
            model_name_found = [each_model]
            break
    if not model_name_found:
        raise ValueError(
            f"That model doesn't exist. This is the list of all available models: {[each_model.name for each_model in all_models]}"
        )
    elif problem_type:
        final_model = _get_models_by_problem_type(model_name_found, problem_type)
        if not final_model:
            raise ValueError(
                f"The model {model_name_found[0].name} was found but doesn't match the problem type {problem_type}"
            )
        else:
            return final_model
    else:
        return model_name_found


def _get_models_by_problem_type(models: list, problem_type: str) -> list:
    accepted_models = []
    for model in models:
        if model.primary_type == handle_problem_type(problem_type):
            accepted_models.append(model)
    return accepted_models
