# Copyright (c) 2021 Phoenix Contact. All rights reserved.
# Licensed under the MIT. See LICENSE file in the project root for full license information.

from abc import ABCMeta, abstractmethod

from PyPlcnextRsc import Device, InvalidOperationException


class IService(metaclass=ABCMeta):
    def __init__(self, device):
        if not isinstance(device, Device):
            raise InvalidOperationException("must pass in Device instance !")

        self._raw_service = self._raw_service_interface()(device)

    @abstractmethod
    def _raw_service_interface(self):
        ...


def variable_names_generator(variableName, prefix):
    if not prefix:
        prefix = ''
    if isinstance(variableName, str):
        ret = (variableName,)
    elif isinstance(variableName, (list, tuple)):
        ret = tuple((prefix + variableName_ for variableName_ in variableName))
    else:
        raise ValueError(f"variableName's type must be str,list or tuple,not '{type(variableName)}'")
    return ret
