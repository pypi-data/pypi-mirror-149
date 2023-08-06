"""Direct Plot

Educational library to directly plot single data points.

ATTENTION: This library is slow and not suited for production use!

It has been developed for educational purpose, especially to visualize 
numerical algorithms e.g. for simulation or plotting measurement data.

It wraps matplotlib and pyplot commands in even simpler commands:

```
import math
import directplot as dp

dp.init()

for i in range(51):
    x = i*2*math.pi/50
    y = math.sin(x)
    dp.add(0, x, y)

dp.waitforclose()
```

The following functions are provided:

* `init()` Initializes and opens a Direct Plot window
* `add()` Adds a single point to a plot line
* `showMarker()` Shows or hides marker points on a plot line or on all plot lines
* `label()` Changes the label of a plot line used in the legend
* `title()` Changes the title of a sub-plot
* `xylabel()` Changes the axis lables of a sub-plot
* `refresh()` Refreshes the contents of the plot window
* `close()` Closes the Direct Plot window
* `clear()` Deletes the contents of the plot window
* `waitforclose()` Displays a new window title on the plot window and
                   blocks execution until user closes the window.
"""

__version__ = '0.4.1'
__author__ = 'Georg Braun'

import inspect as _inspect
from typing import Sequence as _Sequence
from .directplot import __DirectPlot
import platform as _platform
import matplotlib.pyplot as _plt

def init(titles: _Sequence[str] = ["Direct-Plot"], linesPerSubplot: int = 4, showMarker: bool = True, maxPoints: int = 10000) -> None:
    """Initializes and opens a Direct Plot window.

    Parameters:
    -----------
    * titles: A list or tuple containing 1 to 3 strings, resulting in 1 to 3 sub-plots on the plot window. Optional with a default title for a single sub-plot.
    * linesPerSubplot: Number of lines (data series) per sub-plot. Optional with default 4
    * showMarker: Determines if data points are emphasized with a little dot. Optional with default True
    * maxPoints: Maximum number of data points per line (data series). Optional with default 10000

    Returns:
    --------
    None

    Examples:
    ---------
    ```
    dp.init()
    dp.init(["Results"])
    dp.init(["Height", "Speed", "Forces"], 2, False)
    ```
    """

    global __dp
    if __dp is not None:
        raise Exception(f"ERROR in directplot.{_inspect.currentframe().f_code.co_name}(): YOU HAVE CALLED {_inspect.currentframe().f_code.co_name}() TOO OFTEN!")
    __dp = __DirectPlot(titles, linesPerSubplot, showMarker, maxPoints)



def close() -> None:
    """Closes the Direct Plot window.

    Example:
    --------
    ```
    dp.close()
    ```
    """
    global __dp
    try:
        __dp.close()
        del(__dp)
        __dp = None
    except AttributeError:
        raise Exception(f"ERROR in directplot.{_inspect.currentframe().f_code.co_name}(): NO MORE PLOT-WINDOW - DID YOU CLOSE IT ALREADY?")



def clear() -> None:
    """Deletes the contents of the plot window.

    Keeps the number of sub-plots, the number of lines per sub-plot and the titles of the sub-plots. Everything else is reset/deleted.

    Example:
    --------
    ```
    dp.clear()
    ```
    """
    
    global __dp
    try:
        __dp.clear()
    except AttributeError:
        raise Exception(f"ERROR in directplot.{_inspect.currentframe().f_code.co_name}(): NO MORE PLOT-WINDOW - DID YOU CLOSE IT ALREADY?")



def waitforclose(msg: str = None) -> None:
    """Displays a new window title on the plot window and blocks execution until user closes the window.

    Parameters:
    -----------
    * msg: A string to be shown on the window title. Optional with default None resulting in a standard title

    Returns:
    --------
    None

    Examples:
    ---------
    ```
    dp.waitforclose()
    dp.waitforclose("PLEASE CLOSE THIS WINDOW")
    ```
    """

    global __dp
    try:
        __dp.waitforclose(msg)
        del(__dp)
        __dp = None
    except AttributeError:
        raise Exception(f"ERROR in directplot.{_inspect.currentframe().f_code.co_name}(): NO MORE PLOT-WINDOW - DID YOU CLOSE IT ALREADY?")



def add(id: int, x: float, y: float, refresh: bool = True) -> None:
    """Adds a single point to a plot line.

    Parameters:
    -----------
    * id: The id of the target plot line
    * x: x value
    * y: y value
    * refresh: Determines if the plot is refreshed immediately resulting in slower plotting speed. Optional with default True

    Returns:
    --------
    None

    Examples:
    ---------
    ```
    dp.add(0, 0.1, 2.7)
    dp.add(1, 1.1, 7.3, False)
    dp.add(1, 1.2, 7.2)
    ```
    """

    global __dp
    try:
        __dp.add(id, x, y, refresh)
    except AttributeError:
        raise Exception(f"ERROR in directplot.{_inspect.currentframe().f_code.co_name}(): NO MORE PLOT-WINDOW - DID YOU CLOSE IT ALREADY?")



def refresh() -> None:
    """Refreshes the contents of the plot window.

    Mostly used in conjunction with add() and refresh=False.

    Example:
    --------
    ```
    dp.add(0, 0.1, 7.3, False)
    dp.add(0, 0.2, 6.9, False)
    dp.add(0, 0.3, 2.1, False)
    dp.refresh()
    ```
    """

    global __dp
    try:
        __dp.refresh()
    except AttributeError:
        raise Exception(f"ERROR in directplot.{_inspect.currentframe().f_code.co_name}(): NO MORE PLOT-WINDOW - DID YOU CLOSE IT ALREADY?")



