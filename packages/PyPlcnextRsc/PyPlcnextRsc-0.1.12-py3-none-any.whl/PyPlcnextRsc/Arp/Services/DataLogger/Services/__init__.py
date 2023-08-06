# Copyright (c) 2021 Phoenix Contact. All rights reserved.
# Licensed under the MIT. See LICENSE file in the project root for full license information.
from datetime import datetime

from PyPlcnextRsc.Arp.Plc.Commons import DataType
from PyPlcnextRsc.Arp.Plc.Gds.Services import VariableInfo
from PyPlcnextRsc.common.serviceDefinition.all_needed import *

__all__ = ['DataType',
           "ErrorCode",
           "RecordType",
           "RpnItemType",
           "SessionPropertyName",
           "SessionState",
           "SinkType",
           "TriggerConditionOperation",
           "SessionProperty",
           "TriggerRpnItem",
           "IDataLoggerService2"
           ]


@MarshalAs(rscType=RscType.Uint8)
class ErrorCode(RscTpIntEnum):
    """
    Possible error codes for data-logger rsc services.

    """

    NONE = 0
    """Function call succeeded."""

    NoSuchSession = 1
    """The specified session does not exist."""

    SessionRunning = 2
    """The specified session is in running state."""

    NoSuchVariable = 3
    """The specified variable does not exists."""

    AlreadyExists = 4
    """A session with the same name already exists."""

    OutOfMemory = 5
    """An attempt to allocate memory failed."""

    NotSupported = 6
    """Logging of variable not supported."""

    NoData = 7
    """No data exists for the requested time range"""

    DataUnavailable = 8
    """Expected data is unavailable for the requested time range 
    due to an unmounted volume an off-line archive or 
    similar reason for temporary unavailability."""

    InvalidConfig = 9
    """The configuration for the session contains an error"""

    Unspecified = 255
    """Unspecified error. See log file for more information."""


@MarshalAs(rscType=RscType.Uint8)
class RecordType(RscTpIntEnum):
    """
    Attribute to mark the recorded values of a triggered session

    """

    NONE = 0
    """Initialization value"""

    Continuous = 1
    """Record belongs to continously logging session."""

    PreCycle = 2
    """Values are recorded before the condition was triggered"""

    Trigger = 3
    """Records are recorded when the condition was triggered"""

    PostCycle = 4
    """Records are recorded after the condition was triggered"""


@MarshalAs(rscType=RscType.Uint8)
class RpnItemType(RscTpIntEnum):
    """
    Item type of the :py:class:`~PyPlcnextRsc.Arp.Services.DataLogger.Services.TriggerRpnItem` structure. (RPN = Reverse Polnish Notation)

    """

    NONE = 0
    """Initialization value"""

    Variable = 1
    """The Value of Item is the instance path of a variable."""

    Constant = 2
    """The Value of the Item is a constant."""

    Operation = 3
    """The value of Item is a byte containing a value of the :py:class:`~PyPlcnextRsc.Arp.Services.DataLogger.Services.TriggerConditionOperation` enumeration."""


@MarshalAs(rscType=RscType.Int32)
class SessionPropertyName(RscTpIntEnum):
    """
    All available names of properties that can be set on a session

    """

    Undefined = 0
    """Determines a newly created not yet configured property
    :py:class:`~PyPlcnextRsc.Arp.Services.DataLogger.Services.SessionProperty` with undefined name will be ignored.
    """

    SamplingInterval = 1
    """The desired sampling rate. Can either be provided as Int64 which will be interpreted as microseconds count or as string containing the actual unit, e.g. "100ms".
    :py:func:`~PyPlcnextRsc.Arp.Plc.Gds.Services.ISubscriptionService.Subscribe` for more information about the sampling rate
    """

    PublishInterval = 2
    """The rate (as Uint16 ) in which values will be written to the session´s sink. Can either be provided as Int64 which will be interpreted as microseconds count or as string containing the actual unit, 
    e.g. 100ms"""

    BufferCapacity = 3
    """Amount of capacity of the underlying ring buffer. 
    See :py:func:`~PyPlcnextRsc.Arp.Plc.Gds.Services.ISubscriptionService.CreateRecordingSubscription` for more information
    """

    SinkType = 4
    """The type of sink used by the session. Must be of type :py:class:`~PyPlcnextRsc.Arp.Services.DataLogger.Services.SinkType`"""

    SinkProperties = 5
    """Special property to configure a session sinks. Properties must be provided as string."""


