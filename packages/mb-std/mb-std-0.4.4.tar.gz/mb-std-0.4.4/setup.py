import codecs
import os
import re

import setuptools


def find_version(*file_paths):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, *file_paths), "r") as fp:
        version_file = fp.read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setuptools.setup(
    name="mb-std",
    version=find_version("mb_std/__init__.py"),
    packages=setuptools.find_packages(exclude=["tests", "tests.*"]),
    install_requires=[
        "requests==2.27.1",
        "PySocks==1.7.1",
        "sorcery==0.2.2",
        "pydash==5.1.0",
        "wrapt==1.14.1",
        "python-dateutil==2.8.2",
        "pymongo==4.1.1",
        "pydantic==1.9.0",
        "python-dotenv==0.20.0",
    ],
    extras_require={
        "dev": [
            "pytest==7.1.2",
            "pre-commit==2.18.1",
            "pytest-xdist==2.5.0",
            "wheel==0.37.1",
            "twine==4.0.0",
            "pip-audit==2.1.1",
        ],
    },
)
