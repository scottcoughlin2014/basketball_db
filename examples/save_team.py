import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
from basketball_db import create_db
from basketball_db import utils
import pandas as pd
from court import bball_court_half

# need 3-letter code for team...Will add a list of these
TEAM = 'MIN'
# Second year in the season...i.e. 2016 for 2015/2016 season
YEAR = 2016
# which games from that season do you want to save? (optional)
GAMES = [1]
# run the code
create_db.save_team_season(TEAM, YEAR, games=GAMES)

###############################
# THINGS THAT AREN'T SIMPLE YET
###############################

# load the data (need to add a function for this...but it will look like this)a
filename = './2015/10/28/MIN-AT-LAL.hdf5'

# get t-wolves shot chart
shots = pd.read_hdf(filename,'away_shot_chart')
print shots

# plot the shot chart
plt.figure(figsize=(5,4.7))
ax = bball_court_half()
ax.scatter(50- shots['shot_xs'][shots['result']],
    shots['shot_ys'][shots['result']],c='g' )
ax.scatter(50- shots['shot_xs'][~shots['result']],
    shots['shot_ys'][~shots['result']],c='r' )
plt.savefig('test')
plt.close()
