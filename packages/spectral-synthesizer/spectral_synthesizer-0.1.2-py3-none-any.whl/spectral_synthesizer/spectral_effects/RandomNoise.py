from typing import NoReturn, List, Tuple

import numpy as np

from spectral_synthesizer.Base_Models import FluxModel


class RandomNoise(FluxModel):
    creation_level = 'ADDITIONS'
    _name = FluxModel._name + "RandomNoiseEffect"

    def __init__(self):
        super().__init__()

    def apply_effect_to_spectra(self, wave, flux, uncerts, mask, RvGenerator) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        new_flux = np.random.normal(flux, uncerts)
        return wave, new_flux, uncerts, mask
    
    @property
    def model_information(self) -> List[str]:
        base_info = super().model_information
        info_out = [f"Distribution: Gaussian",
                    ]
        return base_info + info_out
