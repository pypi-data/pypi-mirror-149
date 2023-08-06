from optimeed.core import InterfaceDevice
from optimeed.optimize.optiAlgorithms import MultiObjective_GA as OptimizationAlgorithm
from optimeed.optimize import Optimizer, Real_OptimizationVariable, InterfaceObjCons, InterfaceCharacterization
import numpy as np
from optimeed.visualize import plot, figure


class _Device(InterfaceDevice):
    def __init__(self, fitFunction, nbArgs):
        self.functionArgs = [0.0]*nbArgs
        self.fitFunction = fitFunction


class _Objective(InterfaceObjCons):
    def __init__(self, x_data, y_data, fitCriterion):
        self.x_data = x_data
        self.y_data = y_data
        self.fitCriterion = fitCriterion

    def compute(self, theDevice):
        return self.fitCriterion(theDevice.fitFunction, theDevice.functionArgs, self.x_data, self.y_data)


def leastSquare(function, functionArgs, x_data, y_data):
    """
    Least square calculation (sum (y-ŷ)^2)

    :param function: Function to fit
    :param functionArgs: Arguments of the function
    :param x_data: x-axis coordinates of data to fit
    :param y_data: y-axis coordinates of data to fit
    :return: least squares
    """
    return np.sum((y_data - function(x_data, *functionArgs)) ** 2)


def r_squared(function, functionArgs, x_data, y_data):
    """
    R squared calculation

    :param function: Function to fit
    :param functionArgs: Arguments of the function
    :param x_data: x-axis coordinates of data to fit
    :param y_data: y-axis coordinates of data to fit
    :return: R squared
    """
    return -(1 - (np.sum((y_data - function(x_data, *functionArgs)) ** 2))/(np.sum((y_data - np.mean(y_data)) ** 2)))


def fit_function(fitFunction, x_data, y_data, *args, fitCriterion=leastSquare, displayResult=True):
    """
    Main method to fit a function

    :param fitFunction: the function to fit (link to it)
    :param x_data: x-axis coordinates of data to fit
    :param y_data: y-axis coordinates of data to fit
    :param args: for each parameter: [min, max] admissible value
    :param fitCriterion: fit criterion to minimize. Default: least square
    :param displayResult: if true, plots the result.
    :return: [arg_i_optimal, ...].
    """

    theDevice = _Device(fitFunction, len(args))
    theAlgo = OptimizationAlgorithm()

    optimizationVariables = list()
    for i, minmax in enumerate(args):
        optimizationVariables.append(Real_OptimizationVariable('functionArgs[{}]'.format(i), *minmax))  #

    listOfObjectives = [_Objective(x_data, y_data, fitCriterion)]
    listOfConstraints = []

    theOptimizer = Optimizer()
    theOptimizer.set_optionValue(theOptimizer.KWARGS_OPTIHISTO, {"autosave": False})
    _ = theOptimizer.set_optimizer(theDevice, listOfObjectives, listOfConstraints, optimizationVariables, theOptimizationAlgorithm=theAlgo)
    theOptimizer.set_max_opti_time(3)

    resultsOpti, convergence = theOptimizer.run_optimization()

    if displayResult:
        y_est = fitFunction(x_data, *resultsOpti[0].functionArgs)

        plot(x_data, y_data)
        plot(x_data, y_est, hold=False)
        figure()
        plot(x_data, y_data-y_est, hold=True)

    return resultsOpti[0].functionArgs
