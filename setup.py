# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='openfire-restapi',
    version='0.1.1',
    description=u"A python client for Openfire's REST API Plugin",
    license="GPL-3",
    author='Alliance Auth, Sergey Fedotov (seamus-45)',
    author_email='basraaheve+openfire-restapi@gmail.com',
    url='https://github.com/allianceauth/openfire-restapi/',
    packages=['ofrestapi'],
    install_requires=['requests>=2.9.1'],
)
