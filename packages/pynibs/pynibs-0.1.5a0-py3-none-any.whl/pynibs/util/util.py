import os
import math
import copy
import time
import inspect
import warnings
import itertools
import subprocess
import numpy as np
import h5py

from scipy.special import binom
from scipy.spatial import Delaunay
from scipy.interpolate import griddata
from sklearn.neighbors import KernelDensity


def calc_tet_volume(points, abs=True):
    """
    Calculate tetrahedra volumes.

    Parameter
    ---------
    points: np.ndarray
        shape: (n_tets,4,3)
        [[[Ax, Ay, Az],
          [Bx, By, Bz],
          [Cx, Cy, Cz],
          [Dx, Dy, Dy]],

         [[Ax, Ay, Az],
          [Bx, By, Bz],
          [Cx, Cy, Cz],
          [Dx, Dy, Dy]],

        ...

        ]

    Returns
    -------
    volume: np.ndarray
        shape: (n_tets)

    Other Parameters
    ----------------
    abs : bool
        Return magnitude. Default: True.
    """
    if points.ndim == 2:
        points = np.atleast_3d(points).reshape(1,4,3)
    if points.ndim != 3:
        raise ValueError(f"Wrong dimensions for points: ({points.shape}). Expected: (n_tets,4,3))")

    a = np.zeros((points.shape[0], 4, 4))
    a[:, :, 3] = 1
    a[:, :, :3] = points
    a = a.swapaxes(1, 2)

    if abs:
        return np.abs(1 / 6 * np.linalg.det(a))
    else:
        return 1 / 6 * np.linalg.det(a)


def calc_tri_surface(points):
    """
    Calculate triangle surface areas.

    Parameter
    ---------
    points : np.ndarray
        (n_triangles,3,3)

    Returns
    -------
    triange_area : np.ndarray
    """
    a = np.linalg.norm(points[:, 0] - points[:, 1], axis=1)
    b = np.linalg.norm(points[:, 1] - points[:, 2], axis=1)
    c = np.linalg.norm(points[:, 0] - points[:, 2], axis=1)
    s = np.sum((a, b, c), axis=0) / 2
    return (s * (s - a) * (s - b) * (s - c)) ** 0.5


def rd(array, array_ref):
    """
    Determine the relative difference between input data and reference data.

    Parameters
    ----------
    array: np.ndarray
        input data [ (x), y0, y1, y2 ... ]
    array_ref: np.ndarray
        reference data [ (x_ref), y0_ref, y1_ref, y2_ref ... ]
        if array_ref is 1D, all sizes have to match

    Returns
    -------
    rd: ndarray of float [array.shape[1]]
        Relative difference between the columns of array and array_ref
    """

    return np.linalg.norm(array - array_ref) / np.linalg.norm(array_ref)


def get_sphere(mesh=None, mesh_fn=None, target=None, radius=None, roi_idx=None, roi=None, elmtype='tris'):
    """
    Return element idx of elements within a certain distance to provided target.
    Elements might be 'tris' (default) or 'tets'

    If roi object / idx and mesh fn is provided, the roi is expected to have midlayer information and the roi
    geometry is used.



    """

    from ..hdf5_io import load_roi_surface_obj_from_hdf5
    from pynibs import load_mesh_hdf5

    if mesh_fn is not None:
        if mesh is not None:
            raise ValueError("Either provide mesh or mesh_fn")
        if mesh_fn.endswith('.hdf5'):
            mesh = load_mesh_hdf5(mesh_fn)
    if roi is None and roi_idx is not None:
        if mesh_fn is None:
            raise ValueError("Provide mesh_fn to load roi from")
        roi = load_roi_surface_obj_from_hdf5(mesh_fn)[roi_idx]
    if elmtype == 'tris':
        return tris_in_sphere(mesh=mesh, target=target, radius=radius, roi=roi)
    elif elmtype == 'tets':
        return tets_in_sphere(mesh=mesh, target=target, radius=radius, roi=roi)
    else:
        raise ValueError(f"Unknown elmtpye '{elmtype}'")


def tets_in_sphere(mesh, target, radius, roi):
    """
    Worker function for get_sphere()

    """
    if roi is None:
        if radius is None or radius == 0:
            return np.where(np.linalg.norm(mesh.tetrahedra_center - target, axis=1) ==
                            np.min(np.linalg.norm(mesh.tetrahedra_center - target, axis=1)))[0]
    else:

        if radius is not None and radius > 0:
            tri_target_idx = np.where(np.linalg.norm(roi.tri_center_coord_mid - target, axis=1) <= radius)[0]
        else:
            tri_target_idx = np.where(np.linalg.norm(roi.tri_center_coord_mid - target, axis=1) == np.min(
                np.linalg.norm(roi.tri_center_coord_mid - target, axis=1)))[0]
        tet_target_idx = roi.tet_idx_tri_center_mid[tri_target_idx]
        return tet_target_idx


