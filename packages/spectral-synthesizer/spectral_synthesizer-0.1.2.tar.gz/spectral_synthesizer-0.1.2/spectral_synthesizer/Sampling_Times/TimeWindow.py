from typing import List

import numpy as np

from spectral_synthesizer.Base_Models import Time


class TimeWindow(Time):
    _name = Time._name + "Time Window"

    def __init__(self, start_time, end_time, step):
        self.start = start_time
        self.end = end_time
        self.step = step
        super().__init__(np.arange(start_time, end_time + step, step))

    @property
    def model_information(self) -> List[str]:
        base_info = super().model_information

        info_out = ["OBS start: {}".format(self.start),
                    "OBS end: {}".format(self.end),
                    "Sampling step: {}".format(self.step)
                    ]
        return base_info + info_out

