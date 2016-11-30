import matplotlib
matplotlib.use('agg')
import unittest
import numpy.testing as npt
from ..db_utilities import save_team_season, query_db
from ..shotchart import ShotChart
import os
import shutil
import pandas as pd

FILE = 'basketball_db/tests/data/2015/10/28/MIN-AT-LAL.hdf5'

class TestShotChartScatter(unittest.TestCase):
    def test_shot_chart_scatter(self):
        sc = pd.read_hdf(FILE,'home_shot_chart')
        plot = ShotChartScatter(sc)
        plot.savefig('test.png')
        self.assertTrue(isinstance(plot,ShotChartScatter))

if __name__=="__main__":
    unittest.main()


