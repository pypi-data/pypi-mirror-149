import codecs
import os
import re

from setuptools import find_packages, setup

NAME = "political_ml"
META_PATH = os.path.join("src", NAME, "__meta__.py")
TESTS_REQUIRE = [
    "pytest>=6.2.5",
    "coverage==5.5",
]
DEV_REQUIRE = TESTS_REQUIRE + [
    "pre-commit==2.12.0",
    "twine~=3.4",
    "build~=0.7",
]

ABOUT = {
    "name": NAME,
    "description": "An API wrapper for a set of API's related to NLP.",
    "url": "https://github.com/wepublic-nl",
    "author": "Wepublic",
    "email": "stakeholderintel@wepublic.nl",
    "license": "Other/Proprietary License",
    "copyright": "All rights reserved",
}


with open("README.md", "r", encoding="utf-8") as fh:
    ABOUT["long_description"] = fh.read()
    ABOUT["long_description_content_type"] = "text/markdown"


HERE = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    """
    Build an absolute path from *parts* and return the contents of the
    resulting file.  Assume UTF-8 encoding.
    """
    with codecs.open(os.path.join(HERE, *parts), "rb", "utf-8") as f:
        return f.read()


META_FILE = read(META_PATH)


def find_meta(meta):
    """
    Extract __*meta*__ from META_FILE.
    """
    meta_match = re.search(
        r"^__{meta}__ = ['\"]([^'\"]*)['\"]".format(meta=meta), META_FILE, re.M
    )
    if meta_match:
        return meta_match.group(1)
    raise RuntimeError("Unable to find __{meta}__ string.".format(meta=meta))


setup(
    **ABOUT,
    version=find_meta("version"),
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">= 3.8",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    install_requires=[
        "requests>=2.25.1",
    ],
    extras_require={"test": TESTS_REQUIRE, "dev": DEV_REQUIRE},
    project_urls={
        "Source": "https://github.com/wepublic-nl/" + NAME,
    },
)
