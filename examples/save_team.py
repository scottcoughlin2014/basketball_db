from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib
matplotlib.use('agg')
from matplotlib.colors import LogNorm
import matplotlib.pyplot as plt
from basketball_db import db_utilities
from court import (bball_court_half, bball_court_three, bball_court_blocks,
    bball_shot_points)

import argparse
import ConfigParser
import json
import numpy as np
import pandas as pd

def parse_commandline():
    """
    Parse the options given on the command-line.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--team", help="What team do you want to make plots for. Did you query all the appropriate data for this team before running this? [ATL,BOS,BRK,CHI,CHO,CLE,DAL,DEN,DET,GSW,HOU,IND,LAC,LAL,MEM,MIA,MIL,MIN,NOP,NYK,OKC,ORL,PHI,PHO,POR,SAC,SAS,TOR,UTA,WAS]")
    parser.add_argument("--YMDStart", help="[Format: 20151028] What date would you like to start aggregating data for.")
    parser.add_argument("--YMDEnd", help="[Format: 20160413] What date would you like to end aggregating data for.")
    parser.add_argument("--inifile", help="Name of ini file to deal with nitty gritty stuff that is annoying to specify at the command line")
    parser.add_argument("--BaseDir", "-b",
        help="Base directory for querying database", default='./',
        dest="basedir")

    args = parser.parse_args()

    return args

args = parse_commandline()
# need 3-letter code for team...Will add a list of these
TEAM = args.team
# ---- Create configuration-file-parser object and read parameters file.
cp = ConfigParser.ConfigParser()
cp.read(args.inifile)
figSizeShot = json.loads(cp.get('plotsShot','figSize'))
figNameShot = cp.get('plotsShot','figName')
figSizeHeatShot = json.loads(cp.get('plotsHeatShot','figSize'))
figNameHeatShot = cp.get('plotsHeatShot','figName')
figCMapHeatShot = cp.get('plotsHeatShot','figCMap')
figSizeHeatPoint = json.loads(cp.get('plotsHeatPoint','figSize'))
figNameHeatPoint = cp.get('plotsHeatPoint','figName')
figCMapHeatPoint = cp.get('plotsHeatPoint','figCMap')
win = cp.getint('parameters','win')
lose = cp.getint('parameters','lose')
# run the code
#create_db.save_team_season(TEAM, YEAR, games=GAMES)
#create_db.save_team_season(TEAM, YEAR)

###############################
# THINGS THAT AREN'T SIMPLE YET
###############################

# load the data (need to add a function for this...but it will look like this)a
filename = './2015/10/28/MIN-AT-LAL.hdf5'

DATE1 = args.YMDStart
DATE2 = args.YMDEnd
files = db_utilities.query_db(TEAM, date_start=DATE1, date_end=DATE2, basedir=args.basedir)

shots = []
for ii,filename in enumerate(files):
    filenameSplit = filename.split("/")[-1].replace(".hdf5","").split("-")
    if filenameSplit[2] == TEAM:
        isHome = True
    else:
        isHome = False
    if isHome:
        shot = pd.read_hdf(filename,'home_shot_chart')
        if win:
            tmp1 =pd.read_hdf(filename,'home_box_score')
            tmp2 =pd.read_hdf(filename,'away_box_score')
            if tmp1.PTS.iloc[-1] < tmp2.PTS.iloc[-1]:
                continue
        if lose:
            tmp1 =pd.read_hdf(filename,'home_box_score')
            tmp2 =pd.read_hdf(filename,'away_box_score')
            if tmp1.PTS.iloc[-1] > tmp2.PTS.iloc[-1]:
                continue
    else:
        shot = pd.read_hdf(filename,'away_shot_chart')
        if win:
            tmp1 =pd.read_hdf(filename,'home_box_score')
            tmp2 =pd.read_hdf(filename,'away_box_score')
            if tmp1.PTS.iloc[-1] > tmp2.PTS.iloc[-1]:
                continue
        if lose:
            tmp1 =pd.read_hdf(filename,'home_box_score')
            tmp2 =pd.read_hdf(filename,'away_box_score')
            if tmp1.PTS.iloc[-1] < tmp2.PTS.iloc[-1]:
                continue

    shots.append(shot)
shots = pd.concat(shots)

# plot the shot chart
if win:
    figNameShot = figNameShot + '_win'
    figNameHeatShot = figNameHeatShot + '_win'
    figNameHeatPoint = figNameHeatPoint + '_win'

if lose:
    figNameShot = figNameShot + '_lose'
    figNameHeatShot = figNameHeatShot + '_lose'
    figNameHeatPoint = figNameHeatPoint + '_lose'

plt.figure(figsize=figSizeShot)
ax = bball_court_half()
ax.scatter(50- shots['shot_xs'][shots['result']],
    shots['shot_ys'][shots['result']],c='g' )
ax.scatter(50- shots['shot_xs'][~shots['result']],
    shots['shot_ys'][~shots['result']],c='r' )
plt.savefig(figNameShot)
plt.close()

xedges = np.arange(50)
yedges = np.arange(50)
[X,Y] = np.meshgrid(xedges,yedges)

[Xpoints,Ypoints] = np.meshgrid((xedges[1:]+xedges[:-1])/2.0,(yedges[1:]+yedges[:-1])/2.0)
points = bball_court_three(Xpoints,Ypoints)

H_yes, xedges1, yedges1 = np.histogram2d(shots['shot_ys'][shots['result']],50-shots['shot_xs'][shots['result']], bins=(xedges, yedges))
H_no, xedges2, yedges2 = np.histogram2d(shots['shot_ys'][~shots['result']],50-shots['shot_xs'][~shots['result']], bins=(xedges, yedges))
H_total = H_yes + H_no
H_yes_perc = H_yes/H_total
H_no_perc = H_no/H_total

H_yes_perc[np.isnan(H_yes_perc)] = 0.0
H_no_perc[np.isnan(H_no_perc)] = 0.0

print "Percentage of shots made: %.1f%%"%(100*np.nansum(H_yes)/np.nansum(H_total))

# heatmap for the shot chart
plt.figure(figsize=figSizeHeatShot)
ax = bball_court_half()
img = ax.pcolor(X,Y,H_yes_perc, cmap=figCMapHeatShot, vmin=0,vmax=1)
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5.6%", pad=0.05)
plt.colorbar(img,label='Shot percentage',cax=cax)
plt.savefig(figNameHeatShot)
plt.close()

norm_arr = (H_yes_perc*points).reshape((points.size,1)).squeeze()
norm = np.mean(norm_arr[norm_arr>0])
std = np.std(norm_arr[norm_arr>0])

exp_points = H_yes_perc*points

# heat map based on points
plt.figure(figsize=(5.3,4.7))
ax = bball_court_half()
img = ax.pcolor(X,Y,H_yes_perc*points, cmap=figCMapHeatPoint, vmin=norm-0.5,
        vmax=norm+0.5)
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5.6%", pad=0.05)
plt.colorbar(img,label='Expected Points',cax=cax)
plt.savefig(figNameHeatPoint)
plt.close()

ticks = np.asarray([1.5,1.6,1.7,1.8,1.9,2.0,2.1,2.2])
logticks = np.log10(ticks)

# hexbin
points_achieved = bball_shot_points(shots['shot_xs'], shots['shot_ys'])
points_achieved[np.where(~shots['result'])] = 0
# set points to zero if shot missed
plt.figure(figsize=figSizeHeatShot)
ax = bball_court_half()
plt.hexbin(50-shots['shot_xs'],shots['shot_ys'],
        C=points_achieved, reduce_C_function=np.mean,
        gridsize=20, bins='log', cmap='Spectral_r', vmin=0.1, vmax=0.40)
#cax = divider.append_axes("right", size="5.6%", pad=0.05)
#cbar = plt.colorbar(label='Expected Points')
#cbar.ax.set_yticklabels(ticks)
plt.savefig('hexbin_points')
plt.close()

# hexbin shot_locations
plt.figure(figsize=figSizeHeatShot)
ax = bball_court_half()
plt.hexbin(50-shots['shot_xs'],shots['shot_ys'],
           gridsize=10, cmap='viridis', bins='log')
cax = divider.append_axes("right", size=0.295, pad=0.05)
cbar = plt.colorbar(label='log10(Number of shots)', ax=cax)
#cbar.ax.set_yticklabels(ticks)
plt.savefig('hexbin_shot_locations')
plt.close()


shotdists = bball_court_blocks(Xpoints,Ypoints)
for key in shotdists:
    expected_points = np.nansum(points*shotdists[key]*H_yes)/np.nansum(points*shotdists[key]*H_total)
    print "Type: %s, Expected points: %.2f"%(key,expected_points)
