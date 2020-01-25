 # -*- coding: utf-8 -*-
"""
Created on Sat Jan 18 23:05:29 2020

@author: arthurd
"""

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()



setup(name='noiseplanet',
        version='0.1',
        description='GeoJson map matching from Noise Planet data server.',
        long_description=long_description,
        long_description_content_type="text/markdown",
        url='https://github.com/arthurdjn/noise_capture',
        author='Arthur Dujardin',
        author_email='arthur.dujardin@ensg.eu',
        license='Apache License-2.0',
        
        install_requires = ['numpy', 'pandas', 'osmnx', 'json'],
        packages=find_packages(),
        namespace_packages=['noiseplanet'],
        zip_safe=False,
        classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
    
        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Mapping',
    
        # Pick your license as you wish (should match "license" above)
    
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
    ])


