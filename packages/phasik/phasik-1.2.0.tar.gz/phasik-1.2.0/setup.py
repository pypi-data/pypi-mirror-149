from setuptools import find_packages, setup

requirements = [
    "networkx>=2.4",
    "numpy>=1.18.1",
    "pandas>=1.0.5",
    "matplotlib>=3.1.1",
    "seaborn>=0.11.0",
    "scikit-learn>=0.21.3",
    "scipy>=1.4.1",
]

VERSION_FILE = "phasik/_version.py"
with open(VERSION_FILE, "rt") as f:
    version_txt = f.read().strip()
    VERSION = version_txt.split('"')[1]

setup(
    name="phasik",
    version=VERSION,
    author="Maxime Lucas",
    author_email="ml.maximelucas@gmail.com",
    description="Tools to build temporal networks and infer temporal phases from them",
    long_description="Tools to build temporal networks and infer temporal phases from them. Build temporal networks from time series data. Cluster snapshots to infer the multiscale temporal organisation of the network.",
    url="https://gitlab.com/habermann_lab/phasik",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)
