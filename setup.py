#!/usr/bin/env python3
# 'apt-get install python-dev' may be necessary to get .core

""" Set up distutils for xlattice_py. """

import re
from distutils.core import setup, Extension
__version__ = re.search(r"__version__\s*=\s*'(.*)'",
                        open('src/xlattice/__init__.py').read()).group(1)

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

setup(name='xlattice_py',
      version=__version__,
      author='Jim Dixon',
      author_email='jddixon@gmail.com',
      py_modules=[],
      packages=['src/xlattice', 'src/xlattice.u', ],
      scripts=[
          'src/gen_node_id',
          'src/u_consolidate', 'src/u_preen', 'src/u_re_struc', 'src/u_stats',
          'src/verify_content_keys', ],
      ext_modules=[MODULE1],
      description='xlattice building blocks in Python 3',
      url='https://jddixon.github.io/xlattice_py',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Natural Language :: English',
          'Programming Language :: Python 3',
          'Topic :: Software Development :: Libraries :: Python Modules',
      ],)
