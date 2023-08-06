# Copyright (c) 2021 Phoenix Contact. All rights reserved.
# Licensed under the MIT. See LICENSE file in the project root for full license information.

from PyPlcnextRsc.common.objects.rsc_sequence import *
from PyPlcnextRsc.common.objects.rsc_stream import *
from PyPlcnextRsc.common.objects.rsc_struct import *
from PyPlcnextRsc.common.objects.rsc_variant import *


class Version:
    def __init__(self):
        self.major = 0
        self.minor = 0
        self.build = 0
        self.revision = 0


class SecurityToken:
    HEADER_SIZE = 4

    def __init__(self, value):
        self.value = value

    def getValue(self):
        return self.value

    def hasValue(self):
        return self.value is not None and self.value.GetValue() is not None

    def getToken(self):
        return self.value.GetValue()
