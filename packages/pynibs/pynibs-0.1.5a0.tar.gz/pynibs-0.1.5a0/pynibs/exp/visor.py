""" Functions to import data from ANT Visor 2 / ANT EEG software go here """
import warnings

import os
import h5py
import numpy as np
from pynibs import write_arr_to_hdf5
from pynibs.util.util import quat_to_rot
from scipy.spatial.transform import Rotation as R
from scipy import signal
import pandas as pd

try:
    from pynibs.pckg import libeep
except (ImportError, SyntaxError):
    pass
    # print("lipbeep not found. visor import will not work.")


def read_nlr(fname):
    """
    Reads NLR coordinates from *_recording.mri file

    Parameters
    ----------
    fname

    Returns
    -------
    fiducials : np.array of float [3 x 3]
        The rows contain the fiducial points in ANT nifit space (nasion, left ear, right ear)
    """
    f = open(fname, "r")
    text = f.readlines()

    fiducials = np.empty((3, 3))

    for i, line in enumerate(text):
        # nasion
        if "VoxelOnPositiveXAxis" in line:
            line = text[i + 1].replace("\t", " ")
            line = line.replace("\n", "")
            fiducials[0, :] = np.array([int(t) for t in line.split(" ")])

        # left ear
        if "VoxelOnNegativeYAxis" in line:
            line = text[i + 1].replace("\t", " ")
            line = line.replace("\n", "")
            fiducials[1, :] = np.array([int(t) for t in line.split(" ")])

        # right ear
        if "VoxelOnPositiveYAxis" in line:
            line = text[i + 1].replace("\t", " ")
            line = line.replace("\n", "")
            fiducials[2, :] = np.array([int(t) for t in line.split(" ")])

    return fiducials


def get_instrument_marker(im_path, verbose=False):
    """
    Return all instrument markers from visor .cnt file
    Coordinate system in raw ANT space (NLR) defined as:

    origin: intersection between line of ear fiducials and nasion
    x-axis: origin -> nasion
    y-axis: origin -> left ear
    z-axis: origin -> superior

    Parameters
    ----------
    im_path : str
        Path to instrument-marker-file .cnt file
    verbose: bool
        Some verbosity messages (default: False)

    Returns
    -------
    im_list : list of dict
        List containing stimulation parameters:
        - coil_mean_raw [4 x 4 matrix]
        - StimulusID
        - etc...

    """
    f = libeep.read_cnt(im_path)
    n_trig = f.get_trigger_count()
    # some triggers (2?) are some other information
    # so only take the ones with 'StimulusID' at 3rd position
    ims = [f.get_trigger(i)[3] for i in range(n_trig) if "StimulusID" in f.get_trigger(i)[3]]
    # or: if f.get_trigger(i)[0] == '6'

    if verbose:
        print(f"Found {len(ims)} instrument markers.")
    assert len(ims), "No instrument markers found in file"

    # now build list of matsimnibs from the instrument markers
    data = []

    for i, im in enumerate(ims):

        # transform string from .cnt file to dictionary
        data.append(dict(item.split('=') for item in im.split()[1:] if '=' in item))

        # floatify numeric variables
        for key in data[-1].keys():
            try:
                if key == "StimulusID":
                    data[-1][key] = int(data[-1][key])
                else:
                    data[-1][key] = float(data[-1][key])
            except ValueError:
                pass

        # transform to SimNIBS raw format
        matsimnibs_raw = np.zeros((4, 4))
        matsimnibs_raw[3, 3] = 1
        matsimnibs_raw[0:3, 3] = np.array([data[-1]['PosX'], data[-1]['PosY'], data[-1]['PosZ']]) * 1000
        quat = np.array([data[-1]['QuatX'], data[-1]['QuatY'], data[-1]['QuatZ'], data[-1]['QuatW']])
        matsimnibs_raw[0:3, 0:3] = R.from_quat(quat).as_dcm()
        data[-1]["coil_mean_raw"] = matsimnibs_raw

    return data


