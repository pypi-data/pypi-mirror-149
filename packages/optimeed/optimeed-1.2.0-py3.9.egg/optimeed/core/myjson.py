import ast
import inspect
from abc import ABCMeta, abstractmethod
# from typing import Dict, List, Tuple
try:
    from typing import GenericMeta as _Generic
except ImportError:
    from typing import _GenericAlias as _Generic

import traceback
import numpy as np
from optimeed.core.tools import rgetattr, rsetattr, printIfShown, SHOW_ERROR
import sys
import os

MODULE_TAG = '__module__'
CLASS_TAG = '__class__'
EXCLUDED_TAGS = [CLASS_TAG, MODULE_TAG]


def getExecPath():
    try:
        sFile = os.path.abspath(sys.modules['__main__'].__file__)
    except:
        sFile = sys.executable
    basename = os.path.basename(sFile)
    return os.path.splitext(basename)[0]


class SaveableObject(metaclass=ABCMeta):
    """Abstract class for dynamically type-hinted objects.
    This class is to solve the special case where the exact type of an attribute is not known before runtime, yet has to be saved."""

    @abstractmethod
    def get_additional_attributes_to_save(self):
        """Return list of attributes corresponding to object, whose type cannot be determined statically (e.g. topology change)"""
        pass


def _isclass(theObject):
    """Extends the default isclass method with typing"""
    if isinstance(theObject, type):
        return True
    # Test if comes from typing class
    return isinstance(theObject, _Generic)


def get_type_class(typ):
    """Get the type of the class. used to compare eventually objects from Typing."""
    try:
        # Python 3.5 / 3.6
        return typ.__extra__
    except AttributeError:
        try:
            # Python 3.7
            return typ.__origin__
        except AttributeError:
            return typ


def _get_object_class(theObj):
    return theObj.__class__.__qualname__


def _get_object_module(theObj):
    module = theObj.__class__.__module__
    if module == str.__class__.__module__:
        return None
    if module == "__main__":
        return getExecPath()
    return module


def _object_to_FQCN(theobj):
    """Gets module path of object"""
    module = theobj.__class__.__module__
    if module is None or module == str.__class__.__module__:
        return theobj.__class__.__qualname__
    return module + '.' + theobj.__class__.__qualname__
    #
    # return theobj.__module__ + '.' + theobj.__class__.__name__


def _find_class(moduleName, className):
    import importlib
    splitted_name = className.split(".")
    begin = True
    parentClass = None
    for name in splitted_name:
        if begin:
            parentClass = getattr(importlib.import_module(moduleName), name)
            begin = False
        else:
            parentClass = getattr(parentClass, name)
    return parentClass


def json_to_obj(json_dict):
    """Convenience class to create object from dictionary. Only works if CLASS_TAG is valid

    :param json_dict: dictionary loaded from a json file.
    :raise TypeError: if class can not be found
    :raise KeyError: if CLASS_TAG not present in dictionary
    """
    try:
        cls = _find_class(json_dict[MODULE_TAG], json_dict[CLASS_TAG])
        return json_to_obj_safe(json_dict, cls)
    except TypeError:
        raise
    except KeyError:
        raise KeyError("Object class not defined, can not create data. Use from_json_safe method to specify which class to load.")


def json_to_obj_safe(json_dict, cls):
    """Safe class to create object from dictionary.

    :param json_dict: dictionary loaded from a json file
    :param cls: class object to instantiate with dictionary
    """
    type_class = get_type_class(cls)
    if issubclass(type_class, list) or issubclass(type_class, tuple):
        list_type = cls.__args__[0]
        instance = list()
        for value in json_dict:
            instance.append(json_to_obj_safe(value, list_type))
        if issubclass(type_class, list):
            return instance
        else:
            return tuple(instance)
    elif issubclass(type_class, dict):
        key_type = cls.__args__[0]
        val_type = cls.__args__[1]

        instance = dict()
        for key, value in json_dict.items():
            instance.update({json_to_obj_safe(ast.literal_eval(key), key_type): json_to_obj_safe(value, val_type)})  # todo: catch error, put commented line in except
            # instance.update({json_to_obj_safe(ast.literal_eval("\'"+ key + "\'"), key_type): json_to_obj_safe(value, val_type)})  # Changed ... added "\'" + ... + "\'"
        return instance
    elif issubclass(type_class, (float, int, complex, bool, str)):
        return json_dict
    elif issubclass(type_class, np.ndarray):
        return np.array(json_dict)
    else:  # Object must be instantiated
        theInstance = _instantiates_annotated_object(json_dict, cls)
        return theInstance


