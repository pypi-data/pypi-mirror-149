from setuptools import setup, find_packages
from setuptools.dist import Distribution

class BinaryDistribution(Distribution):
    def is_pure(self):
        return False

		
setup(name='cardies',
      version='0.0.2',
      url='https://github.com/iosonobert/cardies/',
      description='The Cardinals',
      author='Stanley Din',
      packages=find_packages(),
      install_requires=['numpy','matplotlib', 'xarray', 'netCDF4', 'Proj'],
      license='unlicensed to all but author',
      include_package_data=True,
      distclass=BinaryDistribution,
    )
