#!/usr/bin/env python

"""
Test parsing of strings with multiple chunks
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

    def testSimpleMultipleItems(self):
        s = datetime.datetime.now()
        t = self.cal.inc(s, year=3) + datetime.timedelta(days=5, weeks=2)

        start  = s.timetuple()
        target = t.timetuple()

        self.assertTrue(_compareResults(self.cal.parse('3 years 2 weeks 5 days', start), target))
        self.assertTrue(_compareResults(self.cal.parse('3years 2weeks 5days',    start), target))
        self.assertTrue(_compareResults(self.cal.parse('3 year 2 week 5 day',    start), target))
        self.assertTrue(_compareResults(self.cal.parse('3year 2week 5day',       start), target))

        t      = self.cal.inc(s, year=3, month=2)
        target = t.timetuple()

        self.assertTrue(_compareResults(self.cal.parse('3 years 2 months', start), target))
        self.assertTrue(_compareResults(self.cal.parse('3 year 2 month',   start), target))

    def testMultipleItemsSingleCharUnits(self):
        s = datetime.datetime.now()
        t = self.cal.inc(s, year=3) + datetime.timedelta(days=5, weeks=2)

        start  = s.timetuple()
        target = t.timetuple()

        self.assertTrue(_compareResults(self.cal.parse('3 y 2 w 5 d', start), target))
        self.assertTrue(_compareResults(self.cal.parse('3y 2w 5d',    start), target))

        t      = self.cal.inc(s, year=3) + datetime.timedelta(hours=5, minutes=50)
        target = t.timetuple()

        self.assertTrue(_compareResults(self.cal.parse('3 years 5 hours 50 minutes', start), target))
        self.assertTrue(_compareResults(self.cal.parse('3 year 5 hour 50 minute',    start), target))
        self.assertTrue(_compareResults(self.cal.parse('3 yr 5 hr 50 min',           start), target))
        self.assertTrue(_compareResults(self.cal.parse('3 y 5 h 50 m',               start), target))
        self.assertTrue(_compareResults(self.cal.parse('3y 5h 50m',                  start), target))


    def testMultipleItemsWithPunctuation(self):
        s = datetime.datetime.now()
        t = self.cal.inc(s, year=3) + datetime.timedelta(days=5, weeks=2)

        start  = s.timetuple()
        target = t.timetuple()

        self.assertTrue(_compareResults(self.cal.parse('3 years, 2 weeks, 5 days',    start), target))
        self.assertTrue(_compareResults(self.cal.parse('3 years, 2 weeks and 5 days', start), target))
        self.assertTrue(_compareResults(self.cal.parse('3 yr, 2 wk and 5 dy',         start), target))
        self.assertTrue(_compareResults(self.cal.parse('3 y, 2 w and 5 d',            start), target))
