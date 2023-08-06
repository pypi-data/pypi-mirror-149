# Copyright (c) 2021 Phoenix Contact. All rights reserved.
# Licensed under the MIT. See LICENSE file in the project root for full license information.
from PyPlcnextRsc import RscType, RscTpUnion, RscTpSequence
from PyPlcnextRsc.Arp.Plc.Gds.Services import IDataAccessService, DataAccessError
from PyPlcnextRsc.wrapper.common import IService


class _wrapper_read_item:
    def __init__(self, read_item):
        self.read_item = read_item

    def __repr__(self):
        return f"wReadItem<{self.portType.name}>,value={self.value},error={self.error.name}"

    @property
    def error(self) -> DataAccessError:
        return self.read_item.Error

    @property
    def value(self) -> any:
        return self.read_item.Value.GetValue()

    @property
    def portType(self) -> RscType:
        return self.read_item.Value.GetType()


class DataAccessService(IService):
    def _raw_service_interface(self):
        return IDataAccessService

    def read(self, port: RscTpUnion[str, RscTpSequence[str]], prefix=None) -> RscTpUnion[_wrapper_read_item, RscTpSequence[_wrapper_read_item], any]:
        is_single = False
        if type(port) == str:
            port = (port,)
            is_single = True
        if prefix:
            port = tuple(map(lambda p: prefix + p, port))
        ret = [_wrapper_read_item(item) for item in self._raw_service.Read(port)]
        if is_single:
            return ret[0].value
        else:
            return [item.value for item in ret]

    def write(self):
        ...
