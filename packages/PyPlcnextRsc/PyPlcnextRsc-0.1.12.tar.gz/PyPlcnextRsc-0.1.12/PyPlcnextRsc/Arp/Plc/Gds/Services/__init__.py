# Copyright (c) 2021 Phoenix Contact. All rights reserved.
# Licensed under the MIT. See LICENSE file in the project root for full license information.

from PyPlcnextRsc.Arp.Plc.Commons import DataType
from PyPlcnextRsc.common.serviceDefinition.all_needed import *

"""
Arp::Plc::Gds::Services
Namespace for Services of the Global Data Space (GDS)
"""

__all__ = [
    "DataType",  # Forward
    "DataAccessError",
    "ReadItem",
    "WriteItem",
    "SubscriptionKind",
    "VariableInfo",
    "ForceItem",
    "IDataAccessService",
    "ISubscriptionService",
    "IForceService",
]


@MarshalAs(rscType=RscType.Uint8)
class DataAccessError(RscTpIntEnum):
    """
    This enumeration contains the possible data access errors.

    """

    NONE = 0
    """No error."""
    NotExists = 1
    """The variable does not exist."""
    NotAuthorized = 2
    """The user is not authorized."""
    TypeMismatch = 3
    """During a Write operation the type of the value is not suitable for the particular variable.
    The :py:class:`~PyPlcnextRsc.Arp.Plc.Gds.Services.IDataAccessService` does not convert types. 
    The type of each value which is to be written needs to be suitable for the particular variable."""
    PortNameSyntaxError = 4
    """The name of the variable as given during a Write or Read operation is syntactically not correct.
    For example the variable name contains an index range."""
    PortNameSemanticError = 5
    """The semantic of the name of the variable as given during a Write or Read operation is semantically not correct.
    For example the variable name contains an index range with a start index not lower than the end index."""
    IndexOutOfRange = 6
    """The variable name contains an index which is out of range."""
    NotImplemented = 7
    """The variable type is not implemented yet. """
    NotSupported = 8
    """The variable type is not supported.   """
    CurrentlyUnavailable = 9
    """The requested service is currently not available. """
    UnvalidSubscription = 10
    """Invalid subscription. """
    NoData = 11
    """NoData available."""
    InvalidConfig = 12
    """The configuration for the subscription contains an error."""
    Unspecified = 255
    """Unspecified error. See log file for more information."""


class ReadItem(RscStruct):
    """
    Stores the data to be Read, written by the controller and a possible data access error.

    """

    Error: DataAccessError
    """Contains the possible data access errors."""

    Value: RscVariant[512]
    """Contains the data to be Read, written by the controller."""


class WriteItem(RscStruct):
    """
    Stores the to be written data and the related variable name to be Write to.

    """

    PortName: RscString512
    """Name of the variable."""

    Value: RscVariant[512]
    """Contains the to be written data."""


@MarshalAs(rscType=RscType.Int32)
class SubscriptionKind(RscTpIntEnum):
    """
    This enumeration contains the possible kinds of subscriptions.

    """

    NONE = 0
    """"""
    HighPerformance = 1
    """The subscription operates with a task-triggered DoubleBuffer, which holds the last written port data."""

    RealTime = 2
    """The subscription operates with a task-triggered QuadBuffer, which holds the last written port data."""

    Recording = 3
    """The subscription operates with a task-triggered RingBuffer, which holds the last N numbers of written data."""

    ClosedRealTime = 4
    """The subscription operates with a task-triggered RingBuffer, which holds the last N numbers of written data."""

    DirectRead = 5
    """The subscription operates with a self-triggered DoubleBuffer, which holds the last written port data."""


class VariableInfo(RscStruct):
    """
    Describes a subscribed variable.

    """

    Name: RscString512
    """Full name of the variable."""
    Type: DataType
    """DataType 0f the variable"""


class ForceItem(RscStruct):
    """
    A force item structure.

    """

    VariableName: RscString512
    """The instance path of the forced item."""
    ForceValue: RscVariant[512]
    """The value of the forced item."""


