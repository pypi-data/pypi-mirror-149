# pyNIBS
Preprocessing, postprocessing, and analyses routines for non-invasive brain stimulation experiments.

[![Latest Release](https://gitlab.gwdg.de/tms-localization/pynibs/-/badges/release.svg)](https://gitlab.gwdg.de/tms-localization/pynibs/-/releases)   

`pyNIBS` provides the necessary tools to allow **cortical mappings** with transcranial magnetic stimulation (TMS) via **functional analysis**. `pyNIBS` is developed to work with [SimNIBS](http://www.simnibs.org), i.e. SimNIBS' meshes and FEM results can directly be used.


See the [documentation](https://pynibs.readthedocs.io/en/latest/) for package details and our [protocol](https://protocolexchange.researchsquare.com/article/pex-1780/v1) publication for an extensive example of the usage.

## Installation
Via pip:

``` bash
pip install pynibs
```

You might need to manually compile the libbiosig package:

``` bash
cd pynibs/pckg/biosig
tar -xvf biosig4c++-1.9.5.src_fixed.tar.gz
cd biosig4c++-1.9.5
./configure
make
cd python
python setup.py install
```

Finally, add :~/.local/lib to your .bashrc:
```
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:~/.local/lib
```


Or clone the source repository and install via `setup.py`:

``` bash
git clone https://gitlab.gwdg.de/tms-localization/pynibs
cd pynibs
python setup.py develop
```

## Bugs
Yes. Drop us a line if you find any or feel free to file a PR.
