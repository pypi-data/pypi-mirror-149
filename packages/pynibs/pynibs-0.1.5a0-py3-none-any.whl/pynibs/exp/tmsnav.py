""" Functions to import data from Localite TMS Navigator """

from xml.etree import ElementTree as xmlt
import numpy as np


def get_tms_elements(xml_paths, verbose=False):
    """
    Read needed elements out of the tms-xml-file.

    Parameters
    ----------
    xml_paths : list of str or str
        Paths to coil0-file and optionally coil1-file if there is no coil1-file, use empty string
    verbose : bool, optional, default: False
        Print output messages

    Returns
    -------
    coils_array : nparray of float [3xNx4x4]
        Coil0, coil1 and mean-value of N 4x4 coil-arrays
    ts_tms_lst : list of int [N]
        Timestamps of valid tms-measurements
    current_lst : list of int [N]
        Measured currents
    idx_invalid : list of int
        List of indices of invalid coil positions (w.r.t. all timestamps incl invalid)
    """
    if isinstance(xml_paths, str):
        xml_paths = [xml_paths]
    # handle case if there is no coil1
    if len(xml_paths) > 1 and not xml_paths[1]:
        xml_paths[1] = xml_paths[0]
    if len(xml_paths) == 1:
        xml_paths.append(xml_paths[0])

    # allocate new array and lists
    coils_array, ts_tms_lst, current_lst = np.empty([3, 0, 4, 4]), [], []

    # parse XML document
    coil0_tree, coil1_tree = xmlt.parse(xml_paths[0]), xmlt.parse(xml_paths[1])
    coil0_root, coil1_root = coil0_tree.getroot(), coil1_tree.getroot()

    # iterate over all 'TriggerMarker' tags
    i_stim = 0
    idx_invalid = []

    for coil0_tm, coil1_tm in zip(coil0_root.iter('TriggerMarker'), coil1_root.iter('TriggerMarker')):
        coil_array = np.empty([0, 1, 4, 4])

        # get tag were the matrix is
        coil0_ma, coil1_ma = coil0_tm.find('Matrix4D'), coil1_tm.find('Matrix4D')

        # get coil0
        coil_array = np.append(coil_array, read_coil(coil0_ma), axis=0)

        # if present, get coil1
        if xml_paths[0] == xml_paths[1]:
            coil_array = np.append(coil_array, np.identity(4)[np.newaxis, np.newaxis, :, :], axis=0)
        else:
            coil_array = np.append(coil_array, read_coil(coil1_ma), axis=0)

        # check for not valid coils and calculate mean value
        if not np.allclose(coil_array[0, 0, :, :], np.identity(4)) and \
                not np.allclose(coil_array[1, 0, :, :], np.identity(4)):
            coil_array = np.append(coil_array,
                                   np.expand_dims((coil_array[0, :, :, :] + coil_array[1, :, :, :]) / 2, axis=0),
                                   axis=0)
        elif np.allclose(coil_array[0, 0, :, :], np.identity(4)) and not np.allclose(coil_array[1, 0, :, :],
                                                                                     np.identity(4)):
            coil_array = np.append(coil_array, np.expand_dims(coil_array[1, :, :, :], axis=0), axis=0)
        elif np.allclose(coil_array[1, 0, :, :], np.identity(4)) and not np.allclose(coil_array[0, 0, :, :],
                                                                                     np.identity(4)):
            coil_array = np.append(coil_array, np.expand_dims(coil_array[0, :, :, :], axis=0), axis=0)
        else:
            idx_invalid.append(i_stim)
            if verbose:
                print("Removing untracked (and possibly accidental) coil position #{} (identity matrix)".format(i_stim))
            i_stim += 1
            continue

        # print(i_stim)
        i_stim += 1

        coils_array = np.append(coils_array, coil_array, axis=1)

        # get timestamp
        ts_tms_lst.append(int(coil0_tm.get('recordingTime')))

        # get current
        xml_rv = coil0_tm.find('ResponseValues')
        xml_va = xml_rv.findall('Value')

        # if valueA is NaN, compute dI/dt with amplitudeA
        if xml_va[0].get('response') == 'NaN':
            current_lst.append(str(round(float(xml_va[2].get('response')) * 1.4461)))  # was 1.38
        else:
            current_lst.append(xml_va[0].get('response'))

    return [coils_array, ts_tms_lst, current_lst, idx_invalid]


