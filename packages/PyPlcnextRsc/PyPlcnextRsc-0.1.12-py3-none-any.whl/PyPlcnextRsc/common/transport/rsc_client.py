# Copyright (c) 2021 Phoenix Contact. All rights reserved.
# Licensed under the MIT. See LICENSE file in the project root for full license information.
import logging
import math
import sys
import threading
import time
import weakref
from datetime import datetime, timezone
from io import BytesIO
from typing import Tuple, Union

from PyPlcnextRsc.common.exceptions import *
from PyPlcnextRsc.common.internalEnums.commandType import CommandType
from PyPlcnextRsc.common.internalEnums.remotingVersion import RemotingVersion
from PyPlcnextRsc.common.internalEnums.string_encoding import RscStringEncoding
from PyPlcnextRsc.common.objects import RscVariant
from PyPlcnextRsc.common.serviceDefinition.marshal import Marshal
from PyPlcnextRsc.common.tag_type import RscType
from PyPlcnextRsc.common.transport.rsc_header import CommandHeader
from PyPlcnextRsc.common.transport.rsc_request import ConnectRequest, DisconnectRequest, GetServiceProviderHandle, GetServiceExtRequest
from PyPlcnextRsc.common.transport.rsc_sock import CreateSockWrapper
from PyPlcnextRsc.common.transport.rsc_value_adapter import *
from PyPlcnextRsc.common.types import RscTpAnnotate, RscTpTuple
from PyPlcnextRsc.common.util import FatalVersionCheck

FatalVersionCheck()
DEBUG = True

__all__ = ["RscClient"]


