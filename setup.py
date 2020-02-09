"""
This is the setup file for Flight simulator Gyro Sensor
"""
from setuptools import setup, find_packages

GIT_URL = ('https://github.com/rb1811/Test/tree/master')

setup(name='flight-gyro-sensors',
      version='1.0.0',
      description='Its a library to read Gyro sensor',
      long_description="" + '\n\n' + "",
      url=GIT_URL,
      author='Aditya Karnam',
      author_email='akarnam@gmail.com',
      license='Open-Source',
      packages=find_packages(exclude=['tests', 'tests.*']),
      platforms=['unix', 'linux', 'osx', 'cygwin', 'win32'],
      install_requires=[
      ],
      classifiers=[
          'Development Status :: Beta',
          'Intended Audience :: For flight simulators',
          'Topic :: Software Development :: ',
          'Programming Language :: Python :: 2.7+'
      ],
      keywords="flight",
      python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
      include_package_data=True,
      zip_safe=False)