def read_coil(xml_ma):
    """
    Read coil-data from xml element.

    Parameters
    ----------
    xml_ma : xml-element
        Coil data

    Returns
    -------
    coil : nparray of float [4x4]
        Coil elements
    """
    # index2 for all coils from triggermarker
    coil = np.empty([1, 1, 4, 4])
    for coil_index1 in range(4):
        for coil_index2 in range(4):
            coil[0, 0, coil_index1, coil_index2] = (float(xml_ma.get('data' + str(coil_index1) + str(coil_index2))))
    return coil


def match_instrument_marker_file(xml_paths, im_path):
    """ Assign right instrument marker condition to every triggermarker (get instrument marker out of file).

    Parameters
    ----------
    xml_paths : list of str
        Paths to coil0-file and optionally coil1-file if there is no coil1-file, use empty string
    im_path : str
        Path to instrument-marker-file

    Returns
    -------
    coil_cond_lst : list of str
        Right conditions
    """

    tm_array, tms_time_arr, tms_cur_arr, tms_idx_invalid = get_tms_elements(xml_paths)
    # get coil mean value
    tm_array = tm_array[2]
    im_array, im_cond_lst = get_instrument_marker(im_path)

    # get indices of conditions
    im_index_lst, drop_idx = match_tm_to_im(tm_array, im_array, tms_time_arr, tms_cur_arr)

    # list to save conditions
    coil_cond_lst = []

    for cond_index in im_index_lst:
        coil_cond_lst.append(im_cond_lst[cond_index])
    return coil_cond_lst, drop_idx


def match_instrument_marker_string(xml_paths, condition_order):
    """
    Assign right instrument marker condition to every triggermarker (get instrument marker out of list of strings).

    Parameters
    ----------
    xml_paths : list of str
        Paths to coil0-file and optionally coil1-file if there is no coil1-file, use empty string
    condition_order : list of str
        Conditions in the right order

    Returns
    -------
    coil_cond_lst : list of strings containing the right conditions
    """
    drop_idx = []
    max_time_dif = 90000
    max_mep_dif = 7

    tm_pos_arr, tms_time_arr, tms_cur_arr, tms_idx_invalid = get_tms_elements(xml_paths)

    # get coil mean value
    tm_pos_arr = tm_pos_arr[2, :, :, :]

    # list for condition results
    conditions = []

    # index of instrument marker
    cond_idx = 0

    # iterate over all trigger marker
    for tm_index in range((tm_pos_arr.shape[0]) - 1):
        conditions.append(condition_order[cond_idx])
        if float(tms_cur_arr[tm_index]) == 0.:
            drop_idx.append(tm_index)
        tm_matrix_post = tm_pos_arr[tm_index + 1, :, :]
        tm_matrix = tm_pos_arr[tm_index, :, :]

        same_tm = arrays_similar(tm_matrix, tm_matrix_post)
        time_dif = tms_time_arr[tm_index + 1] - tms_time_arr[tm_index] > max_time_dif
        amp_dif = np.abs(float(tms_cur_arr[tm_index + 1]) - float(tms_cur_arr[tm_index])) > max_mep_dif
        if not same_tm and time_dif and amp_dif:
            arrays_similar(tm_matrix, tm_matrix_post)
            cond_idx += 1
            if cond_idx == len(condition_order):
                raise ValueError("Too many coil conditions found!")

    # assign last element to very last element
    conditions.append(conditions[-1])
    if cond_idx != len(condition_order) - 1:
        raise ValueError("Did not find all coil positions!")

    return conditions, drop_idx


