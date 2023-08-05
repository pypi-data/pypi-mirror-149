"""A mock type that returns wave data."""
from typing import Optional, Union

import numpy as np
import pandas as pd

from facilyst.mocks import MockBase


class Wave(MockBase):
    """Class to manage mock data creation of a wave.

    :param num_rows: The number of observations in the final dataset. Defaults to 100.
    :type num_rows: int, optional
    :param library: The library of which the final dataset should be, options are 'pandas' and 'numpy'. Defaults to 'numpy'.
    :type library: str, optional
    :param wave_type: The function off of which the wave will be based. Options are `sine` and `cosine`. Defaults to `sine`.
    :type wave_type: str, optional
    :param amplitude: The amplitude (height) of the wave. Defaults to 1.
    :type amplitude: int, optional
    :param frequency: The frequency (thickness) of the wave. Defaults to 1.
    :type frequency: int, optional
    :param random_amplitudes: Flag that determines if different sections of the wave will have different amplitudes. Defaults to False.
    :type random_amplitudes: bool, optional
    :param random_frequency: Flag that determines if different sections of the wave will have different frequencies. Defaults to False.
    :type random_frequency: bool, optional
    :param trend: Determines what sort of trend the wave will have. Higher positive values will result in a larger upwards trend, and vice verse.
    Defaults to 0, which is no trend.
    :type trend: float, optional
    :return: Mock wave data.
    :rtype: np.ndarray by default, can also return pd.DataFrame
    :raises ValueError: If amplitude is 0.
    :raises ValueError: If frequency is non-positive.
    :raises ValueError: If frequency is not a positive integer if `random_amplitude` or `random_frequency` are True.
    """

    name: str = "Wave"

    def __init__(
        self,
        num_rows: int = 100,
        library: str = "numpy",
        wave_type: str = "sine",
        amplitude: int = 1,
        frequency: int = 1,
        random_amplitudes: bool = False,
        random_frequency: bool = False,
        trend: int = 0,
    ) -> None:
        if wave_type.lower() in ["sin", "sine"]:
            wave_type = "sine"
        elif wave_type.lower() in ["cos", "cosine"]:
            wave_type = "cosine"
        else:
            raise ValueError(f"Parameter `wave_type` must be either `sin` or `cos`!")

        if amplitude == 0:
            raise ValueError("Parameter `amplitude` cannot be 0!")
        if not frequency > 0:
            raise ValueError("Parameter `frequency` must be above 0!")
        if not isinstance(frequency, int) and (random_frequency or random_amplitudes):
            raise ValueError(
                "Parameter `frequency` must be an integer if either `random_amplitudes` or `random_frequency` have been set to True."
            )

        self.wave_type = wave_type
        self.amplitude = amplitude
        self.frequency = frequency
        self.random_amplitudes = random_amplitudes
        self.random_frequency = random_frequency
        self.trend = trend

        parameters = {
            "wave_type": wave_type,
            "amplitude": amplitude,
            "frequency": frequency,
            "random_amplitudes": random_amplitudes,
            "random_frequency": random_frequency,
            "trend": trend,
        }

        super().__init__(library, num_rows, parameters)

    def create_data(self) -> Union[pd.Series, np.ndarray]:
        """Main function to be called to create wave data.

        :return: The final wave data created.
        :rtype: pd.DataFrame, list
        """
        data = self.generate_wave()
        if self.trend != 0:
            data = self.add_trend(data)
        data = self.handle_library(data)
        return data

    def generate_wave(self) -> np.ndarray:
        """Generates wave data.

        :return: The initial wave data created.
        :rtype: np.ndarray
        """
        signal = np.ndarray([])
        if not (self.random_frequency or self.random_amplitudes):
            samples = np.arange(self.num_rows) / self.num_rows
            if self.wave_type == "sine":
                signal = self.amplitude * np.sin(2 * np.pi * self.frequency * samples)
            elif self.wave_type == "cosine":
                signal = self.amplitude * np.cos(2 * np.pi * self.frequency * samples)
        else:
            length_of_each_wave = self.num_rows // self.frequency
            split_indices = []
            start = 0
            for split in range(self.frequency):
                if split == self.frequency - 1:
                    end = self.num_rows
                else:
                    end = start + length_of_each_wave
                split_indices.append((start, end))
                start = end
            split_signals = []
            amplitude_sign = np.random.choice(["positive", "negative"], 1)[0]
            for interval in split_indices:
                samples = np.arange(interval[1] - interval[0]) / (
                    interval[1] - interval[0]
                )
                amplitude = (
                    self.amplitude
                    if not self.random_amplitudes
                    else np.random.uniform(1, 10)
                )
                # Ensures that the final wave doesn't abruptly change direction
                amplitude = (
                    -1 * amplitude if amplitude_sign == "negative" else amplitude
                )
                # Only 1 wave per split is required
                frequency = (
                    1
                    if not self.random_frequency
                    else np.random.choice(np.arange(1, 5), 1)[0]
                )
                if self.wave_type == "sine":
                    signal = amplitude * np.sin(2 * np.pi * frequency * samples)
                elif self.wave_type == "cosine":
                    signal = amplitude * np.cos(2 * np.pi * frequency * samples)
                split_signals.extend(signal)
            signal = split_signals
        return np.array(signal)

    def add_trend(self, signal: np.ndarray) -> np.ndarray:
        """Adds trend to the data.

        :param signal: Wave data.
        :type signal: np.ndarray
        :return: The initial wave data with a trend added.
        :rtype: np.ndarray
        """
        trend_line = np.arange(
            0, np.abs(self.trend), np.abs(self.trend) / self.num_rows
        )
        if len(trend_line) != len(signal):
            trend_line = trend_line[: len(signal)]
        signal = signal + trend_line if self.trend > 0 else signal - trend_line
        return signal

    def handle_library(
        self, data: Union[pd.Series, np.ndarray]
    ) -> Union[pd.Series, np.ndarray]:
        """Handles the library that was selected to determine the format in which the data will be returned.

        :param data: The final data to be returned.
        :type data: pd.Series or np.ndarray
        :return: The final data created from the appropriate library.
        :rtype: pd.Series or np.ndarray
        """
        if self.library.lower() == "numpy":
            return data
        else:
            return pd.Series(data)