def showMarker(show: bool = True, id: int = None) -> None:
    """Shows or hides marker points on a plot line or on all plot lines.

    Parameters:
    -----------
    * show: Show or hide markes. Optional with default True
    * id: The id of the target plot line. Optional with default None resulting in a change of markers on all plot lines.

    Returns:
    --------
    None

    Examples:
    ---------
    ```
    dp.showMarker()
    dp.showMarker(False, 1)
    ```
    """

    global __dp
    try:
        __dp.showMarker(show, id)
    except AttributeError:
        raise Exception(f"ERROR in directplot.{_inspect.currentframe().f_code.co_name}(): NO MORE PLOT-WINDOW - DID YOU CLOSE IT ALREADY?")



def label(id: int, label: str) -> None:
    """Changes the label of a plot line used in the legend.

    Parameters:
    -----------
    * id: The id of the target plot line
    * label: The new label text

    Returns:
    --------
    None

    Examples:
    ---------
    ```
    dp.label(0, "mass in kg")
    ```
    """

    global __dp
    try:
        __dp.label(id, label)
    except AttributeError:
        raise Exception(f"ERROR in directplot.{_inspect.currentframe().f_code.co_name}(): NO MORE PLOT-WINDOW - DID YOU CLOSE IT ALREADY?")



def title(id: int, title: str) -> None:
    """Changes the title of a sub-plot

    Parameters:
    -----------
    * id: The id of the target plot line used to determine the corresponding sub-plot
    * title: The new title text

    Returns:
    --------
    None

    Examples:
    ---------
    ```
    dp.title(0, "Simulated Values")
    ```
    """
    
    global __dp
    try:
        __dp.title(id, title)
    except AttributeError:
        raise Exception(f"ERROR in directplot.{_inspect.currentframe().f_code.co_name}(): NO MORE PLOT-WINDOW - DID YOU CLOSE IT ALREADY?")



def xylabel(id: int, xlabel: str, ylabel: str) -> None:
    """Changes the axis lables of a sub-plot

    Parameters:
    -----------
    * id: The id of the target plot line used to determine the corresponding sub-plot
    * xlabel: New label for the x axis
    * ylabel: New label for the y axis

    Returns:
    --------
    None

    Examples:
    ---------
    ```
    dp.xylabel(0, "time in s", "force in N")
    ```
    """
    
    global __dp
    try:
        __dp.xylabel(id, xlabel, ylabel)
    except AttributeError:
        raise Exception(f"ERROR in directplot.{_inspect.currentframe().f_code.co_name}(): NO MORE PLOT-WINDOW - DID YOU CLOSE IT ALREADY?")




def dp_selftest() -> None:
    """Runs some tests and quits."""

    import time

    print()
    print("Welcome to directplot. We will run some tests for you. Have fun...")
    print()

    print("test1:", _test1.__doc__)
    _test1()
    print("test2:", _test2.__doc__)
    _test2()
    print("test3:", _test3.__doc__)
    _test3()

    print()
    print("Done with testing. Bye bye ...")
    for i in range(3, 0, -1):
        print(i, end=" ", flush=True)
        time.sleep(1)
    print()



def _test1() -> None:
    """Plots a sine curve"""

    import math
    import time

    time.sleep(0.2)
    points=51
    init()
    for i in range(points):
        x = i*2*math.pi/(points-1)
        y = math.sin(x)
        add(0, x, y)
    time.sleep(2)
    close()



def _test2() -> None:
    """Combines sine and cosine to a circle in two sub-plots"""

    import math
    import time

    time.sleep(0.2)
    points=51
    init(["Sinus, Cosinus", "Circle"], 2, False)
    label(0, "Cosinus")
    label(1, "Sinus")
    for i in range(points):
        t = i*2*math.pi/(points-1)
        x = math.cos(t)
        y = math.sin(t)
        add(0, t, x, False)
        add(1, t, y, False)
        add(2, x, y, False)
        refresh()
    time.sleep(2)
    close()



def _test3() -> None:
    """Combines sine and cosine to a circle in two sub-plots and plots sinc() in a third one."""

    import math
    import time
    import numpy as _np

    time.sleep(0.2)
    points=51
    init(["Sinus, Cosinus", "Circle", "sinc()"], 2)
    label(0, "Cosinus")
    label(1, "Sinus")
    label(4, "sinc()")
    for i in range(points):
        t = i*2*math.pi/(points-1)
        x = math.cos(t)
        y = math.sin(t)
        add(0, t, x, False)
        add(1, t, y, False)
        add(2, x, y, False)
        add(4, t, _np.sinc(t-math.pi), False)
        refresh()
    time.sleep(3)
    close()


def onImport():
    print(f'directplot v{__version__} started with backend {_plt.get_backend()}')
    handleBackend()
    print()

def handleBackend():
    if _platform.system().lower() == 'darwin':
        targetBackend = 'TkAgg'
        print(f'Seems like MacOS. Trying to switch backend to {targetBackend}')
        try:
            _plt.switch_backend(targetBackend)
        except Exception as exceptionDetails:
            print(f'ERROR: Could not switch to {targetBackend}! Details:')
            print(f'{exceptionDetails}')
            print()
            print(f'Will try with current backend {_plt.get_backend()}')
        else:
            print(f'Successfully switched to backend {_plt.get_backend()}')


__dp = None
onImport()
