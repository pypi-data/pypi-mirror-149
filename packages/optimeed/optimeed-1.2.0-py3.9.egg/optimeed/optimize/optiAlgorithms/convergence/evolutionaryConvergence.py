from optimeed.core.tools import get_ND_pareto
from optimeed.optimize.optiAlgorithms.convergence.hypervolume import HyperVolume
import numpy as np
from .interfaceConvergence import InterfaceConvergence
from optimeed.visualize import Graphs, Data
from typing import Dict, List
from math import floor
from optimeed.core import printIfShown, SHOW_WARNING
import traceback

LIMIT_PARETO_HYPERVOLUME = 50


class EvolutionaryConvergence(InterfaceConvergence):
    """convergence class for population-based algorithm"""
    objectives_per_step: Dict[int, List[List[float]]]
    constraints_per_step: Dict[int, List[List[float]]]
    paretos_per_step: Dict[int, List[List[float]]]
    hypervolume_per_step: Dict[int, List[float]]

    def __init__(self):
        self.objectives_per_step = dict()
        self.constraints_per_step = dict()
        self.paretos_per_step = dict()

    def set_points_at_step(self, theStep, theObjectives_list, theConstraints_list):
        self.objectives_per_step[theStep] = theObjectives_list
        self.constraints_per_step[theStep] = theConstraints_list
        # Find new pareto
        objectives_respect_constraint = self.get_objectives_respect_constraint(theObjectives_list, theConstraints_list)
        prev_pareto = self.paretos_per_step[theStep-1][:] if theStep > 1 else list()
        try:
            new_pareto, _ = get_ND_pareto(prev_pareto + objectives_respect_constraint)
        except IndexError:
            new_pareto = list()
        self.paretos_per_step[theStep] = new_pareto

    @staticmethod
    def get_objectives_respect_constraint(objectives, constraints):
        objectives_respect_constraint = list()
        for i in range(len(objectives)):
            respect_constraints = True
            for constraint in constraints[i]:
                if constraint > 0:
                    respect_constraints = False
                    break
            if respect_constraints:
                objectives_respect_constraint.append(objectives[i])
        return objectives_respect_constraint

    def get_pareto_convergence(self, limiter=None):
        if self.paretos_per_step:
            return self.paretos_per_step
        else:
            printIfShown("Deprecated use, probably from deprecated file.", SHOW_WARNING)
            paretos = dict()
            previous_pareto = list()

            nbSteps = self.last_step()
            if limiter is None or nbSteps <= limiter:
                steps = list(range(1, nbSteps))
            else:
                stepsize = floor(nbSteps/limiter)
                steps = list(range(1, 1+stepsize*limiter, stepsize))
                if steps[-1] != nbSteps:
                    steps.append(nbSteps)

            for step in steps:
                try:
                    paretos[step], _ = get_ND_pareto(previous_pareto + self.get_objectives_respect_constraint(self.objectives_per_step[step], self.constraints_per_step[step]))
                except IndexError:
                    paretos[step] = list()
                previous_pareto = paretos[step][:]
            return paretos

    def get_hypervolume(self, pareto, refPoint=None):
        if not pareto:
            return np.nan, None
        if self.get_nb_objectives() == 1:  # monobj
            return pareto[0][0], None
        if refPoint is None:
            refPoint = self.get_nadir_point(pareto)
        hv = HyperVolume(refPoint)
        return hv.compute(pareto), refPoint

    def get_hypervolume_convergence(self):
        paretos = self.get_pareto_convergence(limiter=LIMIT_PARETO_HYPERVOLUME)
        res_dict = dict()

        if len(paretos[self.last_step()]) == 1 and len(paretos[self.last_step()][0]) > 1:  # only one point in last pareto ... => objectives in same direction
            printIfShown("Objectives go in same direction, using sum of objectives instead", SHOW_WARNING)
            for step in paretos:
                try:
                    res_dict[step] = np.sqrt(sum([objective**2 for objective in paretos[step][0]]))
                except IndexError:
                    res_dict[step] = 0.0
            return res_dict

        nadir_point = self.get_nadir_point(paretos[self.last_step()])
        for step in paretos:
            res_dict[step], _ = self.get_hypervolume(paretos[step], refPoint=nadir_point)
        return res_dict

    def get_nadir_point(self, pareto):
        nb_objectives = self.get_nb_objectives()
        nadir = [-np.inf] * nb_objectives
        if len(pareto) <= 1:  # Only one point in pareto front
            return nadir

        for i in range(nb_objectives):
            try:
                nadir[i] = max([max(nadir[i], objectives[i]) for objectives in pareto])
            except ValueError:
                pass
        return nadir

    def last_step(self):
        if self.objectives_per_step:
            return max(self.objectives_per_step.keys())
        return 0

    def get_nb_objectives(self):
        try:
            return len(self.objectives_per_step[self.last_step()][0])
        except (ValueError, KeyError):
            return 0

    def get_scalar_convergence_evolution(self):
        try:
            hypervolumes = self.get_hypervolume_convergence()
            x = list(hypervolumes.keys())
            y = list(hypervolumes.values())
            return x, y
        except KeyError:
            return [], []

    def get_graphs(self):
        theGraphs = Graphs()
        # noinspection PyBroadException
        try:
            x, y = self.get_scalar_convergence_evolution()

            if self.get_nb_objectives() == 1:
                g2 = theGraphs.add_graph()

                theDataPareto = Data(x, y, x_label="Step", y_label="Objective", symbol=None)
                theGraphs.add_trace(g2, theDataPareto)
            elif self.get_nb_objectives() == 2:
                paretos = self.get_pareto_convergence(limiter=10)
                g1 = theGraphs.add_graph()

                theDataHV = Data(x, y, x_label="Step", y_label="Hypervolume")
                theGraphs.add_trace(g1, theDataHV)

                g2 = theGraphs.add_graph()
                for step in paretos:
                    theDataPareto = Data([objectives[0] for objectives in paretos[step]], [objectives[1] for objectives in paretos[step]], sort_output=True, x_label="Objective1", y_label="Objective2")
                    theGraphs.add_trace(g2, theDataPareto)
            else:
                pass
        except Exception:
            printIfShown("An error in convergence graphs. Error :" + traceback.format_exc(), SHOW_WARNING)

        return theGraphs
