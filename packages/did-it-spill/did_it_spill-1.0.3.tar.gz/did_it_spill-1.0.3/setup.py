from setuptools import setup, find_packages
import pathlib

HERE = pathlib.Path(__file__).parent

VERSION = '1.0.3'
DESCRIPTION = 'Checks if you have data from train set in your test set'
LONG_DESCRIPTION = 'Checks if you have data from train set in your test set'

# Setting up
setup(
    name="did_it_spill",
    version=VERSION,
    author="LaihoE",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=['numpy', "torch", "torchvision"],
    include_package_data=True
)