@MarshalAs(rscType=RscType.Uint8)
class SessionState(RscTpIntEnum):
    """State of a data logger session"""

    NONE = 0
    """Initialization value"""

    Created = 1
    """The session was already created but not yet initialized"""

    Initialized = 2
    """The session has loaded a configuration and is ready to run"""

    Running = 3
    """The session is currently running and logging variables"""

    Stopped = 4
    """The session is currently not running."""

    Error = 5
    """The session is in an error state."""


@MarshalAs(rscType=RscType.Int32)
class SinkType(RscTpIntEnum):
    """Enumeration of possible sink types."""

    NONE = 0
    """Value not initialized."""

    Empty = 1
    """No sink assigned to session yet."""

    Database = 2
    """Sink using SQLite based database."""

    Volatile = 3
    """Sink used to store data in volatile memory, i.e. after a power reset or a deletion of the session all data is lost."""

    TSDB = 4
    """Sink used to store data in timeseries data base."""


@MarshalAs(rscType=RscType.Uint8)
class TriggerConditionOperation(RscTpIntEnum):
    """
    The TraceController provides an Interface to manage and control the LTTng Tracing on the Control

    """

    NONE = 0
    """No trigger condition, start recording immediately."""

    Equals = 1
    """Start recording if TriggerVariable1 is equal to TriggerVariable2."""

    NotEqual = 2
    """Start recording if TriggerVariable1 is greater than to TriggerVariable2."""

    GreaterThan = 3
    """Start recording if TriggerVariable1 is greater than to TriggerVariable2."""

    GreaterEqual = 4
    """Start recording if TriggerVariable1 is greater or equal to TriggerVariable2."""

    LessThan = 5
    """Start recording if TriggerVariable1 is less than TriggerVariable2."""

    LessEqual = 6
    """Start recording if TriggerVariable1 is less or equal to TriggerVariable2."""

    Modified = 7
    """Start recording when a modification of the TriggerVariable1 is detected."""

    RisingEdge = 8
    """Start recording when a positive (rising) edge of the TriggerVariable1 is detected."""

    FallingEdge = 9
    """Start recording when a negative (falling) edge of the TriggerVariable1 is detected."""

    And = 10
    """Start recording if TriggerCondition1 and TriggerCondition2 is true."""

    Or = 11
    """Start recording if TriggerCondition1 or TriggerCondition2 is true."""


class SessionProperty(RscStruct):
    """
    All available names of properties that can be set on a session

    """

    Name: SessionPropertyName
    """Name of attribute"""

    Value: RscVariant[512]
    """
    Current value of attribute
    """


class TriggerRpnItem(RscStruct):
    """
    Item of the trigger condition

    """

    Type: RpnItemType
    """Type of item (Variable, Constant or Operation)"""

    Item: RscVariant[512]
    """Data."""


