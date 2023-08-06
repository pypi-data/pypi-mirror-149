import numpy as np
SPEED_OF_LIGHT = 299792.458


def apply_RVshift(wave: np.ndarray, stellar_RV: float) -> np.ndarray:
    """

    Parameters
    ----------
    wave : np.ndarray
        [description]
    stellar_RV : float
        [description]
    BERV : float, optional
        [description], by default 0

    Returns
    -------
    np.ndarray
        [description]
    """
    return np.multiply(wave, (1 + stellar_RV / SPEED_OF_LIGHT))