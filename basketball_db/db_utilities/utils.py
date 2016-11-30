from bs4 import BeautifulSoup
import requests
import pandas as pd
import os
from datetime import datetime
from collections import OrderedDict
import time
import numpy as np

# one global variable. don't kill me.
BASEURL = 'http://www.basketball-reference.com/'

def _get_pbp_link(link):
    """
    get play-by-play link from box score link
    Parameters
    ----------
    link : `str`
        box score link

    Returns
    -------
    pbp_link : `str`
        play by play link
    """
    pass
    sp = link.split('/')
    newlink = sp[-2] + '/pbp/' + sp[-1]
    return newlink

def _get_shot_chart_link(link):
    """
    get shot chart link from box score link
    Parameters
    ----------
    link : `str`
        box score link

    Returns
    -------
    newlink : `str`
        shot chart link
    """
    sp = link.split('/')
    newlink = sp[-2] + '/shot-chart/' + sp[-1]
    return newlink

def extract_box_score(soup_bs, team=None):
    """
    extract box score from game page

    Parameters
    ----------
    soup_bs : :class:`bs4.BeautifulSoup`
        beautiful soup class object. used to parse full box score
        web page
    team : `str`
        3-letter team tag for one of the two teams
        this box score web page is for

    Returns
    -------
    box_score : :class:`pandas.DataFrame`
        pandas dataframe table for this box score
    """
    id_tag = 'box_' + team.lower() + '_basic'
    tab = soup_bs.find('table',{'id':id_tag})
    if len(tab)==0:
        raise ValueError('You entered team: %s, which does not have a box score on this page' % team)
    header_strs = [td.text for td in tab.findAll('tr')[1].findAll('th')]
    box_score = OrderedDict()
    for h in header_strs:
        box_score[h] = []
    for ii,tr in enumerate(tab.findAll('tr')):
        tds = [td.text for td in tr.findAll('td')]
        # if we're at the last row...continue
        # if we have more than one non-header column
        if len(tds) > 1:
            # loop through header strings
            for jj, head in enumerate(header_strs):
                if jj == 0:
                    # if we're on the first header string, then it's the player's name
                    # and that's in a <th> tag, not <td> tag. If it's the last row,
                    # then the player's "name" ("Team Totals") is in a different type
                    # of th tag.
                    if ii == len(tab.findAll('tr')) - 1:
                        box_score[head].append(tr.find('th').text)
                    else:
                        box_score[head].append(tr.find('th')['data-append-csv'])
                    continue
                else:
                    # otherwise, we loop through tds, and since
                    # these are indexed off-set from headers (since
                    # player names start), we index with jj-1
                    if jj ==1:
                        box_score[head].append(tds[jj-1])
                    else:
                        if tds[jj-1]=='':
                            tds[jj-1] = 0
                        box_score[head].append(float(tds[jj-1]))
    box_score = pd.DataFrame(box_score)
    return box_score

def extract_shot_chart(soup_sc, team=None):
    """
    get shot chart
    Parameters
    ----------
    soup_sc : `bs4.BeautifulSoup`
        Beautiful soup object for shot
        chart webpage. Used to parse webpage
    team : `str`
        3-letter team id code for one of the two
        teams on this shot chart page

    Returns
    -------
    shot_chart : `pandas.DataFrame`
        pandas data frame object
        for shot chart for this game for
        the specified team
    """
    id_tag = 'shots-' + team.upper()
    court_width=50
    court_len=47
    shot_dict = {}
    shot_dict['shot_xs'] = []
    shot_dict['shot_ys'] = []
    shot_dict['shot_time'] = []
    shot_dict['player'] = []
    shot_dict['result'] = []
    shots = soup_sc.find('div',{'id':id_tag}).findAll('div',{'class','tooltip'})
    for shot in shots:
        sp = shot['tip'].split('<br>')
        shot_dict['player'].append(shot['class'][2][2:])
        if shot['class'][-1] == 'make':
            shot_dict['result'].append(True)
        else:
            shot_dict['result'].append(False)
        shot_dict['shot_time'].append(sp[0].split(',')[1][1:-10])
        # get shot coordinates. Image is 500 x 472 px,
        # court is 50 ft. x 47 ft, so just divide by 10.
        shot_dict['shot_xs'].append((int(shot['style'].split(':')[-1][:-3]) +\
            5)*(50/500.))
        shot_dict['shot_ys'].append((int(shot['style'].split(':')[1][:-7]) +
            10)*(47/472.))
    shotFrame = pd.DataFrame(shot_dict)
    return shotFrame

