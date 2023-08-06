import pathlib
from setuptools import setup
from setuptools import find_packages

# the difectory contaning this file
HERE = pathlib.Path(__file__).parent

# the text of the README file
README = (HERE / "README.md").read_text()

# setup
setup(
    name = "chela",
    version = "1.0.5",
    description = "Library for handling chemical formulas",
    long_description = README,
    long_description_content_type = "text/markdown",
    url = "https://github.com/ClaudioPereti/chela",
    author = "Claudio Pereti",
    license = 'MIT',
    classifiers = [
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
    packages = find_packages(exclude=("tests",)),
    include_package_data = True,
    install_requires = [
        'pandas',
        'numpy',
    ],
    entry_points = {
        "console_scripts":[
            "chela= chela.__main__:main"
        ]
    },
)
