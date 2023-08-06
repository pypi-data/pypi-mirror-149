from setuptools import setup, find_packages


setup(
    name='picopi_i2c',
    version='0.0',
    author="James Wang",
    author_email='immarsgoblin@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
)