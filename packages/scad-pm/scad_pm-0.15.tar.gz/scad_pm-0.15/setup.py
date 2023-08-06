
from setuptools import setup

setup(
    name='scad_pm',
    version='0.15',
    scripts=['src/scad_pm'],
    install_requires=[
        'pyyaml',
        'dataclasses_json',
        'scopeton'
   ]
)