def arrays_similar(tm_matrix, tm_matrix_post,  # , tm_mean_last,
                   pos_rtol=0, pos_atol=3.6, ang_rtol=.1, ang_atol=.1):
    """
    Compares angles and position for similarity.

    Splitting the comparison into angles and position is angebracht, as the absolute tolereance (atol) should be
    different for angles (degree) and position (millimeter) comparisons.

    Parameters:
    -----------
    tm_matrix: array-like, shape = (4,4)
        TMS Navigator triggermarker or instrument marker array

    tm_matrix_post: array-like, shape = (4,4)
        TMS Navigator triggermarker or instrument marker array

    tm_mean_last: array-like, shape = (4,4), optional
        Mean TMS Navigator triggermarker or instrument marker array for n zaps

    """
    last_pos = True
    last_ang = True
    # position
    pos = np.allclose(tm_matrix[0:3, 3], tm_matrix_post[0:3, 3], rtol=pos_rtol, atol=pos_atol)

    # angles
    ang = np.allclose(tm_matrix[0:3, 0:2], tm_matrix_post[0:3, 0:2], rtol=ang_rtol, atol=ang_atol)

    # if tm_mean_last is not None:
    #     last_pos = np.allclose(tm_matrix[0:3, 3], tm_mean_last[0:3, 3], rtol=pos_rtol, atol=pos_atol)
    #     last_ang = np.allclose(tm_matrix[0:3, 0:2], tm_mean_last[0:3, 0:2], rtol=ang_rtol, atol=ang_atol)

    next_same = pos and ang
    last_same = last_pos and last_ang
    return next_same


def match_tm_to_im(tm_array, im_array, tms_time_arr, tms_cur_arr):
    """
    Match triggermarker with instrumentmarker and get index of best fitting instrumentmarker.


    Parameters
    ----------
    tm_array : ndarray of float [Nx4x4]
        Mean-value of Nx4x4 coil matrices
    im_array : ndarray of float [Mx4x4]
        Instrument-marker-matrices

    Returns
    -------
    im_index_lst : list of int
        Indices of best fitting instrumentmarkers
    """
    max_time_dif = (tms_time_arr[1] - tms_time_arr[0]) * 3
    max_mep_dif = 9

    im_index_lst = []
    drop_idx = []

    for tm_index in range(tm_array.shape[0]):
        # after first zap, check time diff
        if tm_index > 0:
            if tms_time_arr[tm_index] - tms_time_arr[tm_index - 1] < max_time_dif:
                im_index_lst.append(im_index_lst[-1])
                continue

        allclose_index_lst = []
        diff_small = []

        atol_ori = 0.4
        atol_pos = 3
        repeat = False

        tm = tm_array[tm_index, :, :]

        # proc_diffs = np.argmin[procrustes(tm, im_array[i])[2] for i in range(im_array.shape[0])]

        # diffs = np.abs(tm - im_array)
        # diffs[0:3, 0:3] /= np.max(diffs[:, 0:3, 0:4], axis=0)
        # best_fit = np.argmin(np.array([np.sum(diffs[i]) for i in range(len(diffs))]))
        # small_diff_ori = int(np.argmin(np.array([np.sum(diffs[i][0:3, 0:3]) for i in range(len(diffs))])))
        # small_diff_pos = int(np.argmin(np.array([np.sum(diffs[i][0:3, 3]) for i in range(len(diffs))])))
        # a = rot_to_quat(tm[:3,:3])[1:]
        # b = [quaternion_diff(a, rot_to_quat(im_array[i, :3, :3])[1:]) for i in range(im_array.shape[0])]

        while not allclose_index_lst:
            if repeat:
                print(('Warning: Trigger marker #{:0>4}: No matching instrument marker within '
                       'atol_ori={} and atol_pos={}! Increasing tolerances by 0.1 and 0.5.'
                       .format(tm_index, atol_ori, atol_pos)))

                atol_ori = atol_ori + 0.1
                atol_pos = atol_pos + 0.5

            for im_index in range(im_array.shape[0]):

                # # check if arrays are close
                # if np.allclose(tm_array[tm_index, :, :], im_array[im_index, :, :], rtol=rtol):
                #     allclose_index_lst.append(im_index)

                # check if arrays are close
                diff = np.abs(tm_array[tm_index, :, :] - im_array[im_index, :, :])

                if (diff[0:3, 0:3] < atol_ori).all() and (diff[0:3, 3] < atol_pos).all():
                    diff_small.append(diff)
                    allclose_index_lst.append(im_index)

            if not allclose_index_lst:
                allclose_index_lst.append(-1)
                # repeat = True

        # if multiple arrays are close, choose value, with smallest difference
        if len(allclose_index_lst) > 1:
            smallest_value_index = int(np.argmin(np.array([np.sum(diff_small[i]) for i in range(len(diff_small))])))
            small_diff_ori = int(np.argmin(np.array([np.sum(diff_small[i][0:3, 0:3]) for i in range(len(diff_small))])))
            small_diff_pos = int(np.argmin(np.array([np.sum(diff_small[i][0:3, 3]) for i in range(len(diff_small))])))
            if not small_diff_ori == small_diff_pos:
                #     print allclose_index_lst
                print("Warning: Triggermarker #{:0>4}: " \
                      "Cannot decide for instrument marker , dropping this one. ".format(tm_index))
            #     drop_idx.append(tm_index)
            # im_index_lst.append(im_index_lst[-1])
            # else:
            # assert best_fit == allclose_index_lst[smallest_value_index]
            im_index_lst.append(allclose_index_lst[smallest_value_index])

        else:
            # assert best_fit == allclose_index_lst[0]
            im_index_lst.append(allclose_index_lst[0])

            # # if multile arrays are close, choose value, where the difference to the instrument marker has the smallest
            # # frobenius norm
            # if len(allclose_index_lst) > 1:
            #     smallest_value_index = int(np.argmin(np.linalg.norm(im_array[allclose_index_lst, :, :] -
            #                                                         tm_array[tm_index, :, :], axis=(1, 2))))
            #     im_index_lst.append(allclose_index_lst[smallest_value_index])
            # else:
            #     im_index_lst.append(allclose_index_lst[0])

    return im_index_lst, drop_idx


