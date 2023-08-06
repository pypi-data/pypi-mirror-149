# Copyright (c) 2021 Phoenix Contact. All rights reserved.
# Licensed under the MIT. See LICENSE file in the project root for full license information.

from PyPlcnextRsc.common.types import RscTpEnum

__all__ = ["RscStringEncoding"]


class RscStringEncoding(RscTpEnum):
    Null = 0,
    Ansi = 1,
    Utf8 = 2,
    Utf16 = 3
