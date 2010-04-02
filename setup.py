#!/usr/bin/env python

"""
@file setup.py
@author Paul Hubbard
@date 8/24/09
@brief setup file for txrabbitmq
"""

setupdict = {
    'name' : 'txrabbitmq',
    'version' : '0.1.1',
    'description' : 'rabbitmqctl as a Twisted service',
    'url': 'http://www.oceanobservatories.org/',
    'download_url' : 'http://ooici.net/packages',
    'license' : 'Apache 2.0',
    'author' : 'Alex Clemesha',
    'author_email' : 'clemesha@ucsd.edu',
    'keywords': ['ooci'],
    'classifiers' : [
    'Development Status :: 3 - Alpha',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: Apache Software License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Scientific/Engineering'],
}

try:
    from setuptools import setup, find_packages
    setupdict['packages'] = find_packages()
    setupdict['test_suite'] = 'txrabbitmq.test'
    setupdict['install_requires'] = ['Twisted', 'twotp', 'orbited', 'simplejson', 'stompservice']
    setupdict['include_package_data'] = True
    setup(**setupdict)

except ImportError:
    from distutils.core import setup
    setupdict['packages'] = ['txrabbitmq']
    setup(**setupdict)
