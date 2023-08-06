[![Documentation Status](https://readthedocs.org/projects/phasik/badge/)](http://phasik.readthedocs.io/)
[![PyPI version](https://badge.fury.io/py/phasik.svg)](https://badge.fury.io/py/phasik)
[![PyPI license](https://img.shields.io/pypi/l/phasik.svg)](https://pypi.python.org/pypi/phasik/)
[![Downloads](https://static.pepy.tech/personalized-badge/phasik?period=total&units=international_system&left_color=grey&right_color=green&left_text=Downloads)](https://pepy.tech/project/phasik)

# Code for the paper: "Inferring cell cycle phases from a temporal network of protein interactions"

Phasik was initially created for the analysis presented in the paper "[Inferring cell cycle phases from a partially temporal network of protein interactions](https://doi.org/10.1101/2021.03.26.437187)" by Lucas, M., Morris, A., Townsend-Teague, A., Tichit, L., Habermann, B. H., & Barrat, A. (2021), bioRxiv.

The code contains
- Phasik, our general-use package to infer phases in temporal networks
- the notebooks use in our analysis for the paper, which uses Phasik

Contributors to Phasik: Maxime Lucas, Alex Townsend-Teague, Arthur Morris

Code on Gitlab: [https://gitlab.com/habermann_lab/phasik](https://gitlab.com/habermann_lab/phasik)

**New release: in version 1.x.x, we now have our own classes for temporal networks and partially temporal networks. No more dependency to others**

#### What is Phasik?
The Phasik package was created to infer temporal phases in temporal networks.  It contains various utility classes and functions that can be divided into two main parts:

1. Build, analyse, and visualise temporal networks from time series data.
2. Infer temporal phases by clustering the snapshots of the temporal network.

### Install Phasik 

Install the latest version of `phasik` with `pip`:

```
$ pip install phasik
```

Alternatively, you can clone the repository manually or with `git`, go to the repository and then install locally with `pip`:
```    
$ pip install .
```   

### Documentation

The full documentation of the package is available at <https://phasik.readthedocs.io/en/latest/>, together with tutorials.

### Contact

ml.maximelucas[at]gmail[dot]com
