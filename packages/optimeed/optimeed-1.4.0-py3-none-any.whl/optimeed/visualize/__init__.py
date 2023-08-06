import PyQt5.QtCore

PyQt5.QtCore.QCoreApplication.setAttribute(PyQt5.QtCore.Qt.AA_ShareOpenGLContexts)

from .gui import *
from .displayOptimization import *
from .viewOptimizationResults import *
from .fastPlot import *
from .fastPlot3 import *