def get_cnt_data(fn, channels='all', trigger_val='1', max_duration=10,
                 fn_hdf5=None, path_hdf5=None, verbose=False, return_data=False):
    """
    Reads ANT .cnt EMG/EEG data file and chunks timesieries into triggerN - trigggerN+1
    Can directly write the zaps into hdf5 if argument is provided.
    Starting with the first trigger and ending with get_sample_count()-1

    Parameters
    ----------
    fn: str
        .cnt Filename
    channels: str | int | list of int | list of str
        Which channel(s) to return. Default: all.
        Can be channel number(s) or channel name(s).
    trigger_val: str
        Trigger value to read as zap trigger. Default: '1'
    max_duration : int
        Maximum duration in [s] per chunk. Rest is dropped.
    fn_hdf5: str, optional, default: None
        If given, cnt data is written into hdf5 file under "path_hdf5" as pandas dataframe with column name "qoi_name"
        and nothing is returned. Default: None
    path_hdf5: str, optional, default: None
        If fn_hdf5, path of pandas dataframe where the data is saved (e.g. "/phys_data/raw/EEG")
    verbose: bool
        Some verbosity messages (default: False)
    return_data: bool
        Return data as list of np.array

    Returns
    -------
    data_lst: list of np.ndarray with shape=(samples,channels), optional
        List of EEG/EMG data. Only returned if fn_hdf5 is not None
    """

    f = libeep.read_cnt(fn)
    n_trig = f.get_trigger_count()
    n_samples = f.get_sample_count()
    n_channels = f.get_channel_count()
    sf = f.get_sample_frequency()
    chan_names = [f.get_channel(i)[0].lower() for i in range(n_channels)]

    if channels == 'all' or isinstance(channels, list) and channels[0] == 'all':
        channels_idx = range(n_channels)
    elif isinstance(channels, int):
        channels_idx = [channels]
    elif isinstance(channels, str):
        channels_idx = chan_names.index(channels.lower())
    elif type(channels) == list and all(type(chan) == int for chan in channels):
        channels_idx = channels
        assert np.all(np.array(channels_idx) >= 0), "Only positive channels numbers allowd"
        assert np.max(np.array(channels_idx)) < n_channels, f"Only {n_channels} channels found."

    elif type(channels) == list and all(type(chan) == str for chan in channels):
        channels_idx = [chan_names.index(chan.lower()) for chan in channels]

    else:
        raise NotImplementedError("Channels must be 'all', list(int), list(str)")

    assert channels_idx, "No channels with name / idx found."

    if fn_hdf5 is not None:
        assert path_hdf5, "Please provide path_hdf5="

    if verbose:
        print(f"get_cnt_data: {n_trig} triggers found.")
        print(f"get_cnt_data: {n_samples} samples found.")
        print(f"get_cnt_data: {sf} Hz sampling frequency.")
        print(f"get_cnt_data: {n_channels} channels found.")

    # get data between samples
    data_lst = []

    # chunk into triggers
    trigger_idx = 0
    arr_idx = 0
    last_zap_done = False
    trigger_zap = 0
    # we want the data between trigger and trigger+1
    while trigger_idx < n_trig - 1:

        try:
            start = f.get_trigger(trigger_idx)

            # only use the triggers that have the correct trifger value
            if start[0] != trigger_val:
                if verbose:
                    print(f"get_cnt_data: Skipping idx {trigger_idx}: {start} (start)")
                trigger_idx += 1
                continue
            end = f.get_trigger(trigger_idx + 1)
            # also trigger+1 needs to have the correct trigger_val
            while end[0] != trigger_val:
                if verbose:
                    print(f"Skipping idx {trigger_idx}: {start} (end)")
                trigger_idx += 1
                if trigger_idx >= n_trig - 1:
                    break
                end = f.get_trigger(trigger_idx)

            # some sanity checks
            if not start[1] < end[1]:
                if verbose:
                    print(f"Trigger {trigger_idx} and {trigger_idx + 1}: wrong sample number "
                              f"({trigger_idx}: {start[1]}, {trigger_idx + 1}: {end[1]}]")
                # the eeg cnt files and with a trigger. get data from trigger to end-offile
                if trigger_idx == n_trig - 1:
                    end = (end[0], f.get_sample_count())
                    last_zap_done = True

            assert start[1] < (end[1] - 1), \
                f"Trigger {trigger_idx} and {trigger_idx + 1}: too close together " \
                f"({trigger_idx}: {start[1]}, {trigger_idx + 1}: {end[1]}]"

            # get sample number from trigger-tuple
            start = start[1]
            end = end[1] - 1
            length_org = end - start

            # cut to max duration chunk length
            end = np.min((end, start + sf * max_duration))

            if verbose:
                print(f"get_cnt_data: Trigger {trigger_idx:0>3}: {float(length_org) / sf:2.2}s / "
                      f"{float(end - start) / sf:0.2}s")
            data = f.get_samples(start, end)
            data_res = np.reshape(data, (end - start, n_channels), order='F')

            if return_data:
                data_lst.append(data_res)

        except (SystemError, UnicodeDecodeError) as e:
            print(f"Trigger {trigger_idx} error")
            print(e)
            continue

        if fn_hdf5 is not None:
            with h5py.File(fn_hdf5, "a") as fi:
                fi[path_hdf5 + f"/{trigger_zap:04d}"] = data_res
                trigger_zap += 1

        trigger_idx += 1

    # grap data for the last zap (trigger to end_of_file
    if not last_zap_done:

        try:
            start = f.get_trigger(trigger_idx)

            # only use the triggers that have the correct trigger value
            if start[0] != trigger_val:
                if verbose:
                    print(f"get_cnt_data: Skipping idx {trigger_idx}: {start} (start)")
                trigger_idx += 1
            end = f.get_sample_count()

            assert start[1] < (end - 1), \
                f"Trigger {trigger_idx} and {trigger_idx + 1}: too close together " \
                f"({trigger_idx}: {start[1]}, {trigger_idx + 1}: {end}]"

            # get sample number from trigger-tuple
            start = start[1]
            length_org = end - start

            # cut to max duration chunk length
            end = np.min((end, start + sf * max_duration))

            if verbose:
                print(f"get_cnt_data: Trigger {trigger_idx:0>3}: {float(length_org) / sf:2.2}s / "
                      f"{float(end - start) / sf:0.2}s")
            data = f.get_samples(start, end)
            data_res = np.reshape(data, (end - start, n_channels), order='F')

            if return_data:
                data_lst.append(data_res)

            if fn_hdf5 is not None:
                with h5py.File(fn_hdf5, "a") as fi:
                    fi[path_hdf5 + f"/{trigger_zap:04d}"] = data_res
                    trigger_zap += 1

            trigger_idx += 1

        except (SystemError, UnicodeDecodeError) as e:
            print(f"Trigger {trigger_idx} error")
            print(e)

        # reshape according to channel count
        # [chan1, chan2, chan3, chan1, chan2, chan3]
        # data_res = np.reshape(data, (end - start, n_channels), order='F')
        #
        # if return_data:
        #     data_lst.append(data_res[:, channels_idx])
        #
        # if fn_hdf5 is not None:
        #     with h5py.File(fn_hdf5, "a") as fi:
        #         fi[path_hdf5 + f"/{trigger_idx:04d}"] = data_res[:, channels_idx]

    # append last chunk
    # start = f.get_trigger(n_trig - 2)[1]
    # end = n_samples - 1
    # end = np.min((end, start + sf * max_duration))  # cut to max chunk length
    #
    # data = f.get_samples(start, end)
    # data_res = np.reshape(data, (end - start, n_channels), order='F')
    # if fn_hdf5:
    #     write_arr_to_hdf5(fn_hdf5=fn_hdf5,
    #                       arr_name=arr_name.format(arr_idx),
    #                       data=data_res[:, channels_idx],
    #                       verbose=verbose)
    # else:

    if return_data:
        return data_lst


