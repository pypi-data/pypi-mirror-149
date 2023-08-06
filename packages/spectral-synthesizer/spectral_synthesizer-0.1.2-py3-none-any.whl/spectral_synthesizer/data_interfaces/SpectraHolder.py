from typing import NoReturn, List
from .SimulatedSpectra import Spectrum


class SimulationHolder:
    def __init__(self, N_obs: int, storage_folder: str, available_orders: List[int], bad_orders, list_of_KWs: List[dict], inst_name:str):
        self.simulated_OBS = [Spectrum(index,
                                       available_orders=available_orders,
                                       bad_orders=bad_orders,
                                       storage_folder=storage_folder,
                                       OBS_KWs=list_of_KWs[index],
                                       inst_name=inst_name
                                       ) for index in range(N_obs)
                              ]

    def store_data_from(self, spec_index, order, wavelength, fluxes, uncerts, mask) -> NoReturn:
        spec = self.simulated_OBS[spec_index]
        spec.store_data_from_order(order, wavelength, fluxes, uncerts, mask)
        if spec.is_full:
            spec.store_data_to_disk()
            spec.close_arrays()
