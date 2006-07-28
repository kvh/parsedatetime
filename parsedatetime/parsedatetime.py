#!/usr/bin/env python

"""
Parse human-readable date/time text.
"""

__version__ = '0.6'
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
        self.CRE_MERIDIAN  = re.compile(self.ptc.RE_MERIDIAN,  re.IGNORECASE)
        self.CRE_TIMEHM    = re.compile(self.ptc.RE_TIMEHM,    re.IGNORECASE)
        self.CRE_TIMEHM2   = re.compile(self.ptc.RE_TIMEHM2,   re.IGNORECASE)
        self.CRE_TIMEHMS   = re.compile(self.ptc.RE_TIMEHMS,   re.IGNORECASE)
        self.CRE_TIMEHMS2  = re.compile(self.ptc.RE_TIMEHMS2,  re.IGNORECASE)
        self.CRE_DATE      = re.compile(self.ptc.RE_DATE,      re.IGNORECASE)
        self.CRE_DATE2     = re.compile(self.ptc.RE_DATE2,     re.IGNORECASE)
        self.CRE_REMAINING = re.compile(self.ptc.RE_REMAINING, re.IGNORECASE)


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


    def _buildSourceTime(self, sourceTime, target='now', modifier=None):
        """
        Determine what the source time will be for the given target
        """

        if sourceTime is None:
            yr, mth, dy, hr, mn, sec, wd, yd, isdst = time.localtime()
        else:
            (yr, mth, dy, hr, mn, sec, wd, yd, isdst) = sourceTime

        if target is None:
            target = 'now'
        else:
            target = string.strip(target).lower()

        if modifier is None:
            offset_modifier = 1
        else:
            if self.ptc.Modifiers.has_key(modifier):
                offset_modifier = self.ptc.Modifiers[modifier]
            else:
                offset_modifier = 1

        sources = { 'now':       (yr, mth, dy, hr, mn, sec, wd, yd, isdst),
                    'noon':      (yr, mth, dy, 12,  0,   0, wd, yd, isdst),
                    'lunch':     (yr, mth, dy, 12,  0,   0, wd, yd, isdst),
                    'morning':   (yr, mth, dy,  6,  0,   0, wd, yd, isdst),
                    'breakfast': (yr, mth, dy,  9,  0,   0, wd, yd, isdst),
                    'dinner':    (yr, mth, dy, 19,  0,   0, wd, yd, isdst),
                    'evening':   (yr, mth, dy, 18,  0,   0, wd, yd, isdst),
                    'midnight':  (yr, mth, dy,  0,  0,   0, wd, yd, isdst),
                    'night':     (yr, mth, dy, 21,  0,   0, wd, yd, isdst),
                    'tonight':   (yr, mth, dy, 21,  0,   0, wd, yd, isdst),
                  }

        source = (yr, mth, dy, hr, mn, sec, wd, yd, isdst)

        if target in self.ptc.Target_Text:
            target = self.ptc.Target_Text[target]   # run text thru locale lookup

        if _debug:
            print '++ target [%s] modifier [%s]' % (target, modifier)

        if target in sources:                       # handle special case targets
            source = sources[target]
        else:
            m = self.CRE_TIMEHMS.search(target)
            if m is not None:
                hr, mn, sec = _extract_time(m)
                source      = (yr, mth, dy, hr, mn, sec, wd, yd, isdst)

                if _debug:
                    print 'time: %s' % (target), source
            else:
                m = self.CRE_TIMEHM.search(target)
                if m is not None:
                    hr, mn, sec = _extract_time(m)
                    source      = (yr, mth, dy, hr, mn, sec, wd, yd, isdst)

                    if _debug:
                        print 'time: %s' % (target), source

                elif self.ptc.Modifiers.has_key(modifier) :
                    source = sources['now']     # if the modifier is found,
                                                # return current DateTime
                else:
                    source = sourceTime         # catch-all - if we don't grok it,
                                                #             return sourceTime

        if target.endswith('pm') and hr < 12:
            source = (yr, mth, dy, hr+12, mn, sec, wd, yd, isdst)
        if target.endswith('am') and hr == 12:
            source = (yr, mth, dy, 0, mn, sec, wd, yd, isdst)

        if _debug:
            print '++ source =', source

        return source


    def _buildTime(self, source, quantity, modifier, units):
        """
        Take quantity, modifier and unit strings and convert them into values.
        Then calcuate the time and return the adjusted sourceTime
        """

        if _debug:
            print '[%s][%s][%s]' % (quantity, modifier, units)

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

            if units == None or units == '':
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
        elif units.endswith('th'):
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

        return target.timetuple()


    def parseTime(self, timeString, meridian=None):
        """
        Given timeString, parse the hour, minute and seconds using
        the RE_TIME regular expression.
        """
        if timeString is None:
            return 0, 0, 0

        hr  = 0
        min = 0
        sec = 0

        m = self.CRE_TIMEHMS.search(timeString)

        if (m is None) or (m.group() != timeString):
            m = self.CRE_TIMEHM.search(timeString)

            if (m is None) or (m.group() != timeString):
                  # fancy regex doesn't find a time, so try brute force
                items = timeString.split(self.ptc.TIMESEP)
                l     = len(items)

                try:
                    if l > 0:
                        hr = int(items[0])
                        if l > 1:
                            min = int(items[1])
                            if l > 2:
                                sec = int(items[2])
                    else:
                        return 0, 0, 0

                except ValueError:
                    return 0, 0, 0
            else:
                hr, min, sec = _extract_time(m)
        else:
            hr, min, sec = _extract_time(m)

        if meridian and meridian.startswith('p') and hr < 12:
            hr += 12

        return hr, min, sec


    def parseDate(self, dateString):
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
            #sourceTime = time.localtime() #return current time if date string is invalid
            sourceTime = None

        return sourceTime


    def parse(self, datetimeString, sourceTime=None):
        """
        Parse timeString and return the number of seconds from sourceTime
        that the timeString expression represents.
        """

        dt       = None
        quantity = ''
        units    = ''
        modifier = ''
        target   = ''
        flag     = 1

        s = string.strip(datetimeString)

        if _debug:
            print '------ [%s] ------' % s

          # See if the given string date is a RFC822 date
        if dt is None:
            dt = _parse_date_rfc822(s)

          # See if the given string date is a W3CDTF date
        if dt is None:
            dt = _parse_date_w3dtf(s)

          # the above two checks require case to be left alone
          # but the remaining ones assume lower case
        if dt is None:
            s = s.lower()

          #check if the given sourcedate is a simple date string
        m = self.CRE_DATE.match(datetimeString)
        if (m is not None) and (m.group() == datetimeString):
            sourceTime = self.parseDate(datetimeString)
            dt         = sourceTime

          # See if the given source date is a simple time HMS string
        m = self.CRE_TIMEHMS.match(datetimeString)
        if (m is not None) and (m.group() == datetimeString):
            dt = self._buildSourceTime(sourceTime, datetimeString, '')

        if dt is None:
            m = self.CRE_TIMEHMS2.match(datetimeString)
            if (m is not None) and (m.group() == datetimeString):
                dt = self._buildSourceTime(sourceTime, datetimeString, '')

        if dt is None:
              # See if the given source date is a simple time HM string
            m = self.CRE_TIMEHM.match(datetimeString)
            if (m is not None) and (m.group() == datetimeString):
                dt = self._buildSourceTime(sourceTime, datetimeString, '')

        if dt is None:
            m = self.CRE_TIMEHM2.match(datetimeString)
            if (m is not None) and (m.group() == datetimeString):
                dt = self._buildSourceTime(sourceTime, datetimeString, '')

          #check whether the string is a weekday
        if dt is None:
            if s in self.ptc.WeekDays :
                wkDy = self.ptc.WeekDays[s]
                yr, mth, dy, hr, mn, sec, wd, yd, isdst = time.localtime()
                if wkDy > wd:
                    dy += wkDy - wd
                    wd  = wkDy
                else:
                    diff = 6 - wd + wkDy
                    dy += diff + 1
                    wd  = wkDy

                sourceTime = (yr, mth, dy, hr, mn, sec, wd, yd, isdst)

                  # capturing the remaining string
                pattern = re.compile(r'\s+')
                found   = pattern.search(s)

                if found is not None:
                    indx = found.start() + 1
                    s    = s[indx:]
                    flag = 0
                else:
                    s=''

        if dt is not None:
            return dt
        else:
              # search for any specials
            m = self.CRE_SPECIAL.search(s)
            if m is not None:
                sourceTime = time.localtime()

                s = s[m.end('special'):]

                if _debug:
                    print '**', 'special [%s] modifier [%s] s [%s]' % (m.group('special'), modifier, s)

                  # if any units are present, parse them
                m = self.CRE_UNITS.search(s)
                if m is not None:
                    units    = m.group('units')
                    quantity = s[:m.start('units')]
                    s        = s[m.end('units'):]

                    if _debug:
                        print '*1', 'units [%s] quantity [%s] s [%s]' % (units, quantity, s)
            else:
                  # search for any modifier text,
                  # i.e. "before", "from", etc
                m = self.CRE_MODIFIER.search(s)

                if m is not None:
                    modifier = m.group('modifier')
                    target   = s[m.end('modifier'):]
                    s        = s[:m.start('modifier'):]

                    if _debug:
                        print '**', 'modifier [%s] target [%s] s [%s]' % (modifier, target, s)

                if target == "" and s == "":
                    unit     = 'day'
                    quantity = '1'
                else:
                      # this check basically allows "next week" or "next tuesday"
                      # to be handled as a special case but causes
                      # "5 days before next week" and "5 min" to get normal treatment.
                    if s == "" and target != "":
                        s = target

                      # search for any units and parse if found
                    m = self.CRE_UNITS.search(s)
                    if m is not None:
                        units    = m.group('units')
                        quantity = s[:m.start('units')]
                        s        = s[m.end('units'):]

                          # capturing the remaining string
                        m = self.CRE_REMAINING.search(s)
                        if m is not None:
                            indx = m.start() + 1
                            s    = s[indx:]
                            flag = 0
                        else:
                            s = ''

                        if _debug:
                            print '*2', 'units [%s] quantity [%s] s [%s]' % (units, quantity, s)
                    else:
                          # meridian found? (am/pm)
                        m = self.CRE_MERIDIAN.search(s)
                        if m is not None:
                            t      = m.group('meridian')
                            s      = s[:m.start('meridian')]
                            target = s[m.end('meridian'):]

                            if _debug:
                                print 'meridian: [%s][%s][%s]' % (target, s, t)

                            s = '%02d:%02d:%02d' % self.parseTime(s, t)
                        else:
                            m = self.CRE_QUNITS.search(s)
                            if m is not None:
                                  # search for any single-char units
                                units    = m.group('qunits')
                                quantity = s[:m.start('qunits')]
                                s        = s[m.end('qunits'):]

                                  # capturing the remaining string
                                m = self.CRE_REMAINING.search(s)
                                if m is not None:
                                    indx = m.start() + 1
                                    s    = s[indx:]
                                    flag = 0
                                else:
                                    s = ''

                                if _debug:
                                    print '*QS', 'units [%s] quantity [%s] s [%s]' % (units, quantity, s)

            if _debug:
                print sourceTime
                print ':: quantity [%s] units [%s] modifier [%s] target [%s] s [%s]' % (quantity, units, modifier, target, s)

              # FIXME: really need to have more exception handling code and some way of signalling
              #        failure or partials, like how FeedParser does it

            sourceTime = self._buildSourceTime(sourceTime, s, modifier)
            totalTime  = self._buildTime(sourceTime, quantity, modifier, units)

            if s != '':
                if flag == 0:
                    if modifier != '':
                        s = '%s %s' % (modifier, s)

                    if _debug:
                        print '*R [%s] %d' % (s, flag), totalTime

                    sourceTime = totalTime
                    totalTime  = self.parse(s, sourceTime)

            return totalTime


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
    #  
    # Darshana TODO
    # 1. parse month names
    # 2. convert 'five' to 5

