import os

import numpy as np
from tabletexifier import Table
from spectral_synthesizer.utils import units, data_types
from spectral_synthesizer.utils import data_types
from spectral_synthesizer.Base_Models import Time, SimulationObject

from typing import Tuple, NoReturn, List

from spectral_synthesizer.utils.units import kilometer_second


class RVgenerator(SimulationObject):
    _name = "RvGenerator::"

    def __init__(self, RV_limits, TimeGenerator: Time):
        super().__init__()
        self._internal_RV_units = units.meter_second

        if len(RV_limits) != 2:
            raise ValueError("RV limits should only have two entries, not {}".format(len(RV_limits)))

        if RV_limits[0] >= RV_limits[1]:
            raise ValueError("The lower RV limit is >= than the upper RV limit")

        if isinstance(RV_limits[0], data_types.Quantity):
            RV_limits = units.convert_data(RV_limits, new_units=self._internal_RV_units, as_value=False)
        else:
            raise ValueError("The RV limits should be Quantities!")

        self._RVlimits = RV_limits
        self._TimeGenerator = TimeGenerator
        self._OBS_times = TimeGenerator.all_times
        self._generated_RVs = []
        self._RV_uncertainties = []

        self._generate_RV_timeseries()

    def evaluate_fits_KeyWords(self, OBS_index: int) -> dict:
        KWs = super().evaluate_fits_KeyWords(OBS_index)
        time_kws = self._TimeGenerator.evaluate_fits_KeyWords(OBS_index)
        _, rv, rv_err = self.get_information_from_epoch(OBS_index)
        KWs["True RV"] = rv.to(kilometer_second).value
        KWs["True RV_ERR"] = rv_err.to(kilometer_second).value

        return {** KWs, **time_kws}

    def get_information_from_epoch(self, epoch) -> Tuple[float, data_types.RV_measurement, data_types.RV_measurement]:
        return self._OBS_times[epoch], self._generated_RVs[epoch], self._RV_uncertainties[epoch]

    def _generate_RV_timeseries(self) -> NoReturn:
        for time in self._OBS_times:
            self._generate_RV(time)

    def _generate_RV(self, BJD_OBS: float) -> Tuple[data_types.RV_measurement, data_types.RV_measurement]:
        """
        Generate the RV for a given observation date
        :param BJD_OBS:
        :return:
        """
        RV = 0 * units.kilometer_second
        uncert = 0 * units.kilometer_second

        self._store_computed_RV(RV, uncert)
        return RV, uncert

    def _store_computed_RV(self, RV, uncert) -> NoReturn:
        self._generated_RVs.append(RV)
        self._RV_uncertainties.append(uncert)

    def write_info_to_disk(self, filename, mode='a') -> NoReturn:
        folder_to_store = os.path.dirname(os.path.abspath(filename))
        self._write_true_results_to_disk(os.path.join(folder_to_store, "true_RVs.txt"))

        super().write_info_to_disk(filename, mode=mode)
        self._TimeGenerator.write_info_to_disk(filename, mode='a')

    def _write_true_results_to_disk(self, filename: str, mode: str = 'w') -> NoReturn:
        """
        Write a file to disk with the true (injected) RVs
        :param filename: name of the file
        :param mode: 'w' to write; 'a' to append
        :return:
        """
        with open(filename, mode=mode) as to_write:
            if mode == 'w':
                to_write.write("BJD\tRV\tRV_ERR")
            for index in range(len(self._OBS_times)):
                to_write.write("\n{}\t{}\t{}".format(self._OBS_times[index],
                                                     self._generated_RVs[index].to(self._internal_RV_units).value,
                                                     self._RV_uncertainties[index].to(self._internal_RV_units).value
                                                     )
                               )

    @property
    def N_obs(self) -> int:
        return len(self._OBS_times)

    def _header(self) -> str:
        return "RV simulation"

    def __str__(self):
        tab = Table(["Number", "RV", "ERROR"], table_style="MNRAS")
        for index in range(self.N_obs):
            tab.add_row([self._OBS_times[index], self._generated_RVs[index], self._RV_uncertainties[index]])
        return str(tab)
