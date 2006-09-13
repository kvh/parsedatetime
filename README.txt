Installing parsedatetime
------------------------

python setup.py install


Running Unit Tests
------------------
In the source tree do the following:

    python run_tests.py parsedatetime


Using parsedatetime
-------------------

import parsedatetime.parsedatetime as pdt

cal = pdt.Calendar()

cal.parse("tomorrow")


Documentation
-------------

Epydoc generated documentation can be found in the docs/
directory.

Generated using:

    epydoc --html --config epydoc.conf


Notes
-----

The Calendar class has a member property named ptc which
is created during the class init method to be an instance
of parsedatetime_consts.CalendarConstants() 

This code is under some serious refactoring as now it appears
it will have more than one user.  Up until now I've been the
only person to even look at the code so bear with me please :)

Contact Information
-------------------

    Mike Taylor         mailto://bear@code-bear.com
                        http://code-bear.com
    Darshana Chhajed    mailto://darshana@osafoundation.org

