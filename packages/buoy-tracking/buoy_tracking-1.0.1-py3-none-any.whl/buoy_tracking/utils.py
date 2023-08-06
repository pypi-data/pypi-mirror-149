from datetime import timedelta, datetime
import csv
import logging

logger = logging.getLogger(__name__)

class PrintColor:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


def xldate_to_datetime(xldate, tz="EST"):
    temp = datetime(1899, 12, 30)
    delta = timedelta(days=xldate)
    if tz == "EST":
        utc_offset = timedelta(hours=5)
    else:
        utc_offset = timedelta(hours=0)
    return temp+delta+utc_offset


def decimaldoy_to_datetime(decimaldoy, year=2020):
    temp = datetime(year-1, 12, 31)
    delta = timedelta(days=decimaldoy)
    return temp + delta


def format_timedelta(tdelta, show_seconds=True):
    s = tdelta.total_seconds()
    hours, remainder = divmod(s, 3600)
    minutes, seconds = divmod(remainder, 60)

    if show_seconds:
        return "{:02}h {:02}m {:02}s".format(int(hours), int(minutes), int(seconds))
    else:
        return "{:02}h {:02}m".format(int(hours), int(minutes))


def write_buoy_stats(filename, buoy_id, lat, lon, lkp_time):
    age_of_lkp = datetime.utcnow() - lkp_time
    with open(filename, 'a+') as status_file:
        writer = csv.writer(status_file)
        writer.writerow([buoy_id, lat, lon, age_of_lkp])


def print_buoy_stats(buoy_id, lat, lon, lkp_time):

    age_of_lkp = datetime.utcnow() - lkp_time

    if age_of_lkp < timedelta(hours=4):
        msg = (PrintColor.BOLD + PrintColor.GREEN +
               "{}: ({}, {}) - Time since last update: {}".format(buoy_id, lat, lon, age_of_lkp) + PrintColor.END)
    elif age_of_lkp < timedelta(hours=12):
        msg = (PrintColor.BOLD + PrintColor.YELLOW +
               "{}: ({}, {}) - Time since last update: {}".format(buoy_id, lat, lon, age_of_lkp) + PrintColor.END)
    else:
        msg = (PrintColor.BOLD + PrintColor.RED +
               "{}: ({}, {}) - Time since last update: {}".format(buoy_id, lat, lon, age_of_lkp) + PrintColor.END)

    logger.info(msg)