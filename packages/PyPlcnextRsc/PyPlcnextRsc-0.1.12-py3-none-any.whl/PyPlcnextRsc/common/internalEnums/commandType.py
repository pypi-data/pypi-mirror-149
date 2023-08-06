# Copyright (c) 2021 Phoenix Contact. All rights reserved.
# Licensed under the MIT. See LICENSE file in the project root for full license information.

from PyPlcnextRsc.common.types import RscTpIntEnum

__all__ = ["CommandType"]


class CommandType(RscTpIntEnum):
    GetServiceRequest = 0  # Deprecation
    GetServiceConfirmation = 1  # Deprecation
    InvokeRequest = 2
    InvokeConfirmation = 3
    Error = 4
    # IAmAlive = 5
    # CommunicationTest = 6
    ConnectRequest = 7
    ConnectConfirm = 8
    DisconnectRequest = 9
    DisconnectConfirm = 10
    GetServiceExtRequest = 11
    GetServiceExtConfirmation = 12
    GetServiceProviderRequest = 13
    GetServiceProviderConfirmation = 14
    # IpcGetServiceInfoRequest = 66
    # IpcGetServiceInfoConfirmation = 67