class RscClient:
    def __init__(self, info, config):
        self.logger = logging.getLogger(__name__ + "." + self.__class__.__name__)
        self.info = weakref.proxy(info)
        self.config = weakref.proxy(config)

        self.socketWrapper = CreateSockWrapper(info, config)
        self.remotingVersion = RemotingVersion.RECENT
        self.hasDataTagging = False
        self.hasDataGramming = False
        self.client_context = RscClientContext(rsc_client=self)
        self.rscReader = RscReader(binary_reader=self.socketWrapper.binaryReader, rsc_client_context=self.client_context)
        self.rscWriter = RscWriter(binary_writer=self.socketWrapper.binaryWriter, rsc_client_context=self.client_context)
        self._provider_buffer = {}
        self._service_handler_buffer = {}
        self.__token = None
        self._disposed = False
        self.lock = threading.RLock()
        self._keep_alive_thread = None
        self._last_call_method_time = 0
        self.authentication = None

    def getToken(self):
        return self.__token

    def setToken(self, token):
        self.__token = token

    def consumeConfirmation(self):
        if not self.hasDataTagging:
            return True

        b = self.rscReader.remotingReader.binaryReader.getUnsignedByte()
        if b == 255:
            return True
        if DEBUG:
            self.socketWrapper._socket.setblocking(False)
            rest = bytearray()
            rest.append(b)
            while True:
                try:
                    rest.append(self.rscReader.remotingReader.binaryReader.getUnsignedByte())
                except:
                    break
            print(f"!!!! Un consumed :{rest}", file=sys.stderr)
        return False

    def connect(self):
        with self.lock:
            if self.socketWrapper.isConnected():
                raise InvalidOperationException("already connected!")
            if self._disposed:
                raise InvalidOperationException("Already disposed , must create new connection instance of Device")
            self.socketWrapper.connect()
            cr = ConnectRequest()
            cr.request(self)
            self.authentication = _Authentication(self)
            self.logger.info("connected success")
            self._keep_alive_thread = _KeepAliveThread(self, self.config.keepAlive_ms)
            self._keep_alive_thread.start()

    def dispose(self):
        try:
            with self.lock:
                self.authentication.logout()
                if self._keep_alive_thread and self._keep_alive_thread.is_alive():
                    self._keep_alive_thread.stop()
                    self._keep_alive_thread.join()

                if self.socketWrapper.isConnected():
                    dr = DisconnectRequest().request(self)
                    self._provider_buffer.clear()
                    self._service_handler_buffer.clear()
                    self.socketWrapper.disconnect()
                    self.logger.info('connection closed')
                self._disposed = True
        except:
            ...

    def ReadException(self):
        rscReader = self.rscReader
        rscErrorCode = rscReader.Read(RscTpAnnotate[int, Marshal(rscType=RscType.Uint32)])
        try:
            err = RscError(value=rscErrorCode)
            if err.value & RscError.CommunicationLayerMask == RscError.CommunicationLayerMask:
                exception = CommonRemotingFatalException(rscError=err)
                isServerException = False
            else:
                message = rscReader.Read(RscTpAnnotate[str, Marshal(rscType=RscType.AnsiString)])
                innerExceptionMessage = rscReader.Read(RscTpTuple[RscVariant])
                isServerException = True
                exception = CommonRemotingServerException(err, message, innerExceptionMessage)
        except Exception as E:
            raise E
            # TODO
        return isServerException, exception

    def CallMethod(self, serviceProviderHandle, serviceHandle, methodHandle, parameter_contexts, parameters, return_contexts):
        # TODO move to RscRequest
        with self.lock:
            self._last_call_method_time = time.time()
            try:
                if self.logger.isEnabledFor(logging.DEBUG):
                    self.logger.debug(f"call method:\n"
                                      f"serviceProviderHandle={serviceProviderHandle},\n"
                                      f"serviceHandle={serviceHandle},\n"
                                      f"methodHandle={methodHandle},\n"
                                      f"parameterContexts={parameter_contexts},\n"
                                      f"parameters={parameters},\n"
                                      f"return_context={return_contexts}\n\n")
                if self.socketWrapper.isConnected():
                    rscReader = self.rscReader
                    rscWriter = self.rscWriter
                    header = CommandHeader()
                    header.hasDataTagging = self.hasDataTagging
                    header.remotingVersion = self.remotingVersion
                    header.commandType = CommandType.InvokeRequest
                    header.serviceHandle = serviceHandle
                    header.serviceProviderHandle = serviceProviderHandle
                    header.methodHandle = methodHandle
                    header.Send(self, securityToken=self.getToken())
                    for idx, context in enumerate(parameter_contexts):
                        if not context.isOut:
                            rscWriter.WriteByCtx(parameters[idx], context)
                    rscWriter.WriteConfirmation(flush=True)
                    # ---------------------------------
                    success, header = CommandHeader.Recv(self, CommandType.InvokeConfirmation)
                    if header.additionalHeaderSize > 0:
                        rscReader.remotingReader.binaryReader.getByteBuffer(header.additionalHeaderSize)
                    if header.remotingVersion > self.remotingVersion:
                        raise CommonRemotingFatalException(f"Invalid communication protocol version {header.remotingVersion}, expected {self.remotingVersion}")
                    if success:
                        ret = []
                        for idx, context in enumerate(parameter_contexts):
                            if context.isOut:
                                val = rscReader.ReadByCtx(context)
                                parameters[idx](val)
                        if len(return_contexts) > 1:
                            for rtn_ctx in return_contexts:
                                ret.append(rscReader.ReadByCtx(rtn_ctx))
                            ret = tuple(ret)
                        else:
                            if len(return_contexts) == 0:
                                ret = None
                            else:
                                ret = rscReader.ReadByCtx(return_contexts[0])

                        if not self.consumeConfirmation():
                            raise CommonRemotingFatalException('Protocol violation - missing datatag end in response.')
                        return ret
                    else:
                        isServerException, exception = self.ReadException()
                        if not self.consumeConfirmation():
                            raise CommonRemotingFatalException('Protocol violation - missing datatag end in response.')
                        # TODO
                        raise exception

                else:
                    raise InvalidOperationException("Device not connected")
            except Exception as exc:
                self.socketWrapper.rollback()
                raise exc

    def GetSession(self):
        ...

    def GetServiceProviderHandle(self, serviceProviderName: str) -> int:
        """获取服务提供者"""
        with self.lock:
            ret = self._provider_buffer.get(serviceProviderName, None)
            if ret:
                return ret
            req = GetServiceProviderHandle(serviceProviderName)
            req.request(self)
            if req.ServiceProviderHandle <= 0:
                raise CommonRemotingServiceNotFoundException(f"Unknown service provider ''{serviceProviderName}''")
            ret = self._provider_buffer[serviceProviderName] = req.ServiceProviderHandle
            return ret

    def GetServiceExtRequest(self, serviceProvider, serviceName) -> Union[int, Tuple[int, int]]:
        """获取服务"""
        with self.lock:
            if type(serviceName) == str:
                serviceName = [serviceName]
            bundle = self._service_handler_buffer.get(serviceProvider, None)
            if not bundle:
                bundle = self._service_handler_buffer[serviceProvider] = {}

            if len(serviceName) == 1:
                serviceHandle = bundle.get(serviceName[0], None)
                if serviceHandle:
                    return serviceHandle

            for currentName in serviceName:
                serviceHandle = bundle.get(currentName, None)
                if serviceHandle:
                    return serviceHandle
                provider = self.GetServiceProviderHandle(serviceProvider)
                req = GetServiceExtRequest(provider, currentName)
                req.request(self)
                if req.serviceHandle > 0:
                    if req.ConfirmServiceProviderHandle:
                        self.logger.debug("handler changed!")
                        return req.serviceHandle, req.ConfirmServiceProviderHandle
                    else:
                        serviceHandle = bundle[currentName] = req.serviceHandle
                        return serviceHandle

            raise CommonRemotingServiceNotFoundException(f"Unknown service ''{serviceName}' (provider:{serviceProvider})'")

    def Close(self, disconnectRemoting=True):
        ...

    def BeginTransaction(self, rscServiceProxy):
        ...

    def EndTransaction(self, rscServiceProxy):
        ...

    class TransactionGuard:
        def __init__(self, rscClient, rscServiceProxy):
            self.rscClient = rscClient
            self.rscServiceProxy = rscServiceProxy


