from setuptools import setup, find_packages
from setuptools.dist import Distribution

class BinaryDistribution(Distribution):
    def is_pure(self):
        return False

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()
		
setup(name='cardies',
      version='0.0.3',
      url='https://github.com/iosonobert/cardies/',
      description='The Cardinals',
      author='Stanley Din',
      packages=find_packages(),
      install_requires=['numpy','matplotlib', 'xarray', 'netCDF4', 'Proj'],
      license='unlicensed to all but author',
      include_package_data=True,
      long_description=long_description,
      long_description_content_type='text/markdown',
      distclass=BinaryDistribution,
    )
