#!/usr/bin/env python

from setuptools import setup

desc='Parse "human readable" date/time expressions',


setup(name='parsedatetime',
      version='0.6',
      description=desc,
      summary=desc,
      author='Mike Taylor',
      author_email='bear@code-bear.com',
      url='',
      license='http://www.apache.org/licenses/LICENSE-2.0',
      packages=['parsedatetime'],
      platform=['Any'],
      classifiers=['Development Status :: 4 - Beta',
                   'Environment :: Library',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: Apache Software License',
                   'Operating System :: OS Independent',
                   'Topic :: Text Processing',
                   'Topic :: Software Development :: Libraries :: Python Modules',
                  ]
     )

