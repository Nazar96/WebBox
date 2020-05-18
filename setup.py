 from setuptools import setup

 setup(
   name='webbox',
   version='0.1.0',
   author='Nazarii Tekhta',
   author_email='ntehta96@gmail.com',
   packages=['webbox'],
   url='https://github.com/Nazar96/WebBox',
   install_requires=[
       "selenium==3.141.0",
       "Shapely==1.6.4.post2",
       "tqdm==4.28.1"
   ],
)
