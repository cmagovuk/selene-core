from setuptools import setup, find_packages
from setuptools.command import easy_install

REQUIREMENTS = [
    "numpy",
    "selenium",
    "beautifulsoup4",
    "lxml",
    "ipython",
    "requests",
    "pyvirtualdisplay"
]

REQUIREMENTS_TEST = ["coverage", "interrogate", "pytest", "pytest-cov", "black"]

__version__ = "0.0.9"

setup(
    name="selene",
    version=__version__,
    packages=find_packages(),
    install_requires=REQUIREMENTS,
    tests_require=REQUIREMENTS + ["pytest", "pytest-runner"],
    extras_require={
        "tests": REQUIREMENTS_TEST
    },
    include_package_data=True
)