def tris_in_sphere(mesh, target, radius, roi):
    """
    Worker function for get_sphere()

    """
    if roi is None:
        if radius is None or radius == 0:
            return np.where(np.linalg.norm(mesh.triangles_center - target, axis=1) ==
                            np.min(np.linalg.norm(mesh.triangles_center - target, axis=1)))[0]

    else:
        if radius is not None and radius > 0:
            tri_target_idx = np.where(np.linalg.norm(roi.tri_center_coord_mid - target, axis=1) <= radius)[0]
        else:
            tri_target_idx = np.where(np.linalg.norm(roi.tri_center_coord_mid - target, axis=1) == np.min(
                np.linalg.norm(roi.tri_center_coord_mid - target, axis=1)))[0]

        return tri_target_idx


def sample_sphere(n_points, r):
    """
    Creates n_points evenly spread in a sphere of radius r.

    Parameters
    ----------
    n_points: int
        Number of points to be spread, must be odd
    r: float
        Radius of sphere

    Returns
    -------
    points: ndarray of float [N x 3]
        Evenly spread points in a unit sphere
    """

    assert n_points % 2 == 1, "The number of points must be odd"
    points = []

    # The golden ratio
    phi = (1 + math.sqrt(5)) / 2.
    n = int((n_points - 1) / 2)

    for i in range(-n, n + 1):
        lat = math.asin(2 * i / n_points)
        lon = 2 * math.pi * i / phi
        x = r * math.cos(lat) * math.cos(lon)
        y = r * math.cos(lat) * math.sin(lon)
        z = r * math.sin(lat)
        points.append((x, y, z))

    points = np.array(points, dtype=float)

    return points


def generalized_extreme_value_distribution(x, mu, sigma, k):
    """
    Generalized extreme value distribution

    Parameters
    ----------
    x : ndarray of float [n_x]
        Events
    mu : float
        Mean value
    sigma : float
        Standard deviation
    k : float
        Shape parameter

    Returns
    -------
    y : ndarray of float [n_x]
        Probability density of events
    """
    y = 1 / sigma * np.exp(-(1 + (k * (x - mu)) / sigma) ** (-1 / k)) * (1 + (k * (x - mu)) / sigma) ** (-(1 + 1 / k))

    return y


# Differential Evolution (single core)
############################################################################################################
def differential_evolution(fobj, bounds, mut=0.8, crossp=0.7, popsize=20, its=1000, **kwargs):
    """
    Differential evolution optimization algorithm

    Parameters
    ----------
    fobj : function object
        Function to optimize
    bounds : dict
        Dictionary containing the bounds of the free variables to optimize
    mut : float
        Mutation factor
    crossp : float
        Cross population factor
    popsize : int
        Population size
    its : int
        Number of iterations
    kwargs : dict
        Arguments passed to fobj (constants etc...)

    Returns
    --------
    best : dict
        Dictionary containing the best values
    fitness : float
        Fitness value of best solution
    """
    if kwargs is None:
        kwargs = dict()

    fobj_args = inspect.getfullargspec(fobj).args

    if "bounds" in fobj_args:
        kwargs["bounds"] = bounds
    params_str = list(bounds.keys())

    # set up initial simulations
    dimensions = len(bounds)
    pop = np.random.rand(popsize, dimensions)

    min_b = np.zeros(dimensions)
    max_b = np.zeros(dimensions)

    for i, key in enumerate(bounds):
        min_b[i] = bounds[key][0]
        max_b[i] = bounds[key][1]

    diff = np.fabs(min_b - max_b)
    pop_denorm = min_b + pop * diff

    print("Initial simulations:")
    print("====================")

    fitness = np.zeros(len(pop_denorm))

    for i, po in enumerate(pop_denorm):

        for i_key, key in enumerate(params_str):
            kwargs[key] = po[i_key]

        fitness[i] = fobj(**kwargs)

    best_idx = np.argmin(fitness)
    best = pop_denorm[best_idx]

    parameter_str = [f"{params_str[i_p]}={p_:.5f}" for i_p, p_ in enumerate(pop_denorm[best_idx])]
    print(f"-> Fittest: {fitness[best_idx]:.3f} / " + ", ".join(parameter_str))

    for i in range(its):
        print(f"Iteration: {i}")
        print(f"==============")

        trial_denorm = []
        trial = []

        # create new parameter sets
        for j in range(popsize):
            idxs = [idx for idx in range(popsize) if idx != j]
            a, b, c = pop[np.random.choice(idxs, 3, replace=False)]
            mutant = np.clip(a + mut * (b - c), 0, 1)
            cross_points = np.random.rand(dimensions) < crossp

            if not np.any(cross_points):
                cross_points[np.random.randint(0, dimensions)] = True

            trial.append(np.where(cross_points, mutant, pop[j]))
            trial_denorm.append(min_b + trial[j] * diff)

        # run likelihood function
        f = np.zeros(len(trial))

        for j, tr in enumerate(trial_denorm):
            for i_key, key in enumerate(params_str):
                kwargs[key] = tr[i_key]
            f[j] = fobj(**kwargs)

        for j in range(popsize):
            if f[j] < fitness[j]:
                fitness[j] = copy.deepcopy(f[j])
                pop[j] = trial[j]
                if f[j] < fitness[best_idx]:
                    best_idx = j
                    best = trial_denorm[j]

        parameter_str = [f"{params_str[i_p]}={p_:.5f}" for i_p, p_ in enumerate(best)]
        print(f"-> Fittest: {fitness[best_idx]:.3f} / " + ", ".join(parameter_str))

    best_dict = dict()
    for i_key, key in enumerate(params_str):
        best_dict[key] = best[i_key]

    return best_dict, fitness[best_idx]


