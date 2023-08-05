import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

__version__ = "0.1.1"

# This call to setup() does all the work
setup(
    name="4996",
    version=__version__,
    description="Nothing to see here.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/theoldfather/time-series",
    author="Jeremy Oldfather",
    author_email="contact@jeremyoldfather.com",
    license="Apache",
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    package_dir={"": "src"},
    packages=find_packages("src"),
    include_package_data=False,
    install_requires=[
        "torch==1.10.1",
        "pandas",
        "numpy"
    ],
)
