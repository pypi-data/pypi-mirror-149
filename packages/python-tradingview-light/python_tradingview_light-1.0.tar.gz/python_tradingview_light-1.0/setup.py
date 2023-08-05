import pathlib
from setuptools import setup

HERE = pathlib.Path('tradingview-light.python_tradingview_light.py')

VERSION = '1.0'
PACKAGE_NAME = 'python_tradingview_light'
AUTHOR = 'Gabriel Beguerie'
AUTHOR_EMAIL = 'gabriel.arturo.beguerie@gmail.com'
URL = 'https://github.com/GaboBegue/python_tradingview_data_wrapper'

LICENSE = 'MIT'
DESCRIPTION = 'Library Technical Analysis Tradingview'

INSTALL_REQUIRES = [
      'requests'
      ]

setup(
    name='python_tradingview_light',
    version=1.0,
    description='Library Technical Analysis Tradingview',
    author='Gabriel Beguerie',
    author_email='gabriel.arturo.beguerie@gmail.com',
    url='https://github.com/GaboBegue/python_tradingview_data_wrapper',
    install_requires='requests',
    license='MIT',
    include_package_data=True
)