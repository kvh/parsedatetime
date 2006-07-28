#!/usr/bin/env python

"""
Test Calendar.Inc() routine
"""

import unittest, time, datetime
import parsedatetime.parsedatetime as pt


  # a special compare function is used to allow us to ignore the seconds as
  # the running of the test could cross a minute boundary
def _compareResults(target, value):
    t_yr, t_mth, t_dy, t_hr, t_min, t_sec, t_wd, t_yd, t_isdst = target
    v_yr, v_mth, v_dy, v_hr, v_min, v_sec, v_wd, v_yd, v_isdst = value

    return ((t_yr == v_yr) and (t_mth == v_mth) and (t_dy == v_dy) and
            (t_hr == v_hr) and (t_min == v_min)) #and (t_wd == v_wd) and (t_yd == v_yd))

class test(unittest.TestCase):
    def setUp(self):
        self.cal = pt.Calendar()
        self.yr, self.mth, self.dy, self.hr, self.mn, self.sec, self.wd, self.yd, self.isdst = time.localtime()

    def testIncMonths(self):
        s = datetime.datetime(2006, 1, 1, 12, 0, 0)
        t = datetime.datetime(2006, 2, 1, 12, 0, 0)
        self.assertTrue(_compareResults(self.cal.inc(s, month=1).timetuple(), t.timetuple()))

        s = datetime.datetime(2006, 12, 1, 12, 0, 0)
        t = datetime.datetime(2007,  1, 1, 12, 0, 0)
        self.assertTrue(_compareResults(self.cal.inc(s, month=1).timetuple(), t.timetuple()))

        s = datetime.datetime(2008, 2, 1, 12, 0, 0)
        t = datetime.datetime(2008, 3, 1, 12, 0, 0)
        self.assertTrue(_compareResults(self.cal.inc(s, month=1).timetuple(), t.timetuple()))

        s = datetime.datetime(2008, 2, 29, 12, 0, 0)
        t = datetime.datetime(2008, 3, 29, 12, 0, 0)
        self.assertTrue(_compareResults(self.cal.inc(s, month=1).timetuple(), t.timetuple()))

        s = datetime.datetime(2006,  1, 1, 12, 0, 0)
        t = datetime.datetime(2005, 12, 1, 12, 0, 0)
        self.assertTrue(_compareResults(self.cal.inc(s, month=-1).timetuple(), t.timetuple()))

    def testIncYears(self):
        s = datetime.datetime(2006, 1, 1, 12, 0, 0)
        t = datetime.datetime(2007, 1, 1, 12, 0, 0)
        self.assertTrue(_compareResults(self.cal.inc(s, year=1).timetuple(), t.timetuple()))

        s = datetime.datetime(2006, 1, 1, 12, 0, 0)
        t = datetime.datetime(2008, 1, 1, 12, 0, 0)
        self.assertTrue(_compareResults(self.cal.inc(s, year=2).timetuple(), t.timetuple()))

        s = datetime.datetime(2006, 12, 31, 12, 0, 0)
        t = datetime.datetime(2007, 12, 31, 12, 0, 0)
        self.assertTrue(_compareResults(self.cal.inc(s, year=1).timetuple(), t.timetuple()))

        s = datetime.datetime(2006, 12, 31, 12, 0, 0)
        t = datetime.datetime(2005, 12, 31, 12, 0, 0)
        self.assertTrue(_compareResults(self.cal.inc(s, year=-1).timetuple(), t.timetuple()))

        s = datetime.datetime(2008, 3, 1, 12, 0, 0)
        t = datetime.datetime(2009, 3, 1, 12, 0, 0)
        self.assertTrue(_compareResults(self.cal.inc(s, year=1).timetuple(), t.timetuple()))

        s = datetime.datetime(2008, 3, 1, 12, 0, 0)
        t = datetime.datetime(2007, 3, 1, 12, 0, 0)
        self.assertTrue(_compareResults(self.cal.inc(s, year=-1).timetuple(), t.timetuple()))

