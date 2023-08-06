# Copyright (c) 2021 Phoenix Contact. All rights reserved.
# Licensed under the MIT. See LICENSE file in the project root for full license information.

import collections
import functools
from inspect import signature

from PyPlcnextRsc.common.exceptions import InvalidOperationException
from PyPlcnextRsc.common.transport import DataTagContext
from PyPlcnextRsc.common.types import RscTpGetOrigin, RscTpGetArgs, RscTpUnion, RscTpSequence

__all__ = [
    "RemotingMethod",
    "RemotingService"
]

from PyPlcnextRsc.common.util import SPHINX_AUTODOC_RUNNING


class _RscStaticMethodProxy:
    def __init__(self, index, func):
        self._methodHandle = index
        self.func = func
        self.__name__ = func.__name__
        self.__qualname__ = func.__qualname__
        self.__doc__ = func.__doc__
        self.parameter_tag_contexts = []
        self.parameter_defaults = collections.OrderedDict()
        self.return_tag_contexts = []
        self.serviceProxy = None
        self.methodName = None
        sig = signature(func)
        _isFirst = True
        for argName, parameter in sig.parameters.items():
            if _isFirst:
                # this argument is 'self'
                _isFirst = False
                continue
            self.parameter_defaults[argName] = parameter.default
            self.parameter_tag_contexts.append(DataTagContext.factory(parameter.annotation, param_name=argName))
        return_annotation = sig.return_annotation
        rtn_origin = RscTpGetOrigin(return_annotation)
        rtn_args = RscTpGetArgs(return_annotation)
        if rtn_origin in [list, tuple, collections.abc.Sequence] and len(rtn_args) > 1:
            for rtn in rtn_args:
                self.return_tag_contexts.append(DataTagContext.factory(rtn, param_name='<return>'))
        else:
            if return_annotation != sig.empty:
                self.return_tag_contexts.append(DataTagContext.factory(sig.return_annotation, param_name='<return>'))

        self.parameter_tag_contexts = tuple(self.parameter_tag_contexts)

        arg_list = ""
        rtn_list = ', '.join(self.parameter_defaults.keys())
        if len(self.parameter_defaults) == 1:
            rtn_list += ", "
        for param, value in self.parameter_defaults.items():
            if value != sig.empty:
                arg_list += f"{param} = {value} , "
            else:
                arg_list += f"{param} , "
        self.tuning = eval(f"lambda {arg_list} : ({rtn_list})")


_WHITE_LIST = {
    "Arp.System.Security.Services.IPasswordAuthenticationService",
    "Arp.System.Security.Services.ISecuritySessionInfoService2",
    "Arp.System.Security.Services.ISecureDeviceInfoService",
    "Arp.Device.Interface.Services.IDeviceInfoService",
}


class _DynamicRscMethodProxy:
    def __init__(self, dynamicServiceProxy, staticMethodProxy):
        self.dynamicServiceProxy = dynamicServiceProxy
        self.staticMethodProxy = staticMethodProxy
        self.havePermission = None
        self.__name__ = staticMethodProxy.__name__
        self.__qualname__ = staticMethodProxy.__qualname__
        self.__doc__ = staticMethodProxy.__doc__

        self.parameter_tuning_func = staticMethodProxy.tuning

    def checkPermission(self):
        if self.havePermission is None:
            if self.getServiceName()[0] in _WHITE_LIST:
                self.havePermission = True
            elif self.dynamicServiceProxy.rscClient.authentication:
                self.havePermission = self.dynamicServiceProxy.rscClient.authentication.checkMethodPermission(self)
            else:
                self.havePermission = True

        if not self.havePermission:
            raise PermissionError(f"current session don't have the permission to invoke method '{self.getMethodName()}' ({self.getServiceName()[0]})")

    def __call__(self, *args, **kwargs):
        self.checkPermission()
        return self.dynamicServiceProxy.rscClient.CallMethod(
            self.getServiceProviderHandler(),
            self.getServiceHandler(),
            self.getMethodHandler(),
            self.staticMethodProxy.parameter_tag_contexts,
            self.parameter_tuning_func(*args, **kwargs),
            self.staticMethodProxy.return_tag_contexts)

    def getMethodHandler(self):
        return self.staticMethodProxy._methodHandle

    def getServiceProviderHandler(self):
        return self.dynamicServiceProxy.providerHandle

    def getServiceHandler(self):
        return self.dynamicServiceProxy.serviceHandle

    def getMethodName(self):
        return self.staticMethodProxy.methodName

    def getServiceProviderName(self):
        return self.dynamicServiceProxy.staticServiceProxy.serviceProviderName

    def getServiceName(self):
        return self.dynamicServiceProxy.staticServiceProxy.fullName


