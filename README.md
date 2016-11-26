# basketball_db

[![Build Status](https://travis-ci.org/pmeyers279/basketball_db.svg?branch=master)](https://travis-ci.org/pmeyers279/basketball_db)

[![Coverage Status](https://coveralls.io/repos/github/pmeyers279/basketball_db/badge.svg)](https://coveralls.io/github/pmeyers279/basketball_db)

[![Code Health](https://landscape.io/github/pmeyers279/basketball_db/master/landscape.svg?style=flat)](https://landscape.io/github/pmeyers279/basketball_db/master)


package to query basketball-reference.com and save data.

**NOTE**: This package is still under very heavy development.

## Installation

### Requirements

* `numpy`
* `scipy`
* `pandas`
* `bs4`
* `matplotlib` [will need soon]

### Instructions

1. Clone the repo
2. cd to repo top level directory
3. run `pip install .` or `python setup.py install`

## Save all games for one team for 2015/2016 season

```
>>> from basketball_db import create_db
>>> create_db.save_team_season('MIN','2016',basedir='./')
```

This saves games in

`%(basedir)/%(year)/%(month)/%(day)/%(TEAM1)-AT-%(TEAM2).hdf5`

## Load data

It saves pandas dataframes for `home_box_score` and `away_box_score`, `home_shot_chart`, `away_shot_cart`

You can read this in with:
```
>>> import pandas as pd
>>> fname = './2015/10/28/MIN-AT-LAL.hdf5'
>>> away_shot_chart = pd.read_hdf(fname,'away_shot_chart')
>>> print away_shot_chart
```

## Run tests

1. cd to repo top level
2. For example: `python -m basketball_db.tests.create_db_test`

