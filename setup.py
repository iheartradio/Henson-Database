from setuptools import find_packages, setup

setup(
    name='ingestion.database',
    version='0.1.0',
    namespace_packages=['ingestion'],
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'ingestion.service>=0.3.0',
        'setuptools',
        'SQLAlchemy>=1.0.2',
    ],
    tests_require=[
        'tox',
    ],
)
