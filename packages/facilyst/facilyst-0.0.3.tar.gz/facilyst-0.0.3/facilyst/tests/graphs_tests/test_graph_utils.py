from facilyst.graphs import Line, Scatter, _all_graph_data_types

all_graph_data_types = [Line, Scatter]


def test_graph_data_children():
    all_graph_types = {graph_type.__name__ for graph_type in all_graph_data_types}
    all_subclasses = {subclass.__name__ for subclass in _all_graph_data_types()}
    assert all_graph_types == all_subclasses
