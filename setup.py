# -*- coding: utf-8 -*-
import re
import os
from setuptools import setup


here = os.path.dirname(os.path.abspath(__file__))
version_re = re.compile(r"__version__ = (\'.*?\')")
f = open(os.path.join(here, 'sadisplay.py'))
version = None
for line in f:
    match = version_re.search(line)
    if match:
        version = eval(match.group(1))
        break
else:
    raise Exception("Cannot find version in sadisplay.py")
f.close()


setup(
    name='sadisplay',
    version=version,
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
        'SQLAlchemy >= 0.5',
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ]
)
