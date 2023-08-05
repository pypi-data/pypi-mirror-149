from setuptools import setup, find_packages

VERSION = '0.0.2'

setup(name='notifyurl',
      version=VERSION,
      description="a command line tool to notify via webhook",
      long_description='a command line tool to notify via webhook',
      classifiers=[],  # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='notify',
      author='Yuchen Wu',
      author_email='Curiosity_Wu@outlook.com',
      license='MIT',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=True,
      install_requires=[],
      entry_points={
          'console_scripts': [
              'notify = notifyurl.notify:main'
          ]
      }
      )
