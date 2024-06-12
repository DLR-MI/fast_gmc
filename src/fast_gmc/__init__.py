import numpy as np
from .build.gmc_pybind import GMC


def gmc(curr_frame: np.ndarray, prev_frame: np.ndarray, downscale: int, model="affine"):
    """Performs global camera motion compensation using OpenCVs video stabilization classes.

    Parameters
    ----------
    curr_frame : np.ndarray
        Current frame as numpy array of shape [H, W, 3].
    prev_frame : np.ndarray
        Previous frame as numpy array of shape [H, W, 3].
    downscale : int
        Downscaling factor by which the frames are reduced (1.0 / downscale).
    model : str
        Model to choose for estimation. Can be either "affine" or "homography". Defaults to "affine".

    Returns
    -------
    transform : np.ndarray
        Transformation matrix as numpy array of shape [3, 3].
    """
    return GMC(curr_frame, prev_frame, downscale, model)
