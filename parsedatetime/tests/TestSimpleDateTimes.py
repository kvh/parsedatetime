#!/usr/bin/env python

"""
Test parsing of simple date and times
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

    def testTimes(self):
        start  = datetime.datetime(self.yr, self.mth, self.dy, self.hr, self.mn, self.sec).timetuple()
        target = datetime.datetime(self.yr, self.mth, self.dy, 12, 0, 0).timetuple()

        self.assertTrue(_compareResults(self.cal.parse('12:00:00 PM', start), target))
        self.assertTrue(_compareResults(self.cal.parse('12:00 PM',    start), target))
        self.assertTrue(_compareResults(self.cal.parse('12 PM',       start), target))
        self.assertTrue(_compareResults(self.cal.parse('12PM',        start), target))
        self.assertTrue(_compareResults(self.cal.parse('noon',        start), target))
        self.assertTrue(_compareResults(self.cal.parse('1200',        start), target))
        self.assertTrue(_compareResults(self.cal.parse('12p',         start), target))
        self.assertTrue(_compareResults(self.cal.parse('12pm',        start), target))

        target = datetime.datetime(self.yr, self.mth, self.dy, 7, 30, 0).timetuple()

        self.assertTrue(_compareResults(self.cal.parse('730',  start), target))
        self.assertTrue(_compareResults(self.cal.parse('0730', start), target))

        target = datetime.datetime(self.yr, self.mth, self.dy, 17, 30, 0).timetuple()

        self.assertTrue(_compareResults(self.cal.parse('1730',   start), target))
        self.assertTrue(_compareResults(self.cal.parse('173000', start), target))

        self.assertTrue(_compareResults(self.cal.parse('1799',   start), start)) #target is the start time since time is not valid
        self.assertTrue(_compareResults(self.cal.parse('781',    start), start)) #target is the start time since time is not valid
        self.assertTrue(_compareResults(self.cal.parse('2702',   start), start)) #target is the start time since time is not valid
        self.assertTrue(_compareResults(self.cal.parse('78',     start), start)) #target is the start time since time is not valid
        self.assertTrue(_compareResults(self.cal.parse('11',     start), start)) #target is the start time since time is not valid
        self.assertTrue(_compareResults(self.cal.parse('1',      start), start)) #target is the start time since time is not valid
        self.assertTrue(_compareResults(self.cal.parse('174565', start), start)) #target is the start time since time is not valid
        self.assertTrue(_compareResults(self.cal.parse('177505', start), start)) #target is the start time since time is not valid


    def testDates(self):
        start  = datetime.datetime(self.yr, self.mth, self.dy, self.hr, self.mn, self.sec).timetuple()
        target = datetime.datetime(2006, 8, 25,  self.hr, self.mn, self.sec).timetuple()

        self.assertTrue(_compareResults(self.cal.parse('08/25/2006', start), target))
        self.assertTrue(_compareResults(self.cal.parse('08.25.2006', start), target))
        self.assertTrue(_compareResults(self.cal.parse('8/25/6',     start), target))
        self.assertTrue(_compareResults(self.cal.parse('8/25',       start), target))
        self.assertTrue(_compareResults(self.cal.parse('8.25',       start), target))
        self.assertTrue(_compareResults(self.cal.parse('08/25',      start), target))

          # target is the start time since days 35 is not valid
        self.assertTrue(_compareResults(self.cal.parse('08/35', start), start))

          # target is the start time since months 18 is not valid
        self.assertTrue(_compareResults(self.cal.parse('18/35', start), start))

    def testSpecialTimes(self):
        start = datetime.datetime(self.yr, self.mth, self.dy, self.hr, self.mn, self.sec).timetuple()

        target = datetime.datetime(self.yr, self.mth, self.dy, 6, 0, 0).timetuple()
        self.assertTrue(_compareResults(self.cal.parse('morning', start), target))

        target = datetime.datetime(self.yr, self.mth, self.dy, 9, 0, 0).timetuple()
        self.assertTrue(_compareResults(self.cal.parse('breakfast', start), target))

        target = datetime.datetime(self.yr, self.mth, self.dy, 12, 0, 0).timetuple()
        self.assertTrue(_compareResults(self.cal.parse('noon', start), target))

        target = datetime.datetime(self.yr, self.mth, self.dy, 12, 0, 0).timetuple()
        self.assertTrue(_compareResults(self.cal.parse('lunch', start), target))

        target = datetime.datetime(self.yr, self.mth, self.dy, 18, 0, 0).timetuple()
        self.assertTrue(_compareResults(self.cal.parse('evening', start), target))

        target = datetime.datetime(self.yr, self.mth, self.dy, 19, 0, 0).timetuple()
        self.assertTrue(_compareResults(self.cal.parse('dinner', start), target))

        target = datetime.datetime(self.yr, self.mth, self.dy, 21, 0, 0).timetuple()
        self.assertTrue(_compareResults(self.cal.parse('night',   start), target))
        self.assertTrue(_compareResults(self.cal.parse('tonight', start), target)) 

        target = datetime.datetime(self.yr, self.mth, self.dy, 0, 0, 0).timetuple()
        self.assertTrue(_compareResults(self.cal.parse('midnight', start), target))


    def testFormattedDates(self):
        start  = datetime.datetime(self.yr, self.mth, self.dy, self.hr, self.mn, self.sec).timetuple()
        target = datetime.datetime(2006, 8, 25, 0, 0, 0).timetuple()

          # TODO - these all should be either passing or failing - not both
          # W3CDTF (yyy-mm-dd)
        self.assertTrue(_compareResults(self.cal.parse('2006-08-25',                    start), target))

        target = datetime.datetime(2006, 8, 25, 10, 11, 12).timetuple()

          # W3CDTF (UTC timezone)
        self.assertTrue(_compareResults(self.cal.parse('2006-08-25T10:11:12EST',        start), target))
          # W3CDTF (numeric timezone)
        self.assertTrue(_compareResults(self.cal.parse('2006-08-25T10:11:12-05:00',     start), target))
          # RFC822 (4 digit year)
        self.assertTrue(_compareResults(self.cal.parse('Fri, 25 Aug 2006 10:11:12 EST', start), target))


    def testJunk(self):
        start = datetime.datetime(self.yr, self.mth, self.dy, self.hr, self.mn, self.sec).timetuple()

        self.assertTrue(_compareResults(self.cal.parse('foo',                 start), start))
        self.assertTrue(_compareResults(self.cal.parse('the quick brown fox', start), start))
        self.assertTrue(_compareResults(self.cal.parse('2 donuts',            start), start))
        self.assertTrue(_compareResults(self.cal.parse('3 walrus',            start), start))
        self.assertTrue(_compareResults(self.cal.parse('4 monkey',            start), start))


if __name__ == "__main__":
    unittest.main()