@RemotingService('Arp.Plc.Gds.Services.IDataAccessService')
class IDataAccessService:
    """
    Services for the direct data access.
    The direct access functionality is a way for reading and writing values from and to variables.
    This is the fastest way, with a minimum of influence to the real time process, but it is not guaranteed that the data will be Read/Write in the same task cycle.
    For task consistent reading the subscription service :py:class:`~PyPlcnextRsc.Arp.Plc.Gds.Services.ISubscriptionService` has to be used.
    A client can Read/Write from/to different types of variables provided in :py:class:`PyPlcnextRsc.Arp.Plc.Commons.DataType`. Currently supported types are listed below:

    +--------------------------------------------------------------------+----------+------------------------------------------------------------------------------------------------------------------------------------------------+
    |Type                                                                |Supported |Description                                                                                                                                     |
    +====================================================================+==========+================================================================================================================================================+
    |:py:const:`PyPlcnextRsc.Arp.Plc.Commons.DataType.Primitive`         |YES       |.                                                                                                                                               |
    +--------------------------------------------------------------------+----------+------------------------------------------------------------------------------------------------------------------------------------------------+
    |:py:const:`PyPlcnextRsc.Arp.Plc.Commons.DataType.DateTime`          |YES       |.                                                                                                                                               |
    +--------------------------------------------------------------------+----------+------------------------------------------------------------------------------------------------------------------------------------------------+
    |:py:const:`PyPlcnextRsc.Arp.Plc.Commons.DataType.String`            |(YES)     |Please use :py:const:`~PyPlcnextRsc.Arp.Plc.Commons.DataType.StaticString` or  :py:const:`~PyPlcnextRsc.Arp.Plc.Commons.DataType.IecString`     |
    +--------------------------------------------------------------------+----------+------------------------------------------------------------------------------------------------------------------------------------------------+
    |:py:const:`PyPlcnextRsc.Arp.Plc.Commons.DataType.Enum`              |YES       |                                                                                                                                                |
    +--------------------------------------------------------------------+----------+------------------------------------------------------------------------------------------------------------------------------------------------+
    |:py:const:`PyPlcnextRsc.Arp.Plc.Commons.DataType.Struct`            |YES       |                                                                                                                                                |
    +--------------------------------------------------------------------+----------+------------------------------------------------------------------------------------------------------------------------------------------------+
    |:py:const:`PyPlcnextRsc.Arp.Plc.Commons.DataType.FunctionBlock`     |YES       |                                                                                                                                                |
    +--------------------------------------------------------------------+----------+------------------------------------------------------------------------------------------------------------------------------------------------+
    |:py:const:`PyPlcnextRsc.Arp.Plc.Commons.DataType.Pointer`           |YES       |                                                                                                                                                |
    +--------------------------------------------------------------------+----------+------------------------------------------------------------------------------------------------------------------------------------------------+
    |:py:const:`PyPlcnextRsc.Arp.Plc.Commons.DataType.Array`             |YES       |                                                                                                                                                |
    +--------------------------------------------------------------------+----------+------------------------------------------------------------------------------------------------------------------------------------------------+

    To address a variable, the full variable name uri is necessary. Some valid examples are given below:

        + ComponentName-1/ProgramName-1.Variable_Name
        + ComponentName-1/Global_Variable_Name
        + ComponentName-1/ProgramName-1.Array_Variable_Name
        + ComponentName-1/ProgramName-1.Array_Variable_Name[index]
        + ComponentName-1/ProgramName-1.Array_Variable_Name[startIndex:endIndex]
        + ComponentName-1/ProgramName-1.Struct_Variable_Name.Element1.Leaf
        + ComponentName-1/ProgramName-1.Struct_Variable_Name.Element1.LeafArray
        + ComponentName-1/ProgramName-1.Struct_Variable_Name.Element1.LeafArray[index]

    """

    @RemotingMethod(1)
    def ReadSingle(self, portName: RscString512) -> ReadItem:
        """
        Reads the value of the variable directly from the given variable name.

        Copies the value of the variable, given by the variable name, to the
        :py:class:`~PyPlcnextRsc.Arp.Plc.Gds.Services.ReadItem` object, which will be returned.
        ReadSingle can only Read one single variable, so if you want to Read multiple variables simultaneously, an array or a range of an array,
        you have to use the :py:func:`~PyPlcnextRsc.Arp.Plc.Gds.Services.IDataAccessService.Read` service instead.
        Be aware, this copy process isn't task consistent and the data could be corrupted.

        :param portName: Full variable name uri.
        :type portName: str(max=512)
        :return: see :py:class:`~PyPlcnextRsc.Arp.Plc.Gds.Services.ReadItem`
        :rtype: ReadItem

        """
        pass

    @RemotingMethod(2)
    def Read(self, portNames: RscTpSequence[RscString512]) -> RscTpTuple[ReadItem]:
        """
        Reads the variable values directly from the given variable names.
        Copies the values of the variables, given by the variable names, to a vector of
        :py:class:`~PyPlcnextRsc.Arp.Plc.Gds.Services.ReadItem` objects, which will be returned.
        Be aware, this copy process isn't task consistent and the data could be corrupted.

        :param portNames: An array of full variable name uris.
        :type portNames: Sequence[str(max=512)]
        :return: Returns a tuple of :py:class:`~PyPlcnextRsc.Arp.Plc.Gds.Services.ReadItem`, in the same order as the variables were added.
        :rtype: tuple[ReadItem]

        """
        pass

    @RemotingMethod(3)
    def WriteSingle(self, data: WriteItem) -> DataAccessError:
        """
        Writes the given value to the given variable name containing in the given Arp.Plc.Gds.Services.WriteItem.

        Writes the given value to the given variable containing in the given :py:class:`~PyPlcnextRsc.Arp.Plc.Gds.Services.WriteItem` object.
        WriteSingle can only Write one single value, so if you want to Write to multiple variables simultaneously, to an array or to a range of an array,
        you have to use the :py:func:`~PyPlcnextRsc.Arp.Plc.Gds.Services.IDataAccessService.Write` service instead.
        Be aware, this Write process isn't task consistent and the data could be corrupted.

        :param data: Variable data which contains the variable name and the value to be written.
        :type data: WriteItem
        :return: Returns :py:const:`PyPlcnextRsc.Arp.Plc.Gds.Services.DataAccessError.NONE` on success.
        :rtype: DataAccessError

        """
        pass

    @RemotingMethod(4)
    def Write(self, writeData: RscTpSequence[WriteItem]) -> RscTpTuple[DataAccessError]:
        """
        Writes the given values to the given variables containing in the given :py:class:`~PyPlcnextRsc.Arp.Plc.Gds.Services.WriteItem` objects.

        Writes the given values to the given variables containing in the given :py:class:`~PyPlcnextRsc.Arp.Plc.Gds.Services.WriteItem` objects.
        Be aware, this Write process isn't task consistent and the data could be corrupted.

        :param writeData: Array of :py:class:`~PyPlcnextRsc.Arp.Plc.Gds.Services.WriteItem`, which contains the variable name and the value to be written.
        :type writeData: Sequence[WriteItem]
        :return: Returns a vector of :py:class:`~PyPlcnextRsc.Arp.Plc.Gds.Services.DataAccessError`, :py:const:`PyPlcnextRsc.Arp.Plc.Gds.Services.DataAccessError.NONE` on success,
            in the same order as the variables were added.
        :rtype: tuple[DataAccessError]

        """


