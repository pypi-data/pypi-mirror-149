import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


readme = read('README.rst')
changelog = read('CHANGELOG.rst')

setup(name='cryptosyspki',
      version='20.4.0',
      description='Python interface to CryptoSys PKI (py 3)',
      long_description=readme + '\n\n' + changelog,
      author='David Ireland',
      url='https://www.cryptosys.net/pki/',
      platforms=['Windows'],
      py_modules=['cryptosyspki'],
      license='See source code modules'
      )
