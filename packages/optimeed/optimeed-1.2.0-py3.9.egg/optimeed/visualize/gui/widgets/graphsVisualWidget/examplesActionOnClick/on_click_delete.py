from optimeed.visualize.gui.widgets.widget_graphs_visual import on_graph_click_interface
from optimeed.visualize.gui.gui_collection_exporter import gui_collection_exporter
import os
from PyQt5 import QtWidgets, QtCore
# from optimeed.core.Collection import Collection


class delete_gui(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # Create PyQt5 window
        self.mainbox = QtWidgets.QWidget()
        self.setCentralWidget(self.mainbox)
        self.mainbox.setLayout(QtWidgets.QVBoxLayout())
        self.mainbox.layout().setContentsMargins(0, 0, 0, 0)

        self.button1 = QtWidgets.QPushButton('Apply', self)
        self.mainbox.layout().addWidget(self.button1)

        self.resetButton = QtWidgets.QPushButton('Reset', self)
        self.mainbox.layout().addWidget(self.resetButton)


class on_graph_click_delete(on_graph_click_interface):
    """On Click: Delete the points from the graph, and save the modified collection"""

    def __init__(self, theDataLink):
        """

        :param theDataLink: :class:`~optimeed.visualize.high_level.LinkDataGraph.LinkDataGraph`
        """
        super().__init__()
        self.theDataLink = theDataLink
        self.indicesToDelete = list()
        self.theGraphVisual = None
        self.theGui = delete_gui()
        self.theGui.button1.clicked.connect(self.apply)
        self.theGui.resetButton.clicked.connect(self.reset)

    def apply(self):
        listOfIndexGraph = dict()

        for index_graph, index_trace, index_point in self.indicesToDelete:
            try:
                listOfIndexGraph[index_graph][index_trace].append(index_point)
            except KeyError:
                listOfIndexGraph[index_graph] = dict()
                listOfIndexGraph[index_graph][index_trace] = [index_point]

        for index_graph in listOfIndexGraph:
            for index_trace in listOfIndexGraph[index_graph]:
                indices_points = listOfIndexGraph[index_graph][index_trace]
                for index in indices_points:
                    self.theGraphVisual.get_graph(index_graph).get_trace(index_trace).reset_brush(index, update=False)

                if self.theDataLink.is_slave(index_graph, index_trace):
                    removeFromMasters = [True, False]
                else:
                    removeFromMasters = [False]

                for removeFromMaster in removeFromMasters:

                    theCollection = self.theDataLink.get_collection_from_graph(index_graph, index_trace, getMaster=removeFromMaster)
                    self.theDataLink.remove_elements_from_trace(index_graph, index_trace, indices_points, deleteFromMaster=removeFromMaster)

                    # Get new collection name
                    suffix_filename = '_deleted_points'
                    #curr_filename = os.path.splitext(theCollection.get_filename())[0]
                    # Does not work here :(
                    #filename = curr_filename if curr_filename.endswith(suffix_filename) else curr_filename + suffix_filename
                    # Save it
                    #theCollection.set_filename(filename, change_filename_if_exists=False)
                    #theCollection.save()
        self.theDataLink.update_graphs()
        self.theGraphVisual.update_graphs()
        self.reset()

    def reset(self):
        self.indicesToDelete = list()

    def graph_clicked(self, theGraphVisual, index_graph, index_trace, indices_points):
        theTrace = theGraphVisual.get_graph(index_graph).get_trace(index_trace)
        for index_point in indices_points:
            self.indicesToDelete.append((index_graph, index_trace, index_point))
        theTrace.set_brushes(indices_points, (250, 250, 0))

        self.theGraphVisual = theGraphVisual
        self.theGui.show()

    def get_name(self):
        return "Delete points"# and export collection"