@RemotingService('Arp.Plc.Gds.Services.ISubscriptionService')
class ISubscriptionService:
    """Services for the subscription.

    The subscription functionality is a more elegant way reading values from variables, in contrast to permanently reading (polling).
    A client can subscribe a selection of variables of interest and the subscription will copy the data values to a internalEnums buffer.
    This is the recommended mechanism to “Read” variable values from th PLC system.
    All Read data are always task consistent, because the data is written by the task itself.
    The data updating rate depends of the task to which the variable belongs.
    Because global variables haven't a task affiliation, each global variable will be updated by default from the task 'Globals'.
    This task has a default cycling time of 50ms which is configurable via the ESM configuration.
    For more information to the update rate see Arp.Plc.Gds.Services.ISubscriptionService.Subscribe.
    Initially, the internalEnums buffers are initialized with null values (:py:const:`PyPlcnextRsc.Arp.Plc.Commons.DataType.Void`).
    This is important to know, especially if values are Read immediately after the subscription is created.
    More precisely if the data are Read before the tasks have written the data.
    Additionally a subscription is able to generate timestamps which will be generated at the end of the variable source task.
    :py:func:`~PyPlcnextRsc.Arp.Plc.Gds.Services.ISubscriptionService.ReadTimeStampedValues`
    A client can subscribe to different types of variables provided in :py:class:`~PyPlcnextRsc.Arp.Plc.Commons.DataType`. Currently supported variable types are listed below:

    +--------------------------------------------------------------------+----------+------------------------------------------------------------------------------------------------------------------------------------------------+
    |Type                                                                |Supported |Description                                                                                                                                     |
    +====================================================================+==========+================================================================================================================================================+
    |:py:const:`PyPlcnextRsc.Arp.Plc.Commons.DataType.Primitive`         |YES       |.                                                                                                                                               |
    +--------------------------------------------------------------------+----------+------------------------------------------------------------------------------------------------------------------------------------------------+
    |:py:const:`PyPlcnextRsc.Arp.Plc.Commons.DataType.DateTime`          |YES       |.                                                                                                                                               |
    +--------------------------------------------------------------------+----------+------------------------------------------------------------------------------------------------------------------------------------------------+
    |:py:const:`PyPlcnextRsc.Arp.Plc.Commons.DataType.String`            |(YES)     |Please use :py:const:`~PyPlcnextRsc.Arp.Plc.Commons.DataType.StaticString` or  :py:const:`~PyPlcnextRsc.Arp.Plc.Commons.DataType.IecString`     |
    +--------------------------------------------------------------------+----------+------------------------------------------------------------------------------------------------------------------------------------------------+
    |:py:const:`PyPlcnextRsc.Arp.Plc.Commons.DataType.Enum`              |YES       |                                                                                                                                                |
    +--------------------------------------------------------------------+----------+------------------------------------------------------------------------------------------------------------------------------------------------+
    |:py:const:`PyPlcnextRsc.Arp.Plc.Commons.DataType.Struct`            |YES       |                                                                                                                                                |
    +--------------------------------------------------------------------+----------+------------------------------------------------------------------------------------------------------------------------------------------------+
    |:py:const:`PyPlcnextRsc.Arp.Plc.Commons.DataType.FunctionBlock`     |YES       |                                                                                                                                                |
    +--------------------------------------------------------------------+----------+------------------------------------------------------------------------------------------------------------------------------------------------+
    |:py:const:`PyPlcnextRsc.Arp.Plc.Commons.DataType.Pointer`           |YES       |                                                                                                                                                |
    +--------------------------------------------------------------------+----------+------------------------------------------------------------------------------------------------------------------------------------------------+
    |:py:const:`PyPlcnextRsc.Arp.Plc.Commons.DataType.Array`             |YES       |                                                                                                                                                |
    +--------------------------------------------------------------------+----------+------------------------------------------------------------------------------------------------------------------------------------------------+

    To address a variable, the full variable name (uri) is necessary. Some valid examples are given below:

        + ComponentName-1/ProgramName-1.Variable_Name
        + ComponentName-1/Global_Variable_Name
        + ComponentName-1/ProgramName-1.Array_Variable_Name[index]
        + ComponentName-1/ProgramName-1.Array_Variable_Name[startIndex:endIndex]
        + ComponentName-1/ProgramName-1.Struct_Variable_Name.Element1.Leaf
        + ComponentName-1/ProgramName-1.Struct_Variable_Name.Element1.LeafArray[index]
        + ComponentName-1/ProgramName-1.Struct_Variable_Name.Element1.LeafArrayOfArray[indexX][indexY]

    A Subscription can created in the PLC process, in other processes and also on remote targets.
    All subscriptions will be removed after a :py:const:`~PyPlcnextRsc.Arp.Plc.Domain.Services.PlcStartKind.Cold`,
    :py:const:`~PyPlcnextRsc.Arp.Plc.Domain.Services.PlcStartKind.Warm` and after a download change.
    While a download change is in process the subscription service will be disabled and each function will be return
    the error code :py:const:`PyPlcnextRsc.Arp.Plc.Gds.Services.DataAccessError.CurrentlyUnavailable`.

    """
    pass

    @RemotingMethod(1)
    def CreateSubscription(self, kind: SubscriptionKind) -> Uint32:
        """
        Creates a subscription of the given :py:class:`~PyPlcnextRsc.Arp.Plc.Gds.Services.SubscriptionKind`.

        This method allows other components, also from remote targets, to create a subscription which is able to subscribe each PLC variable.
        On success it returns a unique SubscriptionId which is created internally.
        The SubscriptionId has to be exposed to the SDK user, due to the usage on remote targets.
        The SubscriptionId is the reference to a created subscription at the PLC target and is needed in each
        subscription method exclude this and
        :py:func:`~Arp.Plc.Gds.Services.ISubscriptionService.CreateRecordingSubscription`.
        Each subscription contains at least one buffer which kind depends on the :py:class:`~PyPlcnextRsc.Arp.Plc.Gds.Services.SubscriptionKind`.
        The number of buffer depends on the different tasks which contains the added variables.
        The buffer are initialized with a :py:class:`~PyPlcnextRsc.Arp.Plc.Commons.DataType` specific initial value e.g.: int8 = 0 or boolean = false.
        Apart from :py:const:`~PyPlcnextRsc.Arp.Plc.Gds.Services.SubscriptionKind.DirectRead`, the buffer will filled by the task.
        How often the task stores the data to the buffer depends on the task cycle time and the configured subscription sample interval.

        The :py:class:`~PyPlcnextRsc.Arp.Plc.Gds.Services.SubscriptionKind` decides which kind of a subscription will be created.
        Each kind has its own benefits and differs in consistence, performance and memory usage. The available kinds are listed below:

            SubscriptionKind.DirectRead:
                The subscription itself triggers the copy process and will Read the data directly from the source.
                This could be the fastest way and with no influence to the real time,
                to get the current data, but the task consistency is not guaranteed.

                Usage example: Asynchronous data collection for non critical data.

            SubscriptionKind.HighPerformance:
                This subscription uses a DoubleBuffer which contains the last written data from the added variables.
                This kind is task consistent, has low influence to the real time and is low in memory usage.

                Usage example: Standard way to collect the variable data.

            SubscriptionKind.RealTime:
                This subscription uses a QuadBuffer which contains the last written data from the added variables.
                This kind is task consistent, has the fastest access to the current written data, but uses the fourfold memory.

                Usage example: For variables which are running in high speed tasks and for which it is necessary to guarantee the fastest access to the current written data.

                .. note::

                    In most cases the :py:const:`~PyPlcnextRsc.Arp.Plc.Gds.Services.SubscriptionKind.HighPerformance` is sufficient.

            SubscriptionKind.Recording:
                This subscription uses a RingBuffer which is able to store more than one record of data.
                This kind is task consistent, has low influence to the real time, but needs, dependent to the ring capacity, a lot of memory.
                By default the ring capacity is 10, use
                :py:func:`~PyPlcnextRsc.Arp.Plc.Gds.Services.ISubscriptionService.CreateRecordingSubscription` to create a subscription witch a self defined size.

                Usage example: For variables which are running in faster tasks than the consumer does and for which it is necessary to guarantee that
                every data record will be stored, without a single gap.

                .. note::

                    This kind uses a lot of memory!



        After the subscription is created successfully, variables could be added with
        :py:func:`~PyPlcnextRsc.Arp.Plc.Gds.Services.ISubscriptionService.AddVariable` or
        :py:func:`~PyPlcnextRsc.Arp.Plc.Gds.Services.ISubscriptionService.AddVariables` with the SubscriptionId just returned in this method.

        :param kind: The kind of the subscription.
        :type kind: SubscriptionKind
        :return: The unique subscription id on success, otherwise 0.
        :rtype: int(Uint32)

        """
        pass

    @RemotingMethod(2)
    def CreateRecordingSubscription(self, recordCount: Uint16) -> Uint32:
        """
        Creates a subscription of :py:const:`~PyPlcnextRsc.Arp.Plc.Gds.Services.SubscriptionKind.Recording`.

        This method creates a subscription of the kind :py:const:`~PyPlcnextRsc.Arp.Plc.Gds.Services.SubscriptionKind.Recording`.
        Compared to the method :py:func:`~PyPlcnextRsc.Arp.Plc.Gds.Services.ISubscriptionService.CreateSubscription`,
        it allows to configure the capacity of the internalEnums used ring buffer.
        For further information see :py:func:`~PyPlcnextRsc.Arp.Plc.Gds.Services.ISubscriptionService.CreateSubscription`.

        :param recordCount: The maximum number of storable records.
        :type recordCount: int(Uint16)
        :return: The unique subscription id on success, otherwise 0.
        :rtype: int(Uint32)

        """
        pass

    @RemotingMethod(3)
    def AddVariable(self, subscriptionId: Uint32, variableName: RscString512) -> DataAccessError:
        """
        Extends the subscription with the given id by inserting the given variable name

        The added variable is stored in a internalEnums container and will be subscribed after calling
        :py:func:`~PyPlcnextRsc.Arp.Plc.Gds.Services.ISubscriptionService.Subscribe`.
        If the subscription has already been subscribed, it is necessary to call
        :py:func:`~PyPlcnextRsc.Arp.Plc.Gds.Services.ISubscriptionService.Resubscribe` to subscribe the new added variable finally.
        If the same full variable name is added multiple times, the old variable will be overridden.
        In case, a variable name is invalid or doesn't exists a specific error code will be returned :py:class:`~Arp.Plc.Gds.Services.DataAccessError`,
        on success the code :py:const:`~PyPlcnextRsc.Arp.Plc.Gds.Services.DataAccessError.NONE` of the added variable will be returned.
        A variable which doesn't returned with :py:const:`PyPlcnextRsc.Arp.Plc.Gds.Services.DataAccessError.NONE` won't be added to the subscription and won't be subscribed.

        A single array element can added with its index in brackets e.g.:

            + ComponentName-1/ProgramName-1.Array_Name[index]

        Or a rage of an array can added with tow indexes separated with a colon in brackets e.g.:

            + ComponentName-1/ProgramName-1.Array_Name[StartIndex:EndIndex]

        If an array variable is added without a variable specification, the entire array will be added to the subscription.
        An alternative way to insert variables to the subscription is by using the function
        :py:func:`~PyPlcnextRsc.Arp.Plc.Gds.Services.ISubscriptionService.AddVariables`.

        :param subscriptionId: The id of the subscription where the variable is add to.
        :type subscriptionId: int(Uint32)
        :param variableName: The full name of the variable.
        :type variableName: str(max=512)
        :return: Returns :py:const:`~PyPlcnextRsc.Arp.Plc.Gds.Services.DataAccessError.NONE` on success.
        :rtype: DataAccessError

        """
        pass

    @RemotingMethod(4)
    def AddVariables(self, subscriptionId: Uint32, variableNames: RscTpSequence[RscString512]) -> RscTpTuple[DataAccessError]:
        """
        Extends the subscription with the given id by inserting a range of new variables.

        Allows to add a range of variables to the subscription.
        The returned array of type :py:class:`~PyPlcnextRsc.Arp.Plc.Gds.Services.DataAccessError`,
        is in the same order as the given array of variable names and indicates if the given variables are valid and exist.
        For further information see :py:func:`~PyPlcnextRsc.Arp.Plc.Gds.Services.ISubscriptionService.AddVariable`.

        :param subscriptionId: The id of the subscription where the variable is add to.
        :type subscriptionId: int(Uint32)
        :param variableNames: An array of full variable names.
        :type variableNames: Sequence[str(max=512)]
        :return: Returns a tuple of :py:class:`~PyPlcnextRsc.Arp.Plc.Gds.Services.DataAccessError`, :py:const:`~PyPlcnextRsc.Arp.Plc.Gds.Services.DataAccessError.NONE` on success,
            in the same order as the variables were added.
        :rtype: tuple[DataAccessError]

        """

    @RemotingMethod(5)
    def RemoveVariable(self, subscriptionId: Uint32, variableName: RscString512) -> DataAccessError:
        """
        Removes the variable with the specific variable name from the subscription.

        Removes the variable that compare equal to the given variable name, from the internalEnums variable list.
        If the subscription has already been subscribed, it is necessary to call
        :py:func:`~PyPlcnextRsc.Arp.Plc.Gds.Services.ISubscriptionService.Resubscribe`
        to remove the given variable from the internalEnums created buffer.

        :param subscriptionId: The id of the subscription.
        :type subscriptionId: int(Uint32)
        :param variableName: The full name of the variable to be removed from the subscription.
        :type variableName: str(max=512)
        :return: Returns :py:const:`~PyPlcnextRsc.Arp.Plc.Gds.Services.DataAccessError.NONE` on success.
        :rtype: DataAccessError

        """
        pass

    @RemotingMethod(6)
    def Subscribe(self, subscriptionId: Uint32, sampleRate: Uint64) -> DataAccessError:
        """
        Subscribes the subscription with the given id.

        All previously added variables including in the given subscription will be subscribed.
        Internally the variables are separated in the respective tasks, a buffer for each task will be created
        and connected to the task executed event.
        At this point the task will copy the selected variable data into the task buffer
        (excluded subscriptions from kind :py:const:~`PlcnextRsc.Arp.Plc.Gds.Services.SubscriptionKind.DirectRead`).
        How often the task stores the data to the buffer depends on the task cycle time and the configured subscription sample rate.

        Calling this method on a already subscribed subscription has no effect, even if new variables have been added or removed.
        To make variable modification effective, use :py:func:`~PyPlcnextRsc.Arp.Plc.Gds.Services.ISubscriptionService.Resubscribe`.
        Calling this method while the subscription is in the state Unsubscribed, because
        :py:func:`~PyPlcnextRsc.Arp.Plc.Gds.Services.ISubscriptionService.Unsubscribe` has been called,
        will only connect the already constructed buffer to the respective tasks and will set the given sampleRate.
        Compare to the first and initial call of this method, this call cost more less time because the buffer are already created.
        This also means that variable modification which have been done after the first call of
        :py:func:`~PyPlcnextRsc.Arp.Plc.Gds.Services.ISubscriptionService.Subscribe`, have also no effect. At this point it is also necessary to call
        :py:func:`~PyPlcnextRsc.Arp.Plc.Gds.Services.ISubscriptionService.Resubscribe`.

        A subscribed subscription can operates in different sample rates (excluded subscriptions from kind :py:const:`~PyPlcnextRsc.Arp.Plc.Gds.Services.SubscriptionKind.DirectRead`)
        which depends on several factors. First, each variable belongs to a program which runs in a task and this task has a cycle rate which determines the sample rate.
        This means that at the end of each task cycle, all variable data, subscribed and related to this task, will be written to the corresponding buffer.
        Note that all global variables are assigned to the task 'Globals'. Thats the case if the given sample rate is set to zero,
        which means the subscription operates in 'real-time', the same sample rate the task is operating in. This is also the fastest possible rate for a subscription.
        Note that it's possible that one subscription could contain variables from different tasks, which has the consequence that the subscription operates in different rates!
        If the given sample rate desire to a specific rate, the subscription tries to operate in this rate, for each variable, no matter from which task this variable comes.
        Potential self defined sample rates for a subscription are the task cycle rate or a multiple of them, otherwise the given rate will rounded down. E.g.:
        ::

            Task A cycle rate = 10ms
            Task B cycle rate = 8ms
            Subscription given rate = 50ms
            Subscription rate for task A = 50ms
            Subscription rate for task B = 48ms

        Special handling for global Varibales: If there isn't a given sample rate by the user (value is zero),
        the global variables will be recored by default from the 'Globals' task (50ms, configured in the ESM.config).
        But if there is a given sample rate (value is greater than zero) the global variables will be connected a task
        which fits the given sample rate.
        If no task exists with the given sample rate, the fastest available task will be picked and used for downsampling (see above).
        So it is possible to record data of global variables in the fastest availble interval or an multiple of them.

        :param subscriptionId: The id of the subscription.
        :type subscriptionId: int(Uint32)
        :param sampleRate: The desired sample rate in microseconds.
        :type sampleRate: int(Uint64)
        :return: Returns :py:const:`~PyPlcnextRsc.Arp.Plc.Gds.Services.DataAccessError.NONE` on success
        :rtype: DataAccessError

        """
        pass

    @RemotingMethod(7)
    def Resubscribe(self, subscriptionId: Uint32, sampleRate: Uint64) -> DataAccessError:
        """
        Resubscribes the subscription with the given id.

        Resubscribes the subscription, which will trigger a completely rebuild process of the whole subscription,
        including previously done variable modification which have been done after the first call of
        :py:func:`~PyPlcnextRsc.Arp.Plc.Gds.Services.ISubscriptionService.Subscribe`.
        It destroys the internalEnums buffer and subscribes the subscription again
        (for further information see :py:func:`~PyPlcnextRsc.Arp.Plc.Gds.Services.ISubscriptionService.Subscribe`).
        Note that the subscription is not able to collect data from the variables, while the resubscribe process is in progress.
        This method has only an effect if the given subscription is currently subscribed, otherwise nothing will happen.

        :param subscriptionId: The id of the subscription.
        :type subscriptionId: int(Uint32)
        :param sampleRate:	The desired sample rate in microseconds.
        :type sampleRate: int(Uint64)
        :return: Returns :py:const:`~PyPlcnextRsc.Arp.Plc.Gds.Services.DataAccessError.NONE` on success
        :rtype: DataAccessError

        """
        pass

    @RemotingMethod(8)
    def Unsubscribe(self, subscriptionId: Uint32) -> DataAccessError:
        """
        Unsubscribes the subscription with the given id.

        Unsubscribes the subscription from all task executed events. The subscription data are still exist and
        could be get by the respective Read-methods.
        To subscribe the subscription again, call :py:func:`~PyPlcnextRsc.Arp.Plc.Gds.Services.ISubscriptionService.Subscribe`.
        This method has only an effect if the given subscription is currently subscribed, otherwise nothing will happen.

        :param subscriptionId: The id of the subscription.
        :type subscriptionId: int(Uint32)
        :return: Returns :py:const:`~PyPlcnextRsc.Arp.Plc.Gds.Services.DataAccessError.NONE` on success

        :rtype: DataAccessError

        """
        pass

    @RemotingMethod(9)
    def DeleteSubscription(self, subscriptionId: Uint32) -> DataAccessError:
        """
        Deletes the subscription.

        Deletes the subscription with the given id.
        After that the id is no longer valid and all data, containing in the subscription will be removed.

        :param subscriptionId: The id of the subscription.
        :type subscriptionId: int(Uint32)
        :return: Returns :py:const:`~PyPlcnextRsc.Arp.Plc.Gds.Services.DataAccessError.NONE` on success
        :rtype: DataAccessError

        """
        pass

    @RemotingMethod(10)
    def GetVariableInfos(self, subscriptionId: Uint32) -> \
            RscTpTuple[
                RscTpTuple[VariableInfo],
                DataAccessError
            ]:
        """
        Get the subscribed variable information of the subscription.

        The subscription service provides several Read functions
        ::

            Arp.Plc.Gds.Services.ISubscriptionService.ReadValues,
            Arp.Plc.Gds.Services.ISubscriptionService.ReadTimeStampedValues
            Arp.Plc.Gds.Services.ISubscriptionService.ReadRecords

        which will return the plain values without any information of type and order.
        To assign this plain values to the added variables, this function returns the currently
        subscribed variable information in a array of
        :py:class:`~PyPlcnextRsc.Arp.Plc.Gds.Services.VariableInfo` in the same order as the Read functions will do.
        This order and type information wont change, till
        :py:func:`~PyPlcnextRsc.Arp.Plc.Gds.Services.ISubscriptionService.Resubscribe` was called.

        .. note::

            This order does not have to be the same order like the variables has been added to the subscription.

        This service function relates to the Read function :py:func:`~PyPlcnextRsc.Arp.Plc.Gds.Services.ISubscriptionService.ReadValues`.
        The provided information contains only information of the added and currently subscribed variables.
        It doesn't contain information of timestamps.
        Timestamps could be Read by the function :py:func:`~PyPlcnextRsc.Arp.Plc.Gds.Services.ISubscriptionService.ReadTimeStampedValues` and its
        related information with :py:func:`~PyPlcnextRsc.Arp.Plc.Gds.Services.ISubscriptionService.GetTimeStampedVariableInfos`.
        ::

            Example:

                Added Variable from task A: a1, a2
                Added Variable from task B: b1
                Results in:
                VariableInfo[]
                a1
                a2
                b1

        :param subscriptionId: 	The id of the subscription.
        :type subscriptionId: int(Uint32)
        :return:
            **tuple with 2 return values :**

                + A tuple of :py:class:`~PyPlcnextRsc.Arp.Plc.Gds.Services.VariableInfo`.
                + :py:const:`~PyPlcnextRsc.Arp.Plc.Gds.Services.DataAccessError.NONE` on success

        :rtype: tuple[tuple[VariableInfo],DataAccessError]

        """
        pass

    @RemotingMethod(11)
    def GetTimeStampedVariableInfos(self, subscriptionId: Uint32) -> \
            RscTpTuple[
                RscTpTuple[VariableInfo],
                DataAccessError
            ]:
        """
        Get the subscribed variable information including information of timestamps of the subscription.

        TThis service function relates to the Read function :py:func:`~PyPlcnextRsc.Arp.Plc.Gds.Services.ISubscriptionService.ReadTimeStampedValues`.
        The provided information contains information of the added and currently subscribed variables and additionally information about the timestamps.
        Note that a subscription could contain multiple timestamps, related on the number of used tasks from which the added variables are from.
        The timestamp is always the first value followed by all to the task related variable information.
        ::

            Example:

                Added Variable from task A: a1, a2
                Added Variable from task B: b1
                Results in:
                VariableInfo[]
                timestamp
                a1
                a2
                timestamp
                b1

        Each containing timestamp has the variable name timestamp and the data type :py:const:`~PyPlcnextRsc.Arp.Plc.Commons.DataType.Int64`
        which is provided in :py:class:`~PyPlcnextRsc.Arp.Plc.Gds.Services.VariableInfo` like each other variable information.

        For further information see :py:func:`~PyPlcnextRsc.Arp.Plc.Gds.Services.ISubscriptionService.GetVariableInfos`.

        :param subscriptionId: 	The id of the subscription.
        :type subscriptionId: int(Uint32)
        :return:
            **tuple with 2 return values :**

                + A tuple of :py:class:`~PyPlcnextRsc.Arp.Plc.Gds.Services.VariableInfo`.
                + :py:const:`~PyPlcnextRsc.Arp.Plc.Gds.Services.DataAccessError.NONE` on success

        :rtype: tuple[tuple[VariableInfo],DataAccessError]

        """
        pass

    @RemotingMethod(12)
    def GetRecordInfos(self, subscriptionId: Uint32) -> \
            RscTpTuple[
                RscTpTuple[VariableInfo],
                DataAccessError
            ]:
        """
        Get the subscribed variable information as a record of the subscription.

        .. warning::

            This function is not implemented on the server side, use
            :py:func:`~PyPlcnextRsc.Arp.Plc.Gds.Services.ISubscriptionService.GetTimeStampedVariableInfos` instead.

        This service function relates to the Read function :py:func:`~PyPlcnextRsc.Arp.Plc.Gds.Services.ISubscriptionService.ReadRecords`.
        The provided information contains information of the added and currently subscribed variables,
        its task relation and additionally information about the task related timestamp.
        The information are provided in an array of array of :py:class:`~PyPlcnextRsc.Arp.Plc.Gds.Services.VariableInfo`.
        The first array correspond to the number of different tasks and the second contains the related variable information
        which are related to the variables of this task and additionally information about the task related timestamp.
        Each containing timestamp has the variable name timestamp and the data type :py:const:`~PyPlcnextRsc.Arp.Plc.Commons.DataType.Int64`
        which is provided in :py:class:`~PyPlcnextRsc.Arp.Plc.Gds.Services.VariableInfo` like each other variable information.
        ::

            Example:

                Added Variable from task A: a1, a2
                Added Variable from task B: b1
                Results in:
                VariableInfo[][]
                VariableInfo[]
                timestamp
                a1
                a2
                VariableInfo[]
                timestamp
                b1

        For further information see :py:func:`~PyPlcnextRsc.Arp.Plc.Gds.Services.ISubscriptionService.GetVariableInfos`.

        :param subscriptionId: 	The id of the subscription.
        :type subscriptionId: int(Uint32)
        :return:
            **tuple with 2 return values :**

                + A tuple of :py:class:`~PyPlcnextRsc.Arp.Plc.Gds.Services.VariableInfo`.
                + :py:const:`~PyPlcnextRsc.Arp.Plc.Gds.Services.DataAccessError.NONE` on success

        :rtype: tuple[tuple[VariableInfo],DataAccessError]

        """
        pass

    @RemotingMethod(13)
    def ReadValues(self, subscriptionId: Uint32) -> \
            RscTpTuple[
                RscTpTuple[RscVariant],
                DataAccessError
            ]:
        """
        Read the data from the subscription with the given id.

        This service function returns the plain data values from the added and subscribed variables.
        The data values are returned in a static order and doesn't contain any type information.
        To figure out which value belongs to the added variable, it is necessary to call the related information function
        :py:func:`~PyPlcnextRsc.Arp.Plc.Gds.Services.ISubscriptionService.GetVariableInfos`.
        As long as the subscription doesn't resubscribed with :py:func:`~PyPlcnextRsc.Arp.Plc.Gds.Services.ISubscriptionService.Resubscribe`,
        all the information are valid and both, the Read value data and information data, are in a static order.
        Note that this values doesn't contain timestamps! If the timestamp is needed use the function
        :py:func:`~PyPlcnextRsc.Arp.Plc.Gds.Services.ISubscriptionService.ReadTimeStampedValues` instead.

        The Read data may contain null values (:py:const:`~PyPlcnextRsc.Arp.Plc.Commons.DataType.Void`) if the Read call was executed before the tasks initially have written the data.
        ::

            Example:

                Added Variable from task A: a1, a2
                Added Variable from task B: b1
                Results in:
                object[]
                a1
                a2
                b1

        :param subscriptionId: 	The id of the subscription.
        :type subscriptionId: int(Uint32)
        :return:
            **tuple with 2 return values :**

                + Contains the plain values of the given and subscribed variables.
                + :py:const:`~PyPlcnextRsc.Arp.Plc.Gds.Services.DataAccessError.NONE` on success
        :rtype: tuple[tuple[RscVariant],DataAccessError]

        """
        pass

    @RemotingMethod(14)
    def ReadTimeStampedValues(self, subscriptionId: Uint32) -> \
            RscTpTuple[
                RscTpTuple[RscVariant],
                DataAccessError
            ]:
        """
        Read the data including timestamps from the subscription with the given id.

        This service function returns the plain data values from the added and subscribed variables including timestamps.
        The data values are returned in a static order and doesn't contain any type information.
        To figure out which value belongs to the added variable, it is necessary to call the related information function
        :py:func:`~PyPlcnextRsc.Arp.Plc.Gds.Services.ISubscriptionService.GetTimeStampedVariableInfos`.
        As long as the subscription doesn't resubscribed with :py:func:`~PyPlcnextRsc.Arp.Plc.Gds.Services.ISubscriptionService.Resubscribe`,
        all the information are valid and both, the Read value data and information data, are in a static order.

        The Read data may contain null values (:py:const:`~PyPlcnextRsc.Arp.Plc.Commons.DataType.Void`) if the Read call was executed before the tasks initially have written the data.
        ::

            Example:

                Added Variable from task A: a1, a2
                Added Variable from task B: b1
                Results in:
                object[]
                timestamp task A
                a1
                a2
                timestamp task B
                b1

        :param subscriptionId: The id of the subscription.
        :return:
            **tuple with 2 return values :**

                + Contains the plain values including the timestamps of the given and subscribed variables.
                + :py:const:`~PyPlcnextRsc.Arp.Plc.Gds.Services.DataAccessError.NONE` on success

        :rtype: tuple[tuple[RscVariant],DataAccessError]

        """
        pass

    @RemotingMethod(15)
    def ReadRecords(self, subscriptionId: Uint32, count: Uint16) -> \
            RscTpTuple[
                RscTpTuple[RscVariant],
                DataAccessError
            ]:
        """
        Read the data including timestamps from the subscription with the given id separated in task records.

        This service function returns the plain data values from the added and subscribed variables including timestamps separated in task records.
        The data values are returned in a static order and doesn't contain any type information.
        To figure out which value belongs to the added variable, it is necessary to call the related information function Arp.Plc.Gds.Services.ISubscriptionService.GetRecordInfos.
        As long as the subscription doesn't resubscribed with Arp.Plc.Gds.Services.ISubscriptionService.Resubscribe, all the information are valid and both,
        the Read value data and information data, are in a static order.

        The number of returned value records depends on the count of tasks, the number of sampled data and the number of the given count parameter.

        The structure how the values are returned is strictly defined: The first array (records) contains n arrays (task records) and where n depends on the number of tasks.
        The array from the second dimension (task records) contains n arrays (record), where n depends on the number of collected data, one data record per task cycle.
        The array from the third dimension (record) contains the plain values, starting with the timestamp.

        The Read data may contain null values (:py:const:`~PyPlcnextRsc.Arp.Plc.Commons.DataType.Void`) if the Read call was executed before the tasks initially have written the data.

        ::

            Example:

                Added Variable from task A: a1, a2
                Added Variable from task B: b1
                task A sampled 2 cycles
                task B sampled 1 cycles
                Results in:
                object[] (records)
                object[] (task A records)
                object[] (record cycle 1)
                timestamp
                a1
                a2
                object[] (record cycle 2)
                timestamp
                a1
                a2
                object[] (task B records)
                object[] (record cycle 1)
                timestamp
                a1
                a2

        :param subscriptionId:	The id of the subscription.
        :type subscriptionId: int(Uint32)
        :param count: Number of maximum records to be copied per task. If set to zero, all available records will be copied.
        :type count: int(Uint16)
        :return:
            **tuple with 2 return values :**

                + Tuple for the subscribed data records including timestamps.
                + :py:const:`~PyPlcnextRsc.Arp.Plc.Gds.Services.DataAccessError.NONE` on success

        :rtype: tuple[tuple[RscVariant],DataAccessError]

        """
        pass