def get_instrument_marker(im_path):
    return get_marker(im_path, 'InstrumentMarker')[:2]


def get_marker(im_path, markertype):
    """
    Read instrument-marker and conditions from Neuronavigator .xml-file.

    Parameters
    ----------
    im_path : str or list of str
        Path to instrument-marker-file

    Returns
    -------
    im_array : np.array of float [Mx4x4]
        Instrument-marker-matrices
    im_cond_lst : list of str
        Labels of the instrument-marker-conditions
    im_marker_times : list of float
        Onset times
    """
    if isinstance(im_path, str):
        return get_single_marker_file(im_path, markertype)

    elif isinstance(im_path, list):
        # if multiple triggermarker files are provided, pick a marker with data
        im_array, marker_descriptions, marker_times = [], [], []

        # get data from all files
        for im in im_path:
            im_array_t, marker_descriptions, marker_times = get_single_marker_file(im, markertype)
            im_array.append(im_array_t)

        # get indices for all files where markers are empty
        empty_arr = []
        for arr in im_array:  # arr = im_array[0]
            empty_arr.append(markers_are_empty(arr))
        # assert np.all(np.sum(np.array(empty_arr).astype(int), axis=0) == 1)

        # go through the zaps and pick a marker with data.
        idx = []
        tmp = 0
        for i in range(len(im_array[0])):
            for j in range(len(im_array)):
                if not empty_arr[j][i]:
                    tmp = j
                # if all are empty, just use the last value (is empty anyway)
            idx.append(tmp)  # append

        # build marker idx based on idx
        final_arr = []
        for it, i in enumerate(idx):
            final_arr.append(im_array[i][it])
        return np.array(final_arr), marker_descriptions, marker_times
    else:
        raise NotImplementedError(f"type {type(im_path)} not implemented.")


