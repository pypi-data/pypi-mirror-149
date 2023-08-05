from spectral_synthesizer.Base_Models import RVgenerator
from typing import Tuple, List
from spectral_synthesizer.utils import units, data_types
import numpy as np


class ConstantRV(RVgenerator):
    _name = RVgenerator._name + "Const_RV"

    def __init__(self, const_value: data_types.RV_measurement, TimeGenerator):
        """

        :param const_value:
        :param TimeGenerator: :ref:`TimeGeneratorObjects`
        """
        self._const_value = const_value
        super().__init__([-np.inf*units.meter_second, np.inf*units.meter_second], TimeGenerator)

    def _generate_RV(self, BJD_OBS: float) -> Tuple[data_types.RV_measurement, data_types.RV_measurement]:

        RV = self._const_value
        uncert = 0.0001 * self._internal_RV_units
        self._store_computed_RV(RV, uncert)

        return RV, uncert

    @property
    def model_information(self) -> List[str]:
        base_info = super().model_information

        specific_info = ['RV value: {}'.format(self._const_value)]

        return base_info + specific_info


    @property
    def name(self):
        return self.__class__._name + ": {}".format(self._const_value)