def sigmoid_log_p(x, p):
    y = np.log10(p[0] / (1 + np.exp(-p[1] * (x - p[2]))))
    return y


def likelihood_posterior(x, y, fun, bounds=None, verbose=True, normalized_params=False, **params):
    """
    Determines the likelihood of the data following the function "fun" assuming a two
    variability source of the data pairs (x, y) using the posterior distribution.

    Parameters
    ----------
    x : ndarray of float [n_points]
        x data
    y : ndarray of float [n_points]
        y data
    fun : function object
        Function object to fit the data to (e.g. sigmoid)
    bounds : dict, optional, default: None
        Dictionary containing the bounds of "sigma_x" and "sigma_y" and the free parameters of fun
    verbose : bool, optional, default: True
        Print function output after every calculation
    normalized_params : bool, optional, default: False
        Are the parameters passed in normalized space between [0, 1]? If so, bounds are used to
        denormalize them before calculation
    **params : dict
        Free parameters to optimize. Contains "sigma_x", "sigma_y", and the free parameters of fun


    Returns
    -------
    l : float
        Negative likelihood
    """
    start = time.time()

    # read arguments from function
    # args = inspect.getfullargspec(fun).args

    # extract parameters
    sigma_x = params["sigma_x"]
    sigma_y = params["sigma_y"]

    del params["sigma_x"], params["sigma_y"]

    # denormalize parameters from [0, 1] to bounds
    if normalized_params:
        if bounds is None:
            raise ValueError("Please provide bounds if parameters were passed normalized!")
        sigma_x = sigma_x * (bounds["sigma_x"][1] - bounds["sigma_x"][0]) + bounds["sigma_x"][0]
        sigma_y = sigma_y * (bounds["sigma_y"][1] - bounds["sigma_y"][0]) + bounds["sigma_y"][0]

        for key in enumerate(params):
            params[key] = params[key] * (bounds[key][1] - bounds[key][0]) + bounds[key][0]

    if sigma_x < 0:
        sigma_x = 0

    if sigma_y < 0:
        sigma_y = 0

    # determine posterior of DVS model with test data
    x_pre = np.linspace(np.min(x), np.max(x), 500000)
    x_post = x_pre + np.random.normal(loc=0., scale=sigma_x, size=len(x_pre))
    y_post = fun(x_post, **params) + np.random.normal(loc=0., scale=sigma_y, size=len(x_pre))

    # bin data
    n_bins = 50
    dx_bins = (np.max(x_pre) - np.min(x_pre)) / n_bins
    x_bins_loc = np.linspace(np.min(x_pre) + dx_bins / 2, np.max(x_pre) - dx_bins / 2, n_bins)

    # determine probabilities of observations
    kde = KernelDensity(bandwidth=0.01, kernel='gaussian')

    l = []

    for i in range(n_bins):
        mask = np.logical_and(x_pre >= (x_bins_loc[i] - dx_bins / 2), x_pre < (x_bins_loc[i] + dx_bins / 2))
        mask_data = np.logical_and(x >= (x_bins_loc[i] - dx_bins / 2), x < (x_bins_loc[i] + dx_bins / 2))

        if np.sum(mask_data) == 0:
            continue

        # determine kernel density estimate
        try:
            kde_bins = kde.fit(y_post[mask][:, np.newaxis])
        except ValueError:
            warnings.warn("kde.fit(y_post[mask][:, np.newaxis]) yield NaN ... skipping bin")
            continue

        # get probability densities at data
        kde_y_post_bins = np.exp(kde_bins.score_samples(y[mask_data][:, np.newaxis]))

        l.append(kde_y_post_bins)

    l = np.concatenate(l)

    # mask out zero probabilities
    l[l == 0] = 1e-100

    # determine log likelihood
    l = np.sum(np.log10(l))

    stop = time.time()

    if verbose:
        parameter_str = [f"{p_}={params[p_]:.5f}" for p_ in params]
        print(f"Likelihood: {l:.1f} / sigma_x={sigma_x:.5f}, sigma_y={sigma_y:.5f}, " +
              ", ".join(parameter_str) + f"({stop - start:.2f} sec)")

    return -l


