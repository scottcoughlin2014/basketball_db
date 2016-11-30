import unittest
import numpy.testing as npt
from ..db_utilities import save_team_season, query_db
import os
import shutil

TEAM = 'MIN'
YEAR = 2016
fname = 'TEST_DATA/2015/10/28/MIN-AT-LAL.hdf5'
DATE1 = '20151027'
DATE2 = '20151028'
class TestCreate_db(unittest.TestCase):
    def test_create_db(self):
        save_team_season(TEAM,YEAR, basedir='TEST_DATA', games=[1])
        self.assertTrue(os.path.isfile(fname))
    def test_query_db(self):
        files = query_db(TEAM, date_start=DATE1, date_end=DATE2,
            basedir='TEST_DATA')
        self.assertTrue(files[0]==fname)
    def clean_up(self):
        shutil.rmtree('TEST_DATA')
        print 'Cleaned'
        self.assertTrue(True)

if __name__=="__main__":
    unittest.main()

