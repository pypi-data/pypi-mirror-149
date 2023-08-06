# Copyright (c) 2021 Phoenix Contact. All rights reserved.
# Licensed under the MIT. See LICENSE file in the project root for full license information.

from PyPlcnextRsc.common.serviceDefinition.all_needed import *

__all__ = [
    "AccessErrorCode",
    "DeviceSettingResult",
    "DeviceSettingItem",
    "IDeviceInfoService",
    "IDeviceStatusService",
    "IDeviceSettingsService",
    "IDeviceControlService",
]


@MarshalAs(rscType=RscType.Int32)
class AccessErrorCode(RscTpIntEnum):
    """
    Enumeration for error codes returned from Device.Interface.Services.

    """
    NONE = 0
    """Success"""
    UnknownError = 1
    """Unkown Error"""
    UnknownSetting = 2
    """Unknown setting id"""
    AuthorizationFailure = 3
    """Authorization failure"""
    IncompatibleType = 4
    """The type of the new value is wrong"""
    InvalidFormat = 5
    """The format of the new value is wrong"""
    InvalidParameter = 6
    """A parameter is invalid"""
    OutOfRange = 7
    """A value is out of range"""


class DeviceSettingResult(RscStruct):
    """
    Container for a combination of an error code and a value which is a result for a Read operation to a single setting.

    The structure is used as result by :py:class:`PyPlcnextRsc.Arp.Device.Interface.Services.IDeviceSettingsService`.
    ReadValue A sequence of instances of this structure is used as result by :py:func:`~PyPlcnextRsc.Arp.Device.Interface.Services.IDeviceSettingsService.ReadValues`.

    """

    ErrorCode: AccessErrorCode
    """
    An error code which describes the reason why a setting could not be Read with The error codes can be interpreted with the help of 
    the enumeration :py:class:`PyPlcnextRsc.Arp.Device.Interface.Services.AccessErrorCode`.
    
    """

    Value: RscVariant[512]
    """
    The value for the requested setting which can be :py:const:`PyPlcnextRsc.common.tag_type.RscType.Void` and otherwise is of the simple type the setting has.
    Please note that this property is :py:const:`PyPlcnextRsc.common.tag_type.RscType.Void` whenever the member 
    :py:attr:`~PyPlcnextRsc.Arp.Device.Interface.Services.DeviceSettingResult.ErrorCode`
    indicates an error which means it is not :py:const:`PyPlcnextRsc.Arp.Device.Interface.Services.AccessErrorCode.NONE`.
    
    """


class DeviceSettingItem(RscStruct):
    """
    Container for a (relative) setting identifier with its value.

    The structure is designed for efficient interpretation on the receiving side which is the Remoting server.
    The structure is used by ":py:func:`PyPlcnextRsc.Arp.Device.Interface.Services.IDeviceSettingsService.WriteValue`"
    A sequence of instances of this structure is intended to be passed to the
    method :py:func:`PyPlcnextRsc.Arp.Device.Interface.Services.IDeviceSettingsService.WriteValues`
    """

    Setting: RscString512
    """Tokens which describe the (relative) path to the setting combined with the value.
    If this instance of the structure  TokensAndValue is part of a sequence (an array) then the
    preceeding instance's tokens already provide a context at which the tokens here start with their description."""

    Value: RscVariant[512]
    """The value of the setting which is identified by the (relative) path which is described by the tokens.
    The type of the value must match the value which is defined for the particular setting."""


@RemotingService('Arp.Device.Interface.Services.IDeviceInfoService')
class IDeviceInfoService:
    """
    Use this service to Read Device information.
    """

    @RemotingMethod(1)
    def GetItem(self, identifier: RscString512) -> RscVariant:
        """
        Read a single information

        :return: value as RscVariant on success, :py:const:`PyPlcnextRsc.common.tag_type.RscType.Void` on error
        :rtype: RscVariant

        """
        pass

    @RemotingMethod(2)
    def GetItems(self, identifiers: RscTpSequence[RscString512]) -> RscTpTuple[RscVariant]:
        """
        Read a list of information

        :param identifiers: Sequence of String for select the items
        :return: values as RscVariant on success, :py:const:`PyPlcnextRsc.common.tag_type.RscType.Void` on error
        :rtype: tuple[RscVariant]

        """
        pass


