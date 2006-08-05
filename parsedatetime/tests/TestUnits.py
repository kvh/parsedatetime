#!/usr/bin/env python

"""
Test parsing of units
"""

import unittest, time, datetime
import parsedatetime.parsedatetime as pt


  # a special compare function is used to allow us to ignore the seconds as
  # the running of the test could cross a minute boundary
def _compareResults(result, check):
  target, t_flag = result
  value,  v_flag = check

  t_yr, t_mth, t_dy, t_hr, t_min, t_sec, t_wd, t_yd, t_isdst = target
  v_yr, v_mth, v_dy, v_hr, v_min, v_sec, v_wd, v_yd, v_isdst = value

  return ((t_yr == v_yr) and (t_mth == v_mth) and (t_dy == v_dy) and
          (t_hr == v_hr) and (t_min == v_min)) and (t_flag == v_flag)

class test(unittest.TestCase):
    def setUp(self):
        self.cal = pt.Calendar()
        self.yr, self.mth, self.dy, self.hr, self.mn, self.sec, self.wd, self.yd, self.isdst = time.localtime()

    def testMinutes(self):
        s = datetime.datetime.now()
        t = s + datetime.timedelta(minutes=1)

        start  = s.timetuple()
        target = t.timetuple()

        self.assertTrue(_compareResults(self.cal.parse('1 minute',  start), (target, False)))
        self.assertTrue(_compareResults(self.cal.parse('1 minutes', start), (target, False)))
        self.assertTrue(_compareResults(self.cal.parse('1 min',     start), (target, False)))
        self.assertTrue(_compareResults(self.cal.parse('1min',      start), (target, False)))
        self.assertTrue(_compareResults(self.cal.parse('1 m',       start), (target, False)))
        self.assertTrue(_compareResults(self.cal.parse('1m',        start), (target, False)))

    def testHours(self):
        s = datetime.datetime.now()
        t = s + datetime.timedelta(hours=1)

        start  = s.timetuple()
        target = t.timetuple()

        self.assertTrue(_compareResults(self.cal.parse('1 hour',  start), (target, False)))
        self.assertTrue(_compareResults(self.cal.parse('1 hours', start), (target, False)))
        self.assertTrue(_compareResults(self.cal.parse('1 hr',    start), (target, False)))


    def testDays(self):
        s = datetime.datetime.now()
        t = s + datetime.timedelta(days=1)

        start  = s.timetuple()
        target = t.timetuple()

        self.assertTrue(_compareResults(self.cal.parse('1 day',  start), (target, False)))
        self.assertTrue(_compareResults(self.cal.parse('1 days', start), (target, False)))
        self.assertTrue(_compareResults(self.cal.parse('1days',  start), (target, False)))
        self.assertTrue(_compareResults(self.cal.parse('1 dy',   start), (target, False)))
        self.assertTrue(_compareResults(self.cal.parse('1 d',    start), (target, False)))


    def testWeeks(self):
        s = datetime.datetime.now()
        t = s + datetime.timedelta(weeks=1)

        start  = s.timetuple()
        target = t.timetuple()

        self.assertTrue(_compareResults(self.cal.parse('1 week',  start), (target, False)))
        self.assertTrue(_compareResults(self.cal.parse('1week',   start), (target, False)))
        self.assertTrue(_compareResults(self.cal.parse('1 weeks', start), (target, False)))
        self.assertTrue(_compareResults(self.cal.parse('1 wk',    start), (target, False)))
        self.assertTrue(_compareResults(self.cal.parse('1 w',     start), (target, False)))
        self.assertTrue(_compareResults(self.cal.parse('1w',      start), (target, False)))

    def testMonths(self):
        s = datetime.datetime.now()
        t = self.cal.inc(s, month=1)

        start  = s.timetuple()
        target = t.timetuple()

        self.assertTrue(_compareResults(self.cal.parse('1 month',  start), (target, False)))
        self.assertTrue(_compareResults(self.cal.parse('1 months', start), (target, False)))
        self.assertTrue(_compareResults(self.cal.parse('1month',   start), (target, False)))


    def testYears(self):
        s = datetime.datetime.now()
        t = self.cal.inc(s, year=1)

        start  = s.timetuple()
        target = t.timetuple()

        self.assertTrue(_compareResults(self.cal.parse('1 year',  start), (target, False)))
        self.assertTrue(_compareResults(self.cal.parse('1 years', start), (target, False)))
        self.assertTrue(_compareResults(self.cal.parse('1 yr',    start), (target, False)))
        self.assertTrue(_compareResults(self.cal.parse('1 y',     start), (target, False)))
        self.assertTrue(_compareResults(self.cal.parse('1y',      start), (target, False)))


if __name__ == "__main__":
    unittest.main()
