import numpy as np
from scipy.signal import savgol_filter

from ..core.data import DNPData
from ..processing.integration import integrate

import dnplab as dnp


def calculate_enhancement(integrals, off_spectrum_index=0, return_complex_values=False):
    """Calculate enhancement of a power series. Needs integrals as input



    #     +------------------+----------------------------+-------------+----------------------------------------------------------------------+
    #     | parameter        | type                       | default     | description                                                          |
    #     +==================+============================+=============+======================================================================+
    #     | off_spectrum     | int or dnpdata             | 1           | slice of 2D data to be used as p = 0 spectrum, or dnpdata            |
    #     +------------------+----------------------------+-------------+----------------------------------------------------------------------+
    #     | on_spectra       | str or dnpdata             | "all"       | "all"  unless dnpdata given                                          |
    #     +------------------+----------------------------+-------------+----------------------------------------------------------------------+
    #     | integrate_center | str, int, list, or ndarray | 0           | "max", center of integration window, or index used to find amplitude |
    #     +------------------+----------------------------+-------------+----------------------------------------------------------------------+
    #     | integrate_width  | str, int, list, or ndarray | "full"      | "full" or width of integration window                                |
    #     +------------------+----------------------------+-------------+----------------------------------------------------------------------+
    #     | method           | str                        | "integrate" | either "integrate" or "ampltiude"                                    |
    #     +------------------+----------------------------+-------------+----------------------------------------------------------------------+
    #     | dim              | str                        | "f2"        | dimension to integrate down or search down for max                   |
    #     +------------------+----------------------------+-------------+----------------------------------------------------------------------+


        Args:
        Returns:

    """

    enhancements = integrals.copy()

    if not "experiment_type" in integrals.attrs.keys():

        raise KeyError("Experiment type not defined")

    if integrals.attrs["experiment_type"] != "integrals":

        raise ValueError("dnpdata object does not contain integrals.")

    if integrals.dims[0] == "Power":

        enhancements.attrs["experiment_type"] = "enhancements_P"

        enhancements.values = (
            enhancements.values / enhancements.values[off_spectrum_index]
        )

    elif integrals.dim[0] == "B0":

        enhancements.attrs["experiment_type"] = "enhancements_B0"
        print("This is a DNP enhancement profile. Not implemented yet.")

    else:

        raise TypeError(
            "Integration axis not recognized. First dimension should be Power or B0."
        )

    if return_complex_values == True:
        return enhancements

    elif return_complex_values == False:
        return enhancements.real


def signal_to_noise():
    """Find signal-to-noise ratio

    Returns:
        NotImplemented
    """

    return NotImplemented


def smooth(data, dim="t2", window_length=11, polyorder=3):
    """Apply Savitzky Golay Smoothing

    Args:
        data (DNPData): Data object
        dim (str): Dimension to perform smoothing
        window_length (int): Length of window (number of coefficients)
        polyorder (int): Polynomial order to fit samples

    Returns:
        DNPData: Data with Savitzky Golay smoothing applied
    """
    out = data.copy()

    out.unfold(dim)

    out.values = savgol_filter(out.values, window_length, polyorder, axis=0)

    out.fold()

    return out


def left_shift(data, dim="t2", shift_points=0):
    """Remove points from the left of data

    Args:
        data (dnpdata): Data container for data

    +---------------+------+---------+--------------------------------------------------+
    | parameter     | type | default | description                                      |
    +===============+======+=========+==================================================+
    | dim           | str  | "t2"    | dimension to shift                               |
    +---------------+------+---------+--------------------------------------------------+
    | shift_points  | int  | 0       | Number of points to remove from left of data     |
    +---------------+------+---------+--------------------------------------------------+

    Returns:
        dnpdata: data object with left-shifted data
    """

    data = data[dim, shift_points:]

    proc_attr_name = "left_shift"
    proc_parameters = {
        "dim": dim,
        "points": shift_points,
    }
    data.add_proc_attrs(proc_attr_name, proc_parameters)

    return data


def normalize():
    return NotImplemented


def reference(data, dim="f2", old_ref=0, new_ref=0):
    """Function for referencing NMR spectra

    Args:
        data (DNPData): Data for referencing
        dim (str): dimension to perform referencing down. By default this dimension is "f2".
        old_ref (float): Value of old reference
        new_ref (float): New reference value

    Returns:
        DNPData: referenced data
    """

    data = data.copy()

    data.coords[dim] -= old_ref - new_ref

    return data
