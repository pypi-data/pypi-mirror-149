from setuptools import setup

setup(
  name='sensitive-test',
  packages=['sensitive'],
  version='1.0.1',
  license='MIT',
  description='A small, simple, and fast ordered failfast test-suite for Python.',
  author='vierofernando',
  long_description=open('README.md', 'r', encoding='utf-8').read(),
  long_description_content_type='text/markdown',
  author_email='vierofernando9@gmail.com',
  keywords=['test', 'tests', 'ci', 'debug'],
  install_requires=[],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9'
  ],
  python_requires='>=3.6',
)