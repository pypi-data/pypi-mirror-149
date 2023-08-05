from typing import List, NoReturn


class SimulationObject:
    _name = "BaseClass::None"

    def __init__(self):
        pass

    def evaluate_fits_KeyWords(self, OBS_index: int) -> dict:
        return {}

    def write_info_to_disk(self, filename, mode: str = 'a', nested_mode=False) -> NoReturn:
        header = self._header() + " settings:"
        with open(filename, mode=mode) as to_write:
            if not nested_mode: # horizontal "line" for division
                to_write.write("\n\n" + "="*len(header)*2)

            extra_indents = '' if not nested_mode else '\t'
            to_write.write("\n\n{}{}\n".format(extra_indents, header))
            to_write.write(f"\n\t{extra_indents}" + self.model_information[0])
            to_write.write(f"\n\t\t{extra_indents}" + f"\n\t\t{extra_indents}".join(self.model_information[1:]))

    def load_relevant_info(self) -> NoReturn:
        pass

    def _header(self) -> str:
        """
        Will be used as the header for the "Section" inside the simulations_output.txt file
        :return:
        """
        return "Base Model creation"

    @property
    def model_information(self) -> List[str]:
        info_out = ["Simulator: {}".format(self._name)]
        return info_out

    @property
    def name(self):
        return self.__class__._name