def _get_team(soup_bs,team='home'):
    """
    get team name from box score page
    """
    score_div = soup_bs.find('div',{'class':'scorebox'})
    if team == 'home':
        t = score_div.findAll('strong')[1].a['href'].split('/')[2].lower()
    elif team=='away':
        t = score_div.findAll('strong')[0].a['href'].split('/')[2].lower()
    else:
        raise ValueError('team must be either "home" or "away". Default is "home"')
    return t

def _get_date(soup_bs):
    """
    get date of game from box score page
    """
    content_div = soup_bs.find('div',{'id':'content'})
    month_day = content_div.find('h1').text.split(',')[-2]
    year = content_div.find('h1').text.split(',')[-1]
    date = datetime.strptime(month_day.strip() + year,'%B %d %Y')
    return date

def path2date(path):
    """
    figure out path to file from date of game
    """
    sp = path.split('/')
    yr = sp[1]
    mth = sp[2]
    day = sp[3]
    strdate = mth+day+yr
    print strdate
    date = datetime.strptime(strdate, '%m%d%Y')
    return date

def date2path(date, basedir='./'):
    """
    figure out date of game from file path
    """

    path = date.strftime('%Y/%m/%d')
    return basedir + '/' + path + '/'

def make_data_path(date, basedir='./'):
    """
    create path to file for a game on specified date
    """
    path = date2path(date, basedir=basedir)
    try:
        os.makedirs(path)
    except OSError:
        pass

def make_schedule_path(year, basedir='./'):
    """
    create path to where we want to save schedules
    """
    try:
        os.makedirs(basedir+'/SCHEDULES/')
    except OSError:
        pass

def get_schedule_name(team, year, basedir='./'):
    """
    return name of schedule file to save
    """
    return ('%s/SCHEDULES/%s-%d-%d' % (basedir, team, year-1, year)).replace('//','/')

def get_game_fname(date, home_team, away_team, basedir='./'):
    """
    return name of game file we want to save
    """
    path = date2path(date, basedir=basedir)
    fstring = away_team.upper() + '-AT-' + home_team.upper() + '.hdf5'
    return (path + '/' + fstring).replace('//','/')

def _get_schedule(soup):
    """
    extract schedule from team's schedule page

    Parameters
    ----------
    soup : `bs4.BeautifulSoup`
        beautiful soup object for team's schedule page.
        Used to parse web page

    Returns
    -------
    schedule : `pandas.DataFrame`
        pandas dataframe object for schedule
    """
    tab = soup.find('table',{'id':'games'})
    list_vals =pd.read_html('<table>' + str(tab.find('tbody'))+'</table>')
    headers = []
    sched = list_vals[0]
    for ii,th in enumerate(tab.find('thead').findAll('th')):
            headers.append(th['data-stat'])
    print headers
    sched.columns = headers
    # fix game locations
    print type(sched['game_location'])
    away = np.where(sched['game_location']=='@')
    sched['game_location'] = sched['game_location'].replace('@','A')
    sched['game_location'] = sched['game_location'].replace(np.nan,'H')
    sched['overtimes'] = sched['overtimes'].replace(np.nan,0)
    sched = sched.replace(np.nan,'--')
    return sched

