import setuptools
from numpy.distutils.core import setup
from numpy.distutils.misc_util import Configuration
from distutils.command.sdist import sdist
from sphinx.setup_command import BuildDoc
cmdclass = {'build_sphinx': BuildDoc}

PACKAGE_NAME = 'teklib'
config = Configuration(PACKAGE_NAME)

with open("README.md", "r") as fh:
    long_description = fh.read()

#setuptools.setup(
setup(
    **config.todict(),
    version="1.0.3",
    author="Tim Kendon",
    author_email="timothy.edward.kendon@gmail.com",
    description="Library of tools for the analysis of marine technology",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Timothy-Edward-Kendon/teklib",
    packages=setuptools.find_packages(where="src"),
    package_dir={'': 'src',},
    cmdclass=cmdclass,
    ext_modules = [],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=["numpy", "matplotlib", "scipy", "freesif"]
)