from spectral_synthesizer.Base_Models import RVgenerator
from typing import Tuple, List, NoReturn
from spectral_synthesizer.utils import units, data_types
import numpy as np
from spectral_synthesizer.utils.keplerian import keplerian


class KeplerianRV(RVgenerator):
    """
    Produce a keplerian RV signal with N planets.
    """

    _name = RVgenerator._name + "Keplerian_RV"

    def __init__(self, planet_information: dict, TimeGenerator):
        self.planet_names = list(planet_information.keys())
        if len(self.planet_names) > 1:
            # Keplerian function does not work as expected. Actually implement it...
            # TODO: also update the self._construct_arrays after this is fixed...
            raise NotImplementedError("Can't support more than 1 planet right now.")
        self.planet_information = list(planet_information.values())
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
        model_params = {"k": np.nan,
                        "ecc": 0
                        }

        for planet_index, planet in enumerate(self.planet_information):
            for parameter, default_value in model_params.items():
                if parameter not in planet:
                    if not np.isfinite(default_value):
                        raise RuntimeError(f"{self.name} needs to have the parameter {parameter} to generate RV curve")
                    self.planet_information[parameter] = default_value

    def _construct_input(self):
        return self.planet_information[0]
        #
        # for planet in self.planet_information:
        #     for key, item in planet.items():
        #         param_dict[key].append(item)
        # return param_dict

    def _generate_RV_timeseries(self) -> NoReturn:
        print(self._OBS_times, self._construct_input())
        RV = keplerian(self._OBS_times, **self._construct_input())

        for rv in RV:
            rv = rv*self._internal_RV_units
            uncert = 0.0001 * self._internal_RV_units
            self._store_computed_RV(rv, uncert)

    @property
    def name(self):
        return self.__class__._name + ": N = {}".format(len(self.planet_information))

    @property
    def model_information(self) -> List[str]:
        base_info = super().model_information

        specific_info = ['Number of planets: {}'.format(len(self.planet_information))]

        for index, planet in enumerate(self.planet_information):
            specific_info.append("\tPlanet - {}".format(self.planet_names[index]))
            for key, value in planet.items():
                specific_info.append(f"\t\t{key}: {value}")

        return base_info + specific_info
