# d_star
Python D* (D Star) Lite implementation

Based on https://github.com/daniel-beard/DStarLiteJava

Usage example:

```python
from d_star import DStar

# setting start and end points
pf = DStar(x_start=0, y_start=1, x_goal=3, y_goal=1)

# making cell unpassable
pf.update_cell(2, 1, -1)

# making cell passable
pf.update_cell(2, 1, 0)

# recalculating path
pf.replan()
path = pf.get_path()
```

A couple of useful functions:

```python
pf.update_start(x, y)
pf.update_goal(x, y)
```
