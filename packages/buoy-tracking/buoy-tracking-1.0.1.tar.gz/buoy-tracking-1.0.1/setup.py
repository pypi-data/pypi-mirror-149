from setuptools import setup, find_packages

setup(name='buoy-tracking', version='1.0.1',
      url='https://github.com/wrightni/buoy_tracking',
      author='Nicholas Wright',
      install_requires=['numpy', 'pandas', 'requests', 'scikit-learn',
                        'pyproj', 'scipy', 'netCDF4', 'lxml'],
      include_package_data=True,
      package_data={'': ['static/buoy_staticvars.json',
                         'static/active_buoys.json'],
                    },
      packages=find_packages())