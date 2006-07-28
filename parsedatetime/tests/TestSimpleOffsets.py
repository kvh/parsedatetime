#!/usr/bin/env python

"""
Test parsing of 'simple' offsets
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

    def testMinutesFromNow(self):
        #start  = int(time.time())
        #target = start + 5 * self.cal.ptc.Minute
        s = datetime.datetime.now()
        t = s + datetime.timedelta(minutes=5)

        start  = s.timetuple()
        target = t.timetuple()

        self.assertTrue(_compareResults(self.cal.parse('5 minutes from now', start), target))
        self.assertTrue(_compareResults(self.cal.parse('5 min from now',     start), target))
        self.assertTrue(_compareResults(self.cal.parse('5m from now',        start), target))
        self.assertTrue(_compareResults(self.cal.parse('in 5 minutes',       start), target))
        self.assertTrue(_compareResults(self.cal.parse('in 5 min',           start), target))
        self.assertTrue(_compareResults(self.cal.parse('5 min from now',     start), target))
        self.assertTrue(_compareResults(self.cal.parse('5 minutes',          start), target))
        self.assertTrue(_compareResults(self.cal.parse('5 min',              start), target))
        self.assertTrue(_compareResults(self.cal.parse('5m',                 start), target))


    def testMinutesBeforeNow(self):
        #start  = int(time.time())
        #target = start - 5 * self.cal.ptc.Minute
        s = datetime.datetime.now()
        t = s + datetime.timedelta(minutes=-5)

        start  = s.timetuple()
        target = t.timetuple()

        self.assertTrue(_compareResults(self.cal.parse('5 minutes before now', start), target))
        self.assertTrue(_compareResults(self.cal.parse('5 min before now',     start), target))
        self.assertTrue(_compareResults(self.cal.parse('5m before now',        start), target))


    def testOffsetAfterNoon(self):
        #source_noon = (self.yr, self.mth, self.dy, 12,  0,   0, self.wd, self.yd, self.isdst)
        #start  = int(time.mktime(source_noon))
        #target = start + 5 * self.cal.ptc.Hour
        s = datetime.datetime(self.yr, self.mth, self.dy, 12,  0,   0)
        t = s + datetime.timedelta(hours=5)

        start  = s.timetuple()
        target = t.timetuple()

        self.assertTrue(_compareResults(self.cal.parse('5 hours from noon',      start), target))
        self.assertTrue(_compareResults(self.cal.parse('5 hours after noon',     start), target))
        self.assertTrue(_compareResults(self.cal.parse('5 hours after 12pm',     start), target))
        self.assertTrue(_compareResults(self.cal.parse('5 hours after 12 pm',    start), target))
        self.assertTrue(_compareResults(self.cal.parse('5 hours after 12:00pm',  start), target))
        self.assertTrue(_compareResults(self.cal.parse('5 hours after 12:00 pm', start), target))


    def testOffsetBeforeNoon(self):
        #source_noon = (self.yr, self.mth, self.dy, 12,  0,   0, self.wd, self.yd, self.isdst)
        #start  = int(time.mktime(source_noon))
        #target = start - 5 * self.cal.ptc.Hour
        s = datetime.datetime(self.yr, self.mth, self.dy, 12,  0,   0)
        t = s + datetime.timedelta(hours=-5)

        start  = s.timetuple()
        target = t.timetuple()

        self.assertTrue(_compareResults(self.cal.parse('5 hours before noon',     start), target))
        self.assertTrue(_compareResults(self.cal.parse('5 hours before 12pm',     start), target))
        self.assertTrue(_compareResults(self.cal.parse('5 hours before 12 pm',    start), target))
        self.assertTrue(_compareResults(self.cal.parse('5 hours before 12:00pm',  start), target))
        self.assertTrue(_compareResults(self.cal.parse('5 hours before 12:00 pm', start), target))


    def testWeekFromNow(self):
        #start  = int(time.time())
        #target = start + self.cal.ptc.Week
        s = datetime.datetime.now()
        t = s + datetime.timedelta(weeks=1)

        start  = s.timetuple()
        target = t.timetuple()

        self.assertTrue(_compareResults(self.cal.parse('in 1 week',       start), target))
        self.assertTrue(_compareResults(self.cal.parse('next week',       start), target))
        self.assertTrue(_compareResults(self.cal.parse('1 week from now', start), target))
        self.assertTrue(_compareResults(self.cal.parse('in 7 days',       start), target))
        self.assertTrue(_compareResults(self.cal.parse('7 days from now', start), target))


    def testWeekBeforeNow(self):
        #start  = int(time.time())
        #target = start - self.cal.ptc.Week
        s = datetime.datetime.now()
        t = s + datetime.timedelta(weeks=-1)

        start  = s.timetuple()
        target = t.timetuple()

        self.assertTrue(_compareResults(self.cal.parse('last week',         start), target))
        self.assertTrue(_compareResults(self.cal.parse('1 week before now', start), target))
        self.assertTrue(_compareResults(self.cal.parse('7 days before now', start), target))


    def testSpecials(self):
        s = datetime.datetime.now()
        t = s + datetime.timedelta(days=1)

        start  = s.timetuple()
        target = t.timetuple()

        self.assertTrue(_compareResults(self.cal.parse('today',     start), start))
        self.assertTrue(_compareResults(self.cal.parse('tomorrow',  start), target))
        self.assertTrue(_compareResults(self.cal.parse('next day',  start), target))

        t      = s + datetime.timedelta(days=-1)
        target = t.timetuple()

        self.assertTrue(_compareResults(self.cal.parse('yesterday', start), target))


if __name__ == "__main__":
    unittest.main()
