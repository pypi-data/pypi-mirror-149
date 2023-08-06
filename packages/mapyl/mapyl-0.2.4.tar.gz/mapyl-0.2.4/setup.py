from setuptools import find_packages, setup
from codecs import open
from os import path

# The directory containing this file
HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='mapyl',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(include=['mapyl',
                        'mapyl.utils',
                        'mapyl.classification',
                        'mapyl.regression',
                        'mapyl.data',
                        'mapyl.preprocessing',
                        'mapyl.clustering']),
    version='0.2.4',
    description='A Python Machine learning libary',
    author='brohgue',
    license='Apache License 2.0',
    requires=['numpy'],
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7"
    ]
)