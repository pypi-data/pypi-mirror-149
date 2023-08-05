import numpy as np
import pandas as pd
import pytest

from facilyst.mocks import Wave


@pytest.mark.parametrize("library", ["Pandas", "numpy", "third_option"])
def test_library(library):
    wave_class = Wave(library=library)
    wave_data = wave_class.get_data()
    if library.lower() in ["pandas", "third_option"]:
        assert isinstance(wave_data, pd.Series)
    else:
        assert isinstance(wave_data, np.ndarray)


@pytest.mark.parametrize("wave_type", ["Sine", "sin", "Cosine", "cos", "cosin"])
def test_wave_type(wave_type):
    if wave_type.lower() not in ["sine", "sin", "cosine", "cos"]:
        with pytest.raises(
            ValueError,
            match="Parameter `wave_type` must be either `sin` or `cos`!",
        ):
            _ = Wave(wave_type=wave_type)


@pytest.mark.parametrize("amplitude", [-1, 0, 0.5])
def test_amplitude(amplitude):
    if amplitude == 0:
        with pytest.raises(
            ValueError,
            match="Parameter `amplitude` cannot be 0!",
        ):
            _ = Wave(amplitude=amplitude)


@pytest.mark.parametrize("random_amplitudes", [True, False])
@pytest.mark.parametrize("random_frequency", [True, False])
@pytest.mark.parametrize("frequency", [-1, 0, 0.5])
def test_frequency(random_amplitudes, random_frequency, frequency):
    if not frequency > 0:
        with pytest.raises(
            ValueError,
            match="Parameter `frequency` must be above 0!",
        ):
            _ = Wave(
                frequency=frequency,
                random_frequency=random_frequency,
                random_amplitudes=random_amplitudes,
            )
    elif not isinstance(frequency, int) and (random_frequency or random_amplitudes):
        with pytest.raises(
            ValueError,
            match="Parameter `frequency` must be an integer if either `random_amplitudes` or `random_frequency` have been set to True.",
        ):
            _ = Wave(
                frequency=frequency,
                random_frequency=random_frequency,
                random_amplitudes=random_amplitudes,
            )


def test_wave_default():
    wave_class = Wave()
    assert wave_class.library == "numpy"
    assert wave_class.num_rows == 100
    assert wave_class.wave_type == "sine"
    assert wave_class.amplitude == 1
    assert wave_class.frequency == 1
    assert wave_class.random_amplitudes is False
    assert wave_class.random_frequency is False
    assert wave_class.trend == 0

    wave_data = wave_class.get_data()
    assert isinstance(wave_data, np.ndarray)
    assert wave_data.shape == (100,)


@pytest.mark.parametrize("num_rows", [50, 100, 500])
@pytest.mark.parametrize("wave_type", ["sine", "cosine"])
@pytest.mark.parametrize("amplitude", [-1, 1, 2.5])
@pytest.mark.parametrize("frequency", [0.5, 1, 3])
def test_wave_type_amplitude_frequency_different_lengths(
    num_rows, wave_type, amplitude, frequency
):
    wave_class = Wave(
        num_rows=num_rows, wave_type=wave_type, amplitude=amplitude, frequency=frequency
    )
    wave_data = wave_class.get_data()

    samples = np.arange(num_rows) / num_rows
    if wave_type == "sine":
        expected = amplitude * np.sin(2 * np.pi * frequency * samples)
    else:
        expected = amplitude * np.cos(2 * np.pi * frequency * samples)

    np.testing.assert_array_equal(wave_data, expected)


@pytest.mark.parametrize(
    "random_frequency, random_amplitude, set_value, trend",
    [
        (False, True, 2, 0),
        (False, True, 3, 3),
        (False, True, 1, -2.2),
        (True, False, -8.4, 0),
        (True, False, -2, -5),
        (True, False, 3.5, 4.5),
        (True, True, 0, 0),
        (True, True, 0, 2.5),
        (True, True, 0, -5),
    ],
)
@pytest.mark.parametrize("wave_type", ["sine", "cosine"])
def test_wave_random(wave_type, random_frequency, random_amplitude, set_value, trend):
    if not random_frequency:
        wave_class = Wave(
            wave_type=wave_type,
            num_rows=1000,
            frequency=set_value,
            random_amplitudes=True,
            trend=trend,
        )
    elif not random_amplitude:
        wave_class = Wave(
            wave_type=wave_type,
            num_rows=1000,
            amplitude=set_value,
            random_frequency=True,
            trend=trend,
        )
    else:
        wave_class = Wave(
            wave_type=wave_type,
            num_rows=1000,
            random_frequency=True,
            random_amplitudes=True,
            trend=trend,
        )
    wave_data = wave_class.get_data()

    assert len(wave_data) == 1000
