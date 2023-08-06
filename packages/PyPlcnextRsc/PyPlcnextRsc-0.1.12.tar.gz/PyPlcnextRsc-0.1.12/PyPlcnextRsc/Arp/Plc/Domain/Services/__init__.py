# Copyright (c) 2021 Phoenix Contact. All rights reserved.
from PyPlcnextRsc.common.serviceDefinition.all_needed import *

__all__ = [
    'PlcState',
    'PlcStartKind',
    'PlcInfoId',
    'IPlcManagerService',
    'IPlcManagerService2',
    'IPlcInfoService',
]


@MarshalAs(rscType=RscType.Uint32)
class PlcState(RscFlag):
    __STATE_MASK__ = 0x3F
    __FLAGS_MASK__ = (~__STATE_MASK__)

    NONE = 0
    """Not specified."""
    Ready = 1
    """The firmware is setup, and the PLC is ready."""
    Stop = 2
    """The PLC is loaded and setup but not started yet."""
    Running = 3
    """The PLC is started."""
    Halt = 4
    """The PLC is halted for debug purpose."""
    Warning = (1 << 6)
    """An unspecified warning occurs."""
    Error = (1 << 7)
    """An unspecified error or exception occurs, and the PLC is in state error."""
    SuspendedBySwitch = (1 << 8)
    """This error bit is set, if it could not be started because the PLC is suspended by the hardware switch (STOP-switch)."""
    FatalError = (1 << 9)
    """An unspecified fatal error or exception occurs, and the PLC is in state error."""
    SuspendedBySystemWatchdog = (1 << 10)
    """This error bit is set, if it could not be started because the PLC is suspended by the system watchdog."""
    Changing = (1 << 16)
    """The PLC is changing a configuration, this implies,  that the state <see cref="Running"/> is set."""
    Hot = (1 << 17)
    """The PLC is stopped in hot state, that is all data still remains."""
    Forcing = (1 << 18)
    """The PLC is in force mode. One or more variables are forced by the GDS."""
    Debugging = (1 << 19)
    """The PLC is in debug mode. One or more breakpoints are set."""
    Warm = (1 << 20)
    """The PLC is stopped in warm state, that is the retain data has been restored."""
    DcgNotPossible = (1 << 30)
    """This error bit is set, if the PLC tries to perform a change operation, but it is not possible.
    This bit is usually combined with the state :py:const:`~PyPlcnextRsc.Arp.Plc.Domain.Services.PlcState.Running`
    """
    DcgRealTimeViolation = (1 << 31)
    """This error bit is set, if the PLC tries to perform a change operation, but it is not possible in real time.
    # This bit is usually combined with the state :py:const:`~PyPlcnextRsc.Arp.Plc.Domain.Services.PlcState.Running`"""


@MarshalAs(rscType=RscType.Uint8)
class PlcStartKind(RscTpIntEnum):
    """PLC Start Kind"""
    NONE = 0
    """"""
    Cold = 1
    """Cold start"""
    Warm = 2
    """Warm start"""
    Hot = 3
    """Hot start"""
    RestoreWarm = 4
    """"""


@MarshalAs(rscType=RscType.Int32)
class PlcInfoId(RscTpIntEnum):
    """all identifiers of Plc informations to be read by IPlcInfoService."""
    NONE = 0
    """Not initialized."""
    ProjectName = 1
    """The name of the actual project/application."""


