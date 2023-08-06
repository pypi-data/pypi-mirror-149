import copy
import os
from abc import abstractmethod
from multiprocessing import cpu_count, Pool
import numpy as np

from optimeed.core import Option_class
from optimeed.core.collection import ListDataStruct, AutosaveStruct
from optimeed.core.tools import getPath_workspace, rsetattr, rgetattr


class Unordered_pool_Collection(ListDataStruct):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def get_extension():
        return '.pool'


class Unordered_pool_analysis(Option_class):
    NUMBER_OF_CORES = 765

    def __init__(self, theReferenceDevice, theAttributes, theCharacterization, filename_collection, autosave=False, number_of_cores=1):
        super().__init__()
        self.filename_collection = filename_collection

        self.theCharacterization = theCharacterization
        self.theReferenceDevice = theReferenceDevice
        self.theAttributes = theAttributes

        self.autosave = autosave
        self.my_autosave = None

        self.add_option(self.NUMBER_OF_CORES, "Number of cores used in evaluation", number_of_cores)

    def run(self):
        """Instantiates input arguments for analysis"""

        # Set devices to evaluate
        listOfDevices = list()
        for deviceChanges in self.theAttributes:
            device = copy.deepcopy(self.theReferenceDevice)
            for attribute, value in deviceChanges.items():
                rsetattr(device, attribute, value)
            listOfDevices.append(device)

        # Collections out:
        theCollection_out = self.initialize_output_collection()

        # Simulates
        pool = Pool(min(cpu_count(), min(self.get_optionValue(self.NUMBER_OF_CORES),len(listOfDevices))))
        for device in pool.imap_unordered(self.evaluate, listOfDevices):
            theCollection_out.add_data(device)

        if self.my_autosave is not None:
            self.my_autosave.stop_autosave()
            self.my_autosave.save()
            self.my_autosave = None

        return theCollection_out

    def evaluate(self, theDevice):
        self.theCharacterization.compute(theDevice)
        return theDevice

    def initialize_output_collection(self):

        theCollection_out = Unordered_pool_Collection()
        if self.autosave:
            filename = os.path.join(getPath_workspace(), self.filename_collection + theCollection_out.get_extension())
            self.my_autosave = AutosaveStruct(theCollection_out, filename)
            self.my_autosave.start_autosave(60)

        return theCollection_out
