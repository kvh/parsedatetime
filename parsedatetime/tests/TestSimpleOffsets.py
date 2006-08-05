#!/usr/bin/env python

"""
Test parsing of 'simple' offsets
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

    def testMinutesFromNow(self):
        s = datetime.datetime.now()
        t = s + datetime.timedelta(minutes=5)

        start  = s.timetuple()
        target = t.timetuple()

        self.assertTrue(_compareResults(self.cal.parse('5 minutes from now', start), (target, False)))
        self.assertTrue(_compareResults(self.cal.parse('5 min from now',     start), (target, False)))
        self.assertTrue(_compareResults(self.cal.parse('5m from now',        start), (target, False)))
        self.assertTrue(_compareResults(self.cal.parse('in 5 minutes',       start), (target, False)))
        self.assertTrue(_compareResults(self.cal.parse('in 5 min',           start), (target, False)))
        self.assertTrue(_compareResults(self.cal.parse('5 min from now',     start), (target, False)))
        self.assertTrue(_compareResults(self.cal.parse('5 minutes',          start), (target, False)))
        self.assertTrue(_compareResults(self.cal.parse('5 min',              start), (target, False)))
        self.assertTrue(_compareResults(self.cal.parse('5m',                 start), (target, False)))


    def testMinutesBeforeNow(self):
        s = datetime.datetime.now()
        t = s + datetime.timedelta(minutes=-5)

        start  = s.timetuple()
        target = t.timetuple()

        self.assertTrue(_compareResults(self.cal.parse('5 minutes before now', start), (target, False)))
        self.assertTrue(_compareResults(self.cal.parse('5 min before now',     start), (target, False)))
        self.assertTrue(_compareResults(self.cal.parse('5m before now',        start), (target, False)))


    def testOffsetAfterNoon(self):
        s = datetime.datetime.now()
        t = datetime.datetime(self.yr, self.mth, self.dy, 12, 0, 0) + datetime.timedelta(hours=5)

        start  = s.timetuple()
        target = t.timetuple()

        self.assertTrue(_compareResults(self.cal.parse('5 hours from noon',      start), (target, False)))
        self.assertTrue(_compareResults(self.cal.parse('5 hours after noon',     start), (target, False)))
        self.assertTrue(_compareResults(self.cal.parse('5 hours after 12pm',     start), (target, False)))
        self.assertTrue(_compareResults(self.cal.parse('5 hours after 12 pm',    start), (target, False)))
        self.assertTrue(_compareResults(self.cal.parse('5 hours after 12:00pm',  start), (target, False)))
        self.assertTrue(_compareResults(self.cal.parse('5 hours after 12:00 pm', start), (target, False)))


    def testOffsetBeforeNoon(self):
        s = datetime.datetime.now()
        t = datetime.datetime(self.yr, self.mth, self.dy, 12, 0, 0) + datetime.timedelta(hours=-5)

        start  = s.timetuple()
        target = t.timetuple()

        self.assertTrue(_compareResults(self.cal.parse('5 hours before noon',     start), (target, False)))
        self.assertTrue(_compareResults(self.cal.parse('5 hours before 12pm',     start), (target, False)))
        self.assertTrue(_compareResults(self.cal.parse('5 hours before 12 pm',    start), (target, False)))
        self.assertTrue(_compareResults(self.cal.parse('5 hours before 12:00pm',  start), (target, False)))
        self.assertTrue(_compareResults(self.cal.parse('5 hours before 12:00 pm', start), (target, False)))


    def testWeekFromNow(self):
        s = datetime.datetime.now()
        t = s + datetime.timedelta(weeks=1)

        start  = s.timetuple()
        target = t.timetuple()

        self.assertTrue(_compareResults(self.cal.parse('in 1 week',       start), (target, False)))
        self.assertTrue(_compareResults(self.cal.parse('1 week from now', start), (target, False)))
        self.assertTrue(_compareResults(self.cal.parse('in 7 days',       start), (target, False)))
        self.assertTrue(_compareResults(self.cal.parse('7 days from now', start), (target, False)))
        #self.assertTrue(_compareResults(self.cal.parse('next week',       start), (target, False)))


    def testWeekBeforeNow(self):
        s = datetime.datetime.now()
        t = s + datetime.timedelta(weeks=-1)

        start  = s.timetuple()
        target = t.timetuple()

        self.assertTrue(_compareResults(self.cal.parse('1 week before now', start), (target, False)))
        self.assertTrue(_compareResults(self.cal.parse('7 days before now', start), (target, False)))
        #self.assertTrue(_compareResults(self.cal.parse('last week',         start), (target, False)))


    def testSpecials(self):
        s = datetime.datetime.now()
        t = datetime.datetime(self.yr, self.mth, self.dy, 9, 0, 0) + datetime.timedelta(days=1)

        start  = s.timetuple()
        target = t.timetuple()

        self.assertTrue(_compareResults(self.cal.parse('tomorrow', start), (target, False)))
        self.assertTrue(_compareResults(self.cal.parse('next day', start), (target, False)))

        t      = datetime.datetime(self.yr, self.mth, self.dy, 9, 0, 0) + datetime.timedelta(days=-1)
        target = t.timetuple()

        self.assertTrue(_compareResults(self.cal.parse('yesterday', start), (target, False)))

        t      = datetime.datetime(self.yr, self.mth, self.dy, 9, 0, 0)
        target = t.timetuple()

        self.assertTrue(_compareResults(self.cal.parse('today', start), (target, False)))


if __name__ == "__main__":
    unittest.main()
