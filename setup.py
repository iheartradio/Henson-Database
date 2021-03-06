from setuptools import find_packages, setup
from setuptools.command.test import test as TestCommand
import sys


class PyTest(TestCommand):
    def finalize_options(self):
        super().finalize_options()
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        sys.exit(pytest.main(self.test_args))


def read(filename):
    with open(filename) as f:
        return f.read()

setup(
    name='Henson-Database',
    version='0.5.0',
    author='Andy Dirnberger, Jon Banafato, Leonard Bedner, and others',
    author_email='henson@iheart.com',
    url='https://henson-database.readthedocs.io',
    description='A library for using SQLAlchemy with a Henson application',
    long_description=read('README.rst'),
    license='Apache License, Version 2.0',
    packages=find_packages(exclude=['tests']),
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        # 1.1 is required to extend the CLI.
        'Henson>=1.1',
        'SQLAlchemy>=1.0.2',
    ],
    extras_require={
        'migrations': [
            'alembic',
        ],
    },
    tests_require=[
        'pytest',
    ],
    cmdclass={
        'test': PyTest,
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ]
)
