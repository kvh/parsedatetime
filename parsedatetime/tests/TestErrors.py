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

    def testErrors(self):
        s     = datetime.datetime.now()
        start = s.timetuple()

        self.assertTrue(_compareResults(self.cal.parse('01/0',   start), (start, 0)))
        self.assertTrue(_compareResults(self.cal.parse('08/35',  start), (start, 0)))
        self.assertTrue(_compareResults(self.cal.parse('18/35',  start), (start, 0)))
        self.assertTrue(_compareResults(self.cal.parse('1799',   start), (start, 0)))
        self.assertTrue(_compareResults(self.cal.parse('781',    start), (start, 0)))
        self.assertTrue(_compareResults(self.cal.parse('2702',   start), (start, 0)))
        self.assertTrue(_compareResults(self.cal.parse('78',     start), (start, 0)))
        self.assertTrue(_compareResults(self.cal.parse('11',     start), (start, 0)))
        self.assertTrue(_compareResults(self.cal.parse('1',      start), (start, 0)))
        self.assertTrue(_compareResults(self.cal.parse('174565', start), (start, 0)))
        self.assertTrue(_compareResults(self.cal.parse('177505', start), (start, 0)))


if __name__ == "__main__":
    unittest.main()
