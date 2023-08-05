import numpy as np
import pandas as pd
import pytest

from facilyst.mocks import Features


@pytest.mark.parametrize("library", ["Pandas", "numpy", "third_option"])
def test_library(library):
    features_class = Features(library=library)
    features_data = features_class.get_data()
    if library.lower() in ["pandas", "third_option"]:
        assert isinstance(features_data, pd.DataFrame)
    else:
        assert isinstance(features_data, np.ndarray)


def test_features_default():
    features_class = Features()
    assert features_class.name == "Features"

    features = features_class.get_data()
    assert np.array_equal(
        features.columns, np.array(["ints", "rand_ints", "floats", "rand_floats"])
    )
    assert features.shape == (100, 4)
    assert features_class.library == "pandas"
    assert list(features_class.parameters.keys()) == [
        "ints",
        "rand_ints",
        "floats",
        "rand_floats",
    ]


@pytest.mark.parametrize("library", ["Pandas", "numpy", "third_option"])
@pytest.mark.parametrize("num_rows", [10, 100, 300, 1000, 5000])
@pytest.mark.parametrize(
    "ints, rand_ints, floats, rand_floats, booleans, categoricals, dates, texts, ints_nullable, floats_nullable, booleans_nullable, "
    "full_names, phone_numbers, addresses, countries, email_addresses, urls, currencies, file_paths, ipv4, ipv6, lat_longs",
    [
        [True] * 22,
        [False] * 22,
        [True] * 4 + [False] * 18,
        [False] * 4 + [True] * 18,
    ],
)
def test_features_parameters(
    library,
    num_rows,
    ints,
    rand_ints,
    floats,
    rand_floats,
    booleans,
    categoricals,
    dates,
    texts,
    ints_nullable,
    floats_nullable,
    booleans_nullable,
    full_names,
    phone_numbers,
    addresses,
    countries,
    email_addresses,
    urls,
    currencies,
    file_paths,
    ipv4,
    ipv6,
    lat_longs,
):
    kw_args = locals()
    features_class = Features(**kw_args)
    features = features_class.get_data()

    all_features = {
        k: v for k, v in kw_args.items() if k not in ["library", "num_rows"]
    }
    features_included = {k: v for k, v in all_features.items() if v}
    num_columns = len(features_included) if features_included else 22

    if library.lower() in ["pandas", "third_option"]:
        assert np.array_equal(
            features.columns,
            np.array(
                list(
                    features_included.keys()
                    if features_included
                    else all_features.keys()
                )
            ),
        )
    assert features.shape == (num_rows, num_columns)
    if (
        isinstance(features, pd.DataFrame)
        and len(features_included) == 22
        and num_rows != 10
    ):
        assert (
            len(
                features.ww.select(
                    include=["Integer"], return_schema=True
                ).logical_types
            )
            == 2
        )
        assert (
            len(
                features.ww.select(include=["Double"], return_schema=True).logical_types
            )
            == 3
        )
        assert (
            len(
                features.ww.select(
                    include=["Boolean"], return_schema=True
                ).logical_types
            )
            == 1
        )
        if num_rows == 5000:
            assert (
                len(
                    features.ww.select(
                        include=["Categorical"], return_schema=True
                    ).logical_types
                )
                == 3
            )
        else:
            assert (
                len(
                    features.ww.select(
                        include=["Categorical"], return_schema=True
                    ).logical_types
                )
                == 2
            )
        assert (
            len(
                features.ww.select(
                    include=["Datetime"], return_schema=True
                ).logical_types
            )
            == 1
        )
        assert (
            len(
                features.ww.select(
                    include=["NaturalLanguage"], return_schema=True
                ).logical_types
            )
            == 1
        )
        assert (
            len(
                features.ww.select(
                    include=["IntegerNullable"], return_schema=True
                ).logical_types
            )
            == 1
        )


def test_all_dtypes():
    features_class = Features(all_dtypes=True)
    features = features_class.get_data()

    assert features.shape == (100, 22)
