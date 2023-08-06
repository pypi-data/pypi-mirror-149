from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='devtreeutil',
  version='0.0.4',
  description='devtreeutil is a library that makes simple actions a lot easier and more effective!',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',
  author='DevTree Studios',
  author_email='devtreestudios@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='devtreeutil', 
  packages=find_packages(),
  install_requires=['colorama', 'keyboard', 'mouse'] 
)