class _Authentication:
    """
    used for manager authentication
    """

    def __init__(self, rscClient):
        from PyPlcnextRsc.Arp.System.Security.Services import IPasswordAuthenticationService, ISecuritySessionInfoService2
        self.logger = logging.getLogger(__name__ + "." + self.__class__.__name__)
        self.rscClient = weakref.proxy(rscClient)
        self.SecuritySessionInfoService2 = ISecuritySessionInfoService2(self.rscClient)
        self.passwordAuthenticationService = IPasswordAuthenticationService(self.rscClient)
        require_authentication = self.SecuritySessionInfoService2.isUserAuthenticationRequired()
        self.logger.debug(f"""server {"don't " if not require_authentication else ""}need authentication""")
        if require_authentication:
            if not self.rscClient.info.isAuthenticationProvided():
                raise CommonRemotingException("Must provide the authentication !")
            self.login()
        self.roles = self.SecuritySessionInfoService2.getRoleNames()
        self.logger.debug("user roles = " + str(self.roles))

    def _generateNotifications(self):
        from PyPlcnextRsc.Arp.System.Security.Services import ISecureDeviceInfoService, FileSystemError
        from PyPlcnextRsc.Arp.Device.Interface.Services import IDeviceInfoService
        notification = ""
        rscStream, fileSystemError = ISecureDeviceInfoService(self.rscClient).getSystemUseNotification()
        if fileSystemError == FileSystemError.NONE:
            notification = rscStream.getValue().decode()
        info_service = IDeviceInfoService(self.rscClient)
        INFOS = ["General.SerialNumber", "General.ArticleName", "General.Firmware.Version"]
        ret = {}
        for item, key in zip(info_service.GetItems(INFOS), INFOS):
            ret[key] = item.GetValue()
        ret["Notification"] = notification
        ret["Address"] = self.rscClient.info.getAddr()
        return ret

    def login(self):
        from PyPlcnextRsc.Arp.System.Security.Services import AuthenticationError
        _try_cnt = 0
        if self.rscClient.info.isNotificationNeeded():
            __secure_info = self.rscClient.info.getSecureInfo(self._generateNotifications())
        else:
            __secure_info = self.rscClient.info.getSecureInfo()
        if __secure_info[0] == None or __secure_info[0] == "":
            raise CommonRemotingException("Authentication failed, Must provide UserName")
        while True:
            token, m, errcode = self.passwordAuthenticationService.createSession(*__secure_info)
            if errcode == AuthenticationError.NONE:
                self.rscClient.setToken(token)
                self.logger.debug("login success")
                break
            else:
                if errcode == AuthenticationError.TryAgainLater and _try_cnt < 3:
                    self.logger.warning("retry to login...")
                    time.sleep(2)
                    _try_cnt += 1
                else:
                    raise CommonRemotingException(f"Authentication failed while connecting to target with error '{errcode.name}'." + (f' Penalty: {m} milliseconds.' if m else ""),
                                                  err=ErrType.AUTH_LOGIN_FAILURE)

    def logout(self):
        try:
            if self.rscClient.getToken() and self.rscClient.getToken().hasValue():
                self.passwordAuthenticationService.closeSession(self.rscClient.getToken())
                self.logger.debug("log out success")
        except:
            pass

    def checkMethodPermission(self, dynamicMethodProxy):
        return True
        # method_name = dynamicMethodProxy.getMethodName()
        # method_handle = dynamicMethodProxy.getMethodHandler()
        # provider_name = dynamicMethodProxy.getServiceProviderName()
        # service_name = dynamicMethodProxy.getServiceName()
        # self.logger.debug(f"checkMethodPermission provider={provider_name},service={service_name},method={method_name}({method_handle})")
        # return self.SecuritySessionInfoService2.isServiceCallAllowedOld(provider_name, service_name[0], method_handle)


