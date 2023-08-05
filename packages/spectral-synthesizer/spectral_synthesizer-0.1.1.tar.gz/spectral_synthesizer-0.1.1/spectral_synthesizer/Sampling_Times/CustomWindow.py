from typing import Union, Tuple, List
from spectral_synthesizer.Base_Models import Time


class CustomWindow(Time):
    _name = Time._name + "Custom Window"

    def __init__(self, time_array: Union[Tuple[float, ...], List[float]]):
        self.time_array = time_array
        super().__init__(time_array)

    @property
    def model_information(self) -> List[str]:
        base_info = super().model_information

        info_out = ["Custom array: {}".format(self.time_array)
                    ]

        return base_info + info_out
