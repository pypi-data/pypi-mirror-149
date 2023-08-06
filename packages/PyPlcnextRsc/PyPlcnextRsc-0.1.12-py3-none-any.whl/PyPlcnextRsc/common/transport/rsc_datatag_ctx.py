# Copyright (c) 2021 Phoenix Contact. All rights reserved.
# Licensed under the MIT. See LICENSE file in the project root for full license information.

import collections
import functools
import logging
from datetime import datetime
from enum import Enum
from inspect import signature
from uuid import UUID

from PyPlcnextRsc.common.exceptions import InvalidOperationException
from PyPlcnextRsc.common.internalEnums.string_encoding import RscStringEncoding
from PyPlcnextRsc.common.objects import *
from PyPlcnextRsc.common.serviceDefinition.marshal import Marshal, _MarshalData
from PyPlcnextRsc.common.tag_type import RscType
from PyPlcnextRsc.common.types import *
from PyPlcnextRsc.common.util import SearchInstance

__all__ = [
    "DataTagContext"
]


def _GetMarshalFromEnum(enum):
    """
    从枚举类型或枚举实例（具体条目）中获取Marshal
    """
    if hasattr(enum, "_marshal"):
        return getattr(enum, "_marshal")
    else:
        raise ValueError("Can not get Marshal from " + str(enum))


CHECK_TYPE_ONLY = 1
CHECK_LIMIT = 2

RSC_TYPE_PY_MAP = {
    RscType.Bool: (CHECK_TYPE_ONLY, bool,),
    RscType.Int64: (CHECK_LIMIT, int, -9223372036854775808, 9223372036854775807),
    RscType.Int32: (CHECK_LIMIT, int, -2147483648, 2147483647),
    RscType.Int16: (CHECK_LIMIT, int, -32768, 32767),
    RscType.Int8: (CHECK_LIMIT, int, -127, 128),
    RscType.Uint64: (CHECK_LIMIT, int, 0, 18446744073709551615),
    RscType.Uint32: (CHECK_LIMIT, int, 0, 4294967295),
    RscType.Uint16: (CHECK_LIMIT, int, 0, 65535),
    RscType.Uint8: (CHECK_LIMIT, int, 0, 255),
    RscType.Char: (CHECK_TYPE_ONLY, str,),
    # RscType.AnsiString: (CHECK_TYPE_ONLY, str,),
    # RscType.Utf8String: (CHECK_TYPE_ONLY, str,),
    # RscType.Utf16String: (CHECK_TYPE_ONLY, str,),
    RscType.Real32: (CHECK_TYPE_ONLY, float,),
    RscType.Real64: (CHECK_TYPE_ONLY, float,),
    RscType.Stream: (CHECK_TYPE_ONLY, RscStream,),
    RscType.Object: (CHECK_TYPE_ONLY, RscVariant,),

    RscType.IecTime: (CHECK_LIMIT, int, -2147483648, 2147483647),
    RscType.IecTime64: (CHECK_LIMIT, int, -9223372036854775808, 9223372036854775807),
    RscType.IecDate64: (CHECK_LIMIT, int, -9223372036854775808, 9223372036854775807),
    RscType.IecDateTime64: (CHECK_LIMIT, int, -9223372036854775808, 9223372036854775807),
    RscType.IecTimeOfDay64: (CHECK_LIMIT, int, -9223372036854775808, 9223372036854775807),
}


