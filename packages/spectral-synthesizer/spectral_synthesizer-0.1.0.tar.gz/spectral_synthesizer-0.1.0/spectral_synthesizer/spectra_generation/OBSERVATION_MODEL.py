from typing import NoReturn, List
from spectral_synthesizer.Base_Models import FluxModel
from SBART.Base_Models import Frame


# TODO: ensure that this is a Proxy Object!
class OBSERVATION_MODEL(FluxModel):
    creation_level = 'BASE'
    _name = FluxModel._name + "OBSERVATION_BASIS"

    def __init__(self, OBS_frame: Frame, add_BERV: bool = False):
        super().__init__(
            include_BERV=add_BERV
        )

        self._BASEmodel = OBS_frame

    def load_relevant_info(self) -> NoReturn:
        super().load_relevant_info()
        self._BASEmodel.load_data()

    @property
    def model_information(self) -> List[str]:
        base_info = super().model_information
        info_out = ["BASE observation: {}".format(self._BASEmodel),
                    "Filename: {}".format(self._BASEmodel.file_path)
                    ]

        return base_info + info_out

    def get_instrument_name(self):
        return self._BASEmodel.inst_name