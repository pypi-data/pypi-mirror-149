from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='stprogressbar',
  version='0.0.1',
  description='A Basic Progress Bar',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='ST',
  author_email='amazingfalcon1@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='progressbar', 
  packages=find_packages(),
  install_requires=['colorama', 'math'] 
)