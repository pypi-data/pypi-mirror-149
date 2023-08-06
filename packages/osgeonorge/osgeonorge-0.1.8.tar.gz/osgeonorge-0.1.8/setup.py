# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='osgeonorge',
    version='0.1.8',
    description='Tools and functions for interacting with geonorge.no',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://gitlab.com/ninsbl/osgeonorge',
    author='Stefan Blumentrath',
    author_email='stefan.blumentrath@nina.no',
    license="GPL >= 3",
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Natural Language :: English',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3.6'
    ],
    keywords='geonorge osgeo gdal postgis sosi fyba etl elt',
    packages=find_packages(exclude=['docs', 'tests']),
    install_requires=["requests", "psycopg2", "GDAL"],
    setup_requires=['pytest-runner', 'setuptools'],  # >38.6.0 needed for markdown README.md
    tests_require=['pytest', 'pytest-cov', "requests", "psycopg2", "GDAL"],
    entry_points={
        'console_scripts': [
            'list_atom=osgeonorge.__main__:main'
        ]
    }
)
