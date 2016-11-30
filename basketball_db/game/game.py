from pandas import DataFrame
import ..db_utilities as db
import h5py

class Game(dict):

    """object for storing game information"""

    def __init__(self, home_team, away_team):
        """

        Parameters
        ----------
        home_team : TODO
        away_team : TODO


        """
        dict.__init__(self)
        self.home_team = home_team
        self.away_team = away_team
        self[home_team] = {}
        self[away_team] = {}

    @classmethod
    def from_hdf(cls, filename):
        gm = filename.split('/')[-1][:-4]
        ht = gm[:3]
        at = gm[-3:]
        game = Game(ht, at)
        game[ht]['box_score'] = pd.read_hdf(filename, 'home_box_score')
        game[at]['box_score'] = pd.read_hdf(filename, 'away_box_score')
        game[ht]['shot_chart'] = pd.read_hdf(filename, 'home_shot_chart')
        game[at]['shot_chart'] = pd.read_hdf(filename, 'away_shot_chart')
        return game

    def to_hdf(filename):
        self[ht]['box_score'].to_hdf(filename, 'home_box_score')
        self[ht]['shot_chart'].to_hdf(filename, 'home_shot_chart')
        self[at]['box_score'].to_hdf(filename, 'away_box_score')
        self[at]['shot_chart'].to_hdf(filename, 'away_shot_chart')
        f = h5py.File(filename, 'w')
        f.create_group['teams']
        f['teams'] = [ht, at]
        f.close()

