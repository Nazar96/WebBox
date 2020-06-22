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
       "Shapely==1.7",
       "tqdm==4.46.1",
       "opencv-python==4.2.0.34"
   ],
)
