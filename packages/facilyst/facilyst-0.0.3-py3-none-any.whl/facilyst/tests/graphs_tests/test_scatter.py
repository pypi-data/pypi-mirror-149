import matplotlib
import pandas as pd

from facilyst.graphs import Scatter


def test_scatter():
    X = pd.DataFrame()
    X["x_axis"] = [i for i in range(10)]
    X["y_axis"] = [i for i in range(10)]

    scatter = Scatter(x="x_axis", y="y_axis", dataset=X)
    assert issubclass(type(scatter.graph_obj), matplotlib.axes.SubplotBase)
