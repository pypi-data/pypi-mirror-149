from datetime import datetime, timedelta
from pytz import timezone
import pytz

"""
Some time related functions

"""


def timestamp(*args):
    this_tz = pytz.timezone('UTC')
    now_naive = datetime.utcnow()
    now = this_tz.localize(now_naive)
    return now.timestamp()


def now(*args):
    this_tz = pytz.timezone('UTC')
    now = datetime.utcnow()
    start_date = this_tz.localize(now)
    return start_date


def now_str(*args, **kwargs):
    format_date = kwargs.get('format_date')
    this_tz = pytz.timezone('UTC')
    now = datetime.now(tz=this_tz).astimezone(tz=this_tz)
    if not format_date:
        return now.isoformat()
    else:
        return now.strftime(format_date)


def gps_week2time(week, time_week):
    # start date
    try:
        this_tz = pytz.timezone('UTC')
        t0 = datetime(1980, 1, 6)
        start_date = this_tz.localize(t0)
    except Exception as e:
        print("Error en generar start_date %s" % e)
        raise e
        # how many weeks and milliseconds after start_date
    delta = timedelta(weeks=week, milliseconds=time_week)
    final_date = start_date+delta
    return final_date


def gps_time(data, tipo="GSOF", leap=18):
    fd = datetime.utcnow()
    utc = timezone("UTC")
    final_date = utc.localize(fd)
    if 'UTC' in data.keys():
        utc = data['UTC']
        time_week = utc['GPS_MS_OF_WEEK']
        week = utc['GPS_WEEK']
        offset = utc['UTC_OFFSET']
        offset_time = timedelta(seconds=-offset)
        final_date = gps_week2time(week, time_week)+offset_time
        source = 'UTC'
        #print("UTC TIME %s" %final_date)
    elif 'TIME' in data.keys():
        LEAP = leap
        time = data['TIME']
        GPS_WEEK = time['GPS_WEEK']
        GPS_TIME = time['GPS_TIME']  # miliseconds
        offset_time = timedelta(seconds=-LEAP)
        final_date = gps_week2time(GPS_WEEK, GPS_TIME)+offset_time
        source = 'TIME'       
        #print("GPS TIME %s" %final_date)
    elif "POSITION_BLOCK" in data.keys():
        GPS_WEEK = data["POSITION_BLOCK"].get("GPS_WEEK")
        GPS_MILLISECONDS = data["POSITION_BLOCK"].get("GPS_MILLISECONDS")
        offset_time = timedelta(seconds=-leap)
        final_date = gps_week2time(GPS_WEEK, GPS_MILLISECONDS)+offset_time
        source = 'POSITION_BLOCK'
        
    return final_date, source


def get_datetime_di(delta: int = 600) -> "Datetime UTC Isoformat":
    df = datetime.now(tz=pytz.utc)
    di = df+timedelta(seconds=-delta)
    return di.astimezone(tz=pytz.utc).isoformat()