def mutual_coherence(array):
    """
    Calculate the mutual coherence of a matrix A. It can also be referred as the cosine of the smallest angle
    between two columns.

    mutual_coherence = mutual_coherence(array)

    Parameters
    ----------
    array: ndarray of float
        Input matrix

    Returns
    -------
    mutual_coherence: float
        Mutual coherence
    """

    array = array / np.linalg.norm(array, axis=0)[np.newaxis, :]
    t = np.matmul(array.conj().T, array)
    np.fill_diagonal(t, 0.0)
    mu = np.max(t)

    # s = np.sqrt(np.diag(t))
    # s_sqrt = np.diag(s)
    # mu = np.max(1.0*(t-s_sqrt)/np.outer(s, s))

    return mu


def get_cartesian_product(array_list):
    """
    Generate a cartesian product of input arrays (all combinations).

    cartesian_product = get_cartesian_product(array_list)

    Parameters
    ----------
    array_list : list of 1D ndarray of float
        Arrays to compute the cartesian product with

    Returns
    -------
    cartesian_product : ndarray of float
        Array containing the cartesian products (all combinations of input vectors)
        (M, len(arrays))

    Examples
    --------
    >>> import pygpc
    >>> out = pygpc.get_cartesian_product(([1, 2, 3], [4, 5], [6, 7]))
    >>> out
    """

    cartesian_product = [element for element in itertools.product(*array_list)]
    return np.array(cartesian_product)


def norm_percentile(data, percentile):
    """
    Normalizes data to a given percentile.

    Parameters
    ----------
    data : nparray [n_data, ]
        Dataset to normalize
    percentile : float
        Percentile of normalization value [0 ... 100]

    Returns
    -------
    data_norm : nparray [n_data, ]
        Normalized dataset
    """

    return data / np.percentile(data, percentile)


def compute_chunks(seq, num):
    """
    Splits up a sequence _seq_ into _num_ chunks of similar size.
    If len(seq) < num, (num-len(seq)) empty chunks are returned so that len(out) == num

    Parameters
    ----------
    seq : list of something [N_ele]
        List containing data or indices, which is divided into chunks
    num : int
        Number of chunks to generate

    Returns
    -------
    out : list of num sublists
        num sub-lists of seq with each of a similar number of elements (or empty).
    """
    assert len(seq) > 0
    assert num > 0
    assert isinstance(seq, list), f"{type(seq)} can't be chunked. Provide list."
    avg = len(seq) / float(num)
    n_empty = 0  # if len(seg) < num, how many empty lists to append to return?

    if avg < 1:
        # raise ValueError("seq/num ration too small: " + str(avg))
        avg = 1
        n_empty = num - len(seq)

    out = []
    last = 0.0

    while last < len(seq):
        # if only one element would be left in the last run, add it to the current
        if (int(last + avg) + 1) == len(seq):
            last_append_idx = int(last + avg) + 1
        else:
            last_append_idx = int(last + avg)

        out.append(seq[int(last):last_append_idx])

        if (int(last + avg) + 1) == len(seq):
            last += avg + 1
        else:
            last += avg

    # append empty lists if len(seq) < num
    out += [[]] * n_empty

    return out


