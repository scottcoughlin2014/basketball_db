from __future__ import division
"""An extension of the Plot class for handling shot charts
"""

import re
import numpy as np
from matplotlib import (pyplot, colors)
from matplotlib.projections import register_projection
from matplotlib.artist import allow_rasterization
from matplotlib.cbook import iterable
from .core import Plot
from .axes import Axes
from .decorators import auto_refresh

try:
    from mpl_toolkits.axes_grid1 import make_axes_locatable
except ImportError:
    from mpl_toolkits.axes_grid import make_axes_locatable

class BballAxes(Axes):

    """axes for basketball court"""

    def __init__(self, *args, **kwargs):
        """TODO: to be defined1.

        Parameters
        ----------
        *args : TODO
        **kwargs : TODO


        """
        super(BballAxes, self).__init__(*args, **kwargs)
        ang_1=np.arange(0,np.pi,0.00001)
        ang_2=np.arange(np.pi,2*np.pi,0.00001)

        # Court Lines
        self.plot([0,50],[0,0],'k',linewidth=1)
        self.plot([0,50],[47,47],'k',linewidth=1)
        self.plot([0,0],[0,47],'k',linewidth=1)
        self.plot([50,50],[0,47],'k',linewidth=1)
        self.plot([17,17],[0,19],'k',linewidth=1)
        self.plot([33,33],[0,19],'k',linewidth=1)
        self.plot([19,19],[0,19],'k',linewidth=1)
        self.plot([31,31],[0,19],'k',linewidth=1)
        self.plot([17,33],[19,19],'k',linewidth=1)
        self.plot([17,33],[19,19],'k',linewidth=1)
        self.plot([22,28],[4,4],'k',linewidth=1)

        self.plot([3,3],[0,14],'k',linewidth=1)
        self.plot([47,47],[0,14],'k',linewidth=1)

        # Hoop
        h = self.plot(25+(9.0/12)*np.cos(ang_1),(4 + 9.0/12)+(9.0/12)*np.sin(ang_1),linewidth=1,color='orange')
        h = self.plot(25+(9.0/12)*np.cos(ang_2),(4 + 9.0/12)+(9.0/12)*np.sin(ang_2),linewidth=1,color='orange')

        # Arc
        self.plot(25+6*np.cos(ang_1),19+6*np.sin(ang_1),'k',linewidth=1)
        self.plot(25+6*np.cos(ang_2),19+6*np.sin(ang_2),'k--',linewidth=1)

        # 3-Point
        extra =np.arcsin((14 - 4 - 9/12)/(23 + 9./12))
    #    extra = 0.401
        ang_3= np.arange(extra,np.pi-extra,0.00001)
        three_pt_xs = 25+(23 + 9/12)*np.cos(ang_3)
        three_pt_ys = (4 + 9/12)+(23 + 9/12)*np.sin(ang_3)
        self.plot(three_pt_xs, three_pt_ys,'k',linewidth=1)
        self.set_xlim(0,50)
        self.set_ylim(0,47)
register_projection(BballAxes)

class ShotChartScatter(Plot):

    """Docstring for ShotChartScatter. """
    _DefaultAxesClass = BballAxes
    def __init__(self, shotcharts, **kwargs):
        """shot chart scatter plot

        Parameters
        ----------
        *shotcharts : `list` of :class:`basketball_db.shotchart.ShotChart`
            list of shot charts you want to plot
        **kwargs : `dict`
            keyward arguments for a scatter plot
        """
        super(ShotChartScatter, self).__init__()
        if not isinstance(shotcharts, list):
            shotcharts = [shotcharts]
        for sc in shotcharts:
            self.add_shot_chart(sc, **kwargs)

    def add_shot_chart(self, sc, **kwargs):
        """
        add a shot chart

        Parameters
        ----------
        shotchart : :class:`basketball_db.shotchart.ShotChart`
            shot chart
        """
        mades = sc['result']
        misses = ~sc['result']
        self.add_scatter(50 - sc['shot_xs'][mades],sc['shot_ys'][mades],c='g',
                **kwargs)
        self.add_scatter(50 - sc['shot_xs'][misses],sc['shot_ys'][misses],c='r',
                **kwargs)

#class ShotChartHex(Plot):
#
#    """Docstring for ShotChartHex. """
#    _DefaultAxesClass = BballAxes
#
#    def __init__(self,*shotcharts, histval='points', **kwargs):
#        """shot charts
#
#        Parameters
#        ----------
#        *shotcharts : TODO
#        **kwargs : TODO
#
#
#        """
#        Plot.__init__(self)
#        if histval=='points'
#        self.hexbin(
