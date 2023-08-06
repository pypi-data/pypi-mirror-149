# Copyright (c) 2021 Phoenix Contact. All rights reserved.
# Licensed under the MIT. See LICENSE file in the project root for full license information.
import sys

from PyPlcnextRsc.common.tag_type import IecType
from PyPlcnextRsc.common.types import RscTpAnnotate

__all__ = ["SearchInstance", "IecAnnotation", 'FatalVersionCheck']


def FatalVersionCheck():
    import sys
    if sys.version_info < (3, 7, 6):
        raise EnvironmentError("PyPlcnextRsc package can only run with python >= 3.7.6 !")


def SearchInstance(values, search):
    if type(values) not in (list, tuple, set):
        values = (values,)
    for arg in values:
        if isinstance(arg, search):
            return arg


class IecAnnotation:
    LDATE = RscTpAnnotate[int, IecType.LDATE]
    LDATE_AND_TIME = RscTpAnnotate[int, IecType.LDATE_AND_TIME]
    LTIME = RscTpAnnotate[int, IecType.LTIME]
    LTIME_OF_DAY = RscTpAnnotate[int, IecType.LTIME_OF_DAY]
    TIME = RscTpAnnotate[int, IecType.TIME]

    BOOL = RscTpAnnotate[bool, IecType.BOOL]
    STRING = RscTpAnnotate[str, IecType.STRING]

    LREAL = RscTpAnnotate[float, IecType.LREAL]
    REAL = RscTpAnnotate[float, IecType.REAL]

    LWORD = RscTpAnnotate[int, IecType.LWORD]
    DWORD = RscTpAnnotate[int, IecType.DWORD]
    WORD = RscTpAnnotate[int, IecType.WORD]
    BYTE = RscTpAnnotate[int, IecType.BYTE]

    USINT = RscTpAnnotate[int, IecType.USINT]
    UINT = RscTpAnnotate[int, IecType.UINT]
    UDINT = RscTpAnnotate[int, IecType.UDINT]
    ULINT = RscTpAnnotate[int, IecType.ULINT]

    LINT = RscTpAnnotate[int, IecType.LINT]
    DINT = RscTpAnnotate[int, IecType.DINT]
    INT = RscTpAnnotate[int, IecType.INT]
    SINT = RscTpAnnotate[int, IecType.SINT]


SPHINX_AUTODOC_RUNNING = "sphinx.ext.autodoc" in sys.modules
