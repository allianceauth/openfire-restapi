# -*- coding: utf-8 -*-

from setuptools import setup

__version__ = 'ERR'

with open('ofrestapi/version.py') as f:
    exec(f.read())

setup(
    name='openfire-restapi',
    version=__version__,
    description=u"A python client for Openfire's REST API Plugin",
    license="GPL-3",
    author='Alliance Auth, Sergey Fedotov (seamus-45)',
    author_email='basraaheve+openfire-restapi@gmail.com',
    url='https://github.com/allianceauth/openfire-restapi/',
    packages=['ofrestapi'],
    install_requires=['requests>=2.9.1'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
