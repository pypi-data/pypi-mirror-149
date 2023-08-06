from numpy import ndarray

from spectral_synthesizer.Base_Models import RVgenerator
from typing import Tuple, Union, List
from spectral_synthesizer.utils import units, data_types
from spectral_synthesizer.utils.data_types import RV_measurement
import numpy as np


class RandomRV(RVgenerator):
    """
    ads
    """
    _name = RVgenerator._name + "Random_RV"

    def __init__(self, distribution: str, RV_limits: Tuple[RV_measurement, RV_measurement], TimeGenerator):
        """
        init docstring
        :param distribution:
        :param RV_limits:
        :param TimeGenerator:
        """
        self._prob_distribution = distribution
        super().__init__(RV_limits, TimeGenerator)

    def _random_draw(self) -> Union[ndarray, int, float, complex]:
        """
        :return:
        """

        if self._prob_distribution == "uniform":
            return np.random.uniform(low=self._RVlimits[0].value,
                                     high=self._RVlimits[1].value
                                     )
        else:
            raise ValueError("")

    def _generate_RV(self, BJD_OBS: float) -> Tuple[data_types.RV_measurement, data_types.RV_measurement]:
        RV = self._random_draw() * self._internal_RV_units
        uncert = 0.0010 * self._internal_RV_units
        self._store_computed_RV(RV, uncert)

        return RV, uncert

    @property
    def model_information(self) -> List[str]:
        base_info = super().model_information

        specific_info = ['Distribution: {}'.format(self._prob_distribution),
                         "RV_limits : {}".format(self._RVlimits)]

        return base_info + specific_info
