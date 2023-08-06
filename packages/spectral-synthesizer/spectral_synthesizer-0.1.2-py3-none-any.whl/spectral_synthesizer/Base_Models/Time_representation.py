from typing import Union, Tuple, List, NoReturn
import numpy as np
from spectral_synthesizer.Base_Models import SimulationObject


class Time(SimulationObject):
    _name = "SamplingGenerator::"

    def __init__(self, time_array: Union[Tuple[float, ...], List[float], np.ndarray]):
        self._time_array = np.sort(time_array).tolist()

    @property
    def all_times(self) -> List[float]:
        return self._time_array

    def evaluate_fits_KeyWords(self, OBS_index: int) -> dict:
        KWs = super().evaluate_fits_KeyWords(OBS_index)
        time_kws = {"BJD":  self.all_times[OBS_index]
                    }

        return {** KWs, **time_kws}

    @property
    def model_information(self) -> List[str]:
        base_info = super().model_information

        info_out = ["Number Observations: {}".format(self.N_obs)
                    ]
        return base_info + info_out

    def _header(self) -> str:
        return "OBS sampling"

    @property
    def N_obs(self) -> int:
        return len(self._time_array)
