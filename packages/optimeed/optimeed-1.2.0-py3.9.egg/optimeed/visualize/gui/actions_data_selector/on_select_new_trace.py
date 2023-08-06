from ..gui_data_selector import Action_on_selector_update
from optimeed.core import ListDataStruct


class On_select_new_trace(Action_on_selector_update):
    def __init__(self, theLinkDataGraphs):
        self.theLinkDataGraphs = theLinkDataGraphs

    def selector_updated(self, selection_name, the_collection, indices_data):
        """
        Action to perform once the data have been selected
        :param selection_name: name of the selection (deprecated ?)
        :param the_collection: the collection
        :param indices_data: indices of the data
        :return:
        """
        newStruct = ListDataStruct()
        theData = [the_collection.get_data_at_index(index) for index in indices_data]
        newStruct.set_data(theData)
        new_id_collectionInfo = self.theLinkDataGraphs.add_collection(newStruct, {"legend": selection_name})
        new_collectionInfo = self.theLinkDataGraphs.get_collectionInfo(new_id_collectionInfo)

        id_collection = self.theLinkDataGraphs.get_idcollection_from_collection(the_collection)
        res, _ = self.theLinkDataGraphs.get_graph_and_trace_from_collection(id_collection)
        for idGraph, _ in res:
            howToPlotGraph = self.theLinkDataGraphs.get_howToPlotGraph(idGraph)
            howToPlotGraph.kwargs_graph.pop("color", None)
            self.theLinkDataGraphs.create_trace(new_collectionInfo, howToPlotGraph, idGraph)
        self.theLinkDataGraphs.update_graphs()

    def get_name(self):
        return "Create new trace"
