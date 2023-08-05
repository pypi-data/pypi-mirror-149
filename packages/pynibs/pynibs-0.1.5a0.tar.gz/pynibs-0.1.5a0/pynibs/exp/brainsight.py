""" """
import io
import os
import numpy as np


def write_targets_brainsight(targets, fn_out, names=None, overwrite=True):
    """
    Writes coil position and orientations in .txt file for import into Brainsight.

    Parameters
    ----------
    targets : ndarray of float [4 x 4 x N_targets]
        Tensor containing the 4x4 matrices with coil orientation and position
    fn_out : str
        Filename of output file
    names : list of str, optional, default: None
        Target names (If nothing is provided they will be numbered by their order)
    overwrite : bool, optional, default: True
        Overwrite existing .txt file

    Returns
    -------
    <file> .txt file containing the targets for import into Brainsight
    """

    targets = np.atleast_3d(targets)

    if names is None:
        names = [f"{i:04}" for i in range(targets.shape[2])]
    if isinstance(names, str):
        names = [names]
    assert targets.shape[:2] == (4, 4), 'Expecting array with shape (4, 4, N instrument marker).'

    if not fn_out.lower().endswith('.txt'):
        fn_out += '.txt'

    assert not os.path.exists(fn_out) or overwrite, '.txt file already exists. Remove or set overwrite=True.'

    with io.open(fn_out, 'w', newline='\n') as f:  # correct windows style would be \r\n, but Localite uses \n
        f.write('# Version: 12\n')
        f.write('# Coordinate system: NIfTI:Aligned\n')
        f.write('# Created by: pynibs\n')
        f.write('# Units: millimetres, degrees, milliseconds, and microvolts\n')
        f.write('# Encoding: UTF-8\n')
        f.write('# Notes: Each column is delimited by a tab. Each value within a column is delimited by a semicolon.\n')
        f.write('# Target Name	Loc. X	Loc. Y	Loc. Z	m0n0	m0n1	m0n2	m1n0	m1n1	m1n2	m2n0	m2n1	m2n2\n')

        for i_t in range(targets.shape[2]):
            f.write(f'{names[i_t]}\t' +
                    f'{targets[0, 3, i_t]:.4f}\t{targets[1, 3, i_t]:.4f}\t{targets[2, 3, i_t]:.4f}\t' +
                    f'{targets[0, 0, i_t]:.4f}\t{targets[1, 0, i_t]:.4f}\t{targets[2, 0, i_t]:.4f}\t' +
                    f'{targets[0, 1, i_t]:.4f}\t{targets[1, 1, i_t]:.4f}\t{targets[2, 1, i_t]:.4f}\t' +
                    f'{targets[0, 2, i_t]:.4f}\t{targets[1, 2, i_t]:.4f}\t{targets[2, 2, i_t]:.4f}\n')


def read_targets_brainsight(fn):
    """
    Reads target coil position and orientations from .txt file and returns it as 4 x 4 x N_targets numpy array.

    Parameters
    ----------
    fn : str
        Filename of output file.

    Returns
    -------
    m_nnav : ndarray of float [4 x 4 x N_targets]
        Tensor containing the 4x4 matrices with coil orientation and position.
    """
    with io.open(fn, 'r') as f:
        lines = f.readlines()
    start_idx = [i+1 for i, l in enumerate(lines) if l.startswith("# Target")][0]
    stop_idx = [i for i, l in enumerate(lines) if l.startswith("# Sample Name") or l.startswith("# Session Name")]

    if not stop_idx:
        stop_idx = len(lines)
    else:
        stop_idx = np.min(stop_idx)

    n_targets = stop_idx - start_idx
    names = ['' for _ in range(n_targets)]
    m_nnav = np.zeros((4, 4, n_targets))
    for i_loc, i_glo in enumerate(range(start_idx, stop_idx)):
        line = lines[i_glo].split(sep='\t')
        names[i_loc] = line[0]
        m_nnav[:3, 0, i_loc] = np.array(line[4:7]).astype(float)
        m_nnav[:3, 1, i_loc] = np.array(line[7:10]).astype(float)
        m_nnav[:3, 2, i_loc] = np.array(line[10:13]).astype(float)
        m_nnav[:3, 3, i_loc] = np.array(line[1:4]).astype(float)
        m_nnav[3, 3, i_loc] = 1