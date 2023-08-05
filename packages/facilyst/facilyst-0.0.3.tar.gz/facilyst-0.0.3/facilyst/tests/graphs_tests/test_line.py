import matplotlib
import pandas as pd

from facilyst.graphs import Line


def test_line():
    X = pd.DataFrame()
    X["x_axis"] = [i for i in range(10)]
    X["y_axis"] = [i for i in range(10)]

    line = Line(x="x_axis", y="y_axis", dataset=X)
    assert issubclass(type(line.graph_obj), matplotlib.axes.SubplotBase)
