from spectral_synthesizer.Base_Models import RVgenerator
from typing import Tuple, List
from spectral_synthesizer.utils import units, data_types
import numpy as np


class KeplerianRV(RVgenerator):
    _name = RVgenerator._name + "Keplerian_RV"

    def __init__(self, planet_information: List[dict], TimeGenerator):
        self.planet_information = planet_information
        self._evaluate_user_info()
        super().__init__(RV_limits=[-np.inf * units.meter_second, np.inf * units.meter_second],
                         TimeGenerator=TimeGenerator
                         )

    def _evaluate_user_info(self):
        """
        Check the user-given parameters of the planets and check for the necessary values
        If they are not given, either one happens:
            -i) Use the default value
            -ii) Raises a RunTimeError
        :return:
        """
        # TODO: understand the parameters that we want to use!
        model_params = {"K": np.nan,
                        "ecc": 0
                        }

        for planet in self.planet_information:
            for parameter, default_value in model_params.items():
                if parameter not in planet:
                    if not np.isfinite(default_value):
                        raise RuntimeError(f"{self.name} needs to have the parameter {parameter} to generate RV curve")
                    self.planet_information[parameter] = default_value

    @property
    def name(self):
        return self.__class__._name + ": N = {}".format(len(self.planet_information))

    @property
    def model_information(self) -> List[str]:
        base_info = super().model_information

        specific_info = ['Number of planets: {}'.format(len(self.planet_information))]

        for index, planet in enumerate(self.planet_information):
            specific_info.append("\tPlanet - {}".format(index))
            for key, value in planet.items():
                specific_info.append(f"\t\t{key}: {value}")

        return base_info + specific_info
