# Copyright (c) 2021 Phoenix Contact. All rights reserved.
# Licensed under the MIT. See LICENSE file in the project root for full license information.
from enum import auto

from PyPlcnextRsc.common.types import RscTpIntEnum


class RscError(RscTpIntEnum):
    @staticmethod
    def getMessage(errCode):
        if errCode in RscError._value2member_map_:
            return str(RscError._value2member_map_[errCode])
        else:
            return ""

    Null = 0,
    # masks
    CommunicationLayerMask = 0x80000000,
    RemotingLayerMask = 0x40000000,
    CommonServiceLayerMask = 0x20000000,
    ServiceLayerMask = 0x00000000,
    # communication layer
    ServerAuthenticationFailure = 0x80000001,  # If the Device (server) provides wrong authentication to the application (client) then this error code is used at the client side.
    FatalAuthorizationFailure = 0x80000002,

    ConnectionClosedRemotely = 0x80000003,
    ConnectionClosed = 0x80000004,
    InvalidSecurityToken = 0x80000005,

    # remoting layer
    InvalidProtocolVersion = 0x40000001,
    UnknownServiceHandle = 0x40000002,
    UnknownMethodHandle = 0x40000003,
    InvalidCommand = 0x40000004,
    HeaderXsumError = 0x40000005,
    UnknownProviderHandle = 0x40000006,
    ProtocolViolation = 0x40000007,
    InternalRemotingError = 0x40000008,
    ArrayLengthOutOfRange = 0x40000009,
    MaxConnectionsExceeds = 0x4000000A,
    AuthorizationFailure = 0x4000000B,
    # internally handled by runtime
    AbortRequest = 0x40001000,
    RecvTimeout = 0x40001001,
    RecvFailed = 0x40001002,
    SendTimeout = 0x40001003,
    SendFailed = 0x40001004,
    UnknownObjectFormat = 0x40001005,
    ConnRemotelyClosed = 0x40001006,
    # common service errors
    OutOfMemory = 0x20000001,
    InvalidHandle = 0x20000002,
    ParameterOutOfRange = 0x20000003,
    InvalidServiceState = 0x20000004,
    OtherMasterActive = 0x20000005,
    NoProgramOnTheDevice = 0x20000006,
    ExecutionError = 0x20000007,
    ReadOnly = 0x20000008,
    InvalidEclrState = 0x20000009,
    InternalError = 0x2000000A,
    AuthenticationFailure = 0x2000000B,  # BasicSecurityService, SecurityService
    Exception = 0x2000000C,
    IpcError = 0x2000000D,
    NotSupportedInterface = 0x2000000E,
    InvalidData = 0x2000000F,
    PrematurelyEndOfStream = 0x20000010,  # currently: client-side error code
    # SecuritySessionInfoService (TODO: move this to appropiate place)
    ServiceProviderNameTooLong = 0x521,
    ServiceNameTooLong = 0x522,
    ArgumentsNotSupported = 0x523,

    TempListServiceActive = 0x00000001
    NoTempListServiceActive = 0x00000002

    CannotReadVariableValues = 0x00000003
    CannotWriteVariableValues = 0x00000004
    CannotCreateVariableGroup = 0x00000005
    CannotAccessClrData = 0x00000006
    CannotAddToForceList = 0x00000201
    CannotReadForceList = 0x00000202
    RealTimeErrorDuringOnlineChange = 0x00000301
    PrologErrorDuringOnlineChange = 0x00000302
    OutOfMemoryDuringOnlineChange = 0x00000303
    DuplicatingForceListErrorDuringOnlineChange = 0x00000304
    TooManyPreCyclesRecorded = 0x00000401
    SubscriptionHandleNotFound = 0x00000402
    ClientNotFound = 0x00000403
    SubscriptionCouldNotBeCreated = 0x00000404
    DebugValueListError = 0x00000405
    InterfaceObjectCouldNotBeCreated = 0x00000406
    TokenListParseError = 0x00000408


