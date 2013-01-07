"""
smear
-----

an open source toolkit for spatial interpolation of large irregular two-dimensional scatter datasets
"""

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import sys


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


setup(
    name='smear',
    version='0.1.1-dev',
    license='BSD',
    author='Dharhas Pothina',
    author_email='dharhas@gmail.com',
    description='spatial interpolation of large irregular two-dimensional scatter datasets',
    long_description=__doc__,
    keywords='GIS spatial interpolation bathymetry hydrographic survey scatter datasets',
    packages=find_packages(),
    platforms='any',
    install_requires=[
        'numpy>=1.4.0',
        'pyproj',
        'requests',
        'scipy>=0.9',
        'shapely',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    tests_require=[
        'pytest>=2.3.2',
    ],
    cmdclass={'test': PyTest},
)