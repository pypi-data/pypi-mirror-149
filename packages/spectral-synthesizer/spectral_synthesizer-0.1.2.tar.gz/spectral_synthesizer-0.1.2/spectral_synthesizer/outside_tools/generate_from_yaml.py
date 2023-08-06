import pathlib
import pathlib

import numpy as np
import yaml

from spectral_synthesizer import SpectralSimulator
from spectral_synthesizer.RV_generation import ConstantRV, RandomRV, KeplerianRV
from spectral_synthesizer.Sampling_Times import TimeWindow, CustomWindow
from spectral_synthesizer.spectra_generation import DataClassManager as synthesis_DC_manager
from spectral_synthesizer.spectral_effects import RandomNoise
from spectral_synthesizer.utils import units

curr_file = pathlib.Path(__file__).absolute().parent


def prepare_test_suite(yaml_filepath, main_output_folder, SBART_INSTRUMENT_map, only_generate_missing):
    if isinstance(main_output_folder, str):
        main_output_folder = pathlib.Path(main_output_folder)

    with open(yaml_filepath) as stream:
        config_file = yaml.safe_load(stream)

    for instrument in config_file["General_configs"]["Instruments"]:
        for suite_name, suite_configs in config_file.items():
            if "General_configs" in suite_name:
                continue

            output_path = main_output_folder / f"{instrument}/{suite_name}"
            if only_generate_missing and output_path.exists():
                print("no need to continue, file already exists")
                continue

            if (
                    instrument not in suite_configs["Apply_to"]
                    and "All" not in suite_configs["Apply_to"]
            ):
                print("Instrument not in Apply to")
                continue

            launch_simulation(general_config=config_file["General_configs"],
                              instrument=SBART_INSTRUMENT_map[instrument],
                              instrument_name=instrument,
                              storage_path=output_path,
                              suite_configs=suite_configs
                              )

    generate_input_text_files(main_output_folder)


def launch_simulation(general_config, instrument, instrument_name, storage_path, suite_configs):
    manager = synthesis_DC_manager()
    manager.start()

    if suite_configs["Time_genesis"]["type"].lower() == "steps":
        sampling = TimeWindow(
            suite_configs["Time_genesis"]["Start"],
            suite_configs["Time_genesis"]["End"],
            suite_configs["Time_genesis"]["Step"],
        )
    elif suite_configs["Time_genesis"]["type"].lower() == "custom_locations":
        input_times = np.loadtxt(suite_configs["Time_genesis"]["file_to_load"])
        sampling = CustomWindow(time_array=input_times)

    if suite_configs["RV_genesis"]["distribution"].lower() == "const":
        RVs = ConstantRV(
            const_value=suite_configs["RV_genesis"]["RV_value"] * units.meter_second,
            TimeGenerator=sampling,
        )

    elif suite_configs["RV_genesis"]["distribution"].lower() == "random":
        limits = (
            suite_configs["RV_genesis"]["RV_limits"][0] * units.meter_second,
            suite_configs["RV_genesis"]["RV_limits"][1] * units.meter_second,
        )
        RVs = RandomRV(
            distribution=suite_configs["RV_genesis"]["distribution"].lower(),
            RV_limits=limits,
            TimeGenerator=sampling,
        )
    elif suite_configs["RV_genesis"]["distribution"].lower() == "keplerian":

        RVs = KeplerianRV(planet_information=suite_configs["RV_genesis"]["planets"],
                          TimeGenerator=sampling)


    if suite_configs["Flux_genesis"]["Basis"].lower() == "observation":
        base_frame = instrument(file_path=suite_configs["Flux_genesis"]["Basis_filename"][instrument_name])

        BaseSpectralModel = manager.OBSERVATION_MODEL(base_frame)

    else:
        raise NotImplementedError

    effect_list = []
    effect_map = {"RandomNoise": RandomNoise}
    print(suite_configs["Flux_genesis"]["Effects"])
    for effect, effect_config in suite_configs["Flux_genesis"]["Effects"].items():
        # TODO: pass the configs to the effect generator
        if effect == "None":
            continue
        effect_list.append(effect_map[effect]())

    output_path = storage_path
    output_path.mkdir(parents=True, exist_ok=True)

    simulator = SpectralSimulator(
        BaseSpectralModel=BaseSpectralModel,
        RvGenerator=RVs,
        SpectralEffects=effect_list,
        storage_path=output_path.as_posix(),
    )

    simulator.simulate_observations(N_cores=general_config["N_cores"])


def generate_input_text_files(main_output_folder):
    for instrument in main_output_folder.iterdir():
        for suite in instrument.iterdir():
            with open((suite / "input_filelist.txt").as_posix(), mode="w") as to_write:
                for OBS_index in range(len(list((suite / "simulated_data").iterdir()))):
                    to_write.write(
                        (suite / f"simulated_data/simulation_{OBS_index}.fits").as_posix() + "\n"
                    )


if __name__ == "__main__":
    prepare_test_suite()
