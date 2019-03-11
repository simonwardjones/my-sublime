import sublime
import sublime_plugin
import urllib.parse
from datetime import datetime, timezone, tzinfo, timedelta
import logging
import time

ZERO = timedelta(0)


class UTC(tzinfo):
    """UTC

    Optimized UTC implementation. It unpickles using the single module global
    instance defined beneath this class declaration.
    """
    zone = "UTC"

    _utcoffset = ZERO
    _dst = ZERO
    _tzname = zone

    def fromutc(self, dt):
        if dt.tzinfo is None:
            return self.localize(dt)
        return super(utc.__class__, self).fromutc(dt)

    def utcoffset(self, dt):
        return ZERO

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        return ZERO

    def __reduce__(self):
        return _UTC, ()

    def localize(self, dt, is_dst=False):
        '''Convert naive time to local time'''
        if dt.tzinfo is not None:
            raise ValueError('Not naive datetime (tzinfo is already set)')
        return dt.replace(tzinfo=self)

    def normalize(self, dt, is_dst=False):
        '''Correct the timezone information on the given datetime'''
        if dt.tzinfo is self:
            return dt
        if dt.tzinfo is None:
            raise ValueError('Naive time - no tzinfo set')
        return dt.astimezone(self)

    def __repr__(self):
        return "<UTC>"

    def __str__(self):
        return "UTC"


utc = UTC()
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO)


class ToDatetime(sublime_plugin.TextCommand):
    def run(self, edit):
        for region in self.view.sel():
            text_content = self.view.substr(region)
            text_content.strip()
            try:
                date_content = datetime.utcfromtimestamp(
                    int(text_content))
            except ValueError as e:
                date_content = datetime.utcfromtimestamp(
                    int(text_content)/1000)
            date_content = date_content.replace(tzinfo=utc)
            date_str = date_content.strftime('%Y/%m/%d %H:%M:%S.%f')
            logger.debug(date_str)
            self.view.replace(edit, region, date_str)


class ToTimestamp(sublime_plugin.TextCommand):
    def run(self, edit):
        for region in self.view.sel():
            text_content = self.view.substr(region)
            text_content.strip()
            for format_str in ['%Y-%m-%d %H:%M:%S.%f', '%Y/%m/%d %H:%M:%S.%f']:
                try:
                    date_content = datetime.strptime(
                        text_content,format_str )
                except ValueError as e:
                    logger.info(e)
                else:
                    logger.info('formated as {}'.format(format_str))
                    break
            date_content = date_content.replace(tzinfo=utc)
            logger.debug(text_content)
            logger.debug(date_content.timestamp()*1000)
            date_str = str(int(date_content.timestamp()*1000))
            self.view.replace(edit, region, date_str)



class InsertDatetime(sublime_plugin.TextCommand):
    def run(self, edit):
        sel = self.view.sel();
        for s in sel:
            self.view.replace(
                edit, 
                s, 
                datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))



# examples below

t = 1532174055631
s = '2018/07/21 11:54:15.631000'