class CommonException(Exception):
    ...


class InvalidOperationException(CommonException):
    ...


class NotImplementedException(CommonException): ...


class ErrType(RscTpIntEnum):
    UNSPECIFIED = auto()

    SOCKET_UNSPECIFIED = auto()
    SOCKET_TIMEOUT = auto()
    SOCKET_ABORTED = auto()
    SOCKET_WRONG_SSL_VERSION = auto()

    AUTH_LOGIN_FAILURE = auto()




class CommonRemotingException(CommonException):
    def __init__(self, message: str, cause: BaseException = None, err: ErrType = ErrType.UNSPECIFIED):

        self._message = message
        self._cause = cause
        self._errType = err
        if err != ErrType.UNSPECIFIED:
            self._message = self._message + " ("+err.name+")"
        if cause is None:
            super(CommonRemotingException, self).__init__(self._message)
        else:
            super(CommonRemotingException, self).__init__(self._message, cause)

    def getMessage(self) -> str:
        return self._message

    def getCause(self) -> BaseException:
        return self._cause

    def getErrorType(self):
        return self._errType


class CommonRemotingServiceNotFoundException(CommonRemotingException):
    ...


class CommonRemotingFatalException(CommonRemotingException):
    def __init__(self, message: str = None, cause: BaseException = None, rscError: RscError = None):
        if message:
            super(CommonRemotingFatalException, self).__init__(message, cause)
        else:
            self.rsc_error = rscError
            super(CommonRemotingFatalException, self).__init__(self.__generate_msg(), cause)

    def __generate_msg(self):
        if self.rsc_error is None:
            return ""
        else:
            return f"Non recoverable server communication failure no.{self.rsc_error.value} ({self.rsc_error})."


class CommonRemotingRecoverableException(CommonRemotingException):
    ...


class CommonRemotingClientException(CommonRemotingRecoverableException):
    ...


class _StringBuilder:
    def __init__(self):
        self.msg = ''

    def append(self, msg):
        self.msg += msg

    def get(self):
        return self.msg


class CommonRemotingServerException(CommonRemotingRecoverableException):

    def __init__(self, error_num: int, resourceName: str, parameters):
        self._err_num = error_num
        self._resource_name = resourceName
        self._parameters = parameters
        super(CommonRemotingServerException, self).__init__(self.getMessage())

    def getErrorNumber(self) -> int:
        return self._err_num

    def getResourceName(self) -> str:
        return self._resource_name

    def getCommonResourceKey(self) -> str:
        if self._resource_name is not None and len(self._resource_name) > 0:
            h = hex(self._err_num)[2:]
            while len(h) < 8:
                h = "0" + h
            return f"MSG{h}@{self._resource_name}"

    def getMessage(self):
        sb = _StringBuilder()
        if self._err_num & 0x80000000 != 0:
            sb.append(f"Communication error on communication layer {hex(self._err_num)}({RscError.getMessage(self._err_num)})")
        elif self._err_num & 0xC0000000 != 0:
            sb.append(f"Communication error on remoting layer {hex(self._err_num)}({RscError.getMessage(self._err_num)}).")
        else:
            sb.append(f"Communication error {hex(self._err_num)}({RscError.getMessage(self._err_num)}).")

        if self._parameters is not None:
            for p in self._parameters:
                sb.append("; ")
                self.__parameter_to_str(sb, p)
        return sb.get()

    def __parameter_to_str(self, sb, p):
        if p is None:
            ...
            # sb.append('null')
        else:
            from PyPlcnextRsc.common.objects import RscVariant
            if isinstance(p, RscVariant):
                p = p.GetValue()
                if p is not None:
                    if isinstance(p, (list, tuple)):
                        length = len(p)
                        sb.append('[')
                        for i in range(length):
                            self.__parameter_to_str(sb, p[i])
                            if i < length - 1:
                                sb.append(', ')
                        sb.append(']')
                    else:
                        sb.append(str(p))
                else:
                    sb.append('null')
