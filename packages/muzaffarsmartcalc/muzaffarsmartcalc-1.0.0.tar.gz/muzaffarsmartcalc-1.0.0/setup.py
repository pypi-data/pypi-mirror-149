from setuptools import setup, find_packages
 


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()



classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='muzaffarsmartcalc',
  version='1.0.0',
  description='A very basic calculator',
  long_description=long_description,
  url='',  
  author='Muzaffar Sharofiddiov',
  author_email='smartboymuzaffar@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='calculator', 
  packages=find_packages(),
  install_requires=[''] 
)
