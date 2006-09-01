#!/usr/bin/env python

from ez_setup import use_setuptools

use_setuptools()

import setuptools

desc='Parse human-readable date/time expressions',

setuptools.setup(name='parsedatetime',
      version='0.7.1',
      description=desc,
      author='Mike Taylor',
      author_email='bear@code-bear.com',
      url='http://code-bear.com/code/parsedatetime/',
      license='http://www.apache.org/licenses/LICENSE-2.0',
      packages=['parsedatetime'],
      platforms=['Any'],
      classifiers=['Development Status :: 4 - Beta',
                   'Environment :: Library',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: Apache Software License',
                   'Operating System :: OS Independent',
                   'Topic :: Text Processing',
                   'Topic :: Software Development :: Libraries :: Python Modules',
                  ]
     )

