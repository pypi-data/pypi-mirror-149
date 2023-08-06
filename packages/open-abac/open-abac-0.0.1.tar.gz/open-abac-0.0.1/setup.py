
from __future__ import absolute_import

import os
import setuptools
from setuptools import setup, find_packages
from distutils.version import LooseVersion

if LooseVersion(setuptools.__version__) < LooseVersion("20.5"):
    import sys
    sys.exit("Installation failed: Upgrade setuptools to version 20.5 or later")

base_dir = os.path.dirname(__file__)
about = {}
if base_dir:
    os.chdir(base_dir)
with open(os.path.join(base_dir, "open-abac", "__about__.py")) as f:
    exec(f.read(), about)

with open(os.path.join(base_dir, "README.md"), "r") as f:
    long_description = f.read()


setup(
    name=about["__title__"],
    version=about["__version__"],
    description=about["__summary__"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    license=about["__license__"],
    url=about["__uri__"],
    project_urls={
        "Bug Tracker": "https://github.com/mcode-cc/simple-abac/issues",
    },
    author=about["__author__"],
    author_email=about["__email__"],
    platforms=['Any'],
    install_requires=[],
    packages=find_packages(),
    include_package_data=True,
    data_files=[('.', ['LICENSE', 'COPYRIGHT'])],
    zip_safe=False,
    python_requires=">=3.7",
    classifiers=[
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Development Status :: %s" % about["__status__"],
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries",
        "Topic :: System :: Networking"
    ],
    keywords='ABAC Attribute Based Access Control'
)
