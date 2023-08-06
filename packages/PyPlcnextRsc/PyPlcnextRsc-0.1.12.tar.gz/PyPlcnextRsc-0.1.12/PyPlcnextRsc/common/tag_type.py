# Copyright (c) 2021 Phoenix Contact. All rights reserved.
# Licensed under the MIT. See LICENSE file in the project root for full license information.

from PyPlcnextRsc.common.types import RscTpIntEnum


class RscType(RscTpIntEnum):
    """Datatypes supported by Rsc."""

    Null = 0,
    """No data type set"""
    End = 255
    """End of stream (EOS)"""
    Void = 1
    """void or null object"""
    Bool = 2
    """bool type"""
    Char = 3
    """16 bit character"""
    Int8 = 4
    """signed 8 bit integer (I1)"""
    Uint8 = 5
    """unsigned 8 bit integer (U1)"""
    Int16 = 6
    """signed 16 bit integer (I2)"""
    Uint16 = 7
    """unsigned 16 bit integer (U2)"""
    Int32 = 8
    """signed 32 bit integer (I4)"""
    Uint32 = 9
    """unsigned 32 bit integer (U4)"""
    Int64 = 10
    """signed 64 bit integer (I8)"""
    Uint64 = 11
    """unsigned 64 bit integer (U8)"""
    Real32 = 12
    """32 bit floating point number (R4)"""
    Real64 = 13
    """64 bit floating point number (R8)"""
    Struct = 18
    """Complex datatype"""
    Utf8String = 19
    """Utf-8 string"""
    String = 14
    """String with undefined format. Deprecated with remoting version 4 used by common.In common context with at least remoting version 4 RscType String is mapped to Utf8String"""
    Array = 20
    """Array type"""
    Datetime = 23
    """Datetime"""
    Version = 24
    """Version"""
    Guid = 25
    """Universal unique ID"""
    AnsiString = 26
    """Ansi string, not implemented in common context"""
    Object = 28
    """Object type handled by common as :py:class:`~PyPlcnextRsc.common.objects.rsc_variant.RscVariant`"""
    Utf16String = 30
    """Utf-16 string, not implemented in common context"""
    Stream = 34
    """Stream type to marshal large data packets"""
    Enumerator = 35
    """Enumerator type"""
    SecureString = 36
    """String for security context"""
    Enum = 37
    """Enum type"""
    Dictionary = 38
    """Dictionary type"""
    SecurityToken = 39
    """Security token needed for security Services"""
    Exception = 40
    """Exception"""
    IecTime = 41
    """IEC type: TIME [int32]"""
    IecTime64 = 42
    """IEC type: LTIME [int64]"""
    IecDate = 43
    """IEC type: DATE [N/A]"""
    IecDate64 = 44
    """IEC type: LDATE [int64]"""
    IecDateTime = 45
    """IEC type: DATE_AND_TIME, DT [N/A]"""
    IecDateTime64 = 46
    """IEC type: LDATE_AND_TIME, LDT [int64]"""
    IecTimeOfDay = 47
    """IEC type: TIME_OF_DAY, TOD [N/A]"""
    IecTimeOfDay64 = 48
    """IEC type: LTIME_OF_DAY, LTOD [int64]"""


class IecType:
    """
    Concrete annotation for *IEC61131* data space

    this is just a helper map from *IEC61131* data type to :py:class:`~PyPlcnextRsc.common.tag_type.RscType`
    """
    Null = RscType.Null
    """Mapped to :py:const:`PyPlcnextRsc.common.tag_type.RscType.Null`"""
    TIME = RscType.IecTime
    """Mapped to :py:const:`PyPlcnextRsc.common.tag_type.RscType.IecTime`"""
    LTIME = RscType.IecTime64
    """Mapped to :py:const:`PyPlcnextRsc.common.tag_type.RscType.IecTime64`"""
    LDATE = RscType.IecDate64
    """Mapped to :py:const:`PyPlcnextRsc.common.tag_type.RscType.IecDate64`"""
    LDATE_AND_TIME = RscType.IecDateTime64
    """Mapped to :py:const:`PyPlcnextRsc.common.tag_type.RscType.IecDateTime64`"""
    LTIME_OF_DAY = RscType.IecTimeOfDay64
    """Mapped to :py:const:`PyPlcnextRsc.common.tag_type.RscType.IecTimeOfDay64`"""
    BOOL = RscType.Bool
    """Mapped to :py:const:`PyPlcnextRsc.common.tag_type.RscType.Bool`"""
    STRING = RscType.Utf8String
    """Mapped to :py:const:`PyPlcnextRsc.common.tag_type.RscType.Utf8String`"""
    LREAL = RscType.Real64
    """Mapped to :py:const:`PyPlcnextRsc.common.tag_type.RscType.Real64`"""
    REAL = RscType.Real32
    """Mapped to :py:const:`PyPlcnextRsc.common.tag_type.RscType.Real32`"""
    LWORD = RscType.Uint64
    """Mapped to :py:const:`PyPlcnextRsc.common.tag_type.RscType.Uint64`"""
    DWORD = RscType.Uint32
    """Mapped to :py:const:`PyPlcnextRsc.common.tag_type.RscType.Uint32`"""
    WORD = RscType.Uint16
    """Mapped to :py:const:`PyPlcnextRsc.common.tag_type.RscType.Uint16`"""
    BYTE = RscType.Uint8
    """Mapped to :py:const:`PyPlcnextRsc.common.tag_type.RscType.Uint8`"""
    LINT = RscType.Int64
    """Mapped to :py:const:`PyPlcnextRsc.common.tag_type.RscType.Int64`"""
    DINT = RscType.Int32
    """Mapped to :py:const:`PyPlcnextRsc.common.tag_type.RscType.Int32`"""
    INT = RscType.Int16
    """Mapped to :py:const:`PyPlcnextRsc.common.tag_type.RscType.Int16`"""
    SINT = RscType.Int8
    """Mapped to :py:const:`PyPlcnextRsc.common.tag_type.RscType.Int8`"""
    ULINT = RscType.Uint64
    """Mapped to :py:const:`PyPlcnextRsc.common.tag_type.RscType.Uint64`"""
    UDINT = RscType.Uint32
    """Mapped to :py:const:`PyPlcnextRsc.common.tag_type.RscType.Uint32`"""
    UINT = RscType.Uint16
    """Mapped to :py:const:`PyPlcnextRsc.common.tag_type.RscType.Uint16`"""
    USINT = RscType.Uint8
    """Mapped to :py:const:`PyPlcnextRsc.common.tag_type.RscType.Uint8`"""
