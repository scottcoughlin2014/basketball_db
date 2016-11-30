"""Decorator for basketball_db plotting
"""

from functools import wraps

from matplotlib.figure import Figure
from matplotlib.axes import Axes

__author__ = "Duncan Macleod <duncan.macleod@ligo.org>"


def auto_refresh(func):
    """Decorate `func` to refresh the containing figure when complete
    """
    @wraps(func)
    def wrapper(artist, *args, **kwargs):
        """Call the method, and refresh the figure on exit
        """
        refresh = kwargs.pop('refresh', False)
        try:
            return func(artist, *args, **kwargs)
        finally:
            if isinstance(artist, Axes):
                if refresh or artist.figure.get_auto_refresh():
                    artist.figure.refresh()
            elif isinstance(artist, Figure):
                if refresh or artist.get_auto_refresh():
                    artist.refresh()
            else:
                raise TypeError("Cannot determine containing Figure for "
                                "auto_refresh() decorator")
    return wrapper


def axes_method(func):
    """Decorate `func` to call the same method of the contained `Axes`
    Raises
    ------
    RuntimeError
        if multiple `Axes` are found when the method is called.
        This method makes no attempt to decide which `Axes` to use
    """
    @wraps(func)
    def wrapper(figure, *args, **kwargs):
        """Find the relevant `Axes` and call the method
        """
        axes = [ax for ax in figure.axes if ax not in figure._coloraxes]
        if len(axes) == 0:
            raise RuntimeError("No axes found for which '%s' is applicable"
                               % func.__name__)
        if len(axes) != 1:
            raise RuntimeError("{0} only applicable for a Plot with a "
                               "single set of data axes. With multiple "
                               "data axes, you should access the {0} "
                               "method of the relevant Axes (stored in "
                               "``Plot.axes``) directly".format(func.__name__))
        axesf = getattr(axes[0], func.__name__)
        return axesf(*args, **kwargs)
    return wrapper