class DataTagContext:
    logger = logging.getLogger(__name__ + '.' + 'DataTagContext')

    @classmethod
    def Read(cls, remotingReader):
        t = remotingReader.ReadTag()
        tag = cls()
        tag.rsc_type = t
        if t == RscType.Array:
            tag.subTag.append(DataTagContext.Read(remotingReader))
        elif t == RscType.Struct:
            tag.fieldCounts = remotingReader.ReadFieldCount()
        if cls.logger.isEnabledFor(logging.DEBUG):
            cls.logger.debug(f"Read TagCtx, result:{tag}")
        return tag

    def Write(self, remotingWriter):
        if self.logger.isEnabledFor(logging.DEBUG):
            self.logger.debug(f"Write TagCtx :{self}")

        t = self.rsc_type
        if t == RscType.Enum:
            self.subTag[0].Write(remotingWriter)
        else:
            remotingWriter.WriteTag(t)
            if t == RscType.Array:
                assert len(self.subTag) > 0
                self.subTag[0].Write(remotingWriter)
            elif t == RscType.Struct:
                remotingWriter.WriteFieldCount(self.fieldCounts)

    @classmethod
    @functools.lru_cache(maxsize=4096, typed=True)
    def factory(cls, annotation, param_name=None, marshal=None):
        cls.logger.debug(f"factory:annotation={annotation},param_name={param_name}")
        """
        通过注解获取DataTagContext
        """
        context = cls()
        if param_name:
            context.name = param_name
        elif hasattr(annotation, '__name__'):
            context.name = annotation.__name__
        else:
            context.name = ''

        context.annotation = annotation
        if marshal:
            _marshal_rsc_type = marshal.rscType
            context.string_encoding = marshal.rscStringEncoding
            context.max_string_length = marshal.maxStringSize
            if not (_marshal_rsc_type is None or marshal.rscType == RscType.Null):
                context.rsc_type = _marshal_rsc_type
                return context
        try:
            # 单独检查Enum(因为Enum是实例)
            if issubclass(annotation, Enum):
                context.rsc_type = RscType.Enum
                context.subTag.append(DataTagContext(rscType=_GetMarshalFromEnum(annotation).rscType))  # TODO 是否添加默认值Int32
                return context
        except TypeError:
            ...
        except Exception as e:
            raise e

        type_class = RscTpGetOrigin(annotation)
        if type_class is None:
            if type(annotation) == type:
                # 已经是基本类型 ， 例如bool str ， 或者自定义类型、结构体
                type_class = annotation
            else:
                #
                type_class = type(annotation)

        if type_class:
            if type_class == RscTpSpecialForm or (hasattr(annotation, '__name__') and annotation.__name__ == "any"):  # Any , only used in User Struct Def
                context.rsc_type = RscType.Null

            elif type_class == RscTpAnnotate:
                # 注解
                args = RscTpGetArgs(annotation)
                annotation_real = args[0]
                extra_infos = args[1:]
                # 从注解中获取 Marshal 对象
                marshal = SearchInstance(extra_infos, _MarshalData)

                if not marshal and len(extra_infos) == 1:
                    single_param = extra_infos[0]
                    if isinstance(single_param, RscType):
                        marshal = Marshal(rscType=single_param)
                    elif isinstance(single_param, RscStringEncoding):
                        marshal = Marshal(rscStringEncoding=single_param)

                context = DataTagContext.factory(annotation_real, param_name=param_name, marshal=marshal)
            elif isRscStructType(annotation):
                context.rsc_type = RscType.Struct
                for n, p in signature(type_class).parameters.items():
                    if n.startswith("_"):
                        continue
                    context.subTag.append(DataTagContext.factory(p.annotation, n))
                context.fieldCounts = len(context.subTag)
            elif type_class == collections.abc.Callable:
                input_args, return_arg = RscTpGetArgs(annotation)

                context = DataTagContext.factory(input_args[0], param_name=param_name)
                context.isOut = True

            elif type_class in [list, tuple, collections.abc.Sequence]:
                context.rsc_type = RscType.Array
                element_annotations = RscTpGetArgs(annotation)
                if len(element_annotations) == 0:
                    raise InvalidOperationException("must supply array element in annotation")
                context.subTag.append(DataTagContext.factory(element_annotations[0]))

            elif type_class == RscSequence:  # in user struct def
                context.rsc_type = RscType.Array  # TODO : necessary to generate subTag for strict checking?

            elif type_class == RscEnumerator:
                context.rsc_type = RscType.Enumerator
                element_annotation = RscTpGetArgs(annotation)[0]
                context.subTag.append(DataTagContext.factory(element_annotation))
            elif type_class == dict:
                context.rsc_type = RscType.Dictionary
                keyAnnotation, valueAnnotation = RscTpGetArgs(annotation)
                context.subTag.append(DataTagContext.factory(keyAnnotation))
                context.subTag.append(DataTagContext.factory(valueAnnotation))
            elif type_class == bool:
                context.rsc_type = RscType.Bool
            elif type_class == str:
                context.rsc_type = RscType.Utf8String
                context.max_string_length = 512
            elif type_class == int:
                # set Int32 by default , usually should use Marshal to define the tag
                context.rsc_type = RscType.Int32
            elif issubclass(type_class, RscFlag):
                context.rsc_type = RscType.Enum
                context.subTag.append(DataTagContext(rscType=_GetMarshalFromEnum(annotation).rscType))
            elif type_class == Version:
                context.rsc_type = RscType.Version
            elif type_class == UUID:
                context.rsc_type = RscType.Guid
            elif type_class == datetime:
                context.rsc_type = RscType.Datetime
            elif type_class == RscVariant:
                context.rsc_type = RscType.Object
            elif type_class == SecurityToken:
                context.rsc_type = RscType.SecurityToken
            elif type_class == RscStream:
                context.rsc_type = RscType.Stream
            else:

                raise ValueError("Un implement type_class " + str(type_class))
        else:
            raise ValueError("Un implement annotation " + str(annotation))
        return context

    def __repr__(self):
        return f"TagCtx<{self.rsc_type.name}>" + str(self.subTag)

    def __init__(self,
                 annotation=None,
                 rscType: RscType = RscType.Null,
                 string_encoding: RscStringEncoding = RscStringEncoding.Null,
                 max_string_length: int = -1,
                 ):

        if rscType != RscType.Null and rscType is not None:
            if rscType == RscType.Utf8String:
                string_encoding = RscStringEncoding.Utf8
            elif rscType == RscType.AnsiString:
                string_encoding = RscStringEncoding.Ansi
            elif rscType == RscType.Utf16String:
                string_encoding = RscStringEncoding.Utf16
        elif string_encoding != RscStringEncoding.Null and string_encoding is not None and rscType != RscType.SecureString:
            if string_encoding == RscStringEncoding.Utf8:
                rscType = RscType.Utf8String
            elif string_encoding == RscStringEncoding.Ansi:
                rscType = RscType.AnsiString
            elif string_encoding == RscStringEncoding.Utf16:
                rscType = RscType.Utf16String

        self._rsc_type = rscType
        self.string_encoding = string_encoding
        self.annotation = annotation
        self.max_string_length = max_string_length
        self.isOut = False
        self.subTag = []
        self.fieldCounts = 0
        self.name = ''

    @property
    def rsc_type(self):
        return self._rsc_type

    @rsc_type.setter
    def rsc_type(self, t):
        if t == RscType.Utf8String:
            self.string_encoding = RscStringEncoding.Utf8
        elif t == RscType.Utf16String:
            self.string_encoding = RscStringEncoding.Utf16
        elif t == RscType.AnsiString:
            self.string_encoding = RscStringEncoding.Ansi
        self._rsc_type = t

    def checkValueValid(self, value):
        rscType = self.rsc_type
        if rscType in RSC_TYPE_PY_MAP:
            test_suit = RSC_TYPE_PY_MAP[rscType]
            py_should_type = test_suit[1]
            if type(value) != py_should_type:
                raise ValueError(f"Expect type '{py_should_type.__name__}' for parameter {self.name} , but '{type(value).__name__}' was given")
            if test_suit[0] == CHECK_LIMIT:
                if value > test_suit[3] or test_suit[2] > value:
                    raise ValueError(f"Limit exceed ! for RscType.{rscType.name}:min='{test_suit[2]}',max='{test_suit[3]}' for parameter {self.name} , but '{value}' was given!")
        elif rscType in [RscType.Utf8String, RscType.Utf16String, RscType.AnsiString]:
            if type(value) != str:
                raise ValueError(f"Expect type 'str' for parameter {self.name} , but '{type(value).__name__}' was given")
            maxLen = self.max_string_length
            if 0 < self.max_string_length < len(value):
                raise ValueError(f"The length of string for parameter {self.name} must not exceed {maxLen} but is {len(value)}")
        elif rscType == RscType.Struct:
            if isinstance(value, RscStructMeta):
                return
            if isinstance(value, RscStructBuilder):
                final_ctx = value._proto_context
            elif isRscStructInstance(value):
                final_ctx = DataTagContext.factory(type(value))
            else:
                raise ValueError(f"Expect struct-like instance for parameter {self.name} , but '{type(value).__name__}' was given")

            if final_ctx.fieldCounts != self.fieldCounts:
                raise ValueError(f"Expect struct has {self.fieldCounts} fields but {final_ctx.fieldCounts} was given")

        elif rscType == RscType.Array:
            if not isinstance(value, (tuple, list, RscSequence)):
                raise ValueError(f"Expect array-like type for parameter {self.name} , but '{type(value).__name__}' was given")

            if isinstance(value, RscSequence):
                desire_length = value.getDesireLength()
                if -1 < desire_length != len(value):
                    raise ValueError(f"Expect {desire_length} element{'s' if desire_length > 1 else ''} in array, but is {len(value)} !")
