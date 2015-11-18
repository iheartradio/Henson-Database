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
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ]
)
