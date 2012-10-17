#!/usr/bin/python

from setuptools import setup

setup(
    name='python-proteus', 
    version='0.1', 
    author='Stephan Adig', 
    author_email='sh@sourcecode.de', 
    description='A Proteus IPAM Python Library', 
    license='LGPLv2', 
    url='https://github.com/sadig/proteus-api', 
    packages=[
        'proteus', 
        'proteus.api', 
        'proteus.objects'
    ], 
    install_requires=['suds'], 
)
