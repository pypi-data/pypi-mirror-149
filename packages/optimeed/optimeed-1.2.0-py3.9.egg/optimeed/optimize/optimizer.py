from .characterization import Characterization
from .mathsToPhysics import MathsToPhysics
from .optiAlgorithms import MultiObjective_GA
from optimeed.core.collection import AutosaveStruct, ListDataStruct, Performance_ListDataStruct
from optimeed.core.tools import getPath_workspace, indentParagraph, create_unique_dirname
from optimeed.core.ansi2html import Ansi2HTMLConverter
from optimeed.core.options import Option_class
from optimeed.core import printIfShown, SHOW_DEBUG
from optimeed.core.commonImport import SHOW_INFO, SHOW_WARNING
import traceback
import time
import copy
import math
from typing import List

default = dict()
default['M2P'] = MathsToPhysics()
default['Charac'] = Characterization()
default['Algo'] = MultiObjective_GA()


class PipeOptimization:
    """Provides a live interface of the current optimization"""

    def __init__(self):
        self.OUT_currentDevice = None
        self.OUT_historic = None

    def get_device(self):
        """ :return: :class:`~optimeed.core.interfaceDevice.InterfaceDevice` (not process safe, deprecated) """
        return self.OUT_currentDevice

    def get_historic(self):
        """ :return: :class:`~OptiHistoric` """
        return self.OUT_historic

    def set_device(self, theDevice):
        self.OUT_currentDevice = theDevice

    def set_historic(self, theHistoric):
        self.OUT_historic = theHistoric


class OptiHistoric(object):
    """Contains all the points that have been evaluated"""
    _DEVICE = "autosaved"
    _LOGOPTI = "logopti"
    _RESULTS = "results"
    _CONVERGENCE = "optiConvergence"

    class _pointData:
        time: float
        objectives: List[float]
        constraints: List[float]

        def __init__(self, currTime, objectives, constraints):
            self.time = currTime
            self.objectives = objectives
            self.constraints = constraints

    def __init__(self, **kwargs):
        """

        :param optiname: Name of the optimization (short string)
        :param autosave: Set to True to autosave the data during the optimization
        :param compress_save: Set to True to compress data structure.
        :param timer_autosave: Time in seconds to perform automatic save
        """
        autosaveTimer = kwargs.get('timer_autosave', 60*5)
        optiname = kwargs.get('optiname', 'opti')
        self.autosave = kwargs.get('autosave', True)
        compress_save = kwargs.get('compress_save', True)
        memory_efficient = kwargs.get('memory_efficient', True)

        self.keys = [self._DEVICE, self._LOGOPTI, self._RESULTS, self._CONVERGENCE]

        foldername = getPath_workspace() + '/' + optiname
        if self.autosave:
            foldername = create_unique_dirname(foldername)
        self.foldername = foldername

        self.database = dict()
        for key in self.keys:
            if memory_efficient and key == self._DEVICE:
                newStruct = Performance_ListDataStruct()
            else:
                newStruct = ListDataStruct(compress_save=compress_save)
            self.database[key] = AutosaveStruct(newStruct, filename="{}/{}".format(foldername, key))

        if self.autosave:
            self.database[self._DEVICE].start_autosave(autosaveTimer)
            self.database[self._LOGOPTI].start_autosave(autosaveTimer)
            self.database[self._CONVERGENCE].start_autosave(autosaveTimer)

    def add_point(self, device, currTime, objectives, constraints):
        self.database[self._DEVICE].get_datastruct().add_data(device)
        self.database[self._LOGOPTI].get_datastruct().add_data(self._pointData(currTime, objectives, constraints))

    def set_results(self, devicesList):
        self.database[self._RESULTS].get_datastruct().set_data(devicesList)

    def set_convergence(self, theConvergence):
        self.database[self._CONVERGENCE].get_datastruct().set_data([theConvergence])

    def generate_summary_file(self, theInfo):
        if self.autosave:
            with open(self.foldername + "/summary.html", 'w', encoding='utf-8') as myFile:
                conv = Ansi2HTMLConverter(dark_bg=True)
                myFile.write(conv.convert(theInfo))

    def save(self):
        if self.autosave:
            for key in self.keys:
                self.database[key].stop_autosave()
                self.database[key].save()

    def get_results(self):
        return self.database[self._RESULTS].get_datastruct()

    def get_convergence(self):
        """ :return: convergence :class:`~optimeed.optimize.optiAlgorithms.convergence.interfaceConvergence.InterfaceConvergence` """
        return self.database[self._CONVERGENCE].get_datastruct()

    def get_devices(self):
        """ :return: List of devices (ordered by evaluation number) """
        return self.database[self._DEVICE].get_datastruct()

    def get_logopti(self):
        """:return: Log optimization (to check the convergence) """
        return self.database[self._LOGOPTI].get_datastruct()


