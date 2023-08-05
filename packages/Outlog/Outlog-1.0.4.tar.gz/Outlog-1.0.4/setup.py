from setuptools import setup, find_packages

readme = open('README.md')

setup(
    name='Outlog',
    version='1.0.4',
    url='https://github.com/zsendokame/outlog',
    description='Easy way to log data!.',
    author='Sendokame',
    long_description_content_type='text/markdown',
    long_description=readme.read(),
    packages=(find_packages(include=['outlog']))
)