@RemotingService('Arp.Services.DataLogger.Services.IDataLoggerService2')
class IDataLoggerService2:
    """
    The DataLogger provides an interface to log and store variables during firmware runtime.

    for more information:

        https://www.plcnext.help/te/Service_Components/Remote_Service_Calls_RSC/RSC_IDataLoggerService2.htm

    """

    @RemotingMethod(1)
    def ListSessionNames(self) -> RscTpTuple[RscString512]:
        """
        List all names of sessions inside the data logger component.
        :return: Array of session names.
        :rtype: Tuple[str]

        """
        pass

    @RemotingMethod(2)
    def CreateSession(self, sessionName: RscString512, persistent: bool = False) -> ErrorCode:
        """
        Tries to create a new session.

        :param sessionName: Name of session to be created.
        :type sessionName: str(max=512)
        :param persistent: If set to *true*, the newly created session will not be removed when the RSC connection is closed.
        :type persistent: bool
        :return: :py:class:`~PyPlcnextRsc.Arp.Services.DataLogger.Services.ErrorCode` for more information
        :rtype: ErrorCode

        """
        pass

    @RemotingMethod(3)
    def RemoveSession(self, sessionName: RscString512) -> ErrorCode:
        """
        Tries to remove a session.

        :param sessionName: Name of session to be removed.
        :type sessionName: str(max=512)
        :return: :py:class:`~PyPlcnextRsc.Arp.Services.DataLogger.Services.ErrorCode` for more information
        :rtype: ErrorCode

        """
        pass

    @RemotingMethod(4)
    def StartSession(self, sessionName: RscString512) -> ErrorCode:
        """
        Tries to start a logging session.

        :param sessionName: Name of session to be started.
        :type sessionName: str(max=512)
        :return: :py:class:`~PyPlcnextRsc.Arp.Services.DataLogger.Services.ErrorCode` for more information
        :rtype: ErrorCode

        """
        pass

    @RemotingMethod(5)
    def StopSession(self, sessionName: RscString512) -> ErrorCode:
        """
        Tries to stop a logging session.

        :param sessionName: Name of session to be stopped.
        :type sessionName: str(max=512)
        :return: :py:class:`~PyPlcnextRsc.Arp.Services.DataLogger.Services.ErrorCode` for more information
        :rtype: ErrorCode

        """
        pass

    @RemotingMethod(6)
    def ConfigureSession(self, sessionName: RscString512, properties: RscTpSequence[SessionProperty]) -> ErrorCode:
        """
        (Re)configures a session

        :param sessionName: Name of session to be created or reconfigured
        :type sessionName: str(max=512)
        :param properties: Collection of attributes forming the configuration for the session.
        :type properties: Sequence[SessionProperty]
        :return: :py:class:`~PyPlcnextRsc.Arp.Services.DataLogger.Services.ErrorCode` for more information
        :rtype: ErrorCode

        """
        pass

    @RemotingMethod(7)
    def GetSessionConfiguration(self, sessionName: RscString512) -> \
            RscTpTuple[
                RscTpTuple[SessionProperty],
                bool,
                ErrorCode
            ]:
        """
        Tries to query the current configuration of a session

        :param sessionName: Name of session to be queried
        :type sessionName: str(max=512)


        :return:
            **tuple with 3 return values :**

                + properties: Collection of attributes forming the sessions configuration after successfull invocation
                + isPersistent: Determines if the session will remain (<c>true</c>) when the connection to the server is closed or not
                + ErrorCode: :py:class:`~PyPlcnextRsc.Arp.Services.DataLogger.Services.ErrorCode` for more information
        :rtype: tuple[tuple[SessionProperty],bool,ErrorCode]

        """
        pass

    @RemotingMethod(8)
    def GetSessionState(self, sessionName: RscString512) -> \
            RscTpTuple[
                SessionState,
                ErrorCode
            ]:
        """
        Tries to query the state of a session.

        :param sessionName: Name of session to query state of.
        :type sessionName: str(max=512)

        :return:
            **tuple with 2 return values :**

                + state: Container for state of session, if session exists. The value after return from call is unspecified if the session does not exists.
                + ErrorCode: :py:class:`~PyPlcnextRsc.Arp.Services.DataLogger.Services.ErrorCode` for more information
        :rtype: tuple[SessionState,ErrorCode]

        """
        pass

    @RemotingMethod(9)
    def SetVariables(self, sessionName: RscString512, variableNames: RscTpSequence[RscString512]) -> RscTpTuple[ErrorCode]:
        """
        Tries to add a variable to a session.

        :param sessionName: Name of session where variable should be added.
        :type sessionName: str(max=512)
        :param variableNames: Name of session where variable should be added.
        :type variableNames: Sequence[str(max=512)]
        :return: Returns a tuple of :py:class:`~PyPlcnextRsc.Arp.Services.DataLogger.Services.ErrorCode`, in the same order as the variables were added.
        :rtype: tuple[ErrorCode]

        """
        pass

    @RemotingMethod(10)
    def GetLoggedVariables(self, sessionName: RscString512) -> \
            RscTpTuple[
                RscTpTuple[VariableInfo],
                ErrorCode
            ]:
        """
        Queries all infos about logged variables of a session.

        :param sessionName: Name of session to query logged variables
        :type sessionName: str(max=512)

        :return:
            **tuple with 2 return values :**

                + infos: tuple which list logged variables after successful call.
                + ErrorCode: :py:class:`~PyPlcnextRsc.Arp.Services.DataLogger.Services.ErrorCode` for more information
        :rtype: tuple[tuple[VariableInfo],ErrorCode]

        """
        pass

    @RemotingMethod(11)
    def ReadVariablesData(self, sessionName: RscString512, startTime: datetime, endTime: datetime, variableNames: RscTpSequence[RscString512]) -> \
            RscTpTuple[
                RscEnumerator[RscVariant],
                ErrorCode
            ]:
        """
        Read the data from the given variable from the session with the session name.

        This service function returns the plain data values from the passed variable names
        including timestamps and data series consistent flags, which is called a record.
        In a record the values are in a static order and doesn't contain any type information.
        Each record starts with the timestamp followed by the values from the given variable
        by names and the consistent flag. The record ends with a record type describing the cycle
        the record belongs to.

        Example:
            Read variables  from task A: a1, a2
                            from task B: b1

            Results in:
                    object[]
                    timestamp task A, a1, a2, b1, consistent flag, record type
                    timestamp task B, a1, a2, b1, consistent flag, record type

        The number of records depends on the given start and end time.
        Each values will be returned between the start and end time.
        If the start time is zero, all available records until the end time will be returned.

        If the end time is zero, all available records from the start time until the last available record is reached will be returned.

        If the start and end time is zero, each available record will be returned.

        If the start time is greater than the end time, the resulted values are returned in descending order.


        :param sessionName: Name of session where variable should be read from.
        :type sessionName: str(max=512)

        :param startTime: Start time to be read data.
        :type startTime: datetime

        :param endTime: End time to be read data.
        :type endTime: datetime

        :param variableNames: Name of variables to be read data.
        :type variableNames: Sequence[str(max=512)]

        :return:
            **tuple with 2 return values :**

                + values: tuple which stores the read values.
                + ErrorCode: :py:class:`~PyPlcnextRsc.Arp.Services.DataLogger.Services.ErrorCode` for more information
        :rtype: tuple[tuple[RscVariant],ErrorCode]

        """
        pass

    @RemotingMethod(12)
    def GetRotatedFileNames(self, sessionName: RscString512) -> \
            RscTpTuple[
                RscTpTuple[RscString512],
                ErrorCode
            ]:
        """
        Returns names of all files that have been written by a session

        :param sessionName: Name of session from which rotated files should be listed
        :type sessionName: str(max=512)
        :return:
            **tuple with 2 return values :**

                + filenames: list names of all rotated files on successful call.
                + ErrorCode: :py:class:`~PyPlcnextRsc.Arp.Services.DataLogger.Services.ErrorCode` for more information
        :rtype: tuple[tuple[VariableInfo],ErrorCode]

        """
        pass

    @RemotingMethod(13)
    def GetSessionNames(self, variableName: RscString512) -> RscTpTuple[RscString512]:
        """
        Tries to retrieve names of sessions which log assigned variables

        :param variableName: Name of variable to which corresponding sessions should be found
        :type variableName: str(max=512)

        :return: Tuple of names of sessions which log the variable in question
        :rtype: tuple[str(max=512)]

        """
        pass

    @RemotingMethod(14)
    def SetTriggerCondition(self, sessionName: RscString512, taskName: RscString512, preCycleCount: Uint16, postCycleCount: Uint16, triggerCondition: RscTpSequence[TriggerRpnItem]) -> ErrorCode:
        """
        Sets a trigger condition

        Configuration of the trigger is done in RPN (Reverse Polish Notation). Each operand or operation is a single :py:class:`~PyPlcnextRsc.Arp.Services.DataLogger.Services.TriggerRpnItem`. Only
        if the condition specified by the trigger is fullfilled values are logged and stored inside the sink.


        The amount of cycles that should be stored before the condition was fullfilled can be configured using *preCycleCount* whereas the amount of
        cycles that should be recorded afterwards can be configured using *postCycleCount*. If *postCycleCount* is set to 0 then the
        recording continues until IDataLoggerService::StopSession is called or the PLC project is stopped.

        :param sessionName: Name of session to set trigger condition
        :type sessionName: str(max=512)
        :param taskName: Name of task where trigger condition is evaluated
        :type taskName: str(max=512)

        :param preCycleCount: Amount of datasets recorded before the condition was triggered
        :type preCycleCount: uint16

        :param postCycleCount: Amount of dataset recorded after the condition is triggered (0 means endless)
        :type postCycleCount: uint16

        :param triggerCondition: List of trigger items. All items are evaluated in order of their position inside the list.
        :type triggerCondition: Sequence[TriggerRpnItem]

        :return: Returns a tuple of :py:class:`~PyPlcnextRsc.Arp.Services.DataLogger.Services.ErrorCode`, in the same order as the variables were added.
        :rtype: tuple[ErrorCode]

        """
        pass
