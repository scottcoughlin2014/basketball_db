import unittest
import numpy.testing as npt
from ..create_db.core import save_team_season
import os
import shutil

TEAM = 'MIN'
YEAR = 2016
fname = 'tests/data/2015/10/28/MIN-AT-LAL.hdf5'
class TestCreate_db(unittest.TestCase):
    def test_create_db(self):
        save_team_season(TEAM,YEAR, basedir='tests/data', games=[1])
        self.assertTrue(os.path.isfile(fname))
        shutil.rmtree('tests/data/2015')

if __name__=="__main__":
    unittest.main()