class Optimizer(Option_class):
    """Main optimizing class"""

    DISPLAY_INFO = 1
    KWARGS_OPTIHISTO = 2

    def __init__(self):
        super().__init__()
        # Variables defining an optimization problem
        self.theDevice = None
        self.theMathsToPhysics = None
        self.theCharacterization = None
        self.theObjectives = None
        self.theConstraints = None
        self.theOptimizationAlgorithm = None
        self.theOptimizationVariables = None
        self.theOptiHistoric = None
        # Other optimization variables
        self.thePipeOptimization = None
        self.has_been_set = False
        self.startingTime = None
        self.max_time_sec = 10
        self.add_option(self.DISPLAY_INFO, "Display optimization info", True)
        self.add_option(self.KWARGS_OPTIHISTO, "Kwargs opti historic", {})

    def set_optimizer(self, theDevice, theObjectiveList, theConstraintList,
                      theOptimizationVariables, theOptimizationAlgorithm=default['Algo'], theCharacterization=default['Charac'],
                      theMathsToPhysics=default['M2P']) -> PipeOptimization:
        """
        Prepare the optimizer for the optimization.

        :param theDevice: object of type  :class:`~optimeed.core.interfaceDevice.InterfaceDevice`
        :param theCharacterization: object of type :class:`~optimeed.optimize.characterization.interfaceCharacterization.InterfaceCharacterization`
        :param theMathsToPhysics: object of type :class:`~optimeed.optimize.mathsToPhysics.interfaceMathsToPhysics.InterfaceMathsToPhysics`
        :param theObjectiveList: list of objects of type :class:`~optimeed.optimize.objAndCons.interfaceObjCons.InterfaceObjCons`
        :param theConstraintList: list of objects of type :class:`~optimeed.optimize.objAndCons.interfaceObjCons.InterfaceObjCons`
        :param theOptimizationAlgorithm: list of objects of type :class:`~optimeed.optimize.optiAlgorithms.algorithmInterface.AlgorithmInterface`
        :param theOptimizationVariables: list of objects of type :class:`~optimeed.optimize.optiVariable.OptimizationVariable`
        :return: :class:`~PipeOptimization`
        """
        self.theDevice = theDevice
        self.theMathsToPhysics = theMathsToPhysics
        self.theCharacterization = theCharacterization
        self.theObjectives = theObjectiveList
        self.theConstraints = theConstraintList
        self.theOptimizationAlgorithm = theOptimizationAlgorithm
        self.theOptimizationAlgorithm.reset()
        self.theOptimizationVariables = theOptimizationVariables

        self.theOptiHistoric = OptiHistoric(**self.get_optionValue(self.KWARGS_OPTIHISTO))
        self.thePipeOptimization = PipeOptimization()
        self.thePipeOptimization.set_device(self.theDevice)
        self.thePipeOptimization.set_historic(self.theOptiHistoric)

        self.has_been_set = True
        return self.thePipeOptimization

    def run_optimization(self):
        """
        Perform the optimization.

        :return: :class:`Collection <optimeed.core.collection.Collection>` of the best optimized devices
        """
        # Display what to optimize
        printIfShown("------------------------------------\nSTARTING OPTIMIZATION: \n\n------------------------------------", -1, isToPrint=self.get_optionValue(self.DISPLAY_INFO))
        if not self.has_been_set:
            raise ValueError("Optimizer has not been set ! Please use set_optimizer() function")

        optimization_info = self.formatInfo()
        self.theOptiHistoric.generate_summary_file(optimization_info)
        printIfShown(optimization_info, -1, isToPrint=self.get_optionValue(self.DISPLAY_INFO))

        # Start optimization
        self.startingTime = time.time()

        initialVectorGuess = self.theMathsToPhysics.fromPhysToMaths(self.theDevice, self.theOptimizationVariables)

        self.theOptimizationAlgorithm.set_maxtime(self.max_time_sec)
        self.theOptimizationAlgorithm.set_evaluationFunction(self.evaluateObjectiveAndConstraints, self.callback_on_evaluation,
                                                             len(self.theObjectives), len(self.theConstraints))

        # self.evaluateObjectiveAndConstraints(initialVectorGuess, None)
        convergence = self.theOptimizationAlgorithm.get_convergence()
        self.theOptiHistoric.set_convergence(convergence)
        printIfShown("Performing optimization", SHOW_INFO, isToPrint=self.get_optionValue(self.DISPLAY_INFO))

        solutions = self.theOptimizationAlgorithm.compute(initialVectorGuess, self.theOptimizationVariables)  # Optimize

        printIfShown("Optimization ended", SHOW_INFO, isToPrint=self.get_optionValue(self.DISPLAY_INFO))

        # Reevaluate results
        resultsdevices = [None]*len(solutions)
        for i, solution in enumerate(solutions):
            self.theMathsToPhysics.fromMathsToPhys(solution, self.theDevice, self.theOptimizationVariables)
            self.theCharacterization.compute(self.theDevice)
            resultsdevices[i] = copy.deepcopy(self.theDevice)

        self.theOptiHistoric.set_results(resultsdevices)
        self.theOptiHistoric.save()

        self.has_been_set = False
        return resultsdevices, convergence

    def set_max_opti_time(self, max_time_sec):
        self.max_time_sec = max_time_sec

    def evaluateObjectiveAndConstraints(self, x):
        """
        Evaluates the performances of device associated to entrance vector x. Outputs the objective function and the constraints,
        and other data used in optiHistoric.

        This function is NOT process safe: "self." is actually a FORK in multiprocessing algorithms.
        It means that the motor originally contained in self. is modified only in the fork, and only gathered by reaching the end of the fork.
        It is not (yet?) possible to access this motor on the main process before the end of the fork. This behaviour could be changed by using pipes or Managers.

        :param x: Input mathematical vector from optimization algorithm
        :return: dictionary, containing objective values (list of scalar), constraint values (list of scalar), and other info (motor, time)
        """
        self.theMathsToPhysics.fromMathsToPhys(x, self.theDevice, self.theOptimizationVariables)

        characterization_failed = False
        # noinspection PyBroadException
        try:
            self.theCharacterization.compute(self.theDevice)
        except Exception:
            characterization_failed = True
            printIfShown("An error in characterization. Set objectives to inf. Error :" + traceback.format_exc(), SHOW_WARNING)

        nbr_of_objectives = len(self.theObjectives)
        objective_values = [float('inf')]*nbr_of_objectives

        nbr_of_constraints = len(self.theConstraints)
        constraint_values = [float('inf')] * nbr_of_constraints

        if not characterization_failed:
            for i in range(nbr_of_objectives):
                # noinspection PyBroadException
                try:
                    objective_values[i] = self.theObjectives[i].compute(self.theDevice)
                    if math.isnan(objective_values[i]):
                        objective_values[i] = float('inf')
                except Exception:
                    objective_values[i] = float('inf')
                    printIfShown("An error in objectives. inf value has been set to continue execution. Error:" + traceback.format_exc(), SHOW_DEBUG)

            for i in range(nbr_of_constraints):
                # noinspection PyBroadException
                try:
                    constraint_values[i] = self.theConstraints[i].compute(self.theDevice)
                except Exception:
                    constraint_values[i] = float('inf')
                    printIfShown("An error in constraints. NaN value has been set to continue execution. Error:" + traceback.format_exc(), SHOW_DEBUG)

        valuesToReturn = dict()
        valuesToReturn["device"] = self.theDevice
        valuesToReturn["time"] = time.time()-self.startingTime
        valuesToReturn["objectives"] = objective_values
        valuesToReturn["constraints"] = constraint_values
        return valuesToReturn  # objective_values, constraint_values

    def callback_on_evaluation(self, returnedValues):
        """Save the output of evaluateObjectiveAndConstraints to optiHistoric.
        This function should be called by the optimizer IN a process safe context."""
        self.theOptiHistoric.add_point(returnedValues["device"], returnedValues["time"], returnedValues["objectives"], returnedValues["constraints"])

    def formatInfo(self):
        optimization_info = ''
        optimization_info += '--------------------------------------------------------------------\n'
        optimization_info += 'OBJECTIVES:\n'
        for objective in self.theObjectives:
            optimization_info += indentParagraph('• ' + str(objective), indent_level=1)

        optimization_info += 'CONSTRAINTS:\n'
        for constraint in self.theConstraints:
            optimization_info += indentParagraph('• ' + str(constraint), indent_level=1)

        optimization_info += 'OPTIMIZATION VARIABLES :\n'
        for optiVariable in self.theOptimizationVariables:
            optimization_info += indentParagraph('• ' + str(optiVariable), indent_level=1)

        optimization_info += 'OPTIMIZATION ALGORITHM:\n'
        optimization_info += indentParagraph(str(self.theOptimizationAlgorithm))

        optimization_info += 'CHARACTERISATION SCHEME:\n'
        optimization_info += indentParagraph(str(self.theCharacterization))

        return optimization_info
