from typing import Iterable, NoReturn


class Package:
    __slots__ = ("params", "_locked_params", "extra_keys")

    def __init__(self, extra_keys=None, data_only_pkg=False):
        if data_only_pkg:
            self.params = {}
        else:
            self.params = {"shutdown": False}

        self._locked_params = []
        if extra_keys is None:
            self.extra_keys = []
        else:
            self.extra_keys = list(extra_keys)

    def items(self):
        return self.params.items()

    def to_list(self):
        return list(self.params.values())

    def lock_parameter(self, param):
        self._locked_params.append(param)

    def lock_parameters(self, parameters):
        for param in parameters:
            self.lock_parameter(param)

    def update_params(self, update_dict):
        for key, val in update_dict.items():
            self.update_param(key, val)

    def update_param(self, key, value):
        self.params[key] = value

    def __getitem__(self, key):
        return self.params[key]

    def __setitem__(self, key, val):
        if key in self._locked_params:
            raise Exception("Trying to change a locked entry")

        if key not in self.params and key not in self.extra_keys:
            self.extra_keys.append(key)
        self.params[key] = val

    def ingest_data(self, other):
        """Copy the data from the extra keys of the 'other' Package  to this one

        Parameters
        ----------
        other : Package
            Package with the data that will be copied over
        """
        for key in other.extra_keys:
            if key in self.params:
                Warning(
                    "Trying to override key {} during package ingestion. The two packages share the same extra key, skipping over this key".format(
                        key
                    )
                )
                continue
            # print(self.params)
            # print(other.params)
            self.params[key] = other[key]
            self.extra_keys.append(key)

    def delete_keys(self, keys_to_delete: Iterable[str]) -> NoReturn:
        for key in keys_to_delete:
            del self.params[key]
