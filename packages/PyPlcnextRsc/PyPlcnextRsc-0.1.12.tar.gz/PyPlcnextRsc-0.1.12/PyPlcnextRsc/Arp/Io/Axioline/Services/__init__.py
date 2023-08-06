# Copyright (c) 2021 Phoenix Contact. All rights reserved.
# Licensed under the MIT. See LICENSE file in the project root for full license information.

from PyPlcnextRsc.common.serviceDefinition.all_needed import *


class AxioResult(RscStruct):
    """Contains error information of AXIO service"""
    ServiceDone: bool
    """Flag is set when service is done.Is only needed in non-blocking methods."""
    ErrorCode: Uint16
    """Error code"""
    AddInfo: Uint16
    """Additional information"""


class AxioDeviceConfiguration(RscStruct):
    """Configuration of AXIO device"""
    Type: Uint32
    """Device type"""
    Id: Uint32
    """Device ID"""
    Length: Uint16
    """Length of process data in Byte"""


@RemotingService('Arp.Io.Axioline.Services.IAxioMasterService')
class IAxioMasterService:
    """Provides the access to the AXIO master"""

    @RemotingMethod(1)
    def AxioControl(self, inData: RscTpSequence[Uint16]) -> \
            RscTpTuple[
                RscTpTuple[Uint16],
                Uint16
            ]:
        """
        Raw AXIO service to communicate with the AXIO master.

        :param inData: Request Data to send to the AXIO master. Format has to be according to DDI specification.
        :type inData: Sequence[Uint16]
        :return:
            **tuple with 2 return values :**

                + outData (Tuple[Uint16]) Response Data received from the AXIO master. Format is according to DDI specification.
                + Status value [Uint16] Note: This service only returns internal errors. Negative confirmations have to be evaluated by user.

        :rtype: tuple[tuple[Uint16],Uint16]
        """
        pass

    @RemotingMethod(2)
    def CreateConfiguration(self, frameReference: Uint16) -> AxioResult:
        """
        Automatic creation of a new configuration

        :param frameReference: Frame reference
        :type frameReference: Uint16
        :return: Structure with error information.
        :rtype: :py:class:`~PyPlcnextRsc.Arp.Io.Axioline.Services.AxioResult`.
        """
        pass

    @RemotingMethod(3)
    def ReadConfiguration(self, frameReference: Uint16) -> RscTpTuple[RscTpTuple[AxioDeviceConfiguration], AxioResult]:
        """
        Automatic creation of a new configuration

        :param frameReference: Frame reference
        :type frameReference: Uint16
        :return:
            **tuple with 2 return values :**

                + configuration (Tuple[AxioDeviceConfiguration]) Configuration of AXIO device.
                + AxioResult [Uint16] Structure with error information.

        :rtype: tuple[tuple[AxioDeviceConfiguration],AxioResult]
        """
        pass

    @RemotingMethod(4)
    def WriteConfiguration(self, frameReference: Uint16, configuration: RscTpSequence[AxioDeviceConfiguration]) -> AxioResult:
        """
        Write configuration

        :param frameReference: Frame reference
        :type frameReference: Uint16
        :param configuration: Configuration of AXIO device
        :type configuration: Sequence[AxioDeviceConfiguration]
        :return: Structure with error information.
        :rtype: :py:class:`~PyPlcnextRsc.Arp.Io.Axioline.Services.AxioResult`.
        """
        pass

    @RemotingMethod(5)
    def ActivateConfiguration(self, frameReference: Uint16) -> AxioResult:
        """
        Activate configuration

        :param frameReference: Frame reference
        :type frameReference: Uint16
        :return: Structure with error information.
        :rtype: :py:class:`~PyPlcnextRsc.Arp.Io.Axioline.Services.AxioResult`.
        """
        pass

    @RemotingMethod(6)
    def DeactivateConfiguration(self, frameReference: Uint16) -> AxioResult:
        """
        Deactivate configuration

        :param frameReference: Frame reference
        :type frameReference: Uint16
        :return: Structure with error information.
        :rtype: :py:class:`~PyPlcnextRsc.Arp.Io.Axioline.Services.AxioResult`.
        """
        pass

    @RemotingMethod(7)
    def ResetMaster(self) -> AxioResult:
        """
        Reset AXIO master

        :return: Structure with error information.
        :rtype: :py:class:`~PyPlcnextRsc.Arp.Io.Axioline.Services.AxioResult`.
        """
        pass
