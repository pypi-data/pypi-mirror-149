from setuptools import setup, find_packages


setup(
    name='frproxy',
    version='0.0',
    license='MIT',
    author="ta27",
    author_email='tarangga.code@gmail.com',
    packages=find_packages('frproxy'),
    package_dir={'': 'frproxy'},
    # url='https://github.com/gmyrianthous/example-publish-pypi',
    keywords='free proxy, rotation proxy, proxy, proxies',
    install_requires=[
          'tabulate',
      ],

)