def get_indices_discontinuous_data(data, con, neighbor=False, deviation_factor=2,
                                   min_val=None, not_fitted_elms=None, crit='median', neigh_style='point'):
    """
    Get element indices (and the best neighbor index), where the data is discontinuous

    Parameters
    ----------
    data : ndarray of float [n_data]
        Data array to analyze given in the element center
    con : ndarray of float [n_data, 3 or 4]
        Connectivity matrix
    neighbor : boolean, optional, default=False
        Return also the element index of the "best" neighbor (w.r.t. median of data)
    deviation_factor : float
        Allows data deviation from 1/deviation_factor < data[i]/median < deviation_factor
    min_val : float, optional
        If given, only return elements which have a neighbor with data higher than min_val.
    not_fitted_elms : ndarray
        If given, these elements are not used as neighbors
    crit: str, default: median
        Criterium for best neighbor. Either median or max value
    neigh_style : str, default: 'point'
        Should neighbors share point or 'edge'

    Returns
    -------
    idx_disc : list of int [n_disc]
        Index list containing the indices of the discontinuous elements
    idx_neighbor : list of int [n_disc]
        Index list containing the indices of the "best" neighbors of the discontinuous elements
    """

    n_ele = con.shape[0]
    idx_disc, idx_neighbor = [], []

    data[data == 0] = 1e-12

    if neigh_style == 'point':
        def get_neigh(m):
            return np.logical_and(0 < mask, mask < 3)
    elif neigh_style == 'edge':
        def get_neigh(m):
            return mask == 2
    else:
        raise NotImplementedError(f"neigh_style {neigh_style} unknown.")

    if crit == 'median':
        def is_neigh():
            if not (1 / deviation_factor < data_i / median < deviation_factor):
                neighbor_indices = np.where(mask_neighbor)[0]
                best_neigh = neighbor_indices[(np.abs(data[neighbor_indices] - median)).argmin()]
                if min_val is None or data[best_neigh] > min_val:
                    idx_disc.append(elm_i)
                # if neighbor:
                idx_neighbor.append(best_neigh)
    elif crit == 'max':
        def is_neigh():
            if data_i / median < 1 / deviation_factor:
                neighbor_indices = np.where(mask_neighbor)[0]
                best_neigh = neighbor_indices[(data[neighbor_indices]).argmax()]
                if min_val is None or data[best_neigh] > min_val:
                    idx_disc.append(elm_i)

                # if neighbor:
                idx_neighbor.append(best_neigh)
    elif crit == 'randmax':
        def is_neigh():
            if data_i / median < 1 / deviation_factor:
                neighbor_indices = np.where(mask_neighbor)[0]
                best_neigh = np.random.choice(neighbor_indices[(data[neighbor_indices]) > 0], 1)
                if min_val is None or data[best_neigh] > min_val:
                    idx_disc.append(elm_i)

                # if neighbor:
                idx_neighbor.append(best_neigh)
    else:
        raise NotImplementedError(f"Criterium {crit} unknown. ")

    # start = time.time()
    for elm_i, data_i in zip(range(n_ele), data):
        if elm_i in not_fitted_elms:
            continue

        # find neighbors
        mask = np.sum(np.isin(con, con[elm_i, :]), axis=1)
        mask_neighbor = get_neigh(mask)

        # best_values are set to 0 for bad elements and unfittable ones. do not use these as neighbors
        if not_fitted_elms is not None and len(not_fitted_elms) != 0:
            mask_neighbor[not_fitted_elms] = False

        # if the element is lonely floating and has no neighbors ... continue
        if not np.sum(mask_neighbor):
            continue

        # check if current value does not fit to neighbors
        median = np.median(data[mask_neighbor])

        if not median:
            median = 1e-12

        is_neigh()

        # if not (1 / deviation_factor < data_i / median < deviation_factor):
        #     # find best neighbor idx
        #     neighbor_indices = np.where(mask_neighbor)[0]
        #
        #     if crit == 'max':
        #         best_neigh = neighbor_indices[(data[neighbor_indices]).argmax()]
        #     elif crit == 'median':
        #         best_neigh = neighbor_indices[(np.abs(data[neighbor_indices] - median)).argmin()]
        #     else:
        #         raise  NotImplementedError(f"Criterium {crit} unknown. ")
        #     if min_val is None or data[best_neigh] > min_val:
        #         idx_disc.append(elm_i)
        #
        #     if neighbor:
        #         idx_neighbor.append(best_neigh)

        # stop = time.time()
        # print(stop-start)

    if neighbor:
        return idx_disc, idx_neighbor
    else:
        return idx_disc


