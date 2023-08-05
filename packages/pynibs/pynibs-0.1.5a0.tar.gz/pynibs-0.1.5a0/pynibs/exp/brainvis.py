import numpy as np
import re


def read_channel_names(fname):
    """
    Reads the channel names from .vhdr (info) file, which is recorded during EEG

    Parameters
    ----------
    fname : str
        Filename of .vhdr info file

    Returns
    -------
    channel_names : list of str
        List containing the channel names
    """

    f = open(fname, "r")
    eof = False
    i_line = 0
    channel_info_start = np.inf
    channel_names = []

    while not eof:
        l = f.readline()

        if l == "[Channel Infos]\n":
            channel_info_start = 5 + i_line

        if i_line >= channel_info_start:

            if l == "\n":
                break

            channel_names.append(re.search("(?<=\=)(.*?)(?=\,)", l).group(0))

        i_line += 1

    return channel_names


def read_sampling_frequency(fname):
    """
    Reads the sampling frequency from .vhdr (info) file, which is recorded during EEG

    Parameters
    ----------
    fname : str
        Filename of .vhdr info file

    Returns
    -------
    Sampling_frequency : float
        Sampling frequency
    """

    f = open(fname, "r")
    eof = False

    while not eof:
        l = f.readline()

        if "Sampling Rate [Hz]: " in l:
            start_idx = l.find(":") + 2
            sampling_frequency = float(l[start_idx:])
            break

    return sampling_frequency
