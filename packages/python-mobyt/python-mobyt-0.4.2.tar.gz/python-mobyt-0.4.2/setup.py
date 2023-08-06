from setuptools import setup

setup(name='python-mobyt',
      version='0.4.2',
      description='Mobyt API Client',
      url='https://bitbucket.org/metadonors/python-mobyt',
      author='Metadonors',
      author_email='fabrizio.arzeni@metadonors.it',
      license='MIT',
      packages=['pymobyt'],
      install_requires=[
          'requests',
      ],
      zip_safe=False)