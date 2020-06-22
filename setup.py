from setuptools import setup

requirements = [package.strip() for package in open('requirements.txt', 'r').readlines()]

setup(
   name='webbox',
   version='0.1.0',
   author='Nazarii Tekhta',
   author_email='ntehta96@gmail.com',
   packages=['webbox'],
   url='https://github.com/Nazar96/WebBox',
   install_requires=requirements,
)