class _KeepAliveThread(threading.Thread):
    """
    used by RscClient to keep the session open
    """

    def __init__(self, rscClient: RscClient, timeout_ms):
        assert timeout_ms > 0
        super().__init__()
        self.logger = logging.getLogger(__name__ + "." + self.__class__.__name__)
        self.rscClient = rscClient
        self._dostop = False
        self._cond = threading.Condition()
        self.timeout = timeout_ms

        from PyPlcnextRsc.Arp.Plc.Domain.Services import IPlcManagerService
        self._service_for_alive = IPlcManagerService(rscClient)

    def doKeepAlive(self):
        # ...
        self._service_for_alive.GetPlcState()

    def time_up(self):
        timeout = self.timeout
        delta_time = (time.time() - self.rscClient._last_call_method_time) * 1000
        if delta_time < timeout:
            wait_again = timeout - delta_time
            self.logger.debug("no need to renew channel, next wait %d milliseconds", int(wait_again))
            return timeout - delta_time
        else:
            self.logger.info("renewing channel")
            self.doKeepAlive()
            return timeout

    def run(self):
        self.logger.debug("starting keepalive thread with period of %s milliseconds", self.timeout)
        time_wait = self.timeout
        while not self._dostop:
            with self._cond:
                self._cond.wait(time_wait / 1000)
            if self._dostop:
                break

            time_wait = self.time_up()
        self.logger.debug("keepalive thread has stopped")

    def stop(self):
        self.logger.debug("stopping keepalive thread")
        self._dostop = True
        with self._cond:
            self._cond.notify_all()


class RscClientContext:
    def __init__(self, rsc_client: RscClient):
        self.rscClient = weakref.proxy(rsc_client)

    def GetReader(self):
        ...

    def GetWriter(self):
        ...

    def BeginServiceInvocationRequest(self, serviceProviderHandle, rscServiceHandle, rscMethodHandle):
        ...

    def EndServiceInvocationRequest(self):
        ...

    def BeginServiceInvocationResponse(self, serviceProviderHandle, rscServiceHandle, rscMethodHandle): ...

    def EndServiceInvocationResponse(self): ...


