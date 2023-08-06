from abc import ABCMeta
from inspect import signature


class InterfaceDevice(metaclass=ABCMeta):
    """
    Interface class that represents a device.
    Hidden feature: variables that need to be saved must be type-hinted: e.g.: x: int. See :meth:`~optimeed.core.myjson.obj_to_json` for more info
    """
    def assign(self, device_to_assign, resetAttribute=False):
        """
        Copy the attribute values of device_to_assign to self. The references are not lost.

        :param device_to_assign: :class:`~optimeed.InterfaceDevice.InterfaceDevice`
        :param resetAttribute:
        """
        def _assign(theObjectTemplate, theObjectToAssign):
            attributes = vars(theObjectTemplate)
            for key in attributes:
                subEntityTemplate = getattr(theObjectTemplate, key)  # entity to assign

                try:
                    subEntity = getattr(theObjectToAssign, key)  # get sub entity
                except AttributeError:
                    subEntity = subEntityTemplate  # if not exists => use from template

                if getattr(subEntityTemplate, '__dict__', None) is not None:  # sub entity is an object
                    if not resetAttribute:
                        params = signature(subEntity.__class__).parameters
                        entranceParams = []
                        for param in params.values():
                            if param.default is param.empty:
                                entranceParams.append(None)
                            else:
                                entranceParams.append(param.default)
                        setattr(theObjectTemplate, key, subEntity.__class__(*entranceParams))  # set subentity_template as type of subentity
                        subEntityTemplate = getattr(theObjectTemplate, key)  # Refresh subEntity template
                    _assign(subEntityTemplate, subEntity)  # do again
                else:
                    setattr(theObjectTemplate, key, subEntity)
        _assign(self, device_to_assign)
