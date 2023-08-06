# Copyright (c) 2021 Phoenix Contact. All rights reserved.
# Licensed under the MIT. See LICENSE file in the project root for full license information.

import logging
from abc import ABCMeta, abstractmethod, ABC

from PyPlcnextRsc.common.exceptions import CommonRemotingClientException
from PyPlcnextRsc.common.internalEnums.commandType import CommandType
from PyPlcnextRsc.common.transport.rsc_header import CommandHeader

__all__ = [
    "ConnectRequest",
    "DisconnectRequest",
    "GetServiceProviderHandle",
    "GetServiceExtRequest",
]


class AbstractCommand(metaclass=ABCMeta):
    def __init__(self):
        self.logger = logging.getLogger(__name__ + "." + self.__class__.__name__)

    @abstractmethod
    def _send(self, rsc_client, header):
        ...

    @abstractmethod
    def _receive(self, rsc_client):
        ...

    def request(self, rsc_client):
        try:
            if not rsc_client.socketWrapper.isConnected():
                raise CommonRemotingClientException("not connected")
            _header = CommandHeader()
            _header.remotingVersion = rsc_client.remotingVersion
            _header.hasDataTagging = rsc_client.hasDataTagging
            socket_wrapper = rsc_client.socketWrapper
            self._send(rsc_client, _header)
            socket_wrapper.flush()
            self._receive(rsc_client)
        except Exception as E:
            rsc_client.socketWrapper.rollback()
            raise E


class ConnectRequest(AbstractCommand, ABC):

    def _send(self, rsc_client, header: CommandHeader):
        header.commandType = CommandType.ConnectRequest
        header.hasDataTagging = True
        header.hasDatagramming = True
        header.Send(rsc_client)
        # rsc_client.socketWrapper.Write(bytes("aaaaaaa" * 20, encoding='ascii'))

    def _receive(self, rsc_client):
        success, header = CommandHeader.Recv(rsc_client, CommandType.ConnectConfirm)
        if success:
            rsc_client.remotingVersion = header.remotingVersion
            rsc_client.hasDataTagging = header.hasDataTagging
            rsc_client.hasDataGramming = header.hasDatagramming
        else:
            isServerException, exception = rsc_client.ReadException()
            print(isServerException, exception)


class DisconnectRequest(AbstractCommand):
    def _send(self, rsc_client, header: CommandHeader):
        header.commandType = CommandType.DisconnectRequest
        header.Send(rsc_client)

    def _receive(self, rsc_client):
        success, header = CommandHeader.Recv(rsc_client, CommandType.DisconnectConfirm)
        if success:
            ...
        else:
            isServerException, exception = rsc_client.ReadException()
            raise exception


class GetServiceProviderHandle(AbstractCommand):
    def __init__(self, providerName: str):
        super().__init__()
        self._providerName = providerName
        self._providerHandle = None

    @property
    def ServiceProviderHandle(self):
        return self._providerHandle

    def _send(self, rsc_client, header: CommandHeader):
        header.commandType = CommandType.GetServiceProviderRequest
        header.dataLength = len(self._providerName) + 1
        header.Send(rsc_client)
        rsc_client.socketWrapper.binaryWriter.setString(self._providerName, "utf_8")

    def _receive(self, rsc_client):
        success, header = CommandHeader.Recv(rsc_client, CommandType.GetServiceProviderConfirmation)
        if success:
            handler = header.serviceHandle
            self._providerHandle = handler
            self.logger.debug(f"get providerIndex of {self._providerName} : '{handler}'")
        else:
            isServerException, exception = rsc_client.ReadException()
            if isServerException:
                raise exception
            else:
                self.logger.error("Failed to execute GetServiceProviderCommand.", exc_info=exception)


class GetServiceExtRequest(AbstractCommand):
    def __init__(self, serviceProviderHandler: int, serviceName: str):
        super().__init__()
        self.serviceProviderHandler = serviceProviderHandler
        self.serviceName = serviceName
        self._serviceHandle = None
        self.ConfirmServiceProviderHandle = None

    @property
    def serviceHandle(self):
        return self._serviceHandle

    def _send(self, rsc_client, header: CommandHeader):
        serviceName = self.serviceName
        binaryWriter = rsc_client.socketWrapper.binaryWriter
        header.commandType = CommandType.GetServiceExtRequest
        header.dataLength = 2 + len(serviceName) + 1
        header.Send(rsc_client)
        binaryWriter.setSignedShort(self.serviceProviderHandler)
        binaryWriter.setString(serviceName, 'utf_8')

    def _receive(self, rsc_client):
        success, header = CommandHeader.Recv(rsc_client, CommandType.GetServiceExtConfirmation)
        if success:
            self._serviceHandle = header.serviceHandle
            self.ConfirmServiceProviderHandle = header.serviceProviderHandle
            if self.ConfirmServiceProviderHandle != self.serviceProviderHandler:
                self.logger.debug(f"ServiceProviderChange! new serviceProviderHandle = {self.ConfirmServiceProviderHandle} for {self.serviceName}")
            else:
                self.ConfirmServiceProviderHandle = None
                self.logger.debug(f"get serviceHandle of {self.serviceName}(provider:{self.serviceProviderHandler}) : '{self._serviceHandle}'")
        else:
            isServerException, exception = rsc_client.ReadException()
            print(isServerException, exception)
