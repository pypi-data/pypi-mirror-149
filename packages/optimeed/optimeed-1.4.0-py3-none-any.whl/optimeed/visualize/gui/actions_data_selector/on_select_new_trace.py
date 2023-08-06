from ..gui_data_selector import Action_on_selector_update
from optimeed.core import ListDataStruct


class On_select_new_trace(Action_on_selector_update):
    def __init__(self, theLinkDataGraphs):
        self.theLinkDataGraphs = theLinkDataGraphs

    def selector_updated(self, selection_name, the_collection, selected_data, not_selected_data):
        """
        Action to perform once the data have been selected

        :param selection_name: name of the selection (deprecated ?)
        :param the_collection: the collection
        :param selected_data: indices of the data selected
        :param not_selected_data: indices of the data not selected
        :return:
        """
        newStruct = ListDataStruct()
        theData = [the_collection.get_data_at_index(index) for index in selected_data]
        newStruct.set_data(theData)
        _ = self.theLinkDataGraphs.add_collection(newStruct, {"legend": selection_name})
        self.theLinkDataGraphs.update_graphs()

    def get_name(self):
        return "Create new trace"
