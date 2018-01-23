#!/usr/bin/python3
# xlattice_py/setup.py

""" Setuptools project configuration for xlattice_py. """

from os.path import exists
from setuptools import setup, Extension

# see http://docs.python.org/distutils/setupscript.html

MODULE1 = Extension('cFTLogForPy',
                    include_dirs=['/usr/include/python3.4m',
                                  '/usr/include', ],
                    libraries=['ev', ],
                    library_dirs=['/usr/local/lib', ],
                    sources=[
                        'src/extsrc/cFTLogForPy.c',
                        'src/extsrc/evLoop.c',
                        'src/extsrc/logBufs.c',
                        'src/extsrc/modFunc.c',
                        'src/extsrc/threading.c',
                    ])

LONG_DESC = None
if exists('README.md'):
    with open('README.md', 'r') as file:
        LONG_DESC = file.read()

setup(name='xlattice_py',
      version='1.10.2',
      author='Jim Dixon',
      author_email='jddixon@gmail.com',
      long_description=LONG_DESC,
      packages=['xlattice', 'xlattice.u'],
      package_dir={'': 'src'},
      py_modules=[],
      include_package_data=False,
      zip_safe=False,
      scripts=['src/gen_node_id', 'src/u_consolidate', 'src/u_preen',
               'src/u_re_struc', 'src/u_stats', 'src/verify_content_keys'],
      ext_modules=[MODULE1],
      description='xlattice building blocks for Python 2 and 3',
      url='https://jddixon.github.io/xlattice_py',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Natural Language :: English',
          'Programming Language :: Python 2.7',
          'Programming Language :: Python 3.3',
          'Programming Language :: Python 3.4',
          'Programming Language :: Python 3.5',
          'Programming Language :: Python 3.6',
          'Programming Language :: Python 3.7',
          'Topic :: Software Development :: Libraries :: Python Modules',
      ],)
