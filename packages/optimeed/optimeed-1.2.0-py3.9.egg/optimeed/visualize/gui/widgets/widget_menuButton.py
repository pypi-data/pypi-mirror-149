from PyQt5 import QtWidgets


class widget_menuButton(QtWidgets.QMenu):
    """Same as QMenu, but integrates it behind a button more easily."""
    def __init__(self, theParentButton):
        super().__init__()
        self.theButton = theParentButton
        self.theButton.setMenu(self)

    def showEvent(self, QShowEvent):
        p = self.pos()
        geo = self.theButton.geometry()
        self.move(p.x() + geo.width() - self.geometry().width(), p.y())
