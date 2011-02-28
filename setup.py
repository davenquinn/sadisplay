# -*- coding: utf-8 -*-
from setuptools import setup


setup(
    name='sadisplay',
    version='0.1dev',
    url='http://bitbucket.org/estin/sadisplay',
    license='BSD',
    author='Evgeniy Tatarkin',
    author_email='tatarkin.evg@gmail.com',
    description='SqlAlchemy schema display script',
    long_description=open('README.rst').read(),
    py_modules=['sadisplay'],
    zip_safe=False,
    platforms='any',
    install_requires=[
        'SqlAlchemy >=5.0',
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ]
)
