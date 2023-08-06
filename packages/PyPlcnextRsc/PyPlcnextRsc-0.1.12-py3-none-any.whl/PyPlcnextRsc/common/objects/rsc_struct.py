# Copyright (c) 2021 Phoenix Contact. All rights reserved.
# Licensed under the MIT. See LICENSE file in the project root for full license information.

import warnings
from copy import deepcopy

from PyPlcnextRsc.common.exceptions import InvalidOperationException, CommonRemotingClientException
from PyPlcnextRsc.common.tag_type import RscType
from PyPlcnextRsc.common.types import RscTpNamedTuple

__all__ = [
    'RscStructBuilder',
    'RscStructMeta',
    'GetFieldFromInstance',
    "RscStruct",
    "isRscStructInstance",
    "isRscStructType",
]

RscStruct = RscTpNamedTuple
"""
Represent the struct type with Rsc

.. note::

    At current version ,this is equal to NamedTuple 

Usage:

    .. code:: python

        class ST_Prototype0(RscStruct):
            F0: IecAnnotation.INT
            F1: IecAnnotation.INT
            F2: IecAnnotation.BOOL    

        class ST_Prototype1(RscStruct):
            F1: bool
            F2: int
            F3: RscSequence

        class ST_Prototype2(RscStruct):
            Field1: RscTpAnnotate[int, Marshal(rscType=RscType.Int16)]
            Field2: bool
            Field3: str
            Field_another_struct: ST_Prototype1
            Field5: RscSequence

"""


def isRscStructInstance(value):
    """
    Test whether the given value is the instance of RscStruct
    """
    return hasattr(value, "_field_defaults") and hasattr(value, "_fields") and type(value) != type


def isRscStructType(value):
    """
    Test whether the given value is the prototype (or called 'type') of RscStruct
    """
    return hasattr(value, "_field_defaults") and hasattr(value, "_fields") and type(value) == type


