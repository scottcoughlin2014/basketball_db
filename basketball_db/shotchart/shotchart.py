from __future__ import division
from .court import *
from pandas import DataFrame
import pandas as pd
from ..db_utilities import path2date
from ..plotter.shotchart import ShotChartScatter

class ShotChart(DataFrame):

    """
    Shot Chart object
    """
    def __init__(self, df_data, team_name=None,date=none):
        """shot chart object."""
        super(ShotChart, self).__init__(df_data)
        self.team_name = team_name
        self.date = date

    def plot_makes_misses(self, **kwargs):
        """TODO: Docstring for plot_makes_misses.

        Parameters
        ----------

        Returns
        -------
        TODO

        """
        return ShotChartScatter(self, **kwargs)

    @classmethod
    def load_game(cls, filename):
        """
        load shot charts from file

        Parameters
        ----------
        filename :

        Returns
        -------
        home_shot_chart : :class:`basketball_db.shotchart.ShotChart`
            shot chart for home team for this game
        away_shot_cart : :class:`basketball_db.shotchart.ShotChart`
            shot chart for away team for this game
        """
        ht = filename.split('/')[-1][:-5][:3]
        at = filename.split('/')[-1][:-5][-3:]
        path = './'
        for ii in (4,3,2):
            path += '/' + filename.split('/')[-ii]+'/'
        path = path.replace('//','/')
        home_sc = ShotChart(pd.read_hdf(filename,'home_shot_chart'), team_name=ht)
        away_sc = ShotChart(pd.read_hdf(filename,'away_shot_chart'),
                team_name=at, date=date)
        home_sc['points'] = bball_shot_points(home_sc['shot_xs'],
            home_sc['shot_ys'])
        home_sc['points'][~home_sc['result']] = 0
        away_sc['points'] = bball_shot_points(away_sc['shot_xs'],
            away_sc['shot_ys'])
        away_sc['points'][~home_sc['result']] = 0
        return home_sc, away_sc

