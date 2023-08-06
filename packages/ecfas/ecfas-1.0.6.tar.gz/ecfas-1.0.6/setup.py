from __future__ import absolute_import
from setuptools import setup, find_packages
from os import path

_dir = path.abspath(path.dirname(__file__))

with open(path.join(_dir, 'ecfas', 'version.py')) as f:
  exec(f.read())

with open(path.join(_dir, 'README.md')) as f:
  long_description = f.read()

setup(name='ecfas',
  version=__version__,
  long_description=long_description,
  long_description_content_type='text/markdown',
  url='https://gitlab.mercator-ocean.fr/mirazoki/ecfas',
  author='Maialen Irazoki',
  author_email='mirazoki@mercator-ocean.fr',
  license='BSD Licence',
  packages=find_packages(exclude=["test", "functional_test"]),
  package_data={
    'ecfas': ['output_points/*.txt', 'fes/*ini'],
  },

  project_urls={
    'Repository': 'https://gitlab.mercator-ocean.fr/mirazoki/ecfas',
  },

  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Science/Research',
    'Topic :: Scientific/Engineering',
    'Environment :: Console',
    'Programming Language :: Python :: 3.8',
    'License :: OSI Approved :: BSD License',
  ],

  install_requires=[
        'cartopy==0.18.0',
        'dask==2021.9.1',
        'matplotlib==3.3.3',
        'scipy==1.5.3',
        'netcdf4==1.5.3',
        'motuclient==1.8.8',
        'configobj==5.0.6'
  ],

  setup_requires=['flake8'],
  tests_require=['pytest', 'pytest_cov'],
  python_requires='>3.8,<3.9',
)
