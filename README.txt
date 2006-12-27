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

History
-------

The code in parsedatetime has been implemented over the years in many
different languages (C, Clipper, Delphi) as part of different
custom/proprietary systems I've worked on.  Sadly the previous code is
not "open" in any sense of that word.

When I went to work for Open Source Applications Foundation and realized
that the Chandler project could benefit from my experience with parsing
of date/time text I decided to start from scratch and implement the
code using Python and make it truly open.

After working on the initial concept and creating something that could be
shown to the Chandler folks the code has now evolved to it's current state
with the help the Chandler folks, most especially Darshana.

