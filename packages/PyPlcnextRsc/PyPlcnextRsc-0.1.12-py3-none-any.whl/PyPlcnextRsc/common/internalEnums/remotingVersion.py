# Copyright (c) 2021 Phoenix Contact. All rights reserved.
# Licensed under the MIT. See LICENSE file in the project root for full license information.

from PyPlcnextRsc.common.types import RscTpIntEnum

__all__ = ["RemotingVersion"]


class RemotingVersion(RscTpIntEnum):
    NONE = 0
    VERSION_1 = 1
    VERSION_2 = 2
    VERSION_3 = 3
    VERSION_4 = 4
    RECENT = VERSION_4
    UNKNOWN = 99