def find_nearest(array, value):
    """
    Given an "array", and given a "value" , returns an index j such that "value" is between array[j]
    and array[j+1]. "array" must be monotonic increasing. j=-1 or j=len(array) is returned
    to indicate that "value" is out of range below and above respectively.

    Parameters
    ----------
    array : nparray of float
        Monotonic increasing array
    value : float
        Target value the nearest neighbor index in "array" is computed for

    Returns
    -------
    idx : int
        Index j such that "value" is between array[j] and array[j+1]

    """
    n = len(array)
    if value < array[0]:
        return -1
    elif value > array[n - 1]:
        return n
    jl = 0  # Initialize lower
    ju = n - 1  # and upper limits.
    while ju - jl > 1:  # If we are not yet done,
        jm = (ju + jl) >> 1  # compute a midpoint with a bitshift
        if value >= array[jm]:
            jl = jm  # and replace either the lower limit
        else:
            ju = jm  # or the upper limit, as appropriate.
    # Repeat until the test condition is satisfied.
    if value == array[0]:  # edge cases at bottom
        return 0
    elif value == array[n - 1]:  # and top
        return n - 1
    else:
        return jl


def bash(command):
    """
    Executes bash command and returns output message in stdout (uses os.popen).

    Parameters
    ----------
    command : str
        Bash command

    Returns
    -------
    output : str
        Output from stdout
    error : str
        Error message from stdout
    """

    print(("Running " + command))
    return os.popen(command).read()
    # process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, shell=True)
    # output, error = process.communicate()
    # return output, error


def bash_call(command):
    """
    Executes bash command and returns output message in stdout (uses subprocess.Popen).

    Parameters
    ----------
    command: str
        bash command
    """
    subprocess.Popen(command, shell=True)


def normalize_rot(rot):
    """
    Normalize rotation matrix.

    Parameters
    ----------
    rot : nparray of float [3 x 3]
        Rotation matrix

    Returns
    -------
    rot_norm : nparray of float [3 x 3]
        Normalized rotation matrix
    """

    q = rot_to_quat(rot)
    q /= np.sqrt(np.sum(q ** 2))
    return quat_to_rot(q)


def invert(trans):
    """
    Invert rotation matrix.

    Parameters
    ----------
    trans : nparray of float [3 x 3]
        Rotation matrix

    Returns
    -------
    rot_inv : nparray of float [3 x 3]
        Inverse rotation matrix
    """
    rot = normalize_rot(trans[:3, :3].flatten())
    result = np.zeros((4, 4))
    result[3, 3] = 1.0
    t = -rot.T.dot(trans[:3, 3])
    result[:3, :3] = rot.T
    result[:3, 3] = t
    return result


def list2dict(l):
    """
    Transform list of dicts with same keys to dict of list

    Parameters
    ----------
    l : list of dict
        List containing dictionaries with same keys

    Returns
    -------
    d : dict of lists
        Dictionary containing the entries in a list
    """

    n = len(l)
    keys = l[0].keys()
    d = dict()

    for key in keys:
        d[key] = [0 for _ in range(n)]
        for i in range(n):
            d[key][i] = l[i][key]

    return d


def quat_rotation_angle(q):
    """
    Computes the rotation angle from the quaternion in rad.

    Parameters
    ----------
    q : nparray of float
        Quaternion, either only the imaginary part (length=3) [qx, qy, qz]
        or the full quaternion (length=4) [qw, qx, qy, qz]

    Returns
    -------
    alpha : float
        Rotation angle of quaternion in rad
    """

    if len(q) == 3:
        alpha = 2 * np.arcsin(np.linalg.norm(q))
    elif len(q) == 4:
        alpha = q[0]
    else:
        raise ValueError('Please check size of quaternion')


def quat_to_rot(q):
    """
    Computes the rotation matrix from quaternions.

    Parameters
    ----------
    q : nparray of float
        Quaternion, either only the imaginary part (length=3) or the full quaternion (length=4)

    Returns
    -------
    rot : nparray of float [3 x 3]
        Rotation matrix, containing the x, y, z axis in the columns
    """
    if q.size == 3:
        q = np.hstack([np.sqrt(1 - np.sum(q ** 2)), q])
    rot = np.array([[q[0] ** 2 + q[1] ** 2 - q[2] ** 2 - q[3] ** 2, 2 * (q[1] * q[2] - q[0] * q[3]),
                     2 * (q[1] * q[3] + q[0] * q[2])],
                    [2 * (q[2] * q[1] + q[0] * q[3]), q[0] ** 2 - q[1] ** 2 + q[2] ** 2 - q[3] ** 2,
                     2 * (q[2] * q[3] - q[0] * q[1])],
                    [2 * (q[3] * q[1] - q[0] * q[2]), 2 * (q[3] * q[2] + q[0] * q[1]),
                     q[0] ** 2 - q[1] ** 2 - q[2] ** 2 + q[3] ** 2]])
    return rot


