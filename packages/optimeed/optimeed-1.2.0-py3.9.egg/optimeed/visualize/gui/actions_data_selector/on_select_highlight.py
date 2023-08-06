from ..gui_data_selector import Action_on_selector_update


class On_select_highlight(Action_on_selector_update):
    def __init__(self, theLinkDataGraphs, theWgPlot):
        """

        :param theLinkDataGraphs: :class:`~optimeed.core.linkDataGraph.LinkDataGraph`
        :param theWgPlot: :class:`~optimeed.visualize.gui.widgets.widget_graphs_visual.widget_graphs_visual`
        """

        self.theLinkDataGraphs = theLinkDataGraphs
        self.theWgPlot = theWgPlot
        self.previous_selected = list()

    def selector_updated(self, selection_name, the_collection, indices_data):
        """
        Action to perform once the data have been selected

        :param selection_name: name of the selection (deprecated ?)
        :param the_collection: the collection
        :param indices_data: indices of the data
        :return:
        """
        self.reset_previous_brushes()
        id_collection = self.theLinkDataGraphs.get_idcollection_from_collection(the_collection)
        res, _ = self.theLinkDataGraphs.get_graph_and_trace_from_collection(id_collection)
        for idGraph, idTrace in res:
            idPoints = self.theLinkDataGraphs.get_idPoints_from_indices_in_collection(idGraph, idTrace, indices_data)
            traceVisual = self.theWgPlot.get_trace(idGraph, idTrace)
            traceVisual.set_brushes(idPoints, (255, 0, 0))
            self.previous_selected.append((idPoints, idGraph, idTrace))
        self.theLinkDataGraphs.update_graphs()

    def reset_previous_brushes(self):
        for id_points, graph_id, trace_id in self.previous_selected:
            traceVisual = self.theWgPlot.get_trace(graph_id, trace_id)
            for id_point in id_points:
                traceVisual.reset_brush(id_point, update=False)
            traceVisual.signal_must_update.emit()
        self.previous_selected = list()

    def get_name(self):
        return "Highlight points"
