from distutils.core import setup

import pandas

setup(
    # Application name:
    name="degiro2pp",

    # Version number (initial):
    version="0.0.1",

    # Application author details:
    author="Timo Koole",

    # Packages
    packages=["degiro2pp"],

    # Include additional files into the package
    # include_package_data=True,

    # Details
    # url="http://pypi.python.org/pypi/MyApplication_v010/",

    #
    # license="LICENSE.txt",
    description="Application to convert Degiro files to PortfolioPerformance",

    # long_description=open("README.txt").read(),

    # Dependent packages (distributions)
    install_requires=['pandas', 'currencyconverter']
)