def filter_emg(emg, fs):
    """
    Filter emg signals

    Parameters
    ----------
    emg : list of np.array [n_stimuli]
        Raw EMG data. Each list entry contains a np.array of size [n_samples x n_channel]
        Each channel is filtered in the same way.
    fs : float
        Sampling frequency

    Returns
    -------
    emg_filt : list of np.array [n_stimuli]
        Filtered EMG data
    """

    # 5 Hz Butterworth high pass
    ############################
    b_butterhigh, a_butterhigh = signal.butter(N=5, Wn=5, btype='high', analog=False, fs=fs)
    # plot_frequency_response(a_butterhigh, b_butterhigh, fs=fs)

    # 200 Hz Butterworth low pass
    ############################
    b_butterlow, a_butterlow = signal.butter(N=5, Wn=200, btype='low', analog=False, fs=fs)
    # plot_frequency_response(a_butterlow, b_butterlow, fs=fs)

    # 50 Hz Notch filter
    ############################
    b_notch50, a_notch50 = signal.iirnotch(w0=50 / (fs / 2), Q=30)
    # plot_frequency_response(a_notch50, b_notch50, fs=fs)

    # 100 Hz Notch filter
    ############################
    b_notch100, a_notch100 = signal.iirnotch(w0=100 / (fs / 2), Q=50)
    # plot_frequency_response(a_notch100, b_notch100, fs=fs)

    # 150 Hz Notch filter
    ############################
    b_notch150, a_notch150 = signal.iirnotch(w0=150 / (fs / 2), Q=30)
    # plot_frequency_response(a_notch150, b_notch150, fs=fs)

    # 200 Hz Notch filter
    ############################
    b_notch200, a_notch200 = signal.iirnotch(w0=200 / (fs / 2), Q=30)
    # plot_frequency_response(a_notch200, b_notch200, fs=fs)

    # Filter signals
    emg_filt = []

    for e in emg:
        emg_filt.append(np.zeros(e.shape))
        for i_channel in range(e.shape[1]):
            emg_filt[-1][:, i_channel] = signal.filtfilt(b_notch50, a_notch50, e[:, i_channel])
            emg_filt[-1][:, i_channel] = signal.filtfilt(b_notch100, a_notch100, emg_filt[-1][:, i_channel])
            emg_filt[-1][:, i_channel] = signal.filtfilt(b_notch150, a_notch150, emg_filt[-1][:, i_channel])
            emg_filt[-1][:, i_channel] = signal.filtfilt(b_notch200, a_notch200, emg_filt[-1][:, i_channel])
            emg_filt[-1][:, i_channel] = signal.filtfilt(b_butterlow, a_butterlow, emg_filt[-1][:, i_channel])
            emg_filt[-1][:, i_channel] = signal.filtfilt(b_butterhigh, a_butterhigh, emg_filt[-1][:, i_channel])
            emg_filt[-1][:, i_channel] = signal.filtfilt(b_notch50, a_notch50, emg_filt[-1][:, i_channel])

    return emg_filt