def rot_to_quat(rot):
    """
    Computes the quaternions from rotation matrix.
    (see e.g. http://www.euclideanspace.com/maths/geometry/rotations/conversions/matrixToQuaternion/)

    Parameters
    ----------
    rot : nparray of float [3 x 3]
        Rotation matrix, containing the x, y, z axis in the columns

    Returns
    -------
    q : nparray of float
        Quaternion, full (length=4)
    """

    rot = rot.flatten()
    t = 1. + rot[0] + rot[4] + rot[8]
    if t > np.finfo(rot.dtype).eps:
        s = np.sqrt(t) * 2.
        qx = (rot[7] - rot[5]) / s
        qy = (rot[2] - rot[6]) / s
        qz = (rot[3] - rot[1]) / s
        qw = 0.25 * s
    elif rot[0] > rot[4] and rot[0] > rot[8]:
        s = np.sqrt(1. + rot[0] - rot[4] - rot[8]) * 2.
        qx = 0.25 * s
        qy = (rot[1] + rot[3]) / s
        qz = (rot[2] + rot[6]) / s
        qw = (rot[7] - rot[5]) / s
    elif rot[4] > rot[8]:
        s = np.sqrt(1. - rot[0] + rot[4] - rot[8]) * 2
        qx = (rot[1] + rot[3]) / s
        qy = 0.25 * s
        qz = (rot[5] + rot[7]) / s
        qw = (rot[2] - rot[6]) / s
    else:
        s = np.sqrt(1. - rot[0] - rot[4] + rot[8]) * 2.
        qx = (rot[2] + rot[6]) / s
        qy = (rot[5] + rot[7]) / s
        qz = 0.25 * s
        qw = (rot[3] - rot[1]) / s
    return np.array((qw, qx, qy, qz))


def quaternion_conjugate(q):
    """
    https://stackoverflow.com/questions/15425313/inverse-quaternion

    :param q:
    :type q:
    :return:
    :rtype:
    """
    return np.array((-q[0], -q[1], -q[2]))


def quaternion_inverse(q):
    """
    https://stackoverflow.com/questions/15425313/inverse-quaternion

    :param q:
    :type q:
    :return:
    :rtype:
    """
    return quaternion_conjugate(q) / np.linalg.norm(q)


def quaternion_diff(q1, q2):
    """
    https://math.stackexchange.com/questions/2581668/
    error-measure-between-two-rotations-when-one-matrix-might-not-be-a-valid-rotatio

    :param q1:
    :type q1:
    :param q2:
    :type q2:
    :return:
    :rtype:
    """
    return np.linalg.norm(q1 * quaternion_inverse(q2) - 1)


def euler_angles_to_rotation_matrix(theta):
    """
    Determines the rotation matrix from the three Euler angles theta = [Psi, Theta, Phi] (in rad), which rotate the
    coordinate system in the order z, y', x''.

    Parameters
    ----------
    theta : nparray [3]
        Euler angles in rad

    Returns
    -------
    r : nparray [3 x 3]
        Rotation matrix (z, y', x'')
    """

    # theta in rad
    r_x = np.array([[1., 0., 0.],
                    [0., math.cos(theta[0]), -math.sin(theta[0])],
                    [0., math.sin(theta[0]), math.cos(theta[0])]
                    ])

    r_y = np.array([[math.cos(theta[1]), 0, math.sin(theta[1])],
                    [0., 1., 0.],
                    [-math.sin(theta[1]), 0, math.cos(theta[1])]
                    ])

    r_z = np.array([[math.cos(theta[2]), -math.sin(theta[2]), 0],
                    [math.sin(theta[2]), math.cos(theta[2]), 0],
                    [0., 0., 1.]
                    ])

    r = np.dot(r_z, np.dot(r_y, r_x))

    return r


