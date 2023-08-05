from setuptools import setup
from setuptools.command.develop import develop
from setuptools.command.install import install
from subprocess import check_call
import subprocess
import os
from pathlib import Path
import sys


def compile_and_install_software():
    try:
        import sysconfig
        import tarfile

        site_packages = sysconfig.get_paths()["purelib"]
        """Used the subprocess module to compile/install the C software."""
        src_path = os.path.join(site_packages,'pynibs','pckg','biosig')
        print(f"Extracting libbiosig to {src_path}.")
        tar_fn = 'biosig4c++-1.9.5.src_fixed.tar.gz'

        my_tar = tarfile.open(os.path.join(src_path,tar_fn))
        my_tar.extractall(src_path)  # specify which folder to extract to
        my_tar.close()

        print("Compiling libbiosig")
        subprocess.check_call('./configure',
                              cwd=os.path.join(src_path,'biosig4c++-1.9.5'), shell=True)
        subprocess.check_call('make',
                              cwd=os.path.join(src_path,"biosig4c++-1.9.5"), shell=True)

        print("Installing libbiosig")
        subprocess.check_call(f"{sys.executable} setup.py install",
                              cwd=os.path.join(src_path,"biosig4c++-1.9.5","python"), shell=True)

    except:
        print("Cannot compile/install biosig, do manually if needed.")
        return

class PostDevelopCommand(develop):
    """Post-installation for development mode."""

    def run(self):
        develop.run(self)
        try:
            import sysconfig
            import tarfile

            site_packages = os.path.dirname(os.path.abspath(__file__))
            """Used the subprocess module to compile/install the C software."""
            src_path = os.path.join(site_packages, 'pynibs', 'pckg', 'biosig')
            print(f"Extracting libbiosig to {src_path}.")
            tar_fn = 'biosig4c++-1.9.5.src_fixed.tar.gz'

            my_tar = tarfile.open(os.path.join(src_path, tar_fn))
            my_tar.extractall(src_path)  # specify which folder to extract to
            my_tar.close()

            print("Compiling libbiosig")
            subprocess.check_call('./configure',
                                  cwd=os.path.join(src_path, 'biosig4c++-1.9.5'), shell=True)
            subprocess.check_call('make',
                                  cwd=os.path.join(src_path, "biosig4c++-1.9.5"), shell=True)

            print("Installing libbiosig")
            subprocess.check_call(f"{sys.executable} setup.py install",
                                  cwd=os.path.join(src_path, "biosig4c++-1.9.5", "python"), shell=True)

        except:
            print("Cannot compile/install biosig, do manually if needed.")
            return

class PostInstallCommand(install):
    """Post-installation for installation mode."""

    def run(self):
        # check_call(f"{sys.path[0]}{os.sep}postinstall{os.sep}install.py")
        install.run(self)
        compile_and_install_software()


this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(name='pynibs',
      version='0.1.5a',
      description='A python toolbox to conduct non-invasive brain stimulation experiments (NIBS).',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author='Konstantin Weise, Ole Numssen',
      author_email='kweise@cbs.mpg.de',
      package_data={'pynibs.pckg': ['biosig/biosig4c++-1.9.5.src_fixed.tar.gz']},
      keywords=['NIBS', 'non-invasive brain stimulation', 'TMS', 'FEM'],
      include_package_data=True,
      project_urls={'Home': 'https://gitlab.gwdg.de/tms-localization/pynibs',
                    'Docs': 'https://pynibs.readthedocs.io/',
                    'Download': 'https://pypi.org/project/pynibs/'},

      license='GPL3',
      packages=['pynibs',
                'pynibs.exp',
                'pynibs.models',
                'pynibs.util',
                'pynibs.pckg'],
      # requires=['tvb-gdist'],
      install_requires=['dill',
                        'h5py',
                        'lmfit',
                        'matplotlib',
                        'numpy',
                        'nibabel',
                        'pandas',
                        'pygpc',
                        'pyyaml',
                        'scipy',
                        'scikit-learn',
                        'packaging',
                        'lxml',
                        'tables',
                        'tqdm',
                        'pillow',
                        'fslpy',
                        'mkl',
                        'trimesh',
                        'fmm3dpy',
                        'tvb-gdist',
                        'ortools<=9.1.9490'],
      classifiers=['Development Status :: 3 - Alpha',
                   'Intended Audience :: Science/Research',
                   'Topic :: Scientific/Engineering',
                   'Topic :: Software Development :: Build Tools',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.6',
                   'Programming Language :: Python :: 3.7',
                   'Programming Language :: Python :: 3.8',
                   'Programming Language :: Python :: 3.9', ],

      zip_safe=False,
      cmdclass={
          'develop': PostDevelopCommand,
          'install': PostInstallCommand,
      }, )
