from typing import Any, List, Tuple, Union

import numpy as np
from astropy.units import Quantity

RV_measurement = Quantity

data_vector = Union[List[Quantity], Tuple[Quantity]]

unitless_data_vector = Union[List[float], np.ndarray]

unitless_data_matrix = np.ndarray
