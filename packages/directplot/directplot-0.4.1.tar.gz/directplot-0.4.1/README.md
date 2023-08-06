# python-directplot

Educational library to directly plot single data points.

## Description

Educational library to directly plot single data points.

ATTENTION: This library is slow and not suited for production use!

It has been developed for educational purpose, especially to visualize 
numerical algorithms e.g. for simulation or plotting measurement data.

It wraps matplotlib and pyplot commands in even simpler commands:


```python
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

* [`init()`](#init) Initializes and opens a Direct Plot window
* [`add()`](#add) Adds a single point to a plot line
* [`showMarker()`](#showmarker) Shows or hides marker points on a plot line or on all plot lines
* [`label()`](#label) Changes the label of a plot line used in the legend
* [`title()`](#title) Changes the title of a sub-plot
* [`xylabel()`](#xylabel) Changes the axis lables of a sub-plot
* [`refresh()`](#refresh) Refreshes the contents of the plot window
* [`close()`](#close) Closes the Direct Plot window
* [`clear()`](#clear) Deletes the contents of the plot window
* [`waitforclose()`](#waitforclose) Displays a new window title on the plot window and blocks execution until user closes the window.

## API

Functions are listed alphabetical order. Unless otherwise noted, the return type is `None`.


### add()

Adds a single point to a plot line.

If the number of points per plot line exceeds `maxPoints` (see [`init()`](#init)), the oldest point is removed automatically, resulting in a scroll behavior of the plots.

```python
add(id, x, y, refresh=True)
```

Parameter:

* `id` (int) – The id of the target plot line
* `x` (float) – x value
* `y` (float) – y value
* `refresh` (bool) – Determines if the plot is refreshed immediately resulting in slower plotting speed. Optional with default `True`

Example

```python
dp.add(0, 0.1, 2.7)
dp.add(1, 1.1, 7.3, False)
dp.add(1, 1.2, 7.2)
```

### clear()

Deletes the contents of the plot window.

Keeps the number of sub-plots, the number of lines per sub-plot and the titles of the sub-plots. Everything else is reset/deleted.

```python
clear()
```

Example

```python
dp.clear()
```

### close()

Closes the Single Point Plot window.

```python
close()
```

Example

```python
dp.close()
```


### init()

Initializes and opens a Single Point Plot window.

```python
init(titles=['Single-Point-Plot'], linesPerSubplot=4, showMarker=True, maxPoints=10000)
```

Parameter

* `titles` (list(str)) – A list or tuple containing 1 to 3 strings, resulting in 1 to 3 sub-plots on the plot window. Optional with a default title for a single sub-plot.
* `linesPerSubplot` (int) – Number of lines (data series) per sub-plot. Optional with default `4`
* `showMarker` (bool) – Determines if data points are emphasized with a little dot. Optional with default `True`
* `maxPoints` (int) - Maximum number of data points per line (data series). Optional with default 10000<br>
  If the number of points per plot line exceeds `maxPoints`, the oldest point is removed automatically, resulting in a scroll behavior of the plots.

Example

```python
dp.init()
```

or 

```python
dp.init(["Results"])
```

or

```python
dp.init(["Height", "Speed", "Forces"], linesPerSubplot=2, showMarker=False)
```

or

```python
dp.init(["Temperature °C", "Pressure mbar", "Humidity %"], linesPerSubplot=1,  maxPoints=100)
```



### label()

Changes the label of a plot line used in the legend.

```python
label(id, label)
```


Parameter

* `id` (int) – The id of the target plot line
* `label` (str) – The new label text


Example

```python
dp.label(0, "mass in kg")
```



### refresh()

Refreshes the contents of the plot window.

Mostly used in conjunction with `add()` and `refresh=False`.

```python
refresh()
```


Example

```python
dp.add(0, 0.1, 7.3, False)
dp.add(0, 0.2, 6.9, False)
dp.add(0, 0.3, 2.1, False)
dp.refresh()
```



### showMarker()

Shows or hides marker points on a plot line or on all plot lines.

```python
showMarker(show=True, id=None)
```


Parameter

* `show` (bool) – Show or hide markes. Optional with default `True`
* `id` (int) – The id of the target plot line. Optional with default `None` resulting in a change of markers on all plot lines.


Example

```python
dp.showMarker()
```

or

```python
dp.showMarker(False, 1)
```



### title()

Changes the title of a sub-plot

```python
title(id, title)
```


Parameter

* `id` (int) – The id of the target plot line used to determine the corresponding sub-plot
* `title` (str) – The new title text


Example

```python
dp.title(0, "Simulated Values")
```



### waitforclose()

Displays a new window title on the plot window and blocks execution until user closes the window.

```python
waitforclose(msg=None)
```


Parameter

* `msg` (str) – A string to be shown on the window title. Optional with default `None` resulting in a standard title


Example

```python
dp.waitforclose()
```

or

```python
dp.waitforclose("PLEASE CLOSE THIS WINDOW")
```



### xylabel()

Changes the axis lables of a sub-plot.

```python
xylabel(id, xlabel, ylabel)
```


Parameter

* `id` (int) – The id of the target plot line used to determine the corresponding sub-plot
* `xlabel` (str) – New label for the x axis
* `ylabel` (str) – New label for the y axis



Example

```python
dp.xylabel(0, "time in s", "force in N")
```



## Development

### Build pypi package

Tools needed to build and publish to PyPi under Windows:

```
python -m pip install --upgrade build
python -m pip install --upgrade twine
```

Tools needed to build and publish to PyPi Linux/MacOS:

```
python3 -m pip install --upgrade build
python3 -m pip install --upgrade twine
```


Build package:

```
python -m build
```

Upload package to pypi:

Before uploading, delete outdated build artifacts in the `dist` folder, such that only the latest build files are uploaded.

```
twine upload dist/*
```
