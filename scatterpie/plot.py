from typing import Union, Optional, Sequence, Any, Mapping, List, Tuple, Callable
import operator
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def pie_marker(
        ratios: Sequence[float], 
        res: int = 100, 
        direction: str = "+", 
        start: float = 0.0,
        ) -> Tuple[list, list]:
    """
    Create each slice of pie as a separate marker.
    Args:
        ratios(list): List of ratios that add up to 1.  
        res: Number of points around the circle.
        direction: '+' for counter-clockwise, or '-' for clockwise.
        start: Starting position in radians. 
    Returns:
        xys, ss: Tuple of list of xy points and sizes of each slice in the pie marker.
    """

    if np.abs(np.sum(ratios) - 1) > 0.01:
        print("Warning: Ratios do not add up to 1.")

    if direction == '+':
        op = operator.add
    elif direction == '-':
        op = operator.sub
    
    xys = [] # list of xy points of each slice
    ss = [] # list of size of each slice
    start = float(start)
    for ratio in ratios:
        # points on the circle including the origin (0,0) and the slice
        end = op(start, 2 * np.pi * ratio)
        n = round(ratio * res) # number of points
        x = [0] + np.cos(np.linspace(start, end, n)).tolist()
        y = [0] + np.sin(np.linspace(start, end, n)).tolist()
        xy = np.column_stack([x, y])
        xys.append(xy)
        ss.append(np.abs(xy).max())
        start = end
        
    return xys, ss

def scatter_pie(
    x: Union[int, float, Sequence[int], Sequence[float]], 
    y: Union[int, float, Sequence[int], Sequence[float]], 
    ratios: Union[Sequence[float], Sequence[Sequence[float]]], 
    colors: List, 
    res: int = 100, 
    direction: str = "+", 
    start: float = 0.0,
    ax=None, 
    size=100, 
    edgecolor="none", 
    **kwargs):
    """
    Plot scatter pie plots.
    Args:
        x: list/array of x values
        y: list/array of y values
        ratios: List of lists of ratios that add up to 1.  
        colors: List of colors in order. 
        res: Number of points around the circle.
        direction: '+' for counter-clockwise, or '-' for clockwise.
        start: Starting position in radians. 

    Returns:
        A :class:`~matplotlib.axes.Axes`
    """
    if ax is None:
        _, ax = plt.subplots()

    # convert arguments to interables when there is only one point
    if (type(x) == type(y) != list) and type(ratios[0]==float):
        x = [x]
        y = [y]
        ratios = [ratios]
    
    # make pie marker for each unique set of ratios
    df = pd.DataFrame({'x':x, 'y':y, 'ratios':ratios})
    df.ratios = df.ratios.apply(tuple)
    gb = df.groupby("ratios")
    for ratio in gb.groups:
        group = gb.get_group(ratio)
        xys, ss = pie_marker(ratio)
        for xy, s, color in zip(xys, ss, colors):
            # plot non-zero slices
            if s != 0:
                ax.scatter(group.x, group.y, marker=(xy,0), s=[s*s*size], 
                    facecolor=color, edgecolor=edgecolor, **kwargs)
    return ax
    