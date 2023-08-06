import setuptools


setuptools.setup(
      # package metadata
      name='honeycomb_maze',
      version='0.1.01',
      description='Python Implementation of Honeycomb Maze',
      long_description='To be filled in',
      long_description_content_type="text/markdown",

      #
      license='MIT',
      packages=setuptools.find_packages(),
      zip_safe=False,

      # source metadata:
      url='https://github.com/casualcoffeeaddict/Honeycomb-Maze',
      author='Alif Ul Aziz',
      author_email='alif.aziz@icloud.com',

      # declare dependencies here:
      # find dependencies on PyPI - default install location: https://pypi.org
      install_requires=[
      'markdown', 'networkx', 'logging', 'paramiko'
      ],
)