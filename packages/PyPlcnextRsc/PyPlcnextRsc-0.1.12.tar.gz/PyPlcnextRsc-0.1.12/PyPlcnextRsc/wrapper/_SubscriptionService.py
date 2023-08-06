import logging
import threading
from abc import ABCMeta, abstractmethod
from typing import Union, Sequence, Tuple, Dict, List

from PyPlcnextRsc import InvalidOperationException, RscStruct, RscVariant
from PyPlcnextRsc.Arp.Plc.Gds.Services import ISubscriptionService, DataAccessError, VariableInfo, SubscriptionKind
from PyPlcnextRsc.wrapper.common import IService, variable_names_generator

__all__ = ['SubscriptionService']


class SubscriptionBase:
    __metaclass__ = ABCMeta

    def __init__(self, service: ISubscriptionService, sampleRate: int = 100000):
        self.log = logging.getLogger(__name__ + '.' + self.__class__.__name__)
        self._subscriptionId = 0
        self._service = service
        self._rate = sampleRate
        self._rLock = threading.RLock()

    def getSubscriptionId(self) -> int:
        """
        Get the Id of this subscription.

        :return: subscription Id
        :rtype: int

        """

        return self._subscriptionId

    def addVariables(self, variableNames: Union[str, Sequence[str]], prefix: str = None) \
            -> Union[DataAccessError, Tuple[DataAccessError]]:
        """
        Extends the subscription by inserting the given variable name.

        :param variableNames: The full name of the variable. also can be List or Tuple of name
        :type variableNames: Union[str, Sequence[str]]
        :param prefix: prefix for variableName if not None
        :type prefix: str
        :return: Returns DataAccessError.NONE on success. If variableName is type of List or Tuple, a List of DataAccessError will be returned.
        :rtype: Union[DataAccessError, Tuple[DataAccessError]]

        """
        with self._rLock:
            self._checkIdDeleted()
            variables = variable_names_generator(variableNames, prefix)
            errs = self._service.AddVariables(self.getSubscriptionId(), variables)
            if type(variableNames) == str:
                return errs[0]
            else:
                return errs

    def removeVariables(self, variableNames: Union[str, Sequence[str]], prefix: str = None) \
            -> Union[DataAccessError, Tuple[DataAccessError]]:
        """
        Removes the variable with the specific variable name from the subscription.

        :param variableNames: The full name of the variable. also can be List or Tuple of name
        :type variableNames: Union[str, Sequence[str]]
        :param prefix: prefix for variableName if not None
        :type prefix: str
        :return: Returns DataAccessError.NONE on success. If variableName is type of List or Tuple, a List of DataAccessError will be returned.
        :rtype: Union[DataAccessError, Tuple[DataAccessError]]

        """
        with self._rLock:
            self._checkIdDeleted()
            variables = variable_names_generator(variableNames, prefix)
            errs = []
            for variable in variables:
                errs.append(self._service.RemoveVariable(self.getSubscriptionId(), variable))

            if type(variableNames) == str:
                return errs[0]
            else:
                return tuple(errs)

    def subscribe(self, sampleRate: int = None, createInfo=True) -> DataAccessError:
        """
        Subscribes the subscription with the given id.

        :param sampleRate: The desired sample rate in microseconds.
        :type sampleRate: int
        :param createInfo: auto create info after success
        :type createInfo: bool
        :return: Returns DataAccessError.NONE on success.
        :rtype: DataAccessError

        """
        with self._rLock:
            self._checkIdDeleted()
            if sampleRate:
                self._rate = sampleRate
            err = self._service.Subscribe(self.getSubscriptionId(), self._rate)
            if createInfo and err == DataAccessError.NONE:
                return self.createInfoBuffer()
            return err

    def resubscribe(self, sampleRate: int = None, createInfo=True) -> DataAccessError:
        """
        Resubscribes the subscription with the given id.

        :param sampleRate: The desired sample rate in microseconds. Leave 'None' to use the last setting.
        :type sampleRate: int
        :param createInfo: auto create info after success
        :type createInfo: bool
        :return: Returns DataAccessError.NONE on success.
        :rtype: DataAccessError

        """
        self._checkIdDeleted()

        if sampleRate:
            self._rate = sampleRate
        with self._rLock:
            err = self._service.Resubscribe(self.getSubscriptionId(), self._rate)
            if createInfo and err == DataAccessError.NONE:
                return self.createInfoBuffer()
            return err

    def unsubscribe(self) -> DataAccessError:
        """
        Unsubscribes the subscription with the given id.

        :return: Returns DataAccessError.NONE on success.
        :rtype: DataAccessError

        """
        with self._rLock:
            self._checkIdDeleted()
            return self._service.Unsubscribe(self.getSubscriptionId())

    def deleteSubscription(self) -> DataAccessError:
        """
        Deletes the subscription.

        :return: Returns DataAccessError.NONE on success.
        :rtype: DataAccessError

        """
        with self._rLock:
            self._checkIdDeleted()
            err = self._service.DeleteSubscription(self.getSubscriptionId())
            self._subscriptionId = -1
            return err

    def _checkIdDeleted(self):
        _id = self.getSubscriptionId()
        if _id == -1:
            raise InvalidOperationException("already deleted !")
        elif _id == 0:
            raise InvalidOperationException("not create yet !")

    def __del__(self):
        try:
            self.deleteSubscription()
        except:
            pass

    @abstractmethod
    def createInfoBuffer(self):
        pass

    @abstractmethod
    def create(self):
        pass


