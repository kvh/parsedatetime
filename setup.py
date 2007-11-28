#!/usr/bin/env python

import ez_setup
ez_setup.use_setuptools()

import sys
import setuptools

# swiped from Zanshin's setup.py - thanks Grant!
class MakeDocsCommand(setuptools.Command):
    """
    Command to generate documentation
    """

    description  = "create html documentation"
    user_options = [ ('output-dir=', 'o', "Output directory for html tree"),
                   ]
    output_dir   = None

    def initialize_options(self):
        pass

    def finalize_options(self):
        self.output_dir = self.output_dir or "docs"

    def run(self):
        if self.output_dir:
            import epydoc.cli

            sys.argv = ['epydoc.py', '--html', '--config', 'epydoc.conf']

            if self.dry_run:
                self.announce('skipping running %s (dry run)' % (sys.argv))
            else:
                self.announce('running %s' % (sys.argv))
                epydoc.cli.cli()


desc='Parse human-readable date/time expressions',

setuptools.setup(
    name='parsedatetime',
    version='0.8.6',
    description=desc,
    author='Mike Taylor and Darshana Chhajed',
    author_email='bear@code-bear.com',
    url='http://code-bear.com/code/parsedatetime/',
    license='http://www.apache.org/licenses/LICENSE-2.0',
    packages=['parsedatetime'],
    platforms=['Any'],
    cmdclass={'doc': MakeDocsCommand},
    classifiers=['Development Status :: 4 - Beta',
                 'Environment :: Library',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: Apache Software License',
                 'Operating System :: OS Independent',
                 'Topic :: Text Processing',
                 'Topic :: Software Development :: Libraries :: Python Modules',
                ]
     )

