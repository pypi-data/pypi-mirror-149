from setuptools import find_packages, setup

setup(
    name = 'twisel',
    packages=find_packages(include=['twisel']),
    version='0.1.1',
    description='Library for scraping twitter with selenium',
    author='rafiksept',
    license='MIT',
    install_requires = ['pytest','selenium','pandas'],
    test_suite = 'test'

)