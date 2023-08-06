import copy
from abc import ABCMeta, abstractmethod, ABC
from typing import List, Dict

try:
    from pytypes import is_of_type
except AttributeError:
    def is_of_type(value, the_type):
        return type(value) == the_type

from optimeed.core import printIfShown, SHOW_WARNING, text_format


class Option_class_interface(ABC, metaclass=ABCMeta):
    """
    Interface of the class 'Option_class'. It defines all the necessary methods to manage a set of options.
    """

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def get_optionValue(self, optionId: int):
        pass

    @abstractmethod
    def set_optionValue(self, optionId: int, value):
        pass

    @abstractmethod
    def get_all_options(self) -> dict:
        """
        Return a dictionnary containing tuples (name of the option, value of the option)
        :return: dict
        """
        pass

    @abstractmethod
    def set_all_options(self, options: 'Option_class_interface'):
        """
        The method allows to define all the options from another object of type 'Option_class_interface'
        :param options: Option_class_interface
        :return:
        """
        pass

    @abstractmethod
    def add_option(self, idOption: int, name: str, value):
        pass


class Options:
    def __init__(self):
        self.options = dict()

    def get_name(self, idOption):
        return self.options[idOption][0]

    def get_value(self, idOption):
        return self.options[idOption][1]

    def add_option(self, idOption, name, value):
        self.options[idOption] = (name, value)

    def set_option(self, idOption, value):
        self.options[idOption] = (self.get_name(idOption), value)

    def copy(self):
        return copy.deepcopy(self)

    def set_self(self, the_options):
        for idOption in the_options.options:
            self.set_option(idOption, the_options.get_value(idOption))

    def __str__(self):
        theStr = ''
        if len(self.options):
            theStr += text_format.BLUE + 'Options'
            for key in self.options:
                theStr += '\n◦ {:<15}'.format(self.get_name(key)) + '\t-\t' + str(self.get_value(key))
            theStr += text_format.END
        return theStr


class Option_class(Option_class_interface):
    def __init__(self):
        super().__init__()
        self.Options = Options()

    def __str__(self):
        return str(self.Options)

    def get_optionValue(self, optionId):
        return self.Options.get_value(optionId)

    def set_optionValue(self, optionId, value):
        self.Options.set_option(optionId, value)

    def get_all_options(self):
        return self.Options.options

    def set_all_options(self, options):
        self.Options = options

    def add_option(self, idOption, name, value):
        self.Options.add_option(idOption, name, value)


class Option_class_typed(Option_class_interface):
    my_names: Dict[int, str]
    my_map: Dict[str, str]

    my_options_0: Dict[int, int]
    my_options_1: Dict[int, float]
    my_options_2: Dict[int, bool]
    my_options_3: Dict[int, str]
    my_options_4: Dict[int, List[int]]
    my_options_5: Dict[int, List[float]]
    my_options_6: Dict[int, List[str]]
    my_options_7: Dict[int, List[bool]]
    my_options_8: Dict[int, Dict[int,float]]
    my_options_9: Dict[int, Dict[str,float]]

    def __init__(self):

        super().__init__()
        self.nbr_of_types = len(self.__get_types())

        self.my_names = {}
        self.my_map = {}

        for i in range(self.nbr_of_types):
            setattr(self, 'my_options_' + str(i), {})

    @staticmethod
    def __get_types():
        return [int, float, bool, str, List[int], List[float], List[bool], List[str],Dict[int,float],Dict[str,float] ]

    def get_optionValue(self, optionId: int):
        try:
            return getattr(self, self.my_map[str(optionId)])[str(optionId)]
        except:
            return getattr(self, self.my_map[optionId])[optionId]

    def set_optionValue(self, optionId: int, value):
        try:
            del self.my_map[str(optionId)]
        except KeyError:
            print("There is no option with this id ({}) :/".format(optionId))
            return
        self.add_option(optionId, self.my_names[str(optionId)], value)

    def get_all_options(self):
        options = {}
        for i in range(self.nbr_of_types):
            the_options = getattr(self, 'my_options_' + str(i), {})
            for k in the_options:
                options[k] = (self.my_names[k], the_options[k])

        return options

    def add_option(self, idOption: int, name: str, value):
        if str(idOption) in self.my_map:
            printIfShown("Sorry but this id (" + str(idOption) + ") already exists and is associated to '" + self.my_names[str(idOption)] + "' :/", SHOW_WARNING)
            return

        success = False
        types = self.__get_types()
        for i in range(self.nbr_of_types):
            if self.__match(value, types[i]):
                self.my_names[str(idOption)] = name
                getattr(self, 'my_options_' + str(i))[str(idOption)] = value
                self.my_map[str(idOption)] = 'my_options_' + str(i)
                success = True
                break

        if not success:
            printIfShown("This type of value (" + str(type(value)) + ") is not supported by the 'Options class' yet :/\n Variable '" + name + "' has not been added to the options ! ", SHOW_WARNING)
            return

    @staticmethod
    def __match(value, theType):
        return is_of_type(value, theType)

    def set_all_options(self, options: Option_class_interface):
        for idOption in options.get_all_options():
            self.set_optionValue(idOption, options.get_optionValue(idOption))

    def __str__(self):
        theStr = ''
        if self.my_names:
            theStr += text_format.BLUE + 'Options'
            for key in self.my_map:
                theStr += '\n◦ {:<15}'.format(self.my_names[key]) + '\t-\t' + str(self.get_optionValue(key))
            theStr += text_format.END
        return theStr
