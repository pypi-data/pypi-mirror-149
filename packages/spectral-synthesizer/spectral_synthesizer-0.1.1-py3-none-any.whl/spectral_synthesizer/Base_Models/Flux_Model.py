from typing import NoReturn, List, Optional, Tuple, Set
from multiprocessing import Queue

import numpy as np

from spectral_synthesizer.Base_Models import SimulationObject, RVgenerator

from scipy.constants import convert_temperature

class FluxModel(SimulationObject):
    _name = "FluxModels::"

    # BASE -> create the overall spectrum; ADDITIONS -> add effects (e.g. tellurics, stellar activity, random noise)
    creation_level = "None"

    def __init__(self, static_basis: bool = True, RvGenerator: Optional[RVgenerator] = None,
                 include_BERV: bool = False):
        # Load the observation!
        super().__init__()

        if self.is_base_generator:
            self._static_basis = static_basis
            self._RvGen = RvGenerator
            if not self._static_basis and self._RvGen is None:
                raise RuntimeError("To create a non-static basis {} needs the RvGenerator".format(self.name))
            if not self._static_basis:
                raise NotImplementedError

            self._BASEmodel = None

        self.application_level = 0
    ###
    #  Flux generation  - BASE model
    ###

    def generate_BASE_model(self, epoch, order):
        """
        The "BASE" classes will create the overall shape of the spectrum. This function loads the basis with which
        we will create all available observations

        **NOTE**: If we want to implement this "over-time" we must pre-compute the different epochs
        Otherwise, this will be a bottleneck (the BaseModel lives on a single core!!)
        :return:
        """

        if not self.is_base_generator:
            raise RuntimeError("Trying to build the BASE spectrum with a non-BASE model")

    ###
    #  Flux generation  - ADDITIONS
    ###

    def apply_effect_to_spectra(self, wave, flux, uncerts, mask, RvGenerator):
        if self.is_base_generator:
            raise RuntimeError("Trying to introduce spectral effect with a BASE flux model")

    def store_application_level(self, level:int) -> NoReturn:
        self.application_level = level

    ###
    #  General properties of the object
    ###

    def get_model_from_order(self, epoch, order):
        if not self.is_base_generator:
            raise NotImplementedError("non-BASE model can't return a model")


        wave, flux, uncerts, mask = self._BASEmodel.get_data_from_spectral_order(order)
        return wave, flux, uncerts, mask

    def get_BASIS_bad_orders(self):
        return self._BASEmodel.bad_orders

    def valid_orders(self) -> Set[int]:
        total_orders = set(range(self._BASEmodel.N_orders))
        return total_orders - self._BASEmodel.bad_orders

    def is_base_generator(self):
        return self.__class__.creation_level == "BASE"

    ###
    #   Data storage information!
    ###

    @property
    def model_information(self) -> List[str]:
        base_info = super().model_information

        if not self.is_base_generator():
            info_out = [f"Application level:{self.application_level}"]
        else:
            info_out = []

        return base_info + info_out

    def _header(self) -> str:
        if self.is_base_generator():
            return "Flux simulation"
        else:
            return "Flux noise"

    def write_info_to_disk(self, filename, mode: str = 'a', nested_mode=False) -> NoReturn:
        if self.is_base_generator():
            super().write_info_to_disk(filename, mode, nested_mode)
        else:
            header = self._header() + " settings:"
            with open(filename, mode=mode) as to_write:
                if not nested_mode and self.application_level == 0: # horizontal "line" for division
                    to_write.write("\n\n" + "="*len(header)*2)

                extra_indents = '' if not nested_mode else '\t'
                if self.application_level == 0:
                    to_write.write("\n\n{}{}\n".format(extra_indents, header))
                else:
                    to_write.write("\n\n")
                to_write.write(f"\n\t{extra_indents}" + self.model_information[0])
                to_write.write(f"\n\t\t{extra_indents}" + f"\n\t\t{extra_indents}".join(self.model_information[1:]))


    def evaluate_fits_KeyWords(self, OBS_index: int) -> dict:
        KW = super().evaluate_fits_KeyWords(OBS_index)
        KW["BERV_corrected"] = True

        if self.is_base_generator():
            for internal_name, fits_header_name in self._BASEmodel._KW_map.items():
                KW[fits_header_name] = self._BASEmodel.get_KW_value(internal_name)

            if self._BASEmodel.is_Instrument("ESPRESSO"):
                KW["HIERARCH ESO QC BERVMAX"] = self._BASEmodel.get_KW_value("MAX_BERV").value
                KW["HIERARCH ESO QC BERV"] = self._BASEmodel.get_KW_value("BERV").value
                KW["HIERARCH ESO TEL1 AIRM START"] = self._BASEmodel.get_KW_value("airmass")

                # Environmental KWs for telfit (also needs airmassm previously loaded)
                ambi_KWs = {
                    "relative_humidity": "AMBI RHUM",
                    "ambient_temperature": "AMBI TEMP",
                }
                for name, endKW in ambi_KWs.items():
                    value = self._BASEmodel.get_KW_value(name)
                    if "temperature" in name:  # store temperature in KELVIN for TELFIT
                        value = convert_temperature(
                            value, old_scale="Kelvin", new_scale="Celsius"
                        )
                    KW[f"HIERARCH ESO TEL1 {endKW}"] = value
        # NOTE: the tellurics that might exist on the BASE Model will be mis-aligned after our
        # RV injection!
        return KW
