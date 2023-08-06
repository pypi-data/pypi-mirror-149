from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Utilities for Password Management'

setup(
    name='passwordUtils',
    version=VERSION,
    author='Olliejohnson',
    author_email='oliver.joseph.johnson@gmail.com',
    description=DESCRIPTION,
    long_description=DESCRIPTION,
    packages=find_packages(),
    install_requires = [],

    keywords=['python', 'first package'],
    classifiers= [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)