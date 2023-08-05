import datetime
import traceback
from typing import NoReturn, Optional, Tuple, List
import os
import numpy as np

from itertools import product
from spectral_synthesizer.Base_Models import FluxModel, RVgenerator
from spectral_synthesizer.data_interfaces import SpectraHolder, SimulationHolder
from SBART.utils.work_packages import Package
from SBART.utils.shift_spectra import apply_RVshift
from spectral_synthesizer import __version__
from multiprocessing import Queue, Process

from spectral_synthesizer.utils.units import kilometer_second


def worker(in_queue: Queue, out_queue: Queue, BaseFrameProxy: FluxModel, RvGen: RVgenerator,
           effects_list: List[FluxModel]) -> NoReturn:
    # We will need this if we use numpy random!
    # re-seeding the RNG (from the OS)
    np.random.RandomState(None)

    while True:
        control_info = in_queue.get()
        if control_info["shutdown"]:
            return

        output_package = Package(extra_keys=("epoch", "order", "Wave", "Flux", "FluxError"))
        frameID = control_info["epoch"]
        order = control_info["order"]

        # WARNING: PERFORMANCE BOTTLENECK if we have a non-static (through time) spectral model

        # TODO <Low-Prio>: Possible solution: for non-static cases:
        #   i) Allow to pass non-AutoProxy objects
        #   ii) Load the "basis" model on each worker
        #   iii) Each worker has to compute the model at the given time
        BaseFrameProxy.generate_BASE_model(0, 0)

        _, rv_value, _ = RvGen.get_information_from_epoch(frameID)
        wavelength, flux, uncerts, mask = BaseFrameProxy.get_model_from_order(epoch=frameID, order=order)

        ###
        # Shift OBS by the stellar RV
        ###

        wavelength = apply_RVshift(wave=wavelength,
                                   stellar_RV=rv_value.to(kilometer_second).value,
                                   )

        ###
        #   Add extra effects in the spectra
        ###
        for effect in effects_list:
            wavelength, flux, uncerts, mask = effect.apply_effect_to_spectra(wavelength,
                                                                             flux,
                                                                             uncerts,
                                                                             mask,
                                                                             RvGenerator=RvGen
                                                                             )
        output_package.update_params({"epoch": frameID,
                                      "order": order,
                                      "Wave": wavelength,
                                      "Flux": flux,
                                      "FluxError": uncerts,
                                      "Mask": mask
                                      }
                                     )
        out_queue.put(output_package)


