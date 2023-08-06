from . import pyqtgraph as pg
from PyQt5 import QtCore, QtGui


class TraceVisual(QtCore.QObject):
    """Defines a trace in a graph."""
    signal_must_update = QtCore.pyqtSignal()

    class _ModifiedPaintElem:
        """Hidden class to manage brushes or pens"""
        def __init__(self):
            self.indices = list()
            self.newPaintElems = list()

        def add_modified_paintElem(self, index, newPaintElem):
            try:
                indexInList = self.indices.index(index)
                self.indices[indexInList] = index
                self.newPaintElems[indexInList] = newPaintElem
            except ValueError:
                self.indices.append(index)
                self.newPaintElems.append(newPaintElem)

        def modify_paintElems(self, paintElemsIn_List):
            """ Apply transformation to paintElemsIn_List


            :param paintElemsIn_List: list of brushes or pens to modify
            :return: False if nothing has been modified, True is something has been modified
            """
            if not len(self.indices):
                return False

            for i in range(len(self.indices)):
                try:
                    paintElemsIn_List[self.indices[i]] = self.newPaintElems[i]
                except IndexError:
                    pass
            return True

        def reset_paintElem(self, index):
            """ Remove transformation of point index"""
            try:
                indexInList = self.indices.index(index)
                del self.indices[indexInList]
                del self.newPaintElems[indexInList]
            except ValueError:
                pass

        def reset(self):
            self.__init__()

    def __init__(self, theData, theWGPlot, highlight_last):
        """
        :param theData: from class Data. Contains all the informations to plot (x, y, z, transforms, etc.)
        :param theWGPlot: holder of the trace. This is a plotWidget
        :param highlight_last: Boolean. If set to true, the last point in the data will be highlighted.
        """
        super().__init__()

        # set brush
        self.theBrushesModifier = self._ModifiedPaintElem()

        # set symbolPen
        self.theSymbolPensModifier = self._ModifiedPaintElem()

        # set symbols
        self.theSymbolModifier = self._ModifiedPaintElem()

        # set data
        self.theData = theData

        # set trace item (plotItem)
        if theData.get_legend():
            self.thePlotItem = theWGPlot.plot([float('inf')], name=theData.get_legend())
        else:
            self.thePlotItem = theWGPlot.plot([float('inf')])

        # set highlight last
        self.highlight_last = highlight_last
        self.drawPoints = True

        # signals
        self.signal_must_update.connect(self.updateTrace)

    def hide_points(self):
        """Hide all the points"""
        self.drawPoints = False
        self.signal_must_update.emit()

    def get_color(self):
        """Get colour of the trace, return tuple (r,g,b)"""
        return self.get_data().get_color()

    def set_color(self, color):
        """Set colour of the trace, argument as tuple (r,g,b)"""
        self.get_data().set_color(color)
        self.thePlotItem.scatter.opts['brush'] = color

    def get_base_symbol_brush(self):
        """Get symbol brush configured for this trace, return :class:`pg.QBrush`"""
        return pg.mkBrush(self.get_data().get_color_alpha())

    def get_base_pen(self):
        """Get pen configured for this trace, return :class:`pg.QPen`"""
        return pg.mkPen(self.get_color(), width=self.get_data().get_width())

    def get_base_symbol_pen(self):
        """Get symbol pen configured for this trace, return :class:`pg.QPen`"""
        if self.get_data().symbol_isfilled():
            if self.get_data().get_symbolOutline() == 1:
                return None
            return pg.mkPen(QtGui.QColor(*self.get_color()).darker(int(self.get_data().get_symbolOutline()*100)), isCosmetic=True)  # 120 or 250 ? :)
        else:
            return pg.mkPen(self.get_color(), isCosmetic=False, width=self.get_data().get_width())

    def get_base_symbol(self):
        """Get base symbol configured for this trace, return str of the symbol (e.g. 'o')"""
        return self.get_data().get_symbol()

    def get_symbol(self, size):
        """Get actual symbols for the trace. If the symbols have been modified: return a list which maps each points to a symbol.
        Otherwise: return :meth:TraceVisual.get_base_symbol()"""
        symbol = self.get_base_symbol()
        theSymbolList = [symbol] * size
        hasBeenModified = self.theSymbolModifier.modify_paintElems(theSymbolList)
        return symbol if not hasBeenModified else theSymbolList

    def updateTrace(self):
        """Forces the trace to refresh."""
        try:
            theData = self.get_data()
            x, y = theData.get_plot_data()

            if x and y:
                # print(x, y)
                if self.drawPoints:
                    theBrushes = self.get_brushes(len(x))
                    theSymbolPens = self.get_symbolPens(len(x))
                else:
                    theBrushes = None
                    theSymbolPens = None
                theBasePen = self.get_base_pen()
                if theData.is_scattered():
                    theBasePen.setStyle(QtCore.Qt.NoPen)
                else:
                    self.set_pen_linestyle(theBasePen, theData.get_linestyle())
                self.thePlotItem.setData(x, y, symbolBrush=theBrushes, symbol=self.get_symbol(len(x)), symbolPen=theSymbolPens, symbolSize=self.get_data().get_symbolsize(), pen=theBasePen)  # symbolPen = None for no outline
            else:
                self.thePlotItem.setData([], [], symbolBrush=None)

        except ValueError:
            pass

    def get_length(self):
        """Return number of data to plot"""
        x = self.get_data().get_plot_data()
        return len(x)

    def hide(self):
        """Hides the trace"""
        self.thePlotItem.clear()

    def show(self):
        """Shows the trace"""
        self.signal_must_update.emit()

    def toggle(self, boolean):
        """Toggle the trace (hide/show)"""
        if boolean:
            self.show()
        else:
            self.hide()

    def get_data(self):
        """Get data to plot :class:`~optimeed.visualize.graphs.Graphs.Data`"""
        return self.theData

    def get_brushes(self, size):
        """Get actual brushes for the trace (=symbol filling). return a list which maps each points to a symbol brush"""
        symbolBrush = self.get_base_symbol_brush() if self.get_data().symbol_isfilled() else None
        theBrushList = [symbolBrush] * size

        if self.highlight_last:
            theBrushList[-1] = pg.mkBrush('y')
        hasBeenModified = self.theBrushesModifier.modify_paintElems(theBrushList)
        if not hasBeenModified and not self.highlight_last:
            return symbolBrush
        return theBrushList

    def set_brush(self, indexPoint, newbrush, update=True):
        """Set the symbol brush for a specific point:

        :param indexPoint: Index of the point (in the graph) to modify
        :param newbrush: either QBrush or tuple (r, g, b) of the new brush
        :param update: if True, update the trace afterwards. This is slow operation."""
        if isinstance(newbrush, tuple):
            newbrush = pg.mkBrush(newbrush)
        self.theBrushesModifier.add_modified_paintElem(indexPoint, newbrush)
        if update:
            self.signal_must_update.emit()

    def set_symbol(self, indexPoint, newSymbol, update=True):
        """Set the symbol shape for a specific point:

        :param indexPoint: Index of the point (in the graph) to modify
        :param newSymbol: string of the new symbol (e.g.: 'o')
        :param update: if True, update the trace afterwards. This is slow operation."""
        self.theSymbolModifier.add_modified_paintElem(indexPoint, newSymbol)
        if update:
            self.signal_must_update.emit()

    def set_brushes(self, list_indexPoint, list_newbrush):
        """Same as :meth:`~TraceVisual.set_brush` but by taking a list as input"""
        if not isinstance(list_newbrush, list):
            list_newbrush = [list_newbrush] * len(list_indexPoint)
        for i in range(len(list_indexPoint)):
            self.set_brush(list_indexPoint[i], list_newbrush[i], update=False)
        self.signal_must_update.emit()

    def reset_brush(self, indexPoint, update=True):
        """Reset the brush of the point indexpoint"""
        self.theBrushesModifier.reset_paintElem(indexPoint)
        if update:
            self.signal_must_update.emit()

    def reset_all_brushes(self):
        """Reset all the brushes"""
        self.theBrushesModifier.reset()
        self.signal_must_update.emit()

    def reset_symbol(self, indexPoint, update=True):
        """Reset the symbol shape of the point indexpoint"""
        self.theSymbolModifier.reset_paintElem(indexPoint)
        if update:
            self.signal_must_update.emit()

    def get_symbolPens(self, size):
        """Get actual symbol pens for the trace (=symbol outline). return a list which maps each points to a symbol pen"""
        thePenList = [self.get_base_symbol_pen()] * size
        hasBeenModified = self.theSymbolPensModifier.modify_paintElems(thePenList)
        if not hasBeenModified:
            return self.get_base_symbol_pen()
        return thePenList

    def set_symbolPen(self, indexPoint, newPen, update=True):
        """Set the symbol shape for a specific point:

        :param indexPoint: Index of the point (in the graph) to modify
        :param newPen: QPen item or tuple of the color (r,g,b)
        :param update: if True, update the trace afterwards. This is slow operation."""
        if isinstance(newPen, tuple):
            newPen = pg.mkPen(newPen)
        self.theSymbolPensModifier.add_modified_paintElem(indexPoint, newPen)
        if update:
            self.signal_must_update.emit()

    def set_symbolPens(self, list_indexPoint, list_newpens):
        """Same as :meth:`~TraceVisual.set_symbolPen` but by taking a list as input"""

        for i in range(len(list_indexPoint)):
            self.set_symbolPen(list_indexPoint[i], list_newpens[i], update=False)
        self.signal_must_update.emit()

    def reset_symbolPen(self, indexPoint):
        """Reset the symbol pen of the point indexpoint"""

        self.theSymbolPensModifier.reset_paintElem(indexPoint)
        self.signal_must_update.emit()

    def reset_all_symbolPens(self):
        """Reset all the symbol pens"""

        self.theSymbolPensModifier.reset()
        self.signal_must_update.emit()

    @staticmethod
    def set_pen_linestyle(thePen, linestyle):
        """Transform a pen for dashed lines:

        :param thePen: QPen item
        :param linestyle: str (e.g.: '.', '.-', '--', ...)
        """
        if linestyle in ['.', ':', '..']:
            thePen.setDashPattern([0.1, 2])
            thePen.setCapStyle(QtCore.Qt.RoundCap)
            thePen.setWidthF(thePen.width()*1.75)
        elif linestyle in ['.-', '-.']:
            thePen.setCapStyle(QtCore.Qt.RoundCap)
            thePen.setDashPattern([3, 2, 0.1, 2])
            thePen.setWidthF(thePen.width()*1.25)
        elif linestyle in ['-..', '.-.', '..-']:
            thePen.setDashPattern([0.1, 2, 3, 2, 0.1, 2])
            thePen.setWidthF(thePen.width()*1.25)
        elif linestyle in ['--']:
            thePen.setDashPattern([2.5, 2])
            thePen.setWidthF(thePen.width()*1.1)
        else:
            thePen.setStyle(QtCore.Qt.SolidLine)

    def get_point(self, indexPoint):
        """Return object pyqtgraph.SpotItem"""
        return self.thePlotItem.scatter.points()[indexPoint]
