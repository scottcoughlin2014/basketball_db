import pandas as pd
from .utils import *
from datetime import datetime, timedelta
import glob

def query_db(team, date_start, date_end, basedir='./'):
    """
    query database between dates

    Parameters
    ----------
    team:  `str`
        3-letter team code
    date : `str` or `datetime.datetime` object
        date you want to load. Either string with
        YYYYMMDD format or datetime object

    Returns
    -------
    file_list : `list`
        list of files for games for that team between those dates
    """
    if isinstance(date_start, str):
        date_start = datetime.strptime(date_start, '%Y%m%d')
    elif date_start is None:
        print 'Start date not set...setting it to yesterday'
        date_start = datetime.yesterday
    if isinstance(date_end, str):
        date_end = datetime.strptime(date_end, '%Y%m%d')
    elif date_end is None:
        print 'End date not set...setting it to today'
        date_end = datetime.today
    date_inc = date_start
    files = []
    while date_inc <= date_end:
        path = date2path(date_inc, basedir=basedir)
        match_str = '%s/*%s*' % (path, team)
        games = glob.glob(match_str)
        if len(games)==0:
            date_inc += timedelta(days=1)
            continue
        if len(games) > 1:
            err_mess = """You seem to have a team playing multiple games on the
            same day"""
            raise ValueError(err_mess)
        files.append(games[0])
        date_inc += timedelta(days=1)
    return files