@RemotingService('Arp.Device.Interface.Services.IDeviceStatusService')
class IDeviceStatusService:
    """
    Use this service to Read Device states.
    """

    @RemotingMethod(1)
    def GetItem(self, identifier: RscString512) -> RscVariant:
        """
        Read a single state

        :return: value as RscVariant on success, :py:const:`PyPlcnextRsc.common.tag_type.RscType.Void` on error
        :rtype: RscVariant

        """
        pass

    @RemotingMethod(2)
    def GetItems(self, identifiers: RscTpSequence[RscString512]) -> RscTpTuple[RscVariant]:
        """
        Read a list of state

        :param identifiers: Array of String for select the items
        :type identifiers: Sequence[str(max=512)]
        :return: values as RscVariant on success, :py:const:`PyPlcnextRsc.common.tag_type.RscType.Void` on error
        :rtype: tuple[RscVariant]

        """
        pass


@RemotingService('Arp.Device.Interface.Services.IDeviceSettingsService')
class IDeviceSettingsService:
    """
    Use this service to Read and Write Device settings.
    """

    @RemotingMethod(1)
    def ReadValue(self, setting: RscString512) -> DeviceSettingResult:
        """
        Read a single setting

        :param setting: String for select the item
        :type setting: str(max=512)
        :return: result as :py:class:`~PyPlcnextRsc.Arp.Device.Interface.Services.DeviceSettingResult`
        :rtype: DeviceSettingResult

        """
        pass

    @RemotingMethod(2)
    def ReadValues(self, settings: RscTpSequence[RscString512]) -> RscTpTuple[DeviceSettingResult]:
        """
        Read a list of settings

        :param settings: Sequence of string for select the items
        :type settings: Sequence[str(max=512)]
        :return: result as array of  :py:class:`~PyPlcnextRsc.Arp.Device.Interface.Services.DeviceSettingResult`
        :rtype: tuple[DeviceSettingItem]

        """
        pass

    @RemotingMethod(3)
    def WriteValue(self, settingItem: DeviceSettingItem) -> AccessErrorCode:
        """
        Write a single setting

        :param settingItem: :py:class:`~PyPlcnextRsc.Arp.Device.Interface.Services.DeviceSettingItem` with string for select the item and the new value
        :type settingItem: DeviceSettingItem
        :return: result as :py:class:`~PyPlcnextRsc.Arp.Device.Interface.Services.AccessErrorCode`
        :rtype: AccessErrorCode

        """
        pass

    @RemotingMethod(4)
    def WriteValues(self, settingItems: RscTpSequence[DeviceSettingItem]) -> RscTpTuple[AccessErrorCode]:
        """
        Write a list of settings

        :param settingItems: Sequence of :py:class:`~PyPlcnextRsc.Arp.Device.Interface.Services.DeviceSettingItem` for set the items to new values
        :type settingItems: Sequence[DeviceSettingItem]
        :return: result as tuple of :py:class:`~PyPlcnextRsc.Arp.Device.Interface.Services.AccessErrorCode`
        :rtype: tuple[AccessErrorCode]

        """
        pass


@RemotingService('Arp.Device.Interface.Services.IDeviceControlService')
class IDeviceControlService:
    """Use this service to control the Device."""

    @RemotingMethod(1)
    def RestartDevice(self):
        """
        Reboot the Device

        """
        pass

    @RemotingMethod(2)
    def ResetToFactoryDefaults(self, resetType: Uint16) -> AccessErrorCode:
        """
        Reset Device configuration

        After successful start the PLC will stop and than reboot. While the reboot the requested defaults will be set.

            +----------+-------------------------------------------------------------+
            |Reset type|Description                                                  |
            +==========+=============================================================+
            |1         |Reset Device configuration to factory default.               |
            +----------+-------------------------------------------------------------+
            |2         |Downgrade FW to factory version and reset configuration.     |
            +----------+-------------------------------------------------------------+

        :param resetType: see the table above.
        :type resetType: int(Uint16)
        :return: Result of start execute
        :rtype: AccessErrorCode

        """
        pass

    @RemotingMethod(3)
    def StartFirmwareUpdate(self, updateType: Uint16) -> AccessErrorCode:
        """
        Start FW update

        Before you can start an update a raucb-container must be copied to path "/opt/plcnext".
        After successfull start an update the PLC will stop, execute the update and than reboot.

        :param updateType: Reserved for extensions, must be 0 in this version.
        :type updateType: int(Uint16)
        :return: Result of start execute
        :rtype: AccessErrorCode

        """
        pass