def rotation_matrix_to_euler_angles(r):
    """
    Calculates the euler angles theta = [Psi, Theta, Phi] (in rad) from the rotation matrix R which, rotate the
    coordinate system in the order z, y', x''.
    (https://www.learnopencv.com/rotation-matrix-to-euler-angles/)

    Parameters
    ----------
    M : np.array [3 x 3]
        Rotation matrix (z, y', x'')

    Returns
    -------
    theta : np.array [3]
        Euler angles in rad
    """
    sy = math.sqrt(r[0, 0] * r[0, 0] + r[1, 0] * r[1, 0])

    singular = sy < 1e-6

    if not singular:
        x = math.atan2(r[2, 1], r[2, 2])
        y = math.atan2(-r[2, 0], sy)
        z = math.atan2(r[1, 0], r[0, 0])
    else:
        x = math.atan2(-r[1, 2], r[1, 1])
        y = math.atan2(-r[2, 0], sy)
        z = 0

    return np.array([x, y, z])


# X (yaw)
# Y (pitch)
# Z (roll)


def recursive_len(item):
    """
    Determine len of list of list (recursively).

    Parameters
    ----------
    item : list of list
        List of list

    Returns
    -------
    len : int
        Total length of list of list
    """
    if type(item) == list:
        return sum(recursive_len(subitem) for subitem in item)
    else:
        return 1


def add_center(var):
    """
    Adds center to argument list.

    Parameters
    ----------
    var: list of float [2]
        List containing two values [f1,f2]

    Returns
    -------
    out: list of float [3]
        List containing the average value in the middle [f1, mean(f1,f2), f2]
    """

    return [var[0], sum(var) / 2, var[1]]


def unique_rows(a):
    """
    Returns the unique rows of np.array(a).

    Parameters
    ----------
    a : nparray of float [m x n]
        Array to search for double row entries

    Returns
    -------
    a_unique : np.array [k x n]
        array a with only unique rows
    """

    b = np.ascontiguousarray(a).view(np.dtype((np.void, a.dtype.itemsize * a.shape[1])))
    _, idx = np.unique(b, return_index=True)
    return a[idx]
    # alternative but ~10x slower:
    # surface_points=np.vstack({tuple(row) for row in surface_points})


def in_hull(points, hull):
    """
    Test if points in `points` are in `hull`.
    `points` should be a [N x K] coordinates of N points in K dimensions.
    `hull` is either a scipy.spatial.Delaunay object or the [M x K] array of the
    coordinates of M points in Kdimensions for which Delaunay triangulation
    will be computed.

    Parameters
    ----------
    points : nparray [N_points x 3]
        Set of floating point data to test whether they are lying inside the hull or not
    hull : Delaunay instance or nparray [M x K]
        Surface data

    Returns
    -------
    inside : boolean array
        TRUE: point inside the hull
        FALSE: point outside the hull
    """

    if not isinstance(hull, Delaunay):
        hull = Delaunay(hull)

    return hull.find_simplex(points) >= 0


def calc_n_network_combs(n_e, n_c, n_i):
    """
    Determine number of combinations if all conditions may be replaced between N_i elements (mixed interaction)

    Parameters
    ----------
    n_e : int
        Number of elements in the ROI
    n_c : int
        Number of conditions (I/O curves)
    n_i : int
        Number of maximum interactions

    Returns
    -------
    n_comb : int
        Number of combinations
    """

    return binom(n_e, n_i) * np.sum([((n_i - 1) ** k) * binom(n_c, k) for k in range(1, n_c)])


def cell_data_to_point_data(tris, data_tris, nodes, method='nearest'):
    """
    A wrapper for scipy.interpolate.griddata to interpolate cell data to node data.

    Parameters
    ----------

    tris : np.ndarray
        element number list, (n_tri, 3)
    data_tris : np.ndarray
        data in tris, , (n_tri x 3)
    nodes : np.ndarray
        nodes coordinates, (n_nodes, 3
    method: str, default: 'nearest'
        Which method to use for interpolation. Default uses NearestNDInterpolator

    Returns
    -------
    data_nodes : np.ndarray
        Data in nodes
    """
    elms_center = np.mean(nodes[tris], axis=1)
    return griddata(elms_center, data_tris, nodes, method)


def load_muaps(fn_muaps, fs=1e6, fs_downsample=1e5):
    # load MUAPs and downsample
    with h5py.File(fn_muaps, "r") as f:
        muaps_orig = f["MUAPShapes"][:]
    N_MU = muaps_orig.shape[1]

    t_muap_orig = np.linspace(0, 1 / fs * (muaps_orig.shape[0] - 1), muaps_orig.shape[0])
    t_muap = np.linspace(0, t_muap_orig[-1], int(t_muap_orig[-1] * fs_downsample + 1))
    muaps = np.zeros((len(t_muap), N_MU))

    for i in range(N_MU):
        muaps[:, i] = np.interp(t_muap, t_muap_orig, muaps_orig[:, i])

    return muaps, t_muap
