from optimeed.visualize.gui.widgets.widget_graphs_visual import on_graph_click_interface
from PyQt5 import QtWidgets
import os
from optimeed.core import rgetattr


class On_click_export_to_txtfile(on_graph_click_interface):
    """On click: export the data of the whole the trace selected"""
    def __init__(self, theDataLink, attributes_master=None, attributes_slave=None):
        """

        :param theDataLink: :class:`~optimeed.visualize.high_level.LinkDataGraph.LinkDataGraph`
        :param attributes_master: list of attributes (as string) to recover from the master (data points/devices)
        :param attributes_slave: list of attributes (as string) to recover from the slave (displayed points)
        """
        self.theDataLink = theDataLink
        self.attributes_master = attributes_master if attributes_master is not None else list()
        self.attributes_slave = attributes_slave if attributes_slave is not None else list()

    def graph_clicked(self, theGraphVisual, index_graph, index_trace, indices_points):
        theStr = ""
        for attribute in self.attributes_master:
            theStr += "{}\t".format(attribute)
        for attribute in self.attributes_slave:
            theStr += "{}\t".format(attribute)
        theStr += "\n"

        collection_slave = self.theDataLink.get_collection_from_graph(index_graph, index_trace, getMaster=False)
        collection_master = self.theDataLink.get_collection_from_graph(index_graph, index_trace, getMaster=True)

        for index_point, _ in enumerate(collection_slave.get_data_generator()):
            dataObj = collection_master.get_data_at_index(index_point)
            for attribute in self.attributes_master:
                theStr += "{}\t".format(rgetattr(dataObj, attribute))

            if len(self.attributes_slave):
                dataObj = collection_slave.get_data_at_index(index_point)
                for attribute in self.attributes_slave:
                    theStr += "{}\t".format(rgetattr(dataObj, attribute))
            theStr += "\n"

        # Export
        dlg = QtWidgets.QFileDialog.getSaveFileName()[0]
        if dlg:
            root, ext = os.path.splitext(dlg)
            filename = root + ".txt"
            with open(filename, "w") as f:
                f.write(theStr)

    def get_name(self):
        return "Export trace to text file"