class RscStructBuilder:
    """
    This is a wrapper around RscStruct , supporting filling fields step by step

    Normally this is auto created by :py:class:`PyPlcnextRsc.tools.PlcDataTypeSchema`

    .. note::
        This class has overload the __eq__ method , so this builder instance is compareable to *RscStruct*


    .. tip::

        Since V0.1.4 :

            '_friendlyMode':

            A syntactic sugar for Array (as a field in Struct) operation has been added
            'Struct.ArrField = [100, 200, 300]' in now allowed (the old way is 'Struct.ArrField[:] = [100, 200, 300]').

    Usage:

        .. code:: python

            class ST_Prototype(RscStruct):
                F0: IecAnnotation.INT
                F1: IecAnnotation.INT
                F2: IecAnnotation.BOOL


            # Not possible to init fields' value separately:
            # st = ST_Prototype()
            # st.F0 = 0
            # st.F1 = 100 # Illegal ! , because 'RscStruct' is tuple in fact
            # st.F2 = False

            # You can only instance it by the following way:
            # st = ST_Prototype(0,100,False)

            # use RscStructBuilder:
            builder = RscStructBuilder(ST_Prototype)
            builder(F0 = 0,F1 = 100,F2 = False) # by __call__
            builder.F1 = 200    # by set attribute
            builder.F2 = True

            # not necessary for user to call _getRscStruct because it will auto invoke while sending to PLC
            st = builder._getRscStruct()

    :param prototype: RscStruct prototype
    :type prototype: :py:class:`~PyPlcnextRsc.common.objects.rsc_struct.RscStruct`
    :param defaults: dict with field name and it's default value if supplied, default it None.
    :type defaults: dict
    """

    def __init__(self, prototype, defaults=None):
        self._proto = prototype
        from PyPlcnextRsc.common.transport import DataTagContext
        self._proto_context = DataTagContext.factory(prototype)
        field_names = prototype._fields
        value_map = deepcopy(prototype._field_defaults)
        if defaults is None:
            defaults = {}
        for field, value in defaults.items():
            if field in field_names:
                value_map[field] = value
            else:
                warnings.warn("Have Unknow default value")
        self._value_map = value_map
        self._last_value_map = {}
        self._last_result = None
        self._call_param_checker = None
        # self._repr_fmt = '(' + ', '.join(f'{name}=%r' for name in field_names) + ')'

        self._friendlyMode = True  # a switch to control syntactic sugar for Struct.ArrField[:] = [1,2,3] to Struct.ArrField = [1,2,3]

    def __getattribute__(self, item):
        if item.startswith("_"):
            return super().__getattribute__(item)
        else:
            if item in self._proto._fields:
                return self._value_map.get(item, None)
            else:
                raise AttributeError(f'{self._proto.__name__} object has no attribute {item}')

    def __setattr__(self, key, value):
        from PyPlcnextRsc.common.objects.rsc_sequence import RscList
        if key.startswith("_"):
            super().__setattr__(key, value)
        else:
            field_names = self._proto._fields
            if key in field_names:
                idx = field_names.index(key)
                inner_val = self._value_map[key]
                # the following statement is for : Struct.ArrField = [1,2,3]
                # only a syntactic sugar , but maybe sometime it will not be desired, use 'self._friendlyMode' to switch.
                if self._friendlyMode:
                    if isinstance(inner_val, RscList) and not isinstance(value, RscList):
                        inner_val._internal_setter(value)
                    elif isinstance(inner_val, RscStructBuilder) and not isinstance(value, RscStructBuilder):
                        inner_val._internal_setter(value)
                    else:
                        self._proto_context.subTag[idx].checkValueValid(value)
                        self._value_map[key] = value
                else:
                    # if not in friendlyMode directly push value in map
                    self._proto_context.subTag[idx].checkValueValid(value)
                    self._value_map[key] = value
            else:
                raise AttributeError(f'{self._proto.__name__} object has no attribute {key}')

    def _internal_setter(self, value):
        if isinstance(value, (list, tuple)):
            if len(self._proto._fields) != len(value):
                raise ValueError("Must keep the same size if using list or tuple to fill struct")
            self.__call__(*value)

        elif isinstance(value, dict):
            for field_key, val in value.items():
                self.__setattr__(field_key, val)

    def __call__(self, *args, **kwargs):
        field_names = self._proto._fields
        if not self._call_param_checker:
            num_fields = len(field_names)
            arg_list = ', '.join(field_names)
            if num_fields == 1:
                arg_list += ','
            self._call_param_checker = eval(f"lambda {arg_list}:({arg_list})")
        values = self._call_param_checker(*args, **kwargs)
        for key, value in zip(field_names, values):
            self.__setattr__(key, value)
            # idx = field_names.index(key)
            # self._proto_context.subTag[idx].checkValueValid(value)
            # self._value_map[key] = value
        return self

    def __repr__(self):
        return self._proto.__name__ + str(self._value_map)

    def _getRscStruct(self):
        def create_new():
            proto = self._proto
            value_map = self._value_map
            if len(value_map) != len(proto._fields):
                raise ValueError("Missing parameters")
            return proto(**value_map)

        if self._last_value_map == self._value_map:
            if self._last_result is None:
                self._last_result = create_new()
            return self._last_result
        else:
            self._last_result = create_new()
            self._last_value_map = deepcopy(self._value_map)
            return self._last_result

    def __eq__(self, other):
        if isinstance(other, tuple):
            try:
                return self._getRscStruct() == other
            except:
                return False
        else:
            return super(RscStructBuilder, self).__eq__(other)


