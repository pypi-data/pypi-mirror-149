# Copyright (c) 2021 Phoenix Contact. All rights reserved.
# Licensed under the MIT. See LICENSE file in the project root for full license information.

from datetime import datetime

from PyPlcnextRsc.common.serviceDefinition.all_needed import *

__all__ = ['SortOrder',
           "Severity",
           "NotificationFilter",
           "StoredNotification",
           "Notification",
           "INotificationLoggerService"
           ]


@MarshalAs(rscType=RscType.Int32)
class SortOrder(RscTpIntEnum):
    """Definition how to sort the queried notifications"""

    NONE = 0
    """Do not sort"""

    TimestampAsc = 1
    """sort by timestamp ascending"""

    TimestampDesc = 2
    """sort by timestamp descending"""


@MarshalAs(rscType=RscType.Uint8)
class Severity(RscTpIntEnum):
    """Enumeration of Severities for notifications"""
    Internal = 0
    Info = 1
    Warning = 2
    Error = 3
    Critical = 4
    Fatal = 5
    Emerge = 6


class NotificationFilter(RscStruct):
    """Filter specification to match notification on query or delete"""

    StoredIdLowerLimit: Uint64
    """Minimum matching Id ( >= 0 )
    
    ower limit of the StoredId (> = 1), is ignored if = 0
    In the Notification Logger, a notification is clearly identified by a StoredId (uint64). The StoredId is assigned by the Notification Logger when adding the notification to the input buffer.
    """

    StoredIdUpperLimit: Uint64
    """Maximum matching Id ( <= 1^64 )
    
    Upper limit of the StoredId (> = 1, < = 18446744073709551615, max. uint64), is ignored if = 0
    """

    NotificationNameRegExp: RscString512
    """ Regular expression for the notification name. Is ignored if field is empty."""

    SenderNameRegExp: RscString512
    """	Regular expression for the sender name. Is ignored if field is empty."""

    TimestampBefore: RscString512
    """Matches all timestamps before this timestamp ,Format: YYYY-MM-ddTHH:mm:ss.SSS,Ignored if empty"""

    TimestampAfter: RscString512
    """Matches all timestamps after this timestamp ,Format: YYYY-MM-ddTHH:mm:ss.SSS,Ignored if empty"""

    SeverityLowerLimit: RscString512
    """Minimum matching Severity ,Ignored if empty"""

    SeverityUpperLimit: RscString512
    """Maximum matching Severity,Ignored if empty"""


class StoredNotification(RscStruct):
    """Data structure for notifications from the NotificationLogger"""

    Id: Uint64
    """Id of the notification"""

    Archive: RscString512
    """name of the archive the notification was retreived from. If the same notification was stored in multiple archives this field contains a comma separated list of the archives"""

    NotificationName: RscString512
    """Name of the notification"""

    SenderName: RscString512
    """Name of the sender"""

    TimeStamp: RscString512
    """timestamp when the notification was sent"""

    Severity: RscString512
    """Severity"""

    Payload: RscTpSequence[RscString512]
    """Formatted payload"""

    PayloadXml: RscTpSequence[RscString512]
    """Payload as XML"""


class Notification(RscStruct):
    """Contains meta data and paylod of a Notification"""

    Id: Uint64
    """Returns the id"""
    NotificationNameId: Uint32
    """Returns the NotificationNameId"""
    Timestamp: datetime
    """Returns the timestamp"""
    Severity: Severity
    """Returns the Severity"""

    PayloadTypeId: Uint16
    """Returns the PayloadTypeId"""

    Payload: RscTpSequence[RscVariant[512]]
    """Returns a reference to the raw payload"""


@RemotingService('Arp.Services.NotificationLogger.Services.INotificationLoggerService')
class INotificationLoggerService:
    """The NotificationLogger stores Notifications and provides an interface to retrieve them."""

    @RemotingMethod(1)
    def QueryStoredNotifications(self, archives: RscTpSequence[RscString512], Filter: NotificationFilter, limit: Int32, sortOrder: SortOrder, language: RscString512) -> RscTpTuple[StoredNotification]:
        """
        Queries notifications matching the supplied filter from the mentioned archives and returns them as StoredNotification objects

        :param archives: List of archives to query. Empty list queries all.
        :type archives: Sequence[str(max=512)]
        :param Filter: filter specifications
        :type Filter: NotificationFilter
        :param limit: maximum number of returned notifications
        :type limit: Int32
        :param sortOrder: sorting to apply
        :type sortOrder: SortOrder
        :param language: translate notification payloads
        :type language: str(max=512)

        :return: collection of notifications
        :rtype: tuple[StoredNotification]

        """
        pass

    @RemotingMethod(2)
    def QueryNotifications(self, archives: RscTpSequence[RscString512], Filter: NotificationFilter, limit: Int32, sortOrder: SortOrder, language: RscString512) -> RscTpTuple[Notification]:
        """
        Queries notifications matching the supplied filter from the mentioned archives and returns them as Notification objects

        :param archives: List of archives to query. Empty list queries all.
        :type archives: Sequence[str(max=512)]
        :param Filter: filter specifications
        :type Filter: NotificationFilter
        :param limit: maximum number of returned notifications
        :type limit: Int32
        :param sortOrder: sorting to apply
        :type sortOrder: SortOrder
        :param language: translate notification payloads
        :type language: str(max=512)

        :return: collection of notifications
        :rtype: tuple[Notification]

        """

    @RemotingMethod(3)
    def DeleteNotifications(self, archives: RscTpSequence[RscString512], Filter: NotificationFilter) -> Int32:
        """
        Remove notifications mathing the filter  from the given archives

        :param archives: List of archives to delete notifications from. Empty list deletes from all.
        :type archives: Sequence[str(max=512)]
        :param Filter: filter specification, matching notifications are removed
        :type Filter: NotificationFilter

        :return: number of deleted notifications
        :rtype: Int32

        """
        pass

    @RemotingMethod(4)
    def ListArchives(self) -> RscTpTuple[RscString512]:
        """
        Queries a list of archives

        :return: list of known archives
        :rtype: tuple[str]

        """
        pass

    @RemotingMethod(5)
    def GetArchiveConfiguration(self, archive: RscString512) -> RscTpTuple[RscString512]:
        """
        Query the configuration as XML for the given archive

        ..  warning::

                The operation 'GetArchiveConfiguration' is not implemented yet


        :param archive: name of the archive
        :type archive: str(max=512)
        :return: XML of the configuration
        :rtype: tuple[str]

        """
        pass

    @RemotingMethod(6)
    def SetArchiveConfiguration(self, archive: RscString512, xmlConfiguration: RscTpSequence[RscString512]) -> bool:
        """
        Set the configuration of the given archive

        ..  warning::

                The operation 'SetArchiveConfiguration' is not implemented yet


        :param archive: name of the archive
        :type archive: str(max=512)
        :param xmlConfiguration: XML containing the configuration
        :type xmlConfiguration: Sequence[str(max=512)]

        :return: true on success
        :rtype: bool

        """
        pass

    @RemotingMethod(7)
    def ResetArchiveConfigurationToFiles(self, archive: RscString512) -> bool:
        """
        Resets the configuration of the given archive to the configuration files. All changes made by RSC are reverted.


        ..  warning::

                The operation 'ResetArchiveConfigurationToFiles' is not implemented yet

        :param archive: name of the archive
        :type archive: str(max=512)

        :return: true on success
        :rtype: bool

        """
        pass
