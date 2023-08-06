from ..gui_data_selector import Action_on_selector_update
from ..widgets.graphsVisualWidget.pyqtgraph import mkBrush, mkPen


class On_select_highlight(Action_on_selector_update):
    def __init__(self, theLinkDataGraphs, theWgPlot):
        """

        :param theLinkDataGraphs: :class:`~optimeed.core.linkDataGraph.LinkDataGraph`
        :param theWgPlot: :class:`~optimeed.visualize.gui.widgets.widget_graphs_visual.widget_graphs_visual`
        """

        self.theLinkDataGraphs = theLinkDataGraphs
        self.theWgPlot = theWgPlot
        # self.previous_selected = list()

    def selector_updated(self, selection_name, the_collection, selected_data, not_selected_data):
        """
        Action to perform once the data have been selected

        :param selection_name: name of the selection (deprecated ?)
        :param the_collection: the collection
        :param selected_data: indices of the data selected
        :param not_selected_data: indices of the data not selected
        :return:
        """
        # self.reset_previous_brushes()
        id_collection = self.theLinkDataGraphs.get_idcollection_from_collection(the_collection)
        res, _ = self.theLinkDataGraphs.get_graph_and_trace_from_idCollection(id_collection)
        for idGraph, idTrace in res:
            idPoints_selected = self.theLinkDataGraphs.get_idPoints_from_indices_in_collection(idGraph, idTrace, selected_data)
            idPoints_NOTselected = self.theLinkDataGraphs.get_idPoints_from_indices_in_collection(idGraph, idTrace, not_selected_data)
            traceVisual = self.theWgPlot.get_trace(idGraph, idTrace)
            traceVisual.set_brushes(idPoints_selected, mkBrush(*traceVisual.get_color(), 255), update=False)  # Darkest
            traceVisual.set_symbolPens(idPoints_selected, traceVisual.get_base_symbol_pen(), update=False)  # Clearest
            traceVisual.set_brushes(idPoints_NOTselected, mkBrush(*traceVisual.get_color(), 30), update=False)  # Clearest
            traceVisual.set_symbolPens(idPoints_NOTselected, mkPen(*traceVisual.get_color(), 30), update=False)  # Clearest
            # self.previous_selected.append((idPoints, idGraph, idTrace))
        self.theWgPlot.update_graphs()

    # def reset_previous_brushes(self):
    #     for id_points, graph_id, trace_id in self.previous_selected:
    #         traceVisual = self.theWgPlot.get_trace(graph_id, trace_id)
    #         for id_point in id_points:
    #             traceVisual.reset_brush(id_point, update=False)
    #         traceVisual.signal_must_update.emit()
    #     self.previous_selected = list()

    def get_name(self):
        return "Highlight points"
