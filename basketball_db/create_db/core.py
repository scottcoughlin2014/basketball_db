from bs4 import BeautifulSoup
import requests
import pandas as pd
import os
from datetime import datetime
from collections import OrderedDict
import time
import numpy as np
from ..utils.core import (extract_box_score, extract_shot_chart,
    _get_shot_chart_link, _get_team, _get_date, make_data_path,
    make_schedule_path, date2path, path2date, get_schedule_name,
    get_game_fname, _get_schedule)

# one global variable. don't kill me.
BASEURL = 'http://www.basketball-reference.com/'

def save_team_season(team, year, basedir='./', break_after_missing_game=True,
        games=None):
    """
    Convert all shots and data for a team's season
    into a dataframe

    Parameters
    ----------
    team : `str`
        Three letter team identifier
    year : `int`
        End year of season you want to save

    Returns
    -------
    none :
    """
    # get team's season page
    soup =\
        BeautifulSoup(requests.get('http://www.basketball-reference.com/teams/%s/%d_games.html'\
        % (team, year)).text,'lxml')

    make_schedule_path(year, basedir=basedir)
    sched = _get_schedule(soup)
    sched_fname = get_schedule_name(team, year, basedir=basedir)
    sched.to_hdf(sched_fname,'schedule')
    # get team's schedule
    box_scores =\
        soup.find('table',{'id':'games'}).findAll('td',{'data-stat':'box_score_text'})
    links = [box_scores[ii].a['href'] for ii in range(len(box_scores))]
    sc_links = [BASEURL + _get_shot_chart_link(link.replace('//','/')) for link in links]
    boxscore_links = [BASEURL + link.replace('//','/') for link in links]
    if games is None:
        games = np.arange(len(boxscore_links))
    else:
        games = np.asarray(games) - 1
    counter = 0
    for bs,sc in zip(boxscore_links, sc_links):
        if not np.any(games == counter):
            counter += 1
            continue
        counter += 1
        soup_bs = BeautifulSoup(requests.get(bs).text, 'lxml')
	soup_sc = BeautifulSoup(requests.get(sc).text, 'lxml')
	# get team names
        try:
            home_team = _get_team(soup_bs, team='home')
            away_team = _get_team(soup_bs, team='away')
        except AttributeError:
            print 'This game and future games may not be available yet:\n\t\t%s' % bs
            if break_after_missing_game:
                break
            else:
                print 'Continuing to look for future games...'
                pass
	# get date of game
	date = _get_date(soup_bs)
	make_data_path(date, basedir=basedir)
        fname = get_game_fname(date, home_team, away_team, basedir=basedir)
        if os.path.isfile(fname):
            print '%s already exists!' % fname
            continue
        else:
            # get box scores
            try:
                home_box_score = extract_box_score(soup_bs, team=home_team)
                away_box_score = extract_box_score(soup_bs, team=away_team)
                home_box_score.to_hdf(fname, 'home_box_score')
                away_box_score.to_hdf(fname, 'away_box_score')
            except AttributeError:
                print """It looks like the box score isn't available yet...\n
                This is likely because the game is too recent"""
            # get shot charts
            try:
                home_shot_chart = extract_shot_chart(soup_sc, team=home_team)
                away_shot_chart = extract_shot_chart(soup_sc, team=away_team)
                home_shot_chart.to_hdf(fname, 'home_shot_chart')
                away_shot_chart.to_hdf(fname, 'away_shot_chart')
            except AttributeError:
                print """It looks like the shot charts may not be available for
                this game yet...\nWe're just saving box scores right now"""
            # create path to save
            # get file name

        print 'saved %s' % fname
        wait_time = 0.5 + np.random.rand(1)[0]
        time.sleep(wait_time)
