#!/usr/bin/env python

"""
Parse human-readable date/time text.
"""

__license__ = """Copyright (c) 2004-2006 Mike Taylor, All rights reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
__author__       = 'Mike Taylor <http://code-bear.com>'
__contributors__ = ['Darshana Chhajed <mailto://darshana@osafoundation.org>',
                   ]

_debug = False


import string, re, time
import datetime, calendar, rfc822
import parsedatetime_consts


# Copied from feedparser.py
# Universal Feedparser, Copyright (c) 2002-2006, Mark Pilgrim, All rights reserved.
# Originally a def inside of _parse_date_w3dtf()
def _extract_date(m):
    year = int(m.group('year'))
    if year < 100:
        year = 100 * int(time.gmtime()[0] / 100) + int(year)
    if year < 1000:
        return 0, 0, 0
    julian = m.group('julian')
    if julian:
        julian = int(julian)
        month = julian / 30 + 1
        day = julian % 30 + 1
        jday = None
        while jday != julian:
            t = time.mktime((year, month, day, 0, 0, 0, 0, 0, 0))
            jday = time.gmtime(t)[-2]
            diff = abs(jday - julian)
            if jday > julian:
                if diff < day:
                    day = day - diff
                else:
                    month = month - 1
                    day = 31
            elif jday < julian:
                if day + diff < 28:
                   day = day + diff
                else:
                    month = month + 1
        return year, month, day
    month = m.group('month')
    day = 1
    if month is None:
        month = 1
    else:
        month = int(month)
        day = m.group('day')
        if day:
            day = int(day)
        else:
            day = 1
    return year, month, day

# Copied from feedparser.py 
# Universal Feedparser, Copyright (c) 2002-2006, Mark Pilgrim, All rights reserved.
# Originally a def inside of _parse_date_w3dtf()
def _extract_time(m):
    if not m:
        return 0, 0, 0
    hours = m.group('hours')
    if not hours:
        return 0, 0, 0
    hours = int(hours)
    minutes = int(m.group('minutes'))
    seconds = m.group('seconds')
    if seconds:
        seconds = int(seconds)
    else:
        seconds = 0
    return hours, minutes, seconds


# Copied from feedparser.py
# Universal Feedparser, Copyright (c) 2002-2006, Mark Pilgrim, All rights reserved.
# Modified to return a tuple instead of mktime
#
# Original comment:
#       W3DTF-style date parsing adapted from PyXML xml.utils.iso8601, written by
#       Drake and licensed under the Python license.  Removed all range checking
#       for month, day, hour, minute, and second, since mktime will normalize
#       these later
def _parse_date_w3dtf(dateString):
    # the __extract_date and __extract_time methods were
    # copied-out so they could be used by my code --bear
    def __extract_tzd(m):
        '''Return the Time Zone Designator as an offset in seconds from UTC.'''
        if not m:
            return 0
        tzd = m.group('tzd')
        if not tzd:
            return 0
        if tzd == 'Z':
            return 0
        hours = int(m.group('tzdhours'))
        minutes = m.group('tzdminutes')
        if minutes:
            minutes = int(minutes)
        else:
            minutes = 0
        offset = (hours*60 + minutes) * 60
        if tzd[0] == '+':
            return -offset
        return offset

    __date_re = ('(?P<year>\d\d\d\d)'
                 '(?:(?P<dsep>-|)'
                 '(?:(?P<julian>\d\d\d)'
                 '|(?P<month>\d\d)(?:(?P=dsep)(?P<day>\d\d))?))?')
    __tzd_re = '(?P<tzd>[-+](?P<tzdhours>\d\d)(?::?(?P<tzdminutes>\d\d))|Z)'
    __tzd_rx = re.compile(__tzd_re)
    __time_re = ('(?P<hours>\d\d)(?P<tsep>:|)(?P<minutes>\d\d)'
                 '(?:(?P=tsep)(?P<seconds>\d\d(?:[.,]\d+)?))?'
                 + __tzd_re)
    __datetime_re = '%s(?:T%s)?' % (__date_re, __time_re)
    __datetime_rx = re.compile(__datetime_re)
    m = __datetime_rx.match(dateString)
    if (m is None) or (m.group() != dateString): return
    return _extract_date(m) + _extract_time(m) + (0, 0, 0)


# Copied from feedparser.py
# Universal Feedparser, Copyright (c) 2002-2006, Mark Pilgrim, All rights reserved.
# Modified to return a tuple instead of mktime
#
def _parse_date_rfc822(dateString):
    '''Parse an RFC822, RFC1123, RFC2822, or asctime-style date'''
    data = dateString.split()
    if data[0][-1] in (',', '.') or data[0].lower() in rfc822._daynames:
        del data[0]
    if len(data) == 4:
        s = data[3]
        i = s.find('+')
        if i > 0:
            data[3:] = [s[:i], s[i+1:]]
        else:
            data.append('')
        dateString = " ".join(data)
    if len(data) < 5:
        dateString += ' 00:00:00 GMT'
    return rfc822.parsedate_tz(dateString)

# rfc822.py defines several time zones, but we define some extra ones.
# 'ET' is equivalent to 'EST', etc.
_additional_timezones = {'AT': -400, 'ET': -500, 'CT': -600, 'MT': -700, 'PT': -800}
rfc822._timezones.update(_additional_timezones)


class Calendar:
    """
    A collection of routines to input, parse and manipulate date and times.
    The text can either be 'normal' date values or it can be human readable.
    """

    def __init__(self, constants=None):
          # if a constants reference is not included, use default
        if constants is None:
            self.ptc = parsedatetime_consts.CalendarConstants()
        else:
            self.ptc = constants

        self.CRE_SPECIAL   = re.compile(self.ptc.RE_SPECIAL,   re.IGNORECASE)
        self.CRE_UNITS     = re.compile(self.ptc.RE_UNITS,     re.IGNORECASE)
        self.CRE_QUNITS    = re.compile(self.ptc.RE_QUNITS,    re.IGNORECASE)
        self.CRE_MODIFIER  = re.compile(self.ptc.RE_MODIFIER,  re.IGNORECASE)
        self.CRE_MODIFIER2 = re.compile(self.ptc.RE_MODIFIER2, re.IGNORECASE)
        self.CRE_TIMEHMS   = re.compile(self.ptc.RE_TIMEHMS,   re.IGNORECASE)
        self.CRE_TIMEHMS2  = re.compile(self.ptc.RE_TIMEHMS2,  re.IGNORECASE)
        self.CRE_DATE      = re.compile(self.ptc.RE_DATE,      re.IGNORECASE)
        self.CRE_DATE2     = re.compile(self.ptc.RE_DATE2,     re.IGNORECASE)
        self.CRE_DATE3     = re.compile(self.ptc.RE_DATE3,     re.IGNORECASE)
        self.CRE_MONTH     = re.compile(self.ptc.RE_MONTH,     re.IGNORECASE)
        self.CRE_WEEKDAY   = re.compile(self.ptc.RE_WEEKDAY,   re.IGNORECASE)
        self.CRE_DAY       = re.compile(self.ptc.RE_DAY,       re.IGNORECASE)
        self.CRE_TIME      = re.compile(self.ptc.RE_TIME,      re.IGNORECASE)
        self.CRE_REMAINING = re.compile(self.ptc.RE_REMAINING, re.IGNORECASE)

        self.invalidFlag   = 0  # Is set if the datetime string entered cannot be parsed at all
        self.weekdyFlag    = 0  # monday/tuesday/...
        self.dateStdFlag   = 0  # 07/21/06
        self.dateStrFlag   = 0  # July 21st, 2006
        self.timeFlag      = 0  # 5:50 
        self.meridianFlag  = 0  # am/pm
        self.dayStrFlag    = 0  # tomorrow/yesterday/today/..
        self.timeStrFlag   = 0  # lunch/noon/breakfast/...
        self.modifierFlag  = 0  # after/before/prev/next/..
        self.modifier2Flag = 0  # after/before/prev/next/..
        self.unitsFlag     = 0  # hrs/weeks/yrs/min/..
        self.qunitsFlag    = 0  # h/m/t/d..


    def _convertUnitAsWords(self, unitText):
        """
        Converts text units into their number value

        Five = 5
        Twenty Five = 25
        Two hundred twenty five = 225
        Two thousand and twenty five = 2025
        Two thousand twenty five = 2025
        """
        # TODO: implement this
        pass


    def _buildTime(self, source, quantity, modifier, units):
        """
        Take quantity, modifier and unit strings and convert them into values.
        Then calcuate the time and return the adjusted sourceTime
        """

        if _debug:
            print '_buildTime: [%s][%s][%s]' % (quantity, modifier, units)

        if source is None:
            source = time.localtime()

        if quantity is None:
            quantity = ''
        else:
            quantity = string.strip(quantity)

        if len(quantity) == 0:
            qty = 1
        else:
            try:
                qty = int(quantity)
            except ValueError:
                qty = 0

        if modifier in self.ptc.Modifiers:
            qty = qty * self.ptc.Modifiers[modifier]

            if units is None or units == '':
                units = 'dy'

        # plurals are handled by regex's (could be a bug tho)

        if units in self.ptc.Units:
            u = self.ptc.Units[units]
        else:
            u = 1

        (yr, mth, dy, hr, mn, sec, wd, yd, isdst) = source

        start  = datetime.datetime(yr, mth, dy, hr, mn, sec)
        target = start

        if units.startswith('y'):
            target = self.inc(start, year=qty)
        elif units.endswith('th') or units.endswith('ths'):
            target = self.inc(start, month=qty)
        else:
            if units.startswith('d'):
                target = start + datetime.timedelta(days=qty)
            elif units.startswith('h'):
                target = start + datetime.timedelta(hours=qty)
            elif units.startswith('m'):
                target = start + datetime.timedelta(minutes=qty)
            elif units.startswith('s'):
                target = start + datetime.timedelta(seconds=qty)
            elif units.startswith('w'):
                target = start + datetime.timedelta(weeks=qty)

        if target != start:
            self.invalidFlag = 0

        return target.timetuple()


    def parseDate(self, dateString):
        """
        parses date strings like 05/28/200 or 04.21 and evaluates them
        """
        yr, mth, dy, hr, mn, sec, wd, yd, isdst = time.localtime()

        s = dateString
        m = self.CRE_DATE2.search(s)
        if m is not None:
            indx = m.start()
            mth  = int(s[:indx])
            s    = s[indx + 1:]

        m = self.CRE_DATE2.search(s)
        if m is not None:
            indx = m.start()
            dy   = int(s[:indx])
            yr   = int(s[indx + 1:])
            # TODO should this have a birthday epoch constraint?
            if yr < 99:
                yr += 2000
        else:
            dy = int(string.strip(s))

        if mth <= 12 and dy <= self.ptc.DaysInMonthList[mth - 1]:
            sourceTime = (yr, mth, dy, hr, mn, sec, wd, yd, isdst)
        else:
            self.invalidFlag = 1
            sourceTime       = time.localtime() #return current time if date string is invalid

        return sourceTime


    def parseDateText(self, dateString):
        """
        Parses date strings like "May 31st, 2006" or "Jan 1st" or "July 2006"
        """
        yr, mth, dy, hr, mn, sec, wd, yd, isdst = time.localtime()

        currentMth = mth
        currentDy  = dy

        s   = dateString.lower()
        m   = self.CRE_DATE3.search(s)
        mth = m.group('mthname')
        mth = int(self.ptc.MthNames[mth])

        if m.group('day') !=  None:
            dy = int(m.group('day'))
        else:
            dy = 1

        if m.group('year') !=  None:
            yr = int(m.group('year'))
        elif (mth < currentMth) or (mth == currentMth and dy < currentDy):
            # if that day and month have already passed in this year,
            # then increment the year by 1
            yr += 1

        if dy <= self.ptc.DaysInMonthList[mth - 1]:
            sourceTime = (yr, mth, dy, 9, 0, 0, wd, yd, isdst)
        else:
              # Return current time if date string is invalid
            self.invalidFlag = 1
            sourceTime       = time.localtime()

        return sourceTime


    def evalModifier(self, modifier, str1 , str2, totalTime):
        """
        Evaluates the string if there is a modifier in it
        """
        offset = self.ptc.Modifiers[modifier]

        if totalTime is not None:
            (yr, mth, dy, hr, mn, sec, wd, yd, isdst) = totalTime
        else:
            (yr, mth, dy, hr, mn, sec, wd, yd, isdst) = time.localtime()

        # capture the units after the modifier and the remaining string after the unit
        m = self.CRE_REMAINING.search(str2)
        if m is not None:
            indx = m.start() + 1
            unit = str2[:m.start()]
            str2 = str2[indx:]
        else:
            unit = str2
            str2 = ''

        flag = 0

        if unit == self.ptc.Target_Text['month'] or \
           unit == self.ptc.Target_Text['mth']:
            if offset == 0:
                dy        = self.ptc.DaysInMonthList[mth - 1]
                totalTime = (yr, mth, dy, 9, 0, 0, wd, yd, isdst)
            elif offset == 2:
                # if day is the last day of the month, calculate the last day of the next month
                if dy == self.ptc.DaysInMonthList[mth - 1]:
                    dy = self.ptc.DaysInMonthList[mth]

                start     = datetime.datetime(yr, mth, dy, 9, 0, 0)
                target    = self.inc(start, month=1)
                totalTime = target.timetuple()
            else:
                start     = datetime.datetime(yr, mth, 1, 9, 0, 0)
                target    = self.inc(start, month=offset)
                totalTime = target.timetuple()

            flag = 1

        if unit == self.ptc.Target_Text['week'] or \
             unit == self.ptc.Target_Text['wk'] or \
             unit == self.ptc.Target_Text['w']:
            if offset == 0:
                start     = datetime.datetime(yr, mth, dy, 17, 0, 0)
                target    = start + datetime.timedelta(days=(4-wd))
                totalTime = target.timetuple()
            elif offset == 2:
                start     = datetime.datetime(yr, mth, dy, 9, 0, 0)
                target    = start + datetime.timedelta(days=7)
                totalTime = target.timetuple()
            else:
                return self.evalModifier(modifier, str1, "monday "+str2, totalTime)

            flag = 1

        if unit == self.ptc.Target_Text['day'] or \
            unit == self.ptc.Target_Text['dy'] or \
            unit == self.ptc.Target_Text['d']:
            if offset == 0:
                totalTime = (yr, mth, dy, 17, 0, 0, wd, yd, isdst)
            elif offset == 2:
                start     = datetime.datetime(yr, mth, dy, hr, mn, sec)
                target    = start + datetime.timedelta(days=1)
                totalTime = target.timetuple()
            else:
                start     = datetime.datetime(yr, mth, dy, 9, 0, 0)
                target    = start + datetime.timedelta(days=offset)
                totalTime = target.timetuple()

            flag = 1

        if unit == self.ptc.Target_Text['hour'] or \
           unit == self.ptc.Target_Text['hr']:
            if offset == 0:
                totalTime = (yr, mth, dy, hr, 0, 0, wd, yd, isdst)
            else:
                start     = datetime.datetime(yr, mth, dy, hr, 0, 0)
                target    = start + datetime.timedelta(hours=offset)
                totalTime = target.timetuple()

            flag = 1

        if unit == self.ptc.Target_Text['year'] or \
             unit == self.ptc.Target_Text['yr'] or \
             unit == self.ptc.Target_Text['y']:
            if offset == 0:
                totalTime = (yr, 12, 31, hr, mn, sec, wd, yd, isdst)
            elif offset == 2:
                totalTime = (yr+1, mth, dy, hr, mn, sec, wd, yd, isdst)
            else:
                totalTime = (yr+offset, 1, 1, 9, 0, 0, wd, yd, isdst)

            flag = 1

        if flag == 0:
            m = self.CRE_WEEKDAY.match(unit)
            if m is not None:
                wkdy = m.group()
                wkdy = self.ptc.WeekDays[wkdy]

                if offset == 0:
                    diff      = wkdy - wd
                    start     = datetime.datetime(yr, mth, dy, 9, 0, 0)
                    target    = start + datetime.timedelta(days=diff)
                    totalTime = target.timetuple()
                else:
                    diff      = wkdy - wd
                    start     = datetime.datetime(yr, mth, dy, 9, 0, 0)
                    target    = start + datetime.timedelta(days=diff + 7 * offset)
                    totalTime = target.timetuple()
                flag = 1

        if flag == 0:
            m = self.CRE_TIME.match(unit)
            if m is not None:
                ((yr, mth, dy, hr, mn, sec, wd, yd, isdst),self.invalidFlag) = self.parse(unit)
                start     = datetime.datetime(yr, mth, dy, hr, mn, sec)
                target    = start + datetime.timedelta(days=offset)
                totalTime = target.timetuple()

                flag              = 1
                self.modifierFlag = 0

        # if the word after next is a number, the string is likely to be something like 
        # "next 4 hrs" for which we have to combine the units with the rest of the string
        if flag == 0:
            if offset < 0:
                # if offset is negative, the unit has to be made negative
                unit = '-' + unit
            str2 = '%s %s' % (unit, str2)

        str = '%s %s' % (str1, str2)

        self.modifierFlag = 0

        return str, totalTime


    def evalModifier2(self, modifier, str1 , str2, totalTime):
        """
        Evaluates the string if there is a modifier in it
        """
        offset = self.ptc.Modifiers[modifier]

        if totalTime is not None:
            (yr, mth, dy, hr, mn, sec, wd, yd, isdst) = totalTime
        else:
            (yr, mth, dy, hr, mn, sec, wd, yd, isdst) = time.localtime()

        self.modifier2Flag = 0

        # If the string after the negative modifier starts with digits, then it is likely that the
        # string is similar to " before 3 days" or 'evening prior to 3 days'
        # In this case, the total time is calculated by subtracting '3 days' from the current date.
        # So, we have to identify the quantity and negate it before parsing the string.
        # This is not required for strings not starting with digits since the string is enough to 
        # calculate the totalTime
        if offset < 0:
            digit = r'\d+'

            m = re.match(digit, string.strip(str2))
            if m is not None:
                qty  = int(m.group())*(-1)
                str2 = str2[m.end():]
                str2 = '%d%s' % (qty, str2)

        totalTime, flag = self.parse(str2, totalTime)

        if str1 != '':
            if offset < 0:
                digit = r'\d+'

                m = re.match(digit, string.strip(str1))
                if m is not None:
                    qty  = int(m.group())*(-1)
                    str1 = str1[m.end():]
                    str1 = '%d%s' % (qty, str1)

            totalTime, flag = self.parse (str1, totalTime) 

        return '', totalTime


    def parse(self, datetimeString, sourceTime=None):
        """
        Splits the string into tokens, finds the regex matches and helps evaluate the datetime
        """
        s         = string.strip(datetimeString.lower())
        dateStr   = ''
        parseStr  = ''
        totalTime = sourceTime

        self.invalidFlag = 0

        if s == '' :
            if sourceTime is not None:
                return (sourceTime, 0)
            else:
                return (time.localtime(), 1)

        while len(s) > 0:
            flag = 0
            str1 = ''
            str2 = ''

            if _debug:
                print 'parse (top of loop): [%s][%s]' % (s, parseStr)

            if parseStr == '':
                # Modifier like next\prev..
                m = self.CRE_MODIFIER.search(s)
                if m is not None:
                    self.modifierFlag = 1
                    if (m.group('modifier') != s):
                        # capture remaining string
                        parseStr = m.group('modifier')
                        str1     = string.strip(s[:m.start('modifier')])
                        str2     = string.strip(s[m.end('modifier'):])
                        flag     = 1
                    else:
                        parseStr = s

            if parseStr == '':
                # Modifier like from\after\prior..
                m = self.CRE_MODIFIER2.search(s)
                if m is not None:
                    self.modifier2Flag = 1
                    if (m.group('modifier') != s):
                        # capture remaining string
                        parseStr = m.group('modifier')
                        str1     = string.strip(s[:m.start('modifier')])
                        str2     = string.strip(s[m.end('modifier'):])
                        flag     = 1
                    else:
                        parseStr = s

            if parseStr == '':
                # String date format
                m = self.CRE_DATE3.search(s)
                if m is not None:
                    self.dateStrFlag = 1
                    if (m.group('date') != s):
                        # capture remaining string
                        parseStr = m.group('date')
                        str1     = s[:m.start('date')]
                        str2     = s[m.end('date'):]
                        s        = '%s %s' % (str1, str2)
                        flag     = 1
                    else:
                        parseStr = s

            if parseStr == '':
                # Standard date format
                m = self.CRE_DATE.search(s)
                if m is not None:
                    self.dateStdFlag = 1
                    if (m.group('date') != s):
                        # capture remaining string
                        parseStr = m.group('date')
                        str1     = s[:m.start('date')]
                        str2     = s[m.end('date'):]
                        s        = '%s %s' % (str1, str2)
                        flag     = 1
                    else:
                        parseStr = s

            if parseStr == '':
                # Natural language day strings
                m = self.CRE_DAY.search(s)
                if m is not None:
                    self.dayStrFlag = 1
                    if (m.group('day') != s):
                        # capture remaining string
                        parseStr = m.group('day')
                        str1     = s[:m.start('day')]
                        str2     = s[m.end('day'):]
                        s        = '%s %s' % (str1, str2)
                        flag     = 1
                    else:
                        parseStr = s

            if parseStr == '':
                # Quantity + Units
                m = self.CRE_UNITS.search(s)
                if m is not None:
                    self.unitsFlag = 1
                    if (m.group('qty') != s):
                        # capture remaining string
                        parseStr = m.group('qty')
                        str1     = s[:m.start('qty')]
                        str2     = s[m.end('qty'):]
                        s        = '%s %s' % (str1, str2)
                        flag     = 1
                    else:
                        parseStr = s

            if parseStr == '':
                # Quantity + Units
                m = self.CRE_QUNITS.search(s)
                if m is not None:
                    self.qunitsFlag = 1
                    if (m.group('qty') != s):
                        # capture remaining string
                        parseStr = m.group('qty')
                        str1     = s[:m.start('qty')]
                        str2     = s[m.end('qty'):]
                        s        = '%s %s' % (str1, str2)
                        flag     = 1
                    else:
                        parseStr = s 

            if parseStr == '':
                # Weekday
                m = self.CRE_WEEKDAY.search(s)
                if m is not None:
                    self.weekdyFlag = 1
                    if (m.group('weekday') != s):
                        # capture remaining string
                        parseStr = m.group()
                        str1     = s[:m.start('weekday')]
                        str2     = s[m.end('weekday'):]
                        s        = '%s %s' % (str1, str2)
                        flag     = 1
                    else:
                        parseStr = s

            if parseStr == '':
                # Natural language time strings
                m = self.CRE_TIME.search(s)
                if m is not None:
                    self.timeStrFlag = 1
                    if (m.group('time') != s):
                        # capture remaining string
                        parseStr = m.group('time')
                        str1     = s[:m.start('time')]
                        str2     = s[m.end('time'):]
                        s        = '%s %s' % (str1, str2)
                        flag     = 1
                    else:
                        parseStr = s

            if parseStr == '':
                # HH:MM(:SS) am/pm time strings
                m = self.CRE_TIMEHMS2.search(s)
                if m is not None:
                    self.meridianFlag = 1
                    if m.group('minutes') is not None:
                        if m.group('seconds') is not None:
                            parseStr = m.group('hours')+':'+m.group('minutes')+':'+m.group('seconds')+' '+m.group('meridian')
                            str1     = s[:m.start('hours')]
                            str2     = s[m.end('meridian'):]
                        else:
                            parseStr = m.group('hours')+':'+m.group('minutes')+' '+m.group('meridian')
                            str1     = s[:m.start('hours')]
                            str2     = s[m.end('meridian'):] 
                    else:
                        parseStr = m.group('hours')+' '+m.group('meridian')
                        str1     = s[:m.start('hours')]
                        str2     = s[m.end('meridian'):]

                    s    = '%s %s' % (str1, str2)
                    flag = 1

            if parseStr == '':
                # HH:MM(:SS) time strings
                m = self.CRE_TIMEHMS.search(s)
                if m is not None:
                    self.timeFlag = 1
                    if m.group('seconds') is not None:
                        parseStr = m.group('hours')+':'+m.group('minutes')+':'+m.group('seconds')
                        str1     = s[:m.start('hours')]
                        str2     = s[m.end('seconds'):]
                    else:
                        parseStr = m.group('hours')+':'+m.group('minutes')
                        str1     = s[:m.start('hours')]
                        str2     = s[m.end('minutes'):]

                    s    = '%s %s' % (str1, str2)
                    flag = 1

            # if string does not match any regex, empty string to come out of the while loop
            if flag is 0:
                s = ''

            if _debug:
                print 'parse (bottom) [%s][%s][%s][%s]' % (s, parseStr, str1, str2)
                print 'invalid [%d] weekday [%d] dateStd [%d] dateStr [%d] time [%d] timeStr [%d] meridian [%d]' % \
                       (self.invalidFlag, self.weekdyFlag, self.dateStdFlag, self.dateStrFlag, self.timeFlag, self.timeStrFlag, self.meridianFlag)
                print 'dayStr [%d] modifier [%d] modifier2 [%d] units [%d] qunits[%d]' % \
                       (self.dayStrFlag, self.modifierFlag, self.modifier2Flag, self.unitsFlag, self.qunitsFlag)

            # evaluate the matched string
            if parseStr != '':
                if self.modifierFlag == 1:
                    str, totalTime = self.evalModifier(parseStr, str1, str2, totalTime)

                    return self.parse(str, totalTime)

                elif self.modifier2Flag == 1:
                    s, totalTime = self.evalModifier2(parseStr, str1, str2, totalTime)
                else:
                    totalTime = self.evalString(parseStr, totalTime)
                    parseStr  = ''

        # String is not parsed at all
        if totalTime is None or totalTime == sourceTime:
            totalTime        = time.localtime()
            self.invalidFlag = 1

        return (totalTime, self.invalidFlag)


    def evalString(self, datetimeString, sourceTime=None):
        """
        Parses datetimeString and return time tuple which the expression represents.
        """

        s = string.strip(datetimeString)

          # Given string date is a RFC822 date
        if sourceTime is None:
            sourceTime = _parse_date_rfc822(s)

          # Given string date is a W3CDTF date
        if sourceTime is None:
            sourceTime = _parse_date_w3dtf(s)

        if sourceTime is None:
            s = s.lower()

          # Given string is in the format HH:MM(:SS)(am/pm)
        if self.meridianFlag == 1:
            if sourceTime is None:
                (yr, mth, dy, hr, mn, sec, wd, yd, isdst) = time.localtime()
            else:
                (yr, mth, dy, hr, mn, sec, wd, yd, isdst) = sourceTime

            m = self.CRE_TIMEHMS2.search(s)
            if m is not None:
                dt = s[:m.start('meridian')].strip()
                if len(dt) <= 2:
                    hr  = int(dt)
                    mn  = 0
                    sec = 0
                else:
                    hr, mn, sec = _extract_time(m)

                if hr == 24:
                    hr = 0

                sourceTime = (yr, mth, dy, hr, mn, sec, wd, yd, isdst)
                meridian   = m.group('meridian')

                if (re.compile("a").search(meridian)) and hr == 12:
                    sourceTime = (yr, mth, dy, 0, mn, sec, wd, yd, isdst)
                if (re.compile("p").search(meridian)) and hr < 12:
                    sourceTime = (yr, mth, dy, hr+12, mn, sec, wd, yd, isdst)

              # invalid time
            if hr > 24 or mn > 59 or sec > 59:
                sourceTime       = time.localtime()
                self.invalidFlag = 1

            self.meridianFlag = 0

          # Given string is in the format HH:MM(:SS)
        if self.timeFlag == 1:
            if sourceTime is None:
                (yr, mth, dy, hr, mn, sec, wd, yd, isdst) = time.localtime()
            else:
                (yr, mth, dy, hr, mn, sec, wd, yd, isdst) = sourceTime

            m = self.CRE_TIMEHMS.search(s)
            if m is not None:
                hr, mn, sec = _extract_time(m)
            if hr == 24:
                hr = 0

            if hr > 24 or mn > 59 or sec > 59:
                # invalid time
                sourceTime = time.localtime()
                self.invalidFlag = 1
            else:
                sourceTime = (yr, mth, dy, hr, mn, sec, wd, yd, isdst)

            self.timeFlag = 0

          # Given string is in the format 07/21/2006
        if self.dateStdFlag == 1:
            sourceTime       = self.parseDate(s)
            self.dateStdFlag = 0

          # Given string is in the format  "May 23rd, 2005"
        if self.dateStrFlag == 1:
            sourceTime       = self.parseDateText(s)
            self.dateStrFlag = 0

          # Given string is a weekday
        if self.weekdyFlag == 1:
            yr, mth, dy, hr, mn, sec, wd, yd, isdst = time.localtime()
            start = datetime.datetime(yr, mth, dy, hr, mn, sec)
            wkDy  = self.ptc.WeekDays[s]

            if wkDy > wd:
                qty    = wkDy - wd
                target = start + datetime.timedelta(days=qty)
                wd     = wkDy
            else:
                qty    = 6 - wd + wkDy + 1
                target = start + datetime.timedelta(days=qty)
                wd     = wkDy

            sourceTime      = target.timetuple()
            self.weekdyFlag = 0

          # Given string is a natural language time string like lunch, midnight, etc
        if self.timeStrFlag == 1:
            if sourceTime is None:
                (yr, mth, dy, hr, mn, sec, wd, yd, isdst) = time.localtime()
            else:
                (yr, mth, dy, hr, mn, sec, wd, yd, isdst) = sourceTime

            sources = { 'now':       (yr, mth, dy, hr, mn, sec, wd, yd, isdst),
                        'noon':      (yr, mth, dy, 12,  0,   0, wd, yd, isdst),
                        'lunch':     (yr, mth, dy, 12,  0,   0, wd, yd, isdst),
                        'morning':   (yr, mth, dy,  6,  0,   0, wd, yd, isdst),
                        'breakfast': (yr, mth, dy,  8,  0,   0, wd, yd, isdst),
                        'dinner':    (yr, mth, dy, 19,  0,   0, wd, yd, isdst),
                        'evening':   (yr, mth, dy, 18,  0,   0, wd, yd, isdst),
                        'midnight':  (yr, mth, dy,  0,  0,   0, wd, yd, isdst),
                        'night':     (yr, mth, dy, 21,  0,   0, wd, yd, isdst),
                        'tonight':   (yr, mth, dy, 21,  0,   0, wd, yd, isdst),
                      }

            if s in sources:
                sourceTime = sources[s]
            else:
                sourceTime       = time.localtime()
                self.invalidFlag = 1

            self.timeStrFlag = 0

           # Given string is a natural language date string like today, tomorrow..
        if self.dayStrFlag == 1:
            if sourceTime is None:
                sourceTime = time.localtime()

            (yr, mth, dy, hr, mn, sec, wd, yd, isdst) = sourceTime

            sources = { 'tomorrow':   1,
                        'today':      0,
                        'yesterday': -1,
                       }

            start      = datetime.datetime(yr, mth, dy, 9, 0, 0)
            target     = start + datetime.timedelta(days=sources[s])
            sourceTime = target.timetuple()

            self.dayStrFlag = 0

          # Given string is a time string with units like "5 hrs 30 min"
        if self.unitsFlag == 1:
            modifier = ''  # TODO

            if sourceTime is None:
                sourceTime = time.localtime()

            m = self.CRE_UNITS.search(s)
            if m is not None:
                units    = m.group('units')
                quantity = s[:m.start('units')]

            sourceTime     = self._buildTime(sourceTime, quantity, modifier, units)
            self.unitsFlag = 0

          # Given string is a time string with single char units like "5 h 30 m"
        if self.qunitsFlag == 1:
            modifier = ''  # TODO

            if sourceTime is None:
                sourceTime = time.localtime()

            m = self.CRE_QUNITS.search(s)
            if m is not None:
                units    = m.group('qunits')
                quantity = s[:m.start('qunits')]

            sourceTime      = self._buildTime(sourceTime, quantity, modifier, units)
            self.qunitsFlag = 0

          # Given string does not match anything
        if sourceTime is None:
            sourceTime       = time.localtime()
            self.invalidFlag = 1

        return sourceTime


    def inc(self, source, month=None, year=None):
        """
        Takes the given date, or current date if none is passed, and increments
        it according to the values passed in by month and/or year.

        This routine is needed because the timedelta() routine does not
        allow for month or year increments.
        """
        yr  = source.year
        mth = source.month

        if year:
            try:
                yi = int(year)
            except ValueError:
                yi = 0

            yr += yi

        if month:
            try:
                mi = int(month)
            except ValueError:
                mi = 0

            m = abs(mi)
            y = m / 12      # how many years are in month increment
            m = m % 12      # get remaining months

            if mi < 0:
                mth = mth - m           # sub months from start month
                if mth < 1:             # cross start-of-year?
                    y   -= 1            #   yes - decrement year
                    mth += 12           #         and fix month
            else:
                mth = mth + m           # add months to start month
                if mth > 12:            # cross end-of-year?
                    y   += 1            #   yes - increment year
                    mth -= 12           #         and fix month

            yr += y

        d = source.replace(year=yr, month=mth)

        return source + (d - source)

    #
    # TODO
    #
    #  - convert 'five' to 5 and also 'twenty five' to 25
    #  - incorporate RE changes to make them non-capture (suggested by jemfinch):
    #      RE_SPECIAL  = r'(?P<special>^(?:in|last|next))\s+'
    #      RE_UNITS    = r'\s+(?P<units>(?:hour|minute|second|day|week|month|year))'
    #      RE_QUNITS   = r'(?P<qunits>[0-9]+[hmsdwmy])'
    #      RE_MODIFIER = r'(?P<modifier>(?:from|before|after|ago|prior))\s+'
  
   