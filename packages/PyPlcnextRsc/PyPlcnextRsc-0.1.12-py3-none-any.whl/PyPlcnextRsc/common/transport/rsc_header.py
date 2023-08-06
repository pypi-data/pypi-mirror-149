# Copyright (c) 2021 Phoenix Contact. All rights reserved.
# Licensed under the MIT. See LICENSE file in the project root for full license information.

import logging
import struct

from PyPlcnextRsc.common.exceptions import CommonRemotingFatalException
from PyPlcnextRsc.common.internalEnums.commandType import CommandType
from PyPlcnextRsc.common.internalEnums.remotingVersion import RemotingVersion

__all__ = ["CommandHeader"]


class CommandHeader:
    logger = logging.getLogger(__name__ + '.' + 'CommandHeader')
    """
    数据头
    """
    SIZE = 16

    @classmethod
    def Recv(cls, client, exceptedCmdType: CommandType):
        header = cls()
        header.deserialize(client.socketWrapper.binaryReader.getByteBuffer(cls.SIZE))
        if cls.logger.isEnabledFor(logging.DEBUG):
            cls.logger.debug(header.to_log_string(isSend=False))

        commandType = header.commandType
        if exceptedCmdType:
            if commandType != exceptedCmdType and commandType != CommandType.Error:
                raise CommonRemotingFatalException('Protocol violation - invalid packet type in response.')

        return commandType != CommandType.Error, header

    def Send(self, client, securityToken=None):
        """
        发送命令头
        :param client:
        :param securityToken:
        :return:
        """
        if securityToken is not None and securityToken.hasValue():
            self.isSecure = True
            self.additionalHeaderSize = securityToken.HEADER_SIZE
            self._send_internal(client)
            client.socketWrapper.binaryWriter.setUnsignedInteger(securityToken.getToken())
        else:
            self._send_internal(client)

    def _send_internal(self, client):
        __data = self.serialize()
        if self.logger.isEnabledFor(logging.DEBUG):
            self.logger.debug(self.to_log_string(isSend=True))
        client.socketWrapper.binaryWriter.setByteBuffer(__data)

    # def ReadError(self, rscClient) -> \
    #         Tuple[int,  # errCode
    #               str]:  # message
    #     warnings.warn("ReadError is too old", DeprecationWarning)
    #     len = self.dataLength
    #     buff = rscClient.socketWrapper.Read(len)
    #
    #     class tempWrapper:
    #         def __init__(self, data: bytes):
    #             self._data = data
    #
    #         def Read(self, size):
    #             if size > self._data:
    #                 raise IOError()
    #             ret = self._data[:size]
    #             self._data = self._data[size:]
    #             return ret
    #
    #     br = BinaryReader(tempWrapper(buff))
    #     errCode = br.getUnsignedInteger()
    #     _msgLen = br.getUnsignedShort()
    #     message = br.getString(_msgLen, 'ascii')
    #     return errCode, message

    def __init__(self):
        self._remotingVersion = 0
        self._flags = 0
        self._commandType = 0
        self._additionalHeaderSize = 0
        self._dataLength = 0
        self._serviceHandle = 0
        self._methodHandle = 0
        self._serviceProviderHandle = 0
        self._checksum = 0

    def to_log_string(self, isSend):
        blank = " " * (5 if isSend else 30)
        return "\n" + \
               f"{blank}------{'SEND' if isSend else 'RECV'}------\n" \
               f"{blank}Type.:{str(self.commandType)}\n" \
               f"{blank}Ver. :{str(self.remotingVersion)}\n" \
               f"{blank}Flag.:{self._flags} (hasDataTagging={self.hasDataTagging},hasDatagramming={self.hasDatagramming},isSecure={self.isSecure})\n" \
               f"{blank}Size.:{self.additionalHeaderSize}\n" \
               f"{blank}Len. :{self.dataLength}\n" \
               f"{blank}SH.  :{self.serviceHandle}\n" \
               f"{blank}MH.  :{self.methodHandle}\n" \
               f"{blank}SPH. :{self.serviceProviderHandle}" \
               ""

    @property
    def hasDataTagging(self):
        return self._flags & 64 != 0

    @hasDataTagging.setter
    def hasDataTagging(self, enable):
        if enable:
            self._flags |= 64
        else:
            self._flags &= ~64

    @property
    def hasDatagramming(self):
        return self._flags & 128 != 0

    @hasDatagramming.setter
    def hasDatagramming(self, enable):
        if enable:
            self._flags |= 128
        else:
            self._flags &= ~128

    @property
    def isSecure(self):
        return self._flags & 8 != 0

    @isSecure.setter
    def isSecure(self, enable):
        if enable:
            self._flags |= 8
        else:
            self._flags &= ~8

    @property
    def remotingVersion(self) -> RemotingVersion:
        ret = RemotingVersion.NONE
        try:
            ret = RemotingVersion(self._remotingVersion)
        except ValueError:
            pass
        return ret

    @remotingVersion.setter
    def remotingVersion(self, version: RemotingVersion):
        self._remotingVersion = version.value

    @property
    def flag(self):
        return self._flags

    @property
    def commandType(self):
        return CommandType(self._commandType)

    @commandType.setter
    def commandType(self, t: CommandType):
        self._commandType = t.value

    @property
    def additionalHeaderSize(self):
        return self._additionalHeaderSize

    @additionalHeaderSize.setter
    def additionalHeaderSize(self, value):
        self._additionalHeaderSize = value

    @property
    def dataLength(self):
        return self._dataLength

    @dataLength.setter
    def dataLength(self, length: int):
        self._dataLength = length

    @property
    def serviceProviderHandle(self):
        return self._serviceProviderHandle

    @serviceProviderHandle.setter
    def serviceProviderHandle(self, value):
        self._serviceProviderHandle = value

    @property
    def serviceHandle(self):
        return self._serviceHandle

    @serviceHandle.setter
    def serviceHandle(self, value):
        self._serviceHandle = value

    @property
    def methodHandle(self):
        return self._methodHandle

    @methodHandle.setter
    def methodHandle(self, value):
        self._methodHandle = value

    def deserialize(self, data: bytes):
        try:
            self._remotingVersion, self._flags, self._commandType, self._additionalHeaderSize, self._dataLength, self._serviceHandle, self._methodHandle, self._serviceProviderHandle, self._checksum = struct.unpack(
                '<2B7h', data)
            sum = self._calcSum()
            if self._checksum != sum:
                raise CommonRemotingFatalException('Invalid checksum of remoting header.')
        except CommonRemotingFatalException as fatal:
            raise fatal
        except Exception as E:
            raise CommonRemotingFatalException("Failed to Read command header.", E)

    def serialize(self) -> bytes:
        self._checksum = self._calcSum()

        return self._inner_serialize()

    def _inner_serialize(self):
        return struct.pack('<2B7h', self._remotingVersion, self._flags, self._commandType, self._additionalHeaderSize, self._dataLength, self._serviceHandle, self._methodHandle,
                           self._serviceProviderHandle,
                           self._checksum)

    def _calcSum(self):
        _checksum = self._checksum
        self._checksum = 0
        stream = self._inner_serialize()
        sig = 0
        for i in range(8):
            sig += (int.from_bytes((stream[i * 2], stream[1 + i * 2]), 'little'))
        sig = (sig & 0xFFFF) + ((sig >> 16) & 0xFFFF)
        sig = (sig + ((sig >> 16) & 0xFFFF)) & 0xFFFF
        self._checksum = _checksum
        return struct.unpack('<h', (~sig).to_bytes(4, byteorder='little', signed=True)[:2])[0]
