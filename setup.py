from setuptools import setup, find_packages

setup(
    name='hornet',
    packages=['hornet'],
    package_dir={'':'src'},
    version='1.0.0',
    url='git@github.com/PNAI-CSB-NCI-NIH/HORNET.git',
    description='HORNET is a python open-source library for estimating the RNA RMSD based on energies and global constraints.',
    install_requires=[
        "numpy == 1.22.3", "pandas == 1.5.3", "scikit-learn == 1.2.1",
        "scipy == 1.9.1", "seaborn == 0.12.2", "tensorflow == 2.13",
        "pytest == 7.4.2"],
)