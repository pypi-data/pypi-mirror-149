# Copyright (c) 2021 Phoenix Contact. All rights reserved.
# Licensed under the MIT. See LICENSE file in the project root for full license information.

from PyPlcnextRsc.common.serviceDefinition.all_needed import *

__all__ = [
    "DataType"
]


@MarshalAs(rscType=RscType.Uint32)
class DataType(RscFlag):
    """
    DataType

    """
    NONE = 0
    """Unspecified."""
    Void = 1
    """Void - Arp C++ empty type"""
    Bit = 2
    """Bit - Arp C++ data type (1 Byte)"""
    Boolean = 3
    """Boolean - Arp C++ data type (1 Byte)"""
    UInt8 = 4
    """UInt8 - Arp C++ data type (1 Byte)"""
    Int8 = 5
    """Int8 - Arp C++ data type (1 Byte)"""
    Char8 = 6
    """Char8 - Arp C++ data type (1 Byte)"""
    Char16 = 7
    """Char16 - Arp C++ data type (2 Byte)"""
    UInt16 = 8
    """UInt16 - Arp C++ data type (2 Byte)"""
    Int16 = 9
    """Int16 - Arp C++ data type (2 Byte)"""
    UInt32 = 10
    """UInt32 - Arp C++ data type (4 Byte)"""
    Int32 = 11
    """Int32 - Arp C++ data type (4 Byte)"""
    UInt64 = 12
    """UInt64 - Arp C++ data type (8 Byte)"""
    Int64 = 13
    """Int64 - Arp C++ data type (8 Byte)"""
    Float32 = 14
    """Float32 - Arp C++ data type (4 Byte)"""
    Float64 = 15
    """Float64 - Arp C++ data type (8 Byte)"""
    Primitive = 32
    """Limit of primitive types"""
    DateTime = 33
    """C++ DateTime type"""
    IecTime = 34
    """IEC type: TIME [int32]"""
    IecTime64 = 35
    """IEC type: LTIME [int64]"""
    IecDate = 36
    """IEC type: DATE [N/A],Not supported by PCWE."""
    IecDate64 = 37
    """IEC type: LDATE [int64]"""
    IecDateTime = 38
    """IEC type: DATE_AND_TIME, DT [N/A],Not supported by PCWE."""
    IecDateTime64 = 39
    """IEC type: LDATE_AND_TIME, LDT [int64]"""
    IecTimeOfDay = 40
    """IEC type: TIME_OF_DAY, TOD [N/A],Not supported by PCWE."""
    IecTimeOfDay64 = 41
    """IEC type: LTIME_OF_DAY, LTOD [int64]"""
    StaticString = 42
    """Static String type"""
    IecString = 43
    """Iec String type, only for internal use"""
    ClrString = 44
    """.NET/C# String type, only for internal use"""
    String = 45
    """C++ String type, only for internal use"""
    Elementary = 64
    """Limit of elementary types."""
    ArrayElement = 65
    """ArrayOfArray"""
    Struct = 66
    """Struct"""
    Class = 67
    """Class"""
    FunctionBlock = 68
    """Function Block"""
    Subsystem = 69
    """Subsystem"""
    Program = 70
    """Program"""
    Component = 71
    """Component"""
    Library = 72
    """Library"""
    Complex = 254
    """Limit of complex types"""

    Pointer = 1 << 9
    """Determines a pointer type.Pointer are declared as :py:const:`PyPlcnextRsc.Arp.Plc.Commons.DataType.Elementary` kind."""
    Array = 1 << 10
    """Determines an array type.Arrays are declared as :py:const:`PyPlcnextRsc.Arp.Plc.Commons.DataType.Elementary` kind."""
    Enum = 1 << 11
    """Determines an Enumeration type.Enums are declared as :py:const:`PyPlcnextRsc.Arp.Plc.Commons.DataType.Elementary` kind."""
    Reference = 1 << 12
    """Determines a C# reference type.Reference are declared as :py:const:`PyPlcnextRsc.Arp.Plc.Commons.DataType.Elementary` kind."""
    BaseTypeMask = 0x00FF
    """For removing all flags"""

    __STATE_MASK__ = BaseTypeMask
    __FLAGS_MASK__ = (~__STATE_MASK__)
