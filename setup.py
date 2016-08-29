#!/usr/bin/python3

# 'apt-get install python-dev' may be necessary to get .core

import re
from distutils.core import setup, Extension
__version__ = re.search("__version__\s*=\s*'(.*)'",
                        open('xlattice/__init__.py').read()).group(1)

# see http://docs.python.org/distutils/setupscript.html

module1 = Extension('cFTLogForPy',
                    include_dirs=['/usr/include/python3.4m',
                                  '/usr/include',
                                  ],
                    libraries=['ev', ],
                    library_dirs=['/usr/local/lib', ],
                    sources=[
                        'extsrc/cFTLogForPy.c',
                        'extsrc/evLoop.c',
                        'extsrc/logBufs.c',
                        'extsrc/modFunc.c',
                        'extsrc/threading.c',
                    ])

setup(name='xlattice_py',
      version=__version__,
      author='Jim Dixon',
      author_email='jddixon@gmail.com',
      py_modules=[],
      packages=['xlattice', 'xlattice.u', ],
      scripts=[
           'scripts/genNodeID1',
           'scripts/genNodeID3',
           'uConsolidate', 'uReStruc',
           'uStats',
           'verifyContentKeys', ],
      ext_modules=[module1],
      description='xlattice building blocks in Python 3',
      url='https://jddixon.github.io/xlattice_py',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Natural Language :: English',
          'Programming Language :: Python 3',
          'Topic :: Software Development :: Libraries :: Python Modules',
      ],
      )