class RemotingReader:

    def __init__(self, binary_reader, rsc_reader, rsc_client_context):
        self.rscReader = weakref.proxy(rsc_reader)
        self.binaryReader = weakref.proxy(binary_reader)
        self.rscClientContext = weakref.proxy(rsc_client_context)

    def getRscReader(self):
        return self.rscReader

    def HasDataTagging(self):
        ...

    def ReadArrayLength(self) -> int:
        return self.binaryReader.getSignedInteger()

    # def ReadArrayInformation(self) -> RscArrayInformation:
    #     ...

    def ReadEnumeratorTag(self) -> RscType:
        return self.ReadTag()

    def ReadDataInternal(self, size) -> bytes:
        return self.binaryReader.getByteBuffer(size)

    def TryReadDataInternal(self, size) -> [bytes, int]:
        ...

    def ReadStringEncoding(self) -> RscStringEncoding:
        rsc_type = self.ReadTag()
        if rsc_type == RscType.Utf8String:
            return RscStringEncoding.Utf8
        elif rsc_type == RscType.AnsiString:
            return RscStringEncoding.Ansi
        elif rsc_type == RscType.Utf16String:
            return RscStringEncoding.Utf16
        else:
            raise RuntimeError("invalid string_encoding")

    def ReadStringInternal(self, rscStringEncoding: RscStringEncoding, readTag=True, isChars=False):
        if readTag:
            encoding = self.ReadStringEncoding()
            if encoding != rscStringEncoding:
                raise CommonRemotingFatalException(f"expect string encoding '{rscStringEncoding.name}' but {encoding.name} received .")
        if rscStringEncoding in [RscStringEncoding.Null, None]:
            raise InvalidOperationException("must provide string_encoding")
        if rscStringEncoding == RscStringEncoding.Utf8:
            encoding_str = 'utf_8'
        elif rscStringEncoding == RscStringEncoding.Ansi:
            encoding_str = 'ascii'
        else:
            encoding_str = 'utf_16_le'
        return self.binaryReader.getString(self.binaryReader.getUnsignedShort(), encoding_str, isChars=isChars)

    def ReadObjectType(self) -> RscType:
        self.ReadTag(RscType.Object)
        return self.ReadTag()

    def BeginReadStream(self) -> int:
        return self.binaryReader.getSignedInteger()

    def ReadStream(self) -> BytesIO:
        binaryReader = self.binaryReader
        sock = binaryReader.socket_wrapper
        buf = BytesIO()
        max_packet_size = self.BeginReadStream()
        if max_packet_size == 0 or max_packet_size > 65535:
            max_packet_size = 65535
        while True:
            remain = package_size = binaryReader.getSignedInteger()
            if package_size == -1:
                break

            while remain:
                current_read_size = min(package_size, max_packet_size, remain)
                package = bytearray(package_size)
                sock.recv_into(package, package_size)
                buf.write(package)
                remain -= current_read_size
        buf.seek(0, 0)
        return buf

    def ReadDateTime(self) -> datetime:
        ba = bytearray(self.binaryReader.getUnsignedLong().to_bytes(8, byteorder='big', signed=False))
        kind_mask = ba[0] & 0b1100_0000
        tz = timezone.utc if kind_mask == 0x40 else None
        # if kind_mask == 0x40:
        #     tz = timezone.utc
        # print("UTC")
        # elif kind_mask == 0x80:
        #     print("LOCAL")
        # else:
        #     print("DateTimeKind Unspecified not supported.")
        ba[0] = ba[0] & 0b0011_1111
        ticks = int.from_bytes(ba, byteorder='big', signed=False)
        return datetime.fromtimestamp((ticks - 621355968000000000) / 10000000, tz)

    def ReadTag(self, expectedType: RscType = None) -> RscType:
        rsc_type = RscType(self.binaryReader.getUnsignedByte())
        if expectedType is not None and expectedType != rsc_type:
            raise CommonRemotingFatalException(
                f'Protocol violation - invalid packet type in response. excepted {expectedType} but {rsc_type} received')
        return rsc_type

    def ReadArrayTag(self, elementType: RscType) -> int:  # arrayLength
        # 成员是结构体时要再处理
        self.ReadTag(RscType.Array)
        self.ReadTag(elementType)
        return self.ReadArrayLength()

    def ReadBeginStruct(self, fieldCount: int):
        self.ReadTag(RscType.Struct)
        count = self.ReadFieldCount()
        if count != fieldCount:
            raise CommonRemotingFatalException(f"expect field count is {fieldCount} but {count} received .")

    def ReadFieldCount(self):
        return self.binaryReader.getUnsignedShort()

    def ReadSecurityToken(self):
        ...


class RscReader:

    def __init__(self, binary_reader, rsc_client_context):
        self.remotingReader = RemotingReader(binary_reader=binary_reader, rsc_reader=self, rsc_client_context=rsc_client_context)
        self.rscClient = rsc_client_context.rscClient

    def GetRemotingReader(self) -> RemotingReader:
        return self.remotingReader

    def Read(self, valueAnnotation) -> any:
        return Read(valueAnnotation, self.rscClient)

    def ReadByCtx(self, context) -> any:
        xx = ReadValue(context, self.rscClient, False)
        return xx

    def ReadString(self):
        return self.remotingReader.ReadStringInternal(RscStringEncoding.Utf8)


