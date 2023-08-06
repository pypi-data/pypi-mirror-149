#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages
import versioneer

requirements = [
    'numpy', 'exdir>=0.4.2', 'cclib>=1.7.0', 'scipy'
]

setup_requirements = ['versioneer']

test_requirements = requirements.append(['pytest', 'pytest-order'])

setup(
    install_requires=requirements,
    extras_require={},
    include_package_data=True,
    package_data={'': ['definitions/*.yaml']},
    packages=find_packages(include=['reptar', 'reptar.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    zip_safe=False,
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
)
