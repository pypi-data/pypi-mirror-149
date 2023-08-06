from gettext import install
from setuptools import setup

setup(
    name = 'ABCDanalysis',
    version = '0.0.1',
    description= 'analysis the ABCD dataset to predict mental health issue',
    py_modules=['ABCDanalysis'],
    package_dir={'':'src'},


    install_requires = ["Pandas"]
)