def markers_are_empty(arr):
    return [marker_is_empty(arr[i, :, :]) for i in range(arr.shape[0])]


def marker_is_empty(arr):
    return np.all(arr == np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]))


def get_single_marker_file(im_path, markertype):
    """
        Read instrument-marker and conditions from Neuronavigator .xml-file.

        Parameters
        ----------
        im_path : str or list of str
            Path to instrument-marker-file

        Returns
        -------
        im_array : np.array of float [Mx4x4]
            Instrument-marker-matrices
        im_cond_lst : list of str
            Labels of the instrument-marker-conditions
        """
    im_array = np.empty([0, 4, 4])
    marker_descriptions = []
    marker_times = []
    # parse XML document
    im_tree = xmlt.parse(im_path)
    im_root = im_tree.getroot()
    # iterate over all 'InstrumentMarker' tags
    for marker_i in im_root.iter(markertype):
        marker_array = np.empty([1, 4, 4])
        # get tag were the matrix is
        if markertype == 'InstrumentMarker':
            marker_object = marker_i.find('Marker')
            marker_descriptions.append(marker_object.get('description'))
            matrix4d = marker_object.find('Matrix4D')

        elif markertype == 'TriggerMarker':
            matrix4d = marker_i.find('Matrix4D')
            marker_descriptions.append(marker_i.get('description'))
            marker_times.append(marker_i.get('recordingTime'))
        # get values
        for im_index1 in range(4):
            for im_index2 in range(4):
                marker_array[0, im_index1, im_index2] = (float(matrix4d.get('data' + str(im_index1) + str(im_index2))))
        im_array = np.append(im_array, marker_array, axis=0)

    return im_array, marker_descriptions, marker_times


def read_triggermarker_localite(fn_xml):
    """
    Read instrument-marker and conditions from neuronavigator .xml-file.

    Parameters
    ----------
    fn_xml : str
        Path to TriggerMarker.xml file
        (e.g. Subject_0/Sessions/Session_YYYYMMDDHHMMSS/TMSTrigger/TriggerMarkers_Coil1_YYYYMMDDHHMMSS.xml)

    Returns
    -------
    list of
        m_nnav : ndarray of float [4x4xN]
            Neuronavigation coordinates of N stimuli (4x4 matrices)
        didt : ndarray of float [N]
            Rate of change of coil current in (A/us)
        stim_int : ndarray of float [N]
            Stimulator intensity in (%)
        descr : list of str [N]
            Labels of the instrument-marker-conditions
        rec_time : list of str [N]
            Recording time in ms
    """

    m_nnav = np.empty([4, 4, 0])
    descr = []
    stim_int = []
    didt = []
    rec_time = []

    # parse XML document
    im_tree = xmlt.parse(fn_xml)
    im_root = im_tree.getroot()

    # iterate over all 'InstrumentMarker' tags
    for im_iter in im_root.iter('TriggerMarker'):
        m = np.empty([4, 4, 1])

        # read description
        descr.append(im_iter.get('description'))
        rec_time.append(im_iter.get('recordingTime'))

        # read di/dt and stimulator intensity
        im_rv = im_iter.find('ResponseValues').findall('Value')

        for _im_rv in im_rv:
            # di/dt
            if _im_rv.get('key') == "valueA":
                didt.append(float(_im_rv.get('response')))
            # stimulator intensity
            elif _im_rv.get('key') == "amplitudeA":
                stim_int.append(float(_im_rv.get('response')))

        # read matrix
        im_ma = im_iter.find('Matrix4D')

        for im_index1 in range(4):
            for im_index2 in range(4):
                m[im_index1, im_index2, 0] = (float(im_ma.get('data' + str(im_index1) + str(im_index2))))
        m_nnav = np.append(m_nnav, m, axis=2)

    didt = np.array(didt)
    stim_int = np.array(stim_int)

    return [m_nnav, didt, stim_int, descr, rec_time]
