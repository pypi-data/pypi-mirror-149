# Copyright (c) 2021 Phoenix Contact. All rights reserved.
# Licensed under the MIT. See LICENSE file in the project root for full license information.

import functools

from PyPlcnextRsc.common.internalEnums.string_encoding import RscStringEncoding
from PyPlcnextRsc.common.tag_type import RscType

__all__ = [
    "Marshal",
    "MarshalAs",
    "_MarshalData",
]


@functools.lru_cache()
def Marshal(
        rscStringEncoding: RscStringEncoding = RscStringEncoding.Null,
        maxStringSize: int = -1,
        rscType: RscType = RscType.Null, ):
    if rscStringEncoding != RscStringEncoding.Null and rscStringEncoding is not None and rscType != RscType.SecureString:
        if rscStringEncoding == RscStringEncoding.Utf8:
            rscType = RscType.Utf8String
        elif rscStringEncoding == RscStringEncoding.Ansi:
            rscType = RscType.AnsiString
        elif rscStringEncoding == RscStringEncoding.Utf16:
            rscType = RscType.Utf16String
    return _MarshalData(rscStringEncoding=rscStringEncoding, maxStringSize=maxStringSize, rscType=rscType)


class _MarshalData:
    def __init__(self,
                 rscStringEncoding: RscStringEncoding = RscStringEncoding.Null,
                 maxStringSize: int = -1,
                 rscType: RscType = RscType.Null,
                 ):
        self.rscStringEncoding = rscStringEncoding
        self.maxStringSize = maxStringSize
        self.rscType = rscType


def MarshalAs(*arg, **kwargs):
    def decorator(cls):
        cls._marshal = Marshal(*arg, **kwargs)
        return cls

    return decorator
