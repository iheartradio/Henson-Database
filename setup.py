from setuptools import find_packages, setup

setup(
    name='Henson-Database',
    version='0.3.0',
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'Henson>=0.2.0',
        'SQLAlchemy>=1.0.2',
    ],
    tests_require=[
        'tox',
    ],
)
