
News
====
**2 May 2022** - Release 0.2.4 with several updates and improvements (see [changelog](https://fpdpy.gitlab.io/fpd/changelog.html) for details).

**26 February 2022** - Release 0.2.3 with several updates and improvements (see [changelog](https://fpdpy.gitlab.io/fpd/changelog.html) for details).

**29 November 2021** - Release 0.2.2 with several updates and improvements (see [changelog](https://fpdpy.gitlab.io/fpd/changelog.html) for details).

**19 October 2021** - Release 0.2.1 with several updates and improvements (see [changelog](https://fpdpy.gitlab.io/fpd/changelog.html) for details).

**20 September 2021** - Publication of a diptych on **Parallel mode differential phase contrast in transmission electron microscopy**: Part I [Microsc. Microanal. 27, 1113 (2021)](https://doi.org/10.1017/S1431927621012551), Part II [Microsc. Microanal. 27, 1123 (2021)](https://www.doi.org/10.1017/S1431927621012575).

See https://fpdpy.gitlab.io/fpd/news.html for earlier news.


FPD package
===========
The fpd package provides code for the storage, analysis and visualisation
of data from fast pixelated detectors. The data storage uses the hdf5 based 
EMD file format, and the conversion currently supports the Merlin readout from 
Medipix3 detectors. Differential phase contrast imaging and several other common
data analyses, like radial distributions, virtual apertures, and lattice analysis,
are also implemented, along with many utilities and general electron microscopy
related tools. Some scientific papers about these can be found below. 

The package is relatively lightweight, with most of its few dependencies being
standard scientific libraries. All calculations run on CPUs and many use 
out-of-core processing, allowing data to be visualised and processed on anything
from very modest to powerful hardware.

A degree of optimisation through parallelisation has been implemented, with most
functions using threads. If you need to use process-based parallelism and are on
Windows 10, then you may find the Linux subsystem of benefit.


Citing
------
If you find this software useful and use it to produce results in a 
puplication, please consider citing the website or related paper(s).

An example bibtex entry with the date in the note field yet to be specified:

```
@Misc{fpd,
    Title                    = {{FPD: Fast pixelated detector data storage, analysis and visualisation}},
    howpublished             = {\url{https://gitlab.com/fpdpy/fpd}},
    note                     = {{Accessed} todays date}
}
```

Aspects of the library are covered in papers:

- Fast Pixelated Detectors in Scanning Transmission Electron Microscopy. Part I: Data Acquisition, Live Processing and Storage,\
[arXiv (2019)](https://arxiv.org/abs/1911.11560), [Microsc. Microanal. 26, 653 (2020)](https://doi.org/10.1017/S1431927620001713).
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3479124.svg)](https://doi.org/10.5281/zenodo.3479124)

- Fast Pixelated Detectors in Scanning Transmission Electron Microscopy. Part II: Post Acquisition Data Processing, Visualisation, and Structural Characterisation,\
[Microsc. Microanal. 26, 944 (2020)](https://doi.org/10.1017/S1431927620024307), [arXiv (2020)](https://arxiv.org/abs/2004.02777).
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3903517.svg)](https://doi.org/10.5281/zenodo.3903517)

- Parallel mode differential phase contrast in transmission electron microscopy, I: Theory and analysis,\
[Microsc. Microanal. 27, 1113 (2021)](https://doi.org/10.1017/S1431927621012551), [arXiv (2021)](https://arxiv.org/abs/2104.06769).

- Parallel mode differential phase contrast in transmission electron microscopy, II: K2CuF4 phase transition,\
[Microsc. Microanal. 27, 1123 (2021)](https://doi.org/10.1017/S1431927621012575), [arXiv (2021)](https://arxiv.org/abs/2107.06280).


Publications
------------
Some of the known scientific papers that used the fpd library are listed below.
If you use the library for results contributing to a publication, please pass
the paper details to developers for inclusion in this list.

- Engineering of Fe-pnictide heterointerfaces by electrostatic principles,\
[NPG Asia Materials 13, 67 (2021)](https://doi.org/10.1038/s41427-021-00336-6), [arXiv (2020)](https://arxiv.org/abs/2009.04799).

- Parallel mode differential phase contrast in transmission electron microscopy, I: Theory and analysis,\
[Microsc. Microanal. 27, 1113 (2021)](https://doi.org/10.1017/S1431927621012551), [arXiv (2021)](https://arxiv.org/abs/2104.06769).

- Parallel mode differential phase contrast in transmission electron microscopy, II: K2CuF4 phase transition,\
[Microsc. Microanal. 27, 1123 (2021)](https://doi.org/10.1017/S1431927621012575), [arXiv (2021)](https://arxiv.org/abs/2107.06280).

- Structural and Morphological Characterization of Novel Organic Electrochemical Transistors via Four-dimensional (4D) Scanning Transmission Electron Microscopy,\
[Microsc. Microanal. 27(S1), 1792-1794 (2021)](https://www.doi.org/10.1017/S1431927621006553).

- Formations of narrow stripes and vortex-antivortex pairs in a quasi-two-dimensional ferromagnet K2CuF4,\
[J. Phys. Soc. Jpn. 90, 014702 (2021)](https://doi.org/10.7566/JPSJ.90.014702), [Enlighten: Publications (2020)](http://eprints.gla.ac.uk/224185/).

- Correlative chemical and structural nanocharacterization of a pseudo-binary 0.75Bi(Fe0.97Ti0.03)O3-0.25BaTiO3 ceramic,\
[J. Am. Ceram. Soc. 104, 2388 (2021)](https://doi.org/10.1111/jace.17599), [arXiv (2020)](https://arxiv.org/abs/2010.10975).

- Fast Pixelated Detectors in Scanning Transmission Electron Microscopy. Part II: Post Acquisition Data Processing, Visualisation, and Structural Characterisation,\
[Microsc. Microanal. 26, 944 (2020)](https://doi.org/10.1017/S1431927620024307), [arXiv (2020)](https://arxiv.org/abs/2004.02777).

- Fast Pixelated Detectors in Scanning Transmission Electron Microscopy. Part I: Data Acquisition, Live Processing and Storage,\
[arXiv (2019)](https://arxiv.org/abs/1911.11560), [Microsc. Microanal. 26, 653 (2020)](https://doi.org/10.1017/S1431927620001713).

- Spontaneous creation and annihilation dynamics and strain-limited stability of magnetic skyrmions,\
[arXiv (2019)](https://arxiv.org/abs/1911.10094), [Nat. Commun. 11, 3536 (2020)](https://doi.org/10.1038/s41467-020-17338-7).

- Tensile deformations of the magnetic chiral soliton lattice probed by Lorentz transmission electron microscopy,\
[arXiv (2019)](https://arxiv.org/abs/1911.09634), [Phys. Rev. B 101, 184424 (2020)](https://dx.doi.org/10.1103/PhysRevB.101.184424).

- Sub-100 nanosecond temporally resolved imaging with the Medipix3 direct electron detector,\
[arXiv (2019)](https://arxiv.org/abs/1905.11884), [Ultramicroscopy, 210, 112917 (2020)](https://doi.org/10.1016/j.ultramic.2019.112917).

- Strain Anisotropy and Magnetic Domains in Embedded Nanomagnets,\
[Small, 1904738 (2019)](https://doi.org/10.1002/smll.201904738).

- Heisenberg pseudo-exchange and emergent anisotropies in field-driven pinwheel artificial spin ice,\
[arXiv (2019)](https://arxiv.org/abs/1908.10626), [Phys. Rev. B 100, 174410 (2019)](https://doi.org/10.1103/PhysRevB.100.174410).

- Order and disorder in the magnetization of the chiral crystal CrNb3S6,\
[arXiv (2019)](https://arxiv.org/abs/1903.09519), [Phys. Rev. B 99, 224429 (2019)](https://doi.org/10.1103/PhysRevB.99.224429).


Installation
------------
The package currently supports python version 3.x (2.x support was dropped in v0.1.12).
Hyperspy is used for reading Digital Micrograph files in a few places, but virtually all
of the fpd package can be used without it being installed (simply install the package
dependencies manually and ignore them when using pip by adding ``--no-deps`` to the install
command).

Installation from source:

```bash
pip3 install --user .
```

Instalation from PyPI (https://pypi.org/project/fpd/):

```bash
pip3 install --user fpd
```

``-U`` can be added to force an upgrade / reinstall; in combination with ``--no-deps``,
only the ``fpd`` package will be reinstalled.

The package can be removed with:

```bash
pip3 uninstall fpd
```


Usage
-----
In python or ipython:

```python
import fpd
d = fpd.DPC_Explorer(-64)
```

```python
import fpd.fpd_processing as fpdp
rtn = fpdp.phase_correlation(data, 32, 32)
```
where `data` is any array-like object. For example, this can be an in-memory 
numpy array, an hdf5 object on disk, or a dask array, such as that used in 
'lazy' hyperspy signals.

All functions and classes are documented and can be read, for example, in `ipython`
by appending a `?` to the object. E.g.:

```python
import fpd
fpd.DPC_Explorer?
```

Documentation
-------------
Release: https://fpdpy.gitlab.io/fpd/

Development version: https://gitlab.com/fpdpy/fpd/builds/artifacts/master/file/pages_development/index.html?job=pages_development

Notebook demos: https://gitlab.com/fpdpy/fpd-demos.

Further documentation and examples will be made available over time.


Related projects
----------------

https://www.gla.ac.uk/schools/physics/research/groups/mcmp/researchareas/pixstem/

http://quantumdetectors.com/stem/

https://gitlab.com/fast_pixelated_detectors/merlin_interface

https://gitlab.com/fast_pixelated_detectors/fpd_live_imaging

https://gitlab.com/pixstem/pixstem

https://emdatasets.com/format

http://hyperspy.org/

http://gwyddion.net/

More packages will be added to the https://gitlab.com/fast_pixelated_detectors
group as they develop.


Coverage
--------
[master coverage](https://gitlab.com/fpdpy/fpd/builds/artifacts/master/file/coverage.txt?job=test:p3)


