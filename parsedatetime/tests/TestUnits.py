#!/usr/bin/env python

"""
Test parsing of units
"""

import unittest, time, datetime
import parsedatetime.parsedatetime as pt


  # a special compare function is used to allow us to ignore the seconds as
  # the running of the test could cross a minute boundary
def _compareResults(target, value):
    t_yr, t_mth, t_dy, t_hr, t_min, t_sec, t_wd, t_yd, t_isdst = target
    v_yr, v_mth, v_dy, v_hr, v_min, v_sec, v_wd, v_yd, v_isdst = value

    #print "t: ",t_yr, t_mth, t_dy, t_hr, t_min, t_sec, t_wd, t_yd, t_isdst
    #print "v: ",v_yr, v_mth, v_dy, v_hr, v_min, v_sec, v_wd, v_yd, v_isdst

    return ((t_yr == v_yr) and (t_mth == v_mth) and (t_dy == v_dy) and
            (t_hr == v_hr) and (t_min == v_min)) #and (t_wd == v_wd) and (t_yd == v_yd))

class test(unittest.TestCase):
    def setUp(self):
        self.cal = pt.Calendar()
        self.yr, self.mth, self.dy, self.hr, self.mn, self.sec, self.wd, self.yd, self.isdst = time.localtime()

    def testMinutes(self):
        s = datetime.datetime.now()
        t = s + datetime.timedelta(minutes=1)

        start  = s.timetuple()
        target = t.timetuple()

        self.assertTrue(_compareResults(self.cal.parse('1 minute',  start), target))
        self.assertTrue(_compareResults(self.cal.parse('1 minutes', start), target))
        self.assertTrue(_compareResults(self.cal.parse('1 min',     start), target))
        self.assertTrue(_compareResults(self.cal.parse('1min',      start), target))
        self.assertTrue(_compareResults(self.cal.parse('1 m',       start), target))
        self.assertTrue(_compareResults(self.cal.parse('1m',        start), target))


    def testHours(self):
        s = datetime.datetime.now()
        t = s + datetime.timedelta(hours=1)

        start  = s.timetuple()
        target = t.timetuple()

        self.assertTrue(_compareResults(self.cal.parse('1 hour',  start), target))
        self.assertTrue(_compareResults(self.cal.parse('1 hours', start), target))
        self.assertTrue(_compareResults(self.cal.parse('1 hr',    start), target))


    def testDays(self):
        s = datetime.datetime.now()
        t = s + datetime.timedelta(days=1)

        start  = s.timetuple()
        target = t.timetuple()

        self.assertTrue(_compareResults(self.cal.parse('1 day',  start), target))
        self.assertTrue(_compareResults(self.cal.parse('1day',   start), target))
        self.assertTrue(_compareResults(self.cal.parse('1 days', start), target))
        self.assertTrue(_compareResults(self.cal.parse('1days',  start), target))
        self.assertTrue(_compareResults(self.cal.parse('1 dy',   start), target))
        self.assertTrue(_compareResults(self.cal.parse('1dy',    start), target))
        self.assertTrue(_compareResults(self.cal.parse('1 d',    start), target))
        self.assertTrue(_compareResults(self.cal.parse('1d',     start), target))


    def testWeeks(self):
        s = datetime.datetime.now()
        t = s + datetime.timedelta(weeks=1)

        start  = s.timetuple()
        target = t.timetuple()

        self.assertTrue(_compareResults(self.cal.parse('1 week',  start), target))
        self.assertTrue(_compareResults(self.cal.parse('1week',   start), target))
        self.assertTrue(_compareResults(self.cal.parse('1 weeks', start), target))
        self.assertTrue(_compareResults(self.cal.parse('1weeks',  start), target))
        self.assertTrue(_compareResults(self.cal.parse('1 wk',    start), target))
        self.assertTrue(_compareResults(self.cal.parse('1wk',     start), target))
        self.assertTrue(_compareResults(self.cal.parse('1 w',     start), target))
        self.assertTrue(_compareResults(self.cal.parse('1w',      start), target))


    def testMonths(self):
        s = datetime.datetime.now()
        t = self.cal.inc(s, month=1)

        start  = s.timetuple()
        target = t.timetuple()

        self.assertTrue(_compareResults(self.cal.parse('1 month',  start), target))
        self.assertTrue(_compareResults(self.cal.parse('1month',   start), target))
        self.assertTrue(_compareResults(self.cal.parse('1 months', start), target))
        self.assertTrue(_compareResults(self.cal.parse('1months',  start), target))


    def testYears(self):
        s = datetime.datetime.now()
        t = s + datetime.timedelta(days=365)

        start  = s.timetuple()
        target = t.timetuple()

        self.assertTrue(_compareResults(self.cal.parse('1 year',  start), target))
        self.assertTrue(_compareResults(self.cal.parse('1year',   start), target))
        self.assertTrue(_compareResults(self.cal.parse('1 years', start), target))
        self.assertTrue(_compareResults(self.cal.parse('1years',  start), target))
        self.assertTrue(_compareResults(self.cal.parse('1 yr',    start), target))
        self.assertTrue(_compareResults(self.cal.parse('1yr',     start), target))
        self.assertTrue(_compareResults(self.cal.parse('1 y',     start), target))
        self.assertTrue(_compareResults(self.cal.parse('1y',      start), target))


if __name__ == "__main__":
    unittest.main()
