"""
Package setup.py
"""

import os
from pathlib import Path
from setuptools import setup

about = {}

PACKAGE_NAME = "weltanschauung"

with open(str(Path(__file__).parent.absolute() / PACKAGE_NAME / 'version.py')) as fp:
    exec(fp.read(), about)

VERSION = about['VERSION']

def read_content(filepath):
    with open(filepath) as fobj:
        return fobj.read()


classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: Implementation :: CPython",

    "Natural Language :: English",
    'Operating System :: MacOS :: MacOS X',
    'Operating System :: Microsoft :: Windows :: Windows 7',
    'Operating System :: Microsoft :: Windows :: Windows 8',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'Operating System :: Unix',
    'Operating System :: POSIX :: Linux',

    'Topic :: Software Development :: Libraries :: Python Modules',
]


long_description = (
    read_content("README.rst") +
    #read_content(os.path.join("docs/source", "CHANGELOG.rst")) +
    ""
)

requirements = [
    'setuptools',
    "jinja2",
]

extras_require = {
}

setup(name=PACKAGE_NAME,
      version=VERSION,
      description="Utilities and tools to smooth around the development experience in Python and Jupyter. Scope creep encourag. Scope creep encouraged.",
      long_description=long_description,
      python_requires='>=3.7.0',
      author='Conrad Stansbury',
      author_email='chstansbury@gmail.com',
      url="#",
      classifiers=classifiers,
      packages=[PACKAGE_NAME],
      data_files=[],
      install_requires=requirements,
      include_package_data=True,
      extras_require=extras_require,
)