class RemotingWriter:
    def __init__(self, binary_writer, rsc_writer, rsc_client_context: RscClientContext):
        self.rscWriter = weakref.proxy(rsc_writer)
        self.binaryWriter = weakref.proxy(binary_writer)
        self.rscClientContext = weakref.proxy(rsc_client_context)

    def GetRscWriter(self):
        return self.rscWriter

    def HasDataTagging(self):
        return self.rscClientContext.rscClient.hasDataTagging

    def WriteDateTime(self, date_time: datetime):
        ts = date_time.timestamp()
        frac, t = math.modf(ts)
        us = frac * 1e6
        ba = bytearray(int(t * 10000000 + us * 10 + 621355968000000000).to_bytes(8, byteorder='big', signed=False))
        if date_time.tzname() == "UTC":
            ba[0] = ba[0] | 64
        else:
            ba[0] = ba[0] | 128
        self.binaryWriter.setUnsignedLong(int.from_bytes(ba, byteorder='big', signed=False))

    def WriteArrayLength(self, value):
        self.binaryWriter.setSignedInteger(value)

    def WriteDataInternal(self, data: bytes):
        self.binaryWriter.setByteBuffer(data)

    def WriteStringInternal(self, string, rscStringEncoding: RscStringEncoding = RscStringEncoding.Utf8, writeTag=True, isChars=False):
        if rscStringEncoding in [RscStringEncoding.Null, None]:
            raise InvalidOperationException("must provide string_encoding")
        if rscStringEncoding == RscStringEncoding.Utf8:
            encoding_str = 'utf_8'
        elif rscStringEncoding == RscStringEncoding.Ansi:
            encoding_str = 'ascii'
        else:
            encoding_str = 'utf_16_le'
        if writeTag:
            self.WriteStringEncoding(rscStringEncoding)
        self.WriteStringLength(len(string) + 1)
        self.binaryWriter.setString(string, encoding_str, isChars=isChars)

    def WriteConfirmation(self, flush=False):
        self.binaryWriter.setUnsignedByte(255)
        if flush:
            self.binaryWriter.socket_wrapper.flush()

    def WriteEnumeratorTag(self, tag: RscType):
        ...

    def _BeginWriteStream(self, maxPacketSize):
        self.binaryWriter.setSignedInteger(maxPacketSize)

    def WriteStream(self, buffer, maxPacketSize):
        self._BeginWriteStream(maxPacketSize)
        pack = bytearray(4096)
        while True:
            s_len = buffer.readinto(pack)
            if not s_len:
                break
            binaryWriter = self.binaryWriter
            binaryWriter.setSignedInteger(s_len)
            binaryWriter.setByteBuffer(pack[0:s_len])
        self._EndWriteStream()
        buffer.seek(0, 0)

    def _EndWriteStream(self):
        self.binaryWriter.setSignedInteger(-1)

    def WriteObjectType(self, objType: RscType):
        self.WriteTag(RscType.Object)
        self.WriteTag(objType)

    def WriteStringLength(self, length):
        self.binaryWriter.setUnsignedShort(length)

    def WriteStringEncoding(self, encoding: RscStringEncoding):
        if encoding == RscStringEncoding.Utf8:
            rsc_type = RscType.Utf8String
        elif encoding == RscStringEncoding.Ansi:
            rsc_type = RscType.AnsiString
        elif encoding == RscStringEncoding.Utf16:
            rsc_type = RscType.Utf16String
        else:
            raise InvalidOperationException("invalid string_encoding")
        self.WriteTag(rsc_type)

    def WriteObjectString(self, stringEncoding: RscStringEncoding, string):
        self.WriteTag(RscType.Object)
        self.WriteStringInternal(string, stringEncoding, True)

    def WriteError(self, resourceCatalogue, errorResourceId, errorCode, errorMsg):
        ...

    def WriteTag(self, tag: RscType):
        self.binaryWriter.setUnsignedByte(tag.value)

    def WriteArrayTag(self, elementType: RscType, length):
        self.WriteTag(RscType.Array)
        self.WriteTag(elementType)
        self.WriteArrayLength(length)

    def WriteBeginStruct(self, fieldCount):
        self.WriteTag(RscType.Struct)
        self.WriteFieldCount(fieldCount)

    def WriteFieldCount(self, fieldCount):
        self.binaryWriter.setUnsignedShort(fieldCount)


class RscWriter:
    def __init__(self, binary_writer, rsc_client_context):
        self.remotingWriter = RemotingWriter(binary_writer=binary_writer, rsc_writer=self, rsc_client_context=rsc_client_context)
        self.rscClient = rsc_client_context.rscClient

    def GetRemotingReader(self) -> RemotingWriter:
        return self.remotingWriter

    def WriteConfirmation(self, flush=False):
        self.remotingWriter.WriteConfirmation(flush)

    def Write(self, value, annotation):
        return Write(value, annotation, self.rscClient)

    def WriteByCtx(self, value, context):
        WriteValue(context, value, self.rscClient, False)

    def WriteString(self, string):
        self.remotingWriter.WriteStringInternal(string)
