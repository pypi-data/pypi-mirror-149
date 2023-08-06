# uncompyle6 version 3.8.0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.8 (tags/v3.6.8:3c6b436a57, Dec 24 2018, 00:16:47) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: C:\Users\scienco\Desktop\paper\zdb\richdb\util.py
# Compiled at: 2022-05-05 07:43:09
# Size of source mod 2**32: 3086 bytes
import datetime as dt, time, re, calendar

def get_strdate_format(date):
    fmt = None
    mat = re.match('\\d{4}', date)
    if mat is not None:
        fmt = '%Y'
    mat = re.match('\\d{4}-\\d{2}', date)
    if mat is not None:
        fmt = '%Y-%m'
    mat = re.match('\\d{4}-\\d{2}-\\d{2}', date)
    if mat is not None:
        fmt = '%Y-%m-%d'
    mat = re.match('\\d{4}-\\d{2}-\\d{2}\\s+\\d{2}', date)
    if mat is not None:
        fmt = '%Y-%m-%d %H'
    mat = re.match('\\d{4}-\\d{2}-\\d{2}\\s+\\d{2}:\\d{2}', date)
    if mat is not None:
        fmt = '%Y-%m-%d %H:%M'
    mat = re.match('\\d{4}-\\d{2}-\\d{2}\\s+\\d{2}:\\d{2}:\\d{2}', date)
    if mat is not None:
        fmt = '%Y-%m-%d %H:%M:%S'
    mat = re.match('\\d{4}-\\d{2}-\\d{2}\\s+\\d{2}:\\d{2}:\\d{2}\\.\\d+', date)
    if mat is not None:
        fmt = '%Y-%m-%d %H:%M:%S.%f'
    mat = re.match('\\d{4}\\.\\d{2}', date)
    if mat is not None:
        fmt = '%Y.%m'
    mat = re.match('\\d{4}\\.\\d{2}\\.\\d{2}', date)
    if mat is not None:
        fmt = '%Y.%m.%d'
    mat = re.match('\\d{4}\\.\\d{2}\\.\\d{2}\\s+\\d{2}', date)
    if mat is not None:
        fmt = '%Y.%m.%d %H'
    mat = re.match('\\d{4}\\.\\d{2}\\.\\d{2}\\s+\\d{2}:\\d{2}', date)
    if mat is not None:
        fmt = '%Y.%m.%d %H:%M'
    mat = re.match('\\d{4}\\.\\d{2}\\.\\d{2}\\s+\\d{2}:\\d{2}:\\d{2}', date)
    if mat is not None:
        fmt = '%Y.%m.%d %H:%M:%S'
    mat = re.match('\\d{4}\\.\\d{2}\\.\\d{2}\\s+\\d{2}:\\d{2}:\\d{2}\\.\\d+', date)
    if mat is not None:
        fmt = '%Y.%m.%d %H:%M:%S.%f'
    mat = re.match('\\d{4}/\\d{2}', date)
    if mat is not None:
        fmt = '%Y/%m'
    mat = re.match('\\d{4}/\\d{2}/\\d{2}', date)
    if mat is not None:
        fmt = '%Y/%m/%d'
    mat = re.match('\\d{4}/\\d{2}/\\d{2}\\s+\\d{2}', date)
    if mat is not None:
        fmt = '%Y/%m/%d %H'
    mat = re.match('\\d{4}/\\d{2}/\\d{2}\\s+\\d{2}:\\d{2}', date)
    if mat is not None:
        fmt = '%Y/%m/%d %H:%M'
    mat = re.match('\\d{4}/\\d{2}/\\d{2}\\s+\\d{2}:\\d{2}:\\d{2}', date)
    if mat is not None:
        fmt = '%Y/%m/%d %H:%M:%S'
    mat = re.match('\\d{4}/\\d{2}/\\d{2}\\s+\\d{2}:\\d{2}:\\d{2}\\.\\d+', date)
    if mat is not None:
        fmt = '%Y/%m/%d %H:%M:%S.%f'
    mat = re.match('\\d{4}\\d{2}', date)
    if mat is not None:
        fmt = '%Y%m'
    mat = re.match('\\d{4}\\d{2}\\d{2}', date)
    if mat is not None:
        fmt = '%Y%m%d'
    mat = re.match('\\d{4}\\d{2}\\d{2}\\s\\d{2}', date)
    if mat is not None:
        fmt = '%Y%m%d %H'
    mat = re.match('\\d{4}\\d{2}\\d{2}\\s\\d{2}:\\d{2}', date)
    if mat is not None:
        fmt = '%Y%m%d %H:%M'
    mat = re.match('\\d{4}\\d{2}\\d{2}\\s\\d{2}:\\d{2}:\\d{2}', date)
    if mat is not None:
        fmt = '%Y%m%d %H:%M:%S'
    mat = re.match('\\d{4}\\d{2}\\d{2}\\s\\d{2}:\\d{2}:\\d{2}\\.\\d+', date)
    if mat is not None:
        fmt = '%Y%m%d %H:%M:%S.%f'
    return fmt