class RscStructMeta(tuple):
    """
    Meta-data to represent Struct for transferring with device,
    it carriers all necessary information of each fields such as :py:class:`~PyPlcnextRsc.common.tag_type.RscType`

    Should always used as a value in :py:class:`~PyPlcnextRsc.common.objects.rsc_variant.RscVariant` , and every element are always :py:class:`~PyPlcnextRsc.common.objects.rsc_variant.RscVariant` too
    """

    @classmethod
    def fromInstance(cls, struct_instance):
        """
        Create RscStructMeta from a :py:class:`~PyPlcnextRsc.common.objects.rsc_struct.RscStruct` instance or :py:class:`~PyPlcnextRsc.common.objects.rsc_struct.RscStructBuilder`

        :param struct_instance: struct instance, which can be an instance of :py:class:`~PyPlcnextRsc.common.objects.rsc_struct.RscStruct` directly or :py:class:`~PyPlcnextRsc.common.objects.rsc_struct.RscStructBuilder`
        :type struct_instance: :py:class:`~PyPlcnextRsc.common.objects.rsc_struct.RscStruct` instance or :py:class:`~PyPlcnextRsc.common.objects.rsc_struct.RscStructBuilder`
        """
        if isinstance(struct_instance, RscStructBuilder):
            struct_instance = struct_instance._getRscStruct()

        if not isRscStructInstance(struct_instance):
            raise InvalidOperationException("must pass in RscStruct or RscStructBuilder instance")
        struct_type = type(struct_instance)
        from PyPlcnextRsc.common.transport import DataTagContext
        ctx = DataTagContext.factory(struct_type)
        meta = []
        for idx, field in enumerate(GetFieldFromInstance(struct_instance)):
            fieldCtx = ctx.subTag[idx]
            field_rsc_type = fieldCtx.rsc_type
            from PyPlcnextRsc.common.objects.rsc_variant import RscVariant
            if field_rsc_type == RscType.Struct:
                meta.append(RscVariant(RscStructMeta.fromInstance(field), rscType=field_rsc_type))
            # elif field_rsc_type == RscType.Array:
            #     raise
            else:
                meta.append(RscVariant(field, rscType=field_rsc_type))

        return cls(meta)

    def GetAsRscStruct(self, struct_type, strictMode=True) -> RscStruct:
        """
        Generate certain RscStruct instances from provided :py:class:`~PyPlcnextRsc.common.objects.rsc_struct.RscStruct` type.

        :param struct_type: the type of :py:class:`~PyPlcnextRsc.common.objects.rsc_struct.RscStruct`.
        :type struct_type: :py:class:`~PyPlcnextRsc.common.objects.rsc_struct.RscStruct` type

        :param strictMode: check the shape and type in meta before generate, default is *True*.
        :type strictMode: bool

        :return: the instance of :py:class:`~PyPlcnextRsc.common.objects.rsc_struct.RscStruct` with all fields filled.
        :rtype: :py:class:`~PyPlcnextRsc.common.objects.rsc_struct.RscStruct`

        """

        if not isRscStructType(struct_type):
            raise InvalidOperationException("must pass in RscStruct type")
        from PyPlcnextRsc.common.transport import DataTagContext
        ctx = DataTagContext.factory(struct_type)
        return _GetAsRscStruct(self, ctx, strictMode)

    def __repr__(self):
        return f"RscStructMeta" + super(RscStructMeta, self).__repr__()


def GetFieldFromInstance(struct_like_instance):
    if hasattr(struct_like_instance, "_getRscStruct"):
        struct_like_instance = struct_like_instance._getRscStruct()

    if isRscStructInstance(struct_like_instance):
        # for RscStruct
        for fieldName in struct_like_instance._fields:
            if fieldName.startswith('_'):
                continue
            yield getattr(struct_like_instance, fieldName)
    else:
        # for other class
        for fieldName, val in struct_like_instance.__dict__.items():
            if fieldName.startswith('_'):
                continue
            yield val


def _GetAsRscStruct(fieldValuesFromRsc, ctx, strictMode=True):
    tmp_ret = []
    if strictMode:
        if ctx.rsc_type != RscType.Struct:
            raise InvalidOperationException("must pass in struct annotation")

        if ctx.fieldCounts != len(fieldValuesFromRsc):
            raise CommonRemotingClientException(f"struct field size not match ,should be {ctx.fieldCounts},but is {len(fieldValuesFromRsc)}")

        for idx, field in enumerate(fieldValuesFromRsc):
            t = ctx.subTag[idx].rsc_type
            if field.GetType() != t and t != RscType.Null:
                raise CommonRemotingClientException(
                    f"struct<{ctx.name}> field '{ctx.subTag[idx].name}' type mismatch ,excepted '{ctx.subTag[idx].rsc_type.name}' ,but is '{field.GetType().name}'")

    for idx, field in enumerate(fieldValuesFromRsc):
        currentFieldCtx = ctx.subTag[idx]
        tp = currentFieldCtx.rsc_type
        if tp == RscType.Null:  # any
            tmp_ret.append(field.GetValue())
        elif tp == RscType.Struct:
            tmp_ret.append(_GetAsRscStruct(field.GetValue(), currentFieldCtx, strictMode))
        else:
            tmp_ret.append(field.GetValue())

    return ctx.annotation(*tmp_ret)
