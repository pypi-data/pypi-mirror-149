import os
from typing import NoReturn, List, Dict, Any
from astropy.io import fits
import numpy as np

# from synthesize import __version__
__version__ = 'as'


class Spectrum:
    def __init__(self, OBS_ID: int, available_orders: List[int], bad_orders: List[int], OBS_KWs: dict, storage_folder: str, inst_name):
        self.OBS_ID = OBS_ID
        self.instrument_name = inst_name

        self.storage_folder = storage_folder
        self._order_map = {order:index for index, order in enumerate(available_orders)}
        N_orders = len(available_orders)
        # Lists of data
        # Avoid using np.ndarray as we don't know the size of the orderwise simulations
        self.wavelengths = [[] for _ in range(N_orders)]
        self.fluxes = [[] for _ in range(N_orders)]
        self.uncertainties = [[] for _ in range(N_orders)]
        self.mask = [[] for _ in range(N_orders)]

        self.OBS_properties = OBS_KWs

        self.missing_orders_to_process = set(available_orders)
        self._stored_to_disk = False
        self.N_orders = N_orders
        self.bad_orders = bad_orders

    def generate_internal_header_KWs(self) -> Dict[str, Any]:
        header_KWs = {}
        for order in self.bad_orders:
            if self.instrument_name == "ESPRESSO":
                header_KWs[f"HIERARCH ESO QC ORDER{order + 1} SNR"] = 0

        for echelle_order, internal_order_index in self._order_map.items():
            SNR = np.divide(self.fluxes[internal_order_index], self.uncertainties[internal_order_index])
            middle_SNR = SNR[int(SNR.size/2)]

            if self.instrument_name == "ESPRESSO":
                header_KWs[f"HIERARCH ESO QC ORDER{echelle_order + 1} SNR"] = middle_SNR

        if self.instrument_name == "ESPRESSO":

            # TODO: eventually run the CCF to store this!
            header_KWs["HIERARCH ESO QC CCF RV"] = self.OBS_properties["True RV"]
            header_KWs["HIERARCH ESO QC CCF RV ERROR"] = self.OBS_properties["True RV_ERR"]

            for ind in ["CONTRAST", "FWHM", "BIS SPAN"]:
                header_KWs[f"HIERARCH ESO QC CCF {ind}"] = 0

            header_KWs["HIERARCH ESO QC SCIRED CHECK"] = 1
        return header_KWs


    def store_data_from_order(self, order, wavelength, fluxes, uncerts, mask):
        if order not in self.missing_orders_to_process:
            raise Exception("Storing data from order that is not in the to-process list")

        if self._stored_to_disk:
            raise RuntimeError("Trying to update the data of an observation already stored to disk!")
        internal_order = self._order_map[order]
        self.wavelengths[internal_order] = wavelength
        self.fluxes[internal_order] = fluxes
        self.uncertainties[internal_order] = uncerts
        self.mask[internal_order] = mask

        self.missing_orders_to_process.remove(order)

    def store_data_to_disk(self) -> NoReturn:
        """
        Store the data to disk (fits file). If the different orders have different sizes, then it will zero-pad
        on the right side of the array
        :param filepath:
        :return:
        """
        if len(self.missing_orders_to_process) != 0:
            raise RuntimeError("Trying to store OBS that is still undergoing the simulation process")
        print("Storing data to disk")


        highest_points = max(map(len, self.wavelengths))

        data_array = np.zeros((4, self.N_orders + len(self.bad_orders), highest_points))

        for echelle_order, internal_index in self._order_map.items():
            wave_order = self.wavelengths[internal_index]
            flux_order = self.fluxes[internal_index]
            uncert_order = self.uncertainties[internal_index]
            mask_order = np.multiply(1, self.mask[internal_index])


            number_points = len(wave_order)

            data_array[0, echelle_order, : number_points] = wave_order
            data_array[1, echelle_order, : number_points] = flux_order
            data_array[2, echelle_order, : number_points] = uncert_order
            data_array[3, echelle_order, : number_points] = mask_order

        header = fits.Header()

        header["VERSION"] = __version__
        for key, value in self.OBS_properties.items():
            header["HIERARCH " + key] = value

        for key, value in self.generate_internal_header_KWs().items():
            header[key] = value

        hdu = fits.PrimaryHDU(data=[], header=header)

        hdus_cubes = [hdu]

        if self.instrument_name == "ESPRESSO":
            HDU_names = {"WAVE": "WAVEDATA_VAC_BARY",
                         "SPEC": "SCIDATA",
                         "uncert": "ERRDATA",
                         "QUALDATA": "QUALDATA"
                         }

        hdu_wave = fits.ImageHDU(data=data_array[0], header=header, name=HDU_names["WAVE"])
        hdu_temp = fits.ImageHDU(data=data_array[1], header=header, name=HDU_names["SPEC"])
        hdu_uncerts = fits.ImageHDU(data=data_array[2], header=header, name=HDU_names["uncert"])
        hdu_mask = fits.ImageHDU(data=data_array[3], header=header, name=HDU_names["QUALDATA"])

        for val in [hdu_wave, hdu_temp, hdu_uncerts, hdu_mask]:
            hdus_cubes.append(val)

        hdul = fits.HDUList(hdus_cubes)

        hdul.writeto(self.filepath, overwrite=True)

    @property
    def filepath(self) -> str:
        return os.path.join(self.storage_folder, "simulation_{}.fits".format(self.OBS_ID))

    def close_arrays(self):

        self.wavelengths = []
        self.fluxes = []
        self.uncertainties = []

    @property
    def is_full(self) -> bool:
        return len(self.missing_orders_to_process) == 0

    def __str__(self):
        return "Simulated Spectrum from {}".format(self.OBS_properties["BJD"])


if __name__ == '__main__':
    spec = Spectrum(0, 1, {}, storage_folder='/home/amiguel/phd/tools/spectral_generator/testes/simulated_data')
    spec.store_data_from_order(0, [1, 1], [2, 2], [3, 3])
    # spec.store_data_from_order(1, [1,1,2]*10,[1,2,2]*10, 10*[4,3,3])
    spec.store_data_to_disk()
