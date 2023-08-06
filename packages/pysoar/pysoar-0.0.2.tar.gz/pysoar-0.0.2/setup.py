from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Topic :: Scientific/Engineering :: Chemistry',
    'Topic :: Scientific/Engineering :: Physics',
    'Topic :: Scientific/Engineering',
    'Operating System :: OS Independent'
]

setup(
    name='pysoar',
    version='0.0.2',
    description='A data analysis tool for translocations in nanopores',
    url='https://github.com/VladimirIvanovImperial/PySOAR.git',
    author='Vladimir Ivanov',
    author_email='vi4018@ic.ac.uk',
    license='MIT',
    classifiers=classifiers,
    keywords='nanopore sensing, single molecule detection, signal processing, data analysis',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'scipy',
        'matplotlib',
        'ruptures'
    ]
)