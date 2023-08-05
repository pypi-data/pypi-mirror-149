from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='lib4d',
  version='0.0.1',
  description='Библиотека для работы с четырехмерной алгеброй',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Aktoty',
  author_email='aktoty2000@mail.ru',
  license='MIT', 
  classifiers=classifiers,
  keywords='lib4d', 
  packages=find_packages(),
  install_requires=[''] 
)