class SpectralSimulator:
    def __init__(self, BaseSpectralModel, RvGenerator, storage_path: str, SpectralEffects: Optional[list] = None):
        self.BaseSpecModel = BaseSpectralModel

        if not BaseSpectralModel.is_base_generator():
            raise RuntimeError("Trying to create a BASE flux model from a non-BASE object")

        if "AutoProxy" not in str(type(BaseSpectralModel)):
            # SURELY THERE IS A BETTER WAY OF DOING THIS!!
            raise RuntimeError("The BaseModel must be AutoProxy")

        if SpectralEffects is None:
            self.SpectralEffects = []
        else:
            self.SpectralEffects = SpectralEffects

        for index in range(len(self.SpectralEffects)):
            self.SpectralEffects[index].store_application_level(index)

        self._worker_IN_queue: Optional[Queue] = None
        self._worker_OUT_queue: Optional[Queue] = None
        self._worker_pool: Optional[List[Process]] = None

        self.RvGenerator = RvGenerator
        self.storage_path = storage_path
        self._build_folder_structure()
        self._trigger_data_preload()

        list_of_KWs = self.collect_header_KeyWords()
        self._simulation_results = SimulationHolder(N_obs=self.RvGenerator.N_obs,
                                                    list_of_KWs=list_of_KWs,
                                                    storage_folder=self.SimulatedData_folder_path,
                                                    available_orders=self.BaseSpecModel.valid_orders(),
                                                    bad_orders=self.BaseSpecModel.get_BASIS_bad_orders(),
                                                    inst_name=self.BaseSpecModel.get_instrument_name()
                                                    )


    def _trigger_data_preload(self) -> NoReturn:
        """
        Make sure that each component has teh chance of loading data from disk before starting the simulation
        :return:
        """
        for element in [self.BaseSpecModel] + self.SpectralEffects:
            element.load_relevant_info()

    def simulate_observations(self, N_cores: int) -> NoReturn:
        self.write_info_to_disk()
        self._launch_multiproc_interface(N_cores)

        # create observations
        possible_combinations = product(range(self.RvGenerator.N_obs),
                                        self.BaseSpecModel.valid_orders()
                                        )

        sent = 0
        for combination in possible_combinations:
            pkg = Package(("epoch", "order"))
            pkg.update_param("epoch", combination[0])
            pkg.update_param("order", combination[1])
            self._worker_IN_queue.put(pkg)
            sent += 1

        self.receive_data_from_workers(sent)
        self._close_multiproc_interface()

    def collect_header_KeyWords(self) -> List[dict]:
        list_of_kws = []
        for obs_index in range(self.RvGenerator.N_obs):
            keywords = {}
            for element in [self.BaseSpecModel, self.RvGenerator] + self.SpectralEffects:
                elemnt_KW = element.evaluate_fits_KeyWords(obs_index)
                keywords = {**keywords, **elemnt_KW}
            list_of_kws.append(keywords)
        return list_of_kws

    def write_info_to_disk(self) -> NoReturn:
        """
        Trigger all data storage routines from the components used to construct the simulated data
        :return:
        """
        metadata_filepath = os.path.join(self.metadata_folder_path, "MetaData.txt")
        with open(metadata_filepath, mode='w') as to_write:
            to_write.write("Settings of the simulator:")
            to_write.write("\n\tVersion number: {}".format(__version__))
            to_write.write("\n\tSimulation date: {}".format(datetime.datetime.now()))

        self.BaseSpecModel.write_info_to_disk(filename=metadata_filepath, mode='a')
        for effect in self.SpectralEffects:
            effect.write_info_to_disk(filename=metadata_filepath, mode='a', nested_mode=False)
        self.RvGenerator.write_info_to_disk(filename=metadata_filepath, mode='a')

    ###
    #   Handling the folder structure
    ###
    def _build_folder_structure(self) -> NoReturn:
        for path in [self.metadata_folder_path, self.SimulatedData_folder_path]:
            try:
                os.mkdir(path)
            except OSError:
                pass

    @property
    def metadata_folder_path(self) -> str:
        return os.path.join(self.storage_path, "metadata")

    @property
    def SimulatedData_folder_path(self) -> str:
        return os.path.join(self.storage_path, "simulated_data")

    ###
    #   Multiprocessing
    ###

    def __del__(self):
        self._close_multiproc_interface()

    def _launch_multiproc_interface(self, N_cores: int) -> NoReturn:
        if self._worker_OUT_queue is not None:
            return

        self._worker_IN_queue = Queue()
        self._worker_OUT_queue = Queue()
        self._worker_pool = []
        for _ in range(N_cores):
            p = Process(target=worker,
                        args=(self._worker_IN_queue,
                              self._worker_OUT_queue,
                              self.BaseSpecModel,
                              self.RvGenerator,
                              self.SpectralEffects
                              )
                        )
            p.start()
            self._worker_pool.append(p)

    def _close_multiproc_interface(self):

        if self._worker_pool is None:
            return

        for pkg in self._worker_pool:
            if pkg.is_alive():
                pkg.terminate()

        # TODO: don't I have to close the queues?
        self._worker_OUT_queue = None
        self._worker_IN_queue = None

    def receive_data_from_workers(self, number_packages: int) -> NoReturn:
        received = 0

        try:
            while received < number_packages:
                data_out = self._worker_OUT_queue.get()
                self._simulation_results.store_data_from(spec_index=data_out["epoch"],
                                                         order=data_out["order"],
                                                         wavelength=data_out["Wave"],
                                                         fluxes=data_out["Flux"],
                                                         uncerts=data_out["FluxError"],
                                                         mask=data_out["Mask"]
                                                         )
                received += 1
        except Exception as e:
            print(traceback.print_tb(e.__traceback__))
