from setuptools import find_packages, setup

setup(
    name='Henson-Database',
    version='0.1.0',
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'SQLAlchemy>=1.0.2',
        'Henson',
    ],
    tests_require=[
        'tox',
    ],
)
