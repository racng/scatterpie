from typing import Union, Optional, Sequence, Any, Mapping, List, Tuple, Callable
from collections.abc import Iterable
import operator

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.axes import Axes

def pie_marker(
        ratios: Sequence[float], 
        res: int = 50, 
        direction: str = "+", 
        start: float = 0.0,
        ) -> Tuple[list, list]:
    """
    Create each slice of pie as a separate marker.
    Parameters:
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
        n = round(ratio * res) # number of points forming the arc
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
    colors: Union[List, str] = "tab10", 
    res: int = 50, 
    direction: str = "+", 
    start: float = 0.0,
    ax=None, 
    size=100, 
    edgecolor="none", 
    **kwargs) -> Axes:
    """
    Plot scatter pie plots.
    Parameters:
        x: list/array of x values
        y: list/array of y values
        ratios: List of lists of ratios that add up to 1.  
        colors: List of colors in order, or name of colormap.
        res: Number of points around the circle.
        direction: '+' for counter-clockwise, or '-' for clockwise.
        start: Starting position in radians. 
        kwargs: Arguments passed to :func:`matplotlib.pyplot.scatter`

    Returns:
        A :class:`~matplotlib.axes.Axes`
    """
    if ax is None:
        _, ax = plt.subplots()

    # convert arguments to interables when there is only one point
    if (not isinstance(x, Iterable)) and type(ratios[0]==float):
        print("Plotting single point")
        x = [x]
        y = [y]
        ratios = [ratios]
    
    # Set colors
    if type(colors) == str:
        cmap = plt.get_cmap(colors)
        colors = [cmap(i) for i in range(len(ratios[0]))]

    # make pie marker for each unique set of ratios
    df = pd.DataFrame({'x':x, 'y':y, 'ratios':ratios})
    df.ratios = df.ratios.apply(tuple)
    gb = df.groupby("ratios")
    for ratio in gb.groups:
        group = gb.get_group(ratio)
        xys, ss = pie_marker(ratio, res=res, direction=direction, start=start)
        for xy, s, color in zip(xys, ss, colors):
            # plot non-zero slices
            if s != 0:
                ax.scatter(group.x, group.y, marker=xy, s=[s*s*size], 
                    facecolor=color, edgecolor=edgecolor, **kwargs)
    return ax

def get_palette(categories, cmap):
    """
    Generate dictionary mapping categories to color.
    """
    cc = plt.get_cmap(cmap)
    if len(categories) > len(cc.colors):
        raise ValueError("Number of categories more than number of colors in cmap.")
    palette = {x: cc(i) for i, x in enumerate(categories)}
    return palette

def scatter_pie_from_df(
    df: pd.DataFrame,
    x: str,
    y: str,
    cols: Optional[list] = [],
    normalize: bool = True,
    return_df: bool = False,
    palette: Optional[dict] =  None,
    cmap: Optional[str] = "tab10",
    **kwargs,
    ) -> Axes:
    """
    Plot scatter pie based on columns in a DataFrame.
    
    Parameters:
        df: Dataframe containing x, y, and additional count columns.
        x: Column to use as x-values.
        y: Column to use as y-values.
        cols: List of columns in dataframe to use as ratios and plotting. 
            If [], uses all columns besides x and y.
        normalize: If True, calculate ratios using selected columns. 
        return_df: If True, also return normalized dataframe.
        palette: Dictionary mapping column name to color. 
            If None, create mapping using cmap. 
        cmap: Name of colormap to use if palette not provided. 
        kwargs: Arguments passed to :func:`scatter_pie`

    Returns:
        A :class:`~matplotlib.axes.Axes` and normalized df if `return_df` is True.
    """
    # make copy of dataframe and set xy as index
    df = df.copy().set_index([x, y])
    
    if (type(cols)==list) & (len(cols) > 1):
        # used specified list of columns
        df = df.loc[:, cols]
    elif cols!=[]:
        raise ValueError("cols must be a list of more than one column headers")

    # row normalize
    categories = df.columns
    df = df.div(df.sum(axis=1), axis=0).fillna(0)
    df = df.reset_index()

    # generate mapping of category to color
    if palette == None:
        palette = get_palette(categories, cmap)
    
    ratios =  df[categories].to_records(index=False).tolist()
    colors = [palette[cat] for cat in categories]
    ax = scatter_pie(df[x].values, df[y].values, ratios, colors, **kwargs)

    # generate legend as separate figure 
    if return_df:
        return ax, df
    return ax

def scatter_legend(ax, labels, palette, **kwargs):
    handles = [plt.scatter([], [], color=palette[l], label=l) for l in labels]
    ax.legend(handles=handles, **kwargs)
    