@RemotingService('Arp.Plc.Domain.Services.IPlcManagerService')
class IPlcManagerService:
    """Use this service to control the PLC of the controller."""

    @RemotingMethod(1)
    def Load(self, Async: bool = False):
        """
        Loads the PLC configuration and setup the PLC.

        :param Async: true, if the operation should be processed asynchronously, otherwise false
        :type Async: bool

        """
        pass

    @RemotingMethod(2)
    def Start(self, startKind: PlcStartKind, Async: bool = False):
        """
        Starts the PLC.

        +------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------+
        |StartKind                                                               |Description                                                                                                       |
        +========================================================================+==================================================================================================================+
        |:py:const:`~PyPlcnextRsc.Arp.Plc.Domain.Services.PlcStartKind.Cold`     |A cold start is processed. all data is set to initial values.                                                     |
        +------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------+
        |:py:const:`~PyPlcnextRsc.Arp.Plc.Domain.Services.PlcStartKind.Warm`     |A warm start is processed. all data is set to initial values but retained data is set to the retained values.     |
        +------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------+
        |:py:const:`~PyPlcnextRsc.Arp.Plc.Domain.Services.PlcStartKind.Hot`      |The PLC is just continued without setting or resetting any data.                                                  |
        +------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------+

        :param startKind: Determines how the PLC should be started.
        :type startKind: PlcStartKind
        :param Async: true, if the operation should be processed asynchronously, otherwise false
        :type Async: bool

        """
        pass

    @RemotingMethod(3)
    def Stop(self, Async: bool = False):
        """
        Stops the PLC.

        :param Async: true, if the operation should be processed asynchronously, otherwise false
        :type Async: bool

        """
        pass

    @RemotingMethod(4)
    def Reset(self, Async: bool = False):
        """
        Resets the PLC and unloads its configuration.

        :param Async: true, if the operation should be processed asynchronously, otherwise false
        :type Async: bool

        """
        pass

    @RemotingMethod(5)
    def GetPlcState(self) -> PlcState:
        """
        Gets the actual PLC state.

        :return: The current PLC state. If the PLC has a warning, the :py:const:`~PyPlcnextRsc.Arp.Plc.Domain.Services.PlcState.Warning` Bit is set.
            If the PLC has an actual error, the :py:const:`~PyPlcnextRsc.Arp.Plc.Domain.Services.PlcState.Error` Bit is set.
        :rtype: PlcState

        """
        pass


@RemotingService('Arp.Plc.Domain.Services.IPlcManagerService2')
class IPlcManagerService2:
    """
    The DownloadChange extension of the :py:class:`~PyPlcnextRsc.Arp.Plc.Domain.Services.IPlcManagerService`.
    """

    @RemotingMethod(1)
    def Change(self, Async: bool = False):
        """
        This operation will perform the change of the PLC configuration, which was downloaded before.

        :param Async: true, if the operation should be processed asynchronously, otherwise false.
        :type Async: bool

        """
        pass

    @RemotingMethod(2)
    def Restart(self, startKind: PlcStartKind, Async: bool = False):
        """
        Restarts the Plc, that is, it's stopped and started in a single operation.

        :param startKind:	The start kind :py:const:`~PyPlcnextRsc.Arp.Plc.Domain.Services.PlcStartKind.Cold`,
            PlcStartKind. :py:const:`~PyPlcnextRsc.Arp.Plc.Domain.Services.PlcStartKind.Warm` or :py:const:`~PyPlcnextRsc.Arp.Plc.Domain.Services.PlcStartKind.Hot`
        :type startKind: PlcStartKind
        :param Async: true, if the operation should be processed asynchronously, otherwise false.
        :type Async: bool

        """
        pass


@RemotingService('Arp.Plc.Domain.Services.IPlcInfoService')
class IPlcInfoService:
    """Provides informations about the Plc (realtime) project."""

    @RemotingMethod(1)
    def GetInfo(self, identifier: PlcInfoId) -> RscVariant:
        """
        Gets the specified info from the Plc project.

        :param identifier: The identifier of the info to Read.
        :type identifier: PlcInfoId
        :return: The requested info or null if the identifier is unknown.
        :rtype: RscVariant

        """
        pass

    @RemotingMethod(2)
    def GetInfos(self, identifiers: RscTpSequence[PlcInfoId]) -> RscTpTuple[RscVariant]:
        """
        Gets the specified infos from the Plc project.

        :param identifiers: The identifiers of the infos to Read.
        :type identifiers: Sequence[PlcInfoId]
        :return: The requested infos as tuple. If an identifiers is unknown, the according array element is null.
        :rtype: tuple[RscVariant]

        """
        pass
