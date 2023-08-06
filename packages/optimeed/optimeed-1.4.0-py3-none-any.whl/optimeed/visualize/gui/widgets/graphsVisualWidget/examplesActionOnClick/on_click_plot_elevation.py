from optimeed.visualize.gui.widgets.widget_graphs_visual import on_graph_click_interface
import numpy as np
from ..colormap_pyqtgraph import matplotlib_colormap_to_pg_colormap


class on_click_plot_elevation(on_graph_click_interface):
    """On click: extract the pareto from the cloud of points"""
    def __init__(self, theDataLink, get_third_dim_method, colormap_name='jet'):
        """
        :param theDataLink: :class:`~optimeed.core.linkDataGraph.LinkDataGraph`
        :param get_third_dim_method: method that takes as input a device and returns the elevation value
        """
        self.theDataLink = theDataLink
        self.get_third_dim_method = get_third_dim_method
        self.theColormap = matplotlib_colormap_to_pg_colormap(colormap_name)

    def graph_clicked(self, theGraphVisual, index_graph, index_trace, _):

        theCollection = self.theDataLink.get_collection_from_graph(index_graph, index_trace, getMaster=True)
        # Get third dimension
        indices = list()
        values = list()
        for k, data in enumerate(theCollection.get_data_generator()):
            value = self.get_third_dim_method(data)
            if np.isfinite(value):
                indices.append(k)
                values.append(value)
        # Get colors to set
        min_value = min(values)
        max_value = max(values)
        colors = [(0, 0, 0)]*len(values)
        for k, value in enumerate(values):
            normalized_value = (value - min_value)/(max_value-min_value)
            colors[k] = self.theColormap.mapToQColor(normalized_value)
        # Get equivalent points to change
        points_indices = self.theDataLink.get_idPoints_from_indices_in_collection(index_graph, index_trace, indices)
        # Set the colors
        theGraphVisual.get_graph(index_graph).get_trace(index_trace).set_brushes(points_indices, colors)
        self.theDataLink.update_graphs()

    def get_name(self):
        return "Show elevation"
