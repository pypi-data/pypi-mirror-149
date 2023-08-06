from abc import abstractmethod, ABCMeta


class InterfaceConvergence(metaclass=ABCMeta):
    """Simple interface to visually get the convergence of any optimization problem"""

    @abstractmethod
    def get_graphs(self):
        """Return :class:`~optimeed.core.graphs.Graphs`"""
        pass
