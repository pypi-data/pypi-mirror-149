from setuptools import setup
import codecs
import os
import re


# parse version from init
# from: https://github.com/pypa/pip/blob/master/setup.py
here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    # intentionally *not* adding an encoding option to open, See:
    #   https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    with codecs.open(os.path.join(here, *parts), 'r') as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='fpd',
      version=find_version("fpd", "__init__.py"),
      description='FPD: Fast pixelated detector data storage, analysis and visualisation.',
      long_description=long_description,
      long_description_content_type="text/markdown",
      classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Physics',
      ],
      keywords=[
          'microscopy',
          'STEM',
          'TEM',
          'fast pixelated detector',
          'fpd',
          'data storage',
          'EMD',
          'hdf5',
          'data analysis',
          'differential phase contrast',
          'DPC',
          'segmented DPC',
          'pixelated DPC',
          'virtual detector',
          'lattice analyis',
          'strain analysis',
          'non-rigid image alignment',
      ],
      url='http://gitlab.com/fpdpy/fpd',
      author='Gary Paterson',
      author_email='dr.gary.paterson@gmail.com',
      license='GPL v3',
      packages=['fpd'],
      package_data={'fpd': ['perceptually_uniform_cmap.npy']},
      install_requires=[
          'numpy',
          'scipy',
          'scikit-image',
          'matplotlib',
          'h5py>=2.10.0',
          'tqdm',
          'hyperspy',
          'threadpoolctl',
          'hdf5plugin',
      ],
      include_package_data=True,
      zip_safe=True)