@RemotingService('Arp.Plc.Gds.Services.IForceService')
class IForceService:
    """
    Service for managing and controlling force variables by the Arp GDS.

    Use :py:class:`~PyPlcnextRsc.Arp.Plc.Gds.Services.IForceService` in order to force and to unforce variables.

    """

    @RemotingMethod(1)
    def AddVariable(self, item: ForceItem) -> DataAccessError:
        """
        Adds a new variable and value for forcing. Enables force mode.

        The enabled force mode is signalized by notification and by the activated
        ':py:const:`~PyPlcnextRsc.Arp.Plc.Domain.Services.PlcState.Forcing`'

        :param item:    Force item :py:class:`~PyPlcnextRsc.Arp.Plc.Gds.Services.ForceItem`, which contains the the name of the variable with the full instance path and the force value.
                        The data type of the force value must be equal with the data type of the target variable.
        :return: Returns :py:const:`~PyPlcnextRsc.Arp.Plc.Gds.Services.DataAccessError.NONE` on success
        :rtype: DataAccessError

        """
        pass

    @RemotingMethod(2)
    def RemoveVariable(self, variableName: RscString512):
        """
        Resets forced variable. Disables force mode after force list is empty.

        :param variableName: Instance path of the variable.
        :type variableName: str(max=512)

        """
        pass

    @RemotingMethod(3)
    def GetVariables(self) -> RscTpTuple[ForceItem]:
        """
        Gets a list of all forced variables.

        :return: Returns a list with all existing :py:class:`~PyPlcnextRsc.Arp.Plc.Gds.Services.ForceItem` objects.
        :rtype: tuple(ForceItem)

        """
        pass

    @RemotingMethod(4)
    def Reset(self):
        """
        Resets the force list. Disables force mode.

        The disabled force mode is signalized by notification and by the deactivated PlcState.

        """
        pass

    @RemotingMethod(5)
    def IsForcable(self, variableName: RscString512) -> bool:
        """
        Tests whether variable is forcable.

        The variable has to meet the following requirements to be forcable:

            + The kind of variable should be an In- or an Out-port of a program (IEC, C ++, Simulink ...) or a variable that is connected to I/O data.

            + The data type of the variable has to be supported.

        :return: true if the variable is forcable.
        :rtype: bool

        """
        pass

    @RemotingMethod(6)
    def IsActive(self) -> bool:
        """
        Tests whether force mode is active.

        :return: true if the force mode is active.
        :rtype: bool

        """
        pass
