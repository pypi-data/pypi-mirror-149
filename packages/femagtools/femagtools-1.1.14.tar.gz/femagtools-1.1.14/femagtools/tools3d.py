""" Interface for 3D plotting functions

Module containing functions that allow to access the 3d-functions
with the normal pylab syntax.

>>> from pylab import *
>>> from tools3d import *
>>> x = frange(-2,2,0.1)
>>> X, Y = meshgrid(x,x)
>>> wireframe(X, Y, X**2+Y**2)             #doctest: +ELLIPSIS
<mpl_toolkits.mplot3d.art3d.Line3DCollection object at 0x...>
>>> show()

"""

from pylab import gca, figure, subplot, draw_if_interactive
from mpl_toolkits.mplot3d import axes3d


def _check_axis():
    from matplotlib.projections import get_projection_class
    from matplotlib import _pylab_helpers

    create_axis = True
    if _pylab_helpers.Gcf.get_active() is not None:
        if isinstance(gca(), get_projection_class('3d')):
            create_axis = False
    if create_axis:
        figure()
        subplot(111, projection='3d')


def wireframe(*args, **kwargs):
    """
        wrapper for axes3d.Axes3D.plot_wireframe
    
        allows to create wireframe plots with the usual
        pylab syntax.

    """
    _check_axis()
    ret = gca().plot_wireframe(*args, **kwargs)
    draw_if_interactive()
    return ret

def surface(*args, **kwargs):
    """
        wrapper for axes3d.Axes3D.plot_surface
    
        allows to create surface plots with the usual
        pylab syntax.

        Don't forget to set cstride=1 and rstride=1. 
        Otherwise you might get very ugly plots.

    """
    _check_axis()
    ret = gca().plot_surface(*args, **kwargs)
    draw_if_interactive()
    return ret

wireframe.__doc__ += axes3d.Axes3D.plot_wireframe.__doc__
surface.__doc__   += axes3d.Axes3D.plot_surface.__doc__

