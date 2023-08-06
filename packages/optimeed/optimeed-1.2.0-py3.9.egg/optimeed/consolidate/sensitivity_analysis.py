from optimeed.optimize import Real_OptimizationVariable
from SALib.sample import saltelli
from SALib.analyze import sobol
from SALib.test_functions import Ishigami

from optimeed.core import Performance_ListDataStruct, SaveableObject, AutosaveStruct, create_unique_dirname, getPath_workspace
from multiprocessing import Pool
from typing import List
from .sensitivity_analysis_evaluation import evaluate
import numpy as np


class ResultStruct(SaveableObject):
    paramsToEvaluate: List[float]
    success: bool
    index: int

    def __init__(self):
        self.paramsToEvaluate = [0.0]
        self.device = None
        self.success = False
        self.index = 0

    def add_data(self, params, device, success, index):
        self.device = device
        self.success = success
        self.paramsToEvaluate = params
        self.index = index

    def get_additional_attributes_to_save(self):
        return ["device"]


def get_sensitivity_problem(list_of_optimization_variables):
    """
    This is the first method to use. Convert a list of optimization varisbles to a SALib problem

    :param list_of_optimization_variables: List of optimization variables
    :return: SALib problem
    """
    num_vars = len(list_of_optimization_variables)
    names = list()
    bounds = list()

    for variable in list_of_optimization_variables:
        if isinstance(variable, Real_OptimizationVariable):
            names.append(variable.get_attribute_name())
            bounds.append([variable.get_min_value(), variable.get_max_value()])
        else:
            raise TypeError("Optimization variable must be of real type to perform this analysis")
    problem = {'num_vars': num_vars, 'names': names, 'bounds': bounds}
    return problem


def evaluate_sensitivities(param_values, list_of_optimization_variables, theDevice, theMathsToPhys, theCharacterization, numberOfCores, studyname="sensitivity", indices_to_evaluate=None):
    """
    Evaluate the sensitivities

    :param param_values: 2D array, in which each row is the vector of params to evaluate
    :param list_of_optimization_variables: list of OptiVariables that are analyzed
    :param theDevice: /
    :param theMathsToPhys: /
    :param theCharacterization: /
    :param numberOfCores: number of core for multicore evaluation
    :param studyname:
    :param indices_to_evaluate: if None, evaluate all param_values, otherwise if list: evaluate subset of param_values defined by indices_to_evaluate
    :return: /
    """
    myDataStruct = Performance_ListDataStruct()
    foldername = create_unique_dirname(getPath_workspace() + '/' + studyname)
    # Start saving
    autosaveStruct = AutosaveStruct(myDataStruct, filename="{}/sensitivity".format(foldername))
    autosaveStruct.start_autosave(timer_autosave=60*5)

    if indices_to_evaluate is None:
        indices = list(range(len(param_values)))
    else:
        indices = indices_to_evaluate
        param_values = [param_values[index] for index in indices_to_evaluate]

    np.savetxt("{}/inputs.txt".format(foldername), param_values)
    theStr = ''
    for optiVariable in list_of_optimization_variables:
        theStr += str(optiVariable) + "\n"
    with open("{}/boundaries.txt".format(foldername), "w") as f:
        f.write(theStr)

    # create jobs
    jobs = []
    for index, params in zip(indices, param_values):
        jobs.append([params.tolist(), theDevice, theMathsToPhys, theCharacterization, list_of_optimization_variables, index])

    pool = Pool(numberOfCores)
    nb_to_do = len(param_values)
    nb_done = 0
    for output in pool.imap_unordered(evaluate, jobs):
        result = ResultStruct()
        result.add_data(output["x"], output["device"], output["success"], output["index"])
        myDataStruct.add_data(result)
        nb_done += 1
        print("did {} over {}".format(nb_done, nb_to_do))

    # save results
    autosaveStruct.stop_autosave()
    autosaveStruct.save()

    pool.close()
    pool.join()
