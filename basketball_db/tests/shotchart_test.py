import matplotlib
matplotlib.use('agg')
import unittest
import numpy.testing as npt
from ..db_utilities import save_team_season, query_db
from ..shotchart import ShotChart
from ..plotter.shotchart import ShotChartScatter
import os
import shutil
import pandas as pd

FILE = 'basketball_db/tests/data/2015/10/28/MIN-AT-LAL.hdf5'
TEAM1='MIN'
TEAM2='LAL'
COLS=['player', 'result', 'shot_time', 'shot_xs', 'shot_ys', 'points']

class TestShotChart(unittest.TestCase):
    TEST_CLASS=ShotChart
    def test_shot_chart_scatter_init(self):
        ht,at = self.TEST_CLASS.load_game(FILE)
        self.assertTrue(isinstance(ht,ShotChart))
        self.assertTrue(isinstance(at,ShotChart))
        self.assertTrue(ht.team_name==TEAM1)
        self.assertTrue(at.team_name==TEAM2)
        npt.assert_array_equal(COLS,ht.columns)
        npt.assert_array_equal(COLS,at.columns)

    def test_plot_makes_misses(self):
        ht,at = self.TEST_CLASS.load_game(FILE)
        plot = ht.plot_makes_misses()
        ax = plot.gca()
        ax.set_title(ht.team_name)
        plot.savefig('test.png')
        self.assertTrue(isinstance(plot, ShotChartScatter))

if __name__=="__main__":
    unittest.main()