def _instantiates_annotated_object(_json_dict, _cls):
    # annotations: dict = _cls.__annotations__ if hasattr(_cls, '__annotations__') else None
    # Instantiate the object
    entranceParams = []
    params = inspect.signature(_cls).parameters
    for param in params.values():
        if param.default is param.empty:
            if param.annotation is not param.empty:
                entranceParams.append(param.annotation())
            else:
                entranceParams.append(None)
        else:
            entranceParams.append(param.default)
    # We desactivate the print during the reinstantiation of all the defaults elements:
    # sys.stdout = None
    try:
        instance = _cls(*entranceParams)
    except TypeError:
        printIfShown("Error while loading:\n{}".format(traceback.format_exc()), SHOW_ERROR)
        return None
    # sys.stdout = sys.__stdout__

    annotations = _get_annotations(instance)
    # Set object attributes from data items
    if annotations:
        for name, value in _json_dict.items():
            if name not in EXCLUDED_TAGS:
                field_type = annotations.get(name)
                if _isclass(field_type) and isinstance(value, (dict, tuple, list, set, frozenset)):
                    rsetattr(instance, name, json_to_obj_safe(value, field_type))
                else:
                    rsetattr(instance, name, value)
                    # print(name, inspect.isclass(field_type), value)
    if isinstance(instance, SaveableObject):
        for additionalAttribute in instance.get_additional_attributes_to_save():
            theSubDict = _json_dict[additionalAttribute]
            try:
                rsetattr(instance, additionalAttribute, json_to_obj(theSubDict))
            except TypeError:
                rsetattr(instance, additionalAttribute, theSubDict)
    return instance


def _get_annotations(theObj):
    """Return annotated attributes"""

    annotations: dict = theObj.__annotations__ if hasattr(theObj, '__annotations__') else dict()
    parentClass = theObj.__mro__[1] if hasattr(theObj, '__mro__') else None
    if parentClass is not None and parentClass != object:
        theAnnotations = _get_annotations(parentClass)
        theAnnotations.update(annotations)
        return theAnnotations
    return annotations


def obj_to_json(theObj):
    """Extract the json dictionary from the object. The data saved are automatically detected, using typehints.
     ex: x: int=5 will be saved, x=5 won't.
     Inheritance of annotation is managed by this function
     """

    def _to_json(recObj, is_first=False):
        if isinstance(recObj, list) or isinstance(recObj, tuple):
            theList = list()
            for elem in recObj:
                theList.append(_to_json(elem))
            return theList
        elif isinstance(recObj, dict):
            output_dict = dict()
            for key in list(recObj):
                output_dict[str(key)] = _to_json(recObj[key])
            return output_dict
        elif isinstance(recObj, int) or isinstance(recObj, float):
            return recObj
        elif isinstance(recObj, str):
            return recObj
        elif np.issubdtype(type(recObj), np.integer) or np.issubdtype(type(recObj), np.floating):
            return float(recObj)
        elif isinstance(recObj, bool):
            return str(recObj).lower()
        elif isinstance(recObj, np.ndarray):
            return _to_json(recObj.tolist())
        elif recObj is None:
            return "null"
        else:  # Item is a user-defined object
            output_dict = dict()
            if recObj is not None:
                if is_first:
                    output_dict[MODULE_TAG] = _get_object_module(recObj)
                    output_dict[CLASS_TAG] = _get_object_class(recObj)

                for attribute, is_first in _get_attributes_to_save(recObj):
                    try:
                        value = rgetattr(recObj, attribute)
                        output_dict[attribute] = _to_json(value, is_first=is_first)
                    except AttributeError:
                        pass
            return output_dict

    return _to_json(theObj, is_first=True)


def _get_attributes_to_save(theObj):
    """Return list (attribute, is_first)"""
    list_1 = list()
    list_2 = list()

    # List 1
    annotations = _get_annotations(type(theObj))
    if annotations is not None:
        list_1 = list(zip(annotations, [False]*len(annotations)))

    # List 2
    if isinstance(theObj, SaveableObject):
        additional_attributes = theObj.get_additional_attributes_to_save()
        list_2 = list(zip(additional_attributes, [True]*len(additional_attributes)))
    return list_1 + list_2


# def get_json_module_tree(theObj):
#     """Return dict containing {CLASS_TAG: "class_name", MODULE_TAG: "module_name", "attribute1":{"class_name": "module_name", ...}}"""
#     def _nested_module_tree(recObj):
#         theDict = dict()
#         theClass = _get_object_class(recObj)
#         theModule = _get_object_module(recObj)
#         if theModule is not None:
#             theDict[CLASS_TAG] = theClass
#             theDict[MODULE_TAG] = theModule
#         for attribute, _ in _get_attributes_to_save(recObj):
#             nestedObj = rgetattr(recObj, attribute)
#             nested_subtree = _nested_module_tree(nestedObj)
#             if nested_subtree:
#                 theDict[attribute] = nested_subtree
#         return theDict
#     return _nested_module_tree(theObj)


def get_json_module_tree_from_dict(jsonDict):
    """Return dict containing {CLASS_TAG: "class_name", MODULE_TAG: "module_name", "attribute1":{"class_name": "module_name", ...}}"""
    def _nested_module_tree(recDict):
        theDict = dict()
        theClass = recDict.get(CLASS_TAG)
        theModule = recDict.get(MODULE_TAG)
        if theModule is not None:
            theDict[CLASS_TAG] = theClass
            theDict[MODULE_TAG] = theModule
        for key in recDict:
            nestedObj = recDict[key]
            if isinstance(nestedObj, dict):
                nested_subtree = _nested_module_tree(nestedObj)
                if nested_subtree:
                    theDict[key] = nested_subtree
        return theDict
    return _nested_module_tree(jsonDict)


def encode_str_json(theStr):
    return theStr.__repr__().replace("\\", "\\\\")[1:-1]


def decode_str_json(theStr):
    return str(theStr.__repr__().replace("\\\\", "\\"))