class SubResultItem(RscStruct):
    """
    # TODO
    """
    VariableInfo: VariableInfo
    """# TODO"""
    Value: RscVariant
    """# TODO"""
    TimeStamp: Union[int, None] = None
    """# TODO"""


_PLACEHOLDER_TIMESTAMP = 0


class Subscription(SubscriptionBase):
    """

    """

    def __init__(self, service: ISubscriptionService, kind: SubscriptionKind, sampleRate: int = 100000):
        super().__init__(service, sampleRate)
        self._info_for_readValues = []
        self._info_for_readTimeStampedValues = []
        self._kind = kind

    def create(self):
        _id = self._service.CreateSubscription(self._kind)
        if _id > 0:
            self._subscriptionId = _id
        return _id

    def _createVariableInfos(self) -> DataAccessError:
        """

        """
        infos, err = self._service.GetVariableInfos(self.getSubscriptionId())
        if err == DataAccessError.NONE:
            self._info_for_readValues = infos
        return err

    def _createTimeStampedVariableInfos(self) -> DataAccessError:
        """

        """
        infos, err = self._service.GetTimeStampedVariableInfos(self.getSubscriptionId())
        if err == DataAccessError.NONE:
            # for quick timestamp check, use _PLACEHOLDER_TIMESTAMP
            self._info_for_readTimeStampedValues = tuple((info if info.Name != 'timestamp' else _PLACEHOLDER_TIMESTAMP for info in infos))
        return err

    def readValues(self) -> Tuple[DataAccessError, Dict[str, SubResultItem]]:
        """

        """
        _info_for_readValues = self._info_for_readValues
        values, err = self._service.ReadValues(self.getSubscriptionId())
        if err == DataAccessError.NONE:
            assert len(values) == len(_info_for_readValues), "internal info not match"
            return err, {info.Name: SubResultItem(VariableInfo=info, Value=value) for info, value in zip(_info_for_readValues, values)}
        else:
            return err, {}

    def readTimeStampedValues(self) -> Tuple[DataAccessError, Dict[str, SubResultItem]]:
        """

        """
        _info_for_readTimeStampedValues = self._info_for_readTimeStampedValues
        _timestamp = 0
        _items = {}
        values, err = self._service.ReadTimeStampedValues(self.getSubscriptionId())
        if err == DataAccessError.NONE:
            assert len(values) == len(_info_for_readTimeStampedValues), "internal info not match"
            for info, value in zip(_info_for_readTimeStampedValues, values):
                if info == _PLACEHOLDER_TIMESTAMP:
                    _timestamp = value.GetValue()
                    continue
                _items[info.Name] = SubResultItem(VariableInfo=info, Value=value, TimeStamp=_timestamp)
        return err, _items

    def createInfoBuffer(self):
        err = self._createVariableInfos()
        if err == DataAccessError.NONE:
            err = self._createTimeStampedVariableInfos()
        return err