class _DynamicRscServiceProxy:
    def __init__(self, rscClient, staticServiceProxy):
        self.staticServiceProxy = staticServiceProxy
        self.rscClient = rscClient
        self.providerHandle = rscClient.GetServiceProviderHandle(staticServiceProxy.serviceProviderName)
        h = rscClient.GetServiceExtRequest(staticServiceProxy.serviceProviderName, staticServiceProxy.fullName)
        if type(h) is tuple:
            self.serviceHandle = h[0]
            self.providerHandle = h[1]
        else:
            self.serviceHandle = h


class _StaticRscServiceProxy:
    def __init__(self, serviceInterfaceType, fullName, serviceProviderName):
        if type(fullName) == str:
            fullName = (fullName,)
        self.serviceInterfaceType = serviceInterfaceType
        self.__name__ = serviceInterfaceType.__name__
        self.__qualname__ = serviceInterfaceType.__qualname__
        self.__doc__ = serviceInterfaceType.__doc__

        self.fullName = fullName
        self.serviceProviderName = serviceProviderName

        # 向所有的方法注入本代理
        for n, v in self.serviceInterfaceType.__dict__.items():
            if n.startswith("__"):
                continue
            if isinstance(v, _RscStaticMethodProxy):
                v.serviceProxy = self

    def __call__(self, device):
        from PyPlcnextRsc.common.transport.rsc_client import RscClient
        if isinstance(device, RscClient):
            rscClient = device
        elif hasattr(device, "_rscClient"):
            rscClient = device._rscClient
        else:
            raise InvalidOperationException("should pass in PLCnext Device instance")
        ins = self.serviceInterfaceType()
        ins.__name__ = self.__name__ + "Impl"
        ins.__qualname__ = self.__qualname__ + "Impl"
        ins.__doc__ = self.__doc__
        dyService = _DynamicRscServiceProxy(rscClient=rscClient, staticServiceProxy=self)
        setattr(ins, '_DynamicRscServiceProxy', dyService)
        for n, v in self.serviceInterfaceType.__dict__.items():
            if n.startswith("__"):
                continue
            if isinstance(v, _RscStaticMethodProxy):
                v.methodName = n
                setattr(ins, n, _DynamicRscMethodProxy(dynamicServiceProxy=dyService, staticMethodProxy=v))
        return ins


if SPHINX_AUTODOC_RUNNING:

    def RemotingService(fullName: RscTpUnion[str, RscTpSequence[str]], serviceProviderName: str = 'Arp'):
        """ Decorator to define an implementation for a RemotingService
        fullName , names , serviceProviderName

        """

        def decorator(cls):
            return cls

        return decorator


    def RemotingMethod(index: int):
        """ Decorator to define an implementation for a RemotingMethod
        :param index:

        """

        def decorator(func):
            @functools.wraps(func)
            def inner(*args, **kwargs):
                return func(*args, **kwargs)

            return inner

        return decorator
else:
    def RemotingService(fullName: RscTpUnion[str, RscTpSequence[str]], serviceProviderName: str = 'Arp'):
        """ Decorator to define an implementation for a RemotingService
        fullName , names , serviceProviderName
        """

        def decorator(cls):
            return _StaticRscServiceProxy(serviceInterfaceType=cls, fullName=fullName, serviceProviderName=serviceProviderName)

        return decorator


    def RemotingMethod(index: int):
        """ Decorator to define an implementation for a RemotingMethod

        :param index:
        :return:
        """
        if not isinstance(index, int):
            raise TypeError("RemotingMethod's index requires int")

        def decorator(func):
            return _RscStaticMethodProxy(index, func)

        return decorator
