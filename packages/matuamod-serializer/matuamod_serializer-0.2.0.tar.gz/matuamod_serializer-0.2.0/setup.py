from setuptools import find_packages, setup

setup(
    name='matuamod_serializer',
    packages=find_packages(),
    version='0.2.0',
    description='My json, toml, yaml serializer/parser library',
    author='matuamod',
    author_email='matua.models2003@gmail.com',
    setup_requires=['pytest-runner', 'pyyaml'],
    url='https://github.com/matuamod/ISP-2022-053504/',
    license='MIT',
)