class RecordingSubscription(SubscriptionBase):
    def __init__(self, service: ISubscriptionService, recordCount: int, sampleRate: int = 100000):
        super().__init__(service, sampleRate)
        self._info = []
        self._recordCount = recordCount

    def create(self):
        """

        """
        _id = self._service.CreateRecordingSubscription(self.getRecordCount())
        if _id > 0:
            self._subscriptionId = _id
        return _id

    def getRecordCount(self):
        """

        """
        return self._recordCount

    def readRecords(self, count: int = 0) -> Tuple[DataAccessError, List[List[Dict[str, SubResultItem]]]]:
        """
        Read the data including timestamps from the subscription with the given id separated in task records.

        :param count: Number of maximum records to be copied per task. If set to zero, all available records will be copied.
        :type count: int

        """
        tasks_infos = self._info
        raw_tasks_records, err = self._service.ReadRecords(self.getSubscriptionId(), count)
        tasks_records = []
        if err == DataAccessError.NONE:
            assert len(tasks_infos) == len(raw_tasks_records), "internal info not match"
            for task_index, raw_task_record in enumerate(raw_tasks_records):
                task_data = []
                task_info = tasks_infos[task_index]
                for record_index, record in enumerate(raw_task_record.GetValue()):
                    item_data = {}
                    item_timestamp = None
                    item_records = record.GetValue()
                    assert len(task_info) == len(item_records), "internal info not match"
                    for item_index, item_value in enumerate(item_records):
                        if item_index > 0:
                            item_info = task_info[item_index]
                            item_data[item_info.Name] = SubResultItem(VariableInfo=item_info, Value=item_value, TimeStamp=item_timestamp)
                        else:
                            # if i == _PLACEHOLDER_TIMESTAMP:
                            item_timestamp = item_value.GetValue()

                    task_data.append(item_data)
                tasks_records.append(task_data)
        return err, tasks_records

    def createInfoBuffer(self):
        infos, err = self._service.GetTimeStampedVariableInfos(self.getSubscriptionId())
        if err == DataAccessError.NONE:
            _tasks = []
            _task = None
            for info in infos:
                if info.Name == 'timestamp':
                    if not _task:
                        _task = [_PLACEHOLDER_TIMESTAMP]
                    else:
                        _tasks.append(_task)
                        _task = [_PLACEHOLDER_TIMESTAMP]
                else:
                    _task.append(info)
            if _task and len(_task) > 1:
                _tasks.append(_task)
            self._info = _tasks
        return err


class SubscriptionService(IService):
    def _raw_service_interface(self):
        return ISubscriptionService

    def createSubscription(self, kind: SubscriptionKind, sampleRate: int = 100000) -> Subscription:
        """
        Creates a subscription object of the given SubscriptionKind.

        :param kind: The kind of the subscription.
        :type kind: SubscriptionKind
        :param sampleRate: The desired sample rate in microseconds.
        :type sampleRate: int(Uint64)
        :return: a subscription object
        :rtype: Subscription
        """
        if kind == SubscriptionKind.Recording:
            raise InvalidOperationException("Use createRecordingSubscription to create Recording Subscription instead")
        return Subscription(self._raw_service, kind, sampleRate)

    def createRecordingSubscription(self, recordCount: int = 10, sampleRate: int = 100000) -> RecordingSubscription:
        """
        Creates a subscription of SubscriptionKind.Recording.

        :param recordCount: The maximum number of storable records.
        :type recordCount: int
        :param sampleRate: The desired sample rate in microseconds.
        :type sampleRate: int(Uint64)
        :return: RecordingSubscription object
        :rtype: RecordingSubscription

        """
        return RecordingSubscription(self._raw_service, recordCount, sampleRate)
