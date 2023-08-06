# Copyright (c) 2021 Phoenix Contact. All rights reserved.
# Licensed under the MIT. See LICENSE file in the project root for full license information.
from enum import (
    IntEnum as _IntEnum,
    IntFlag as _IntFlag,
    _decompose as _normal_decompose,
    Enum as _Enum
)

from PyPlcnextRsc.common.sys_util import SPHINX_AUTODOC_RUNNING

# Handle with sphinx for doc generate
# if types all from _rsc_typing_lib the doc will not generate the signature,
# so have to reindex the types in project from typing.py
# And another problem is some new type (Annotated, List) are different between 3.9 with lower
# so did a job to switch index again.
if SPHINX_AUTODOC_RUNNING:
    from PyPlcnextRsc.common.sys_util import PYVER_IS_NEW_THAN
    from typing import (
        NamedTuple as _NamedTuple,
        Callable as _Callable,
        Tuple as _Tuple,
        Sequence as _Sequence,
        Dict as _Dict,
        Union as _Union,
        get_origin as _get_origin,
        get_args as _get_args,
        _SpecialForm as __SpecialForm
    )

    if PYVER_IS_NEW_THAN(3, 9, 0):
        from typing import Annotated as _Annotated, List as _List
    else:
        from PyPlcnextRsc.common.types._rsc_typing_lib import Annotated as _Annotated, List as _List

else:
    # At runtime, all types used by this project are indexed from _rsc_typing_lib
    # to make sure python version is compatible widely.
    from PyPlcnextRsc.common.types._rsc_typing_lib import (
        NamedTuple as _NamedTuple,
        Callable as _Callable,
        Annotated as _Annotated,
        Tuple as _Tuple,
        List as _List,
        Sequence as _Sequence,
        Dict as _Dict,
        Union as _Union,
        get_origin as _get_origin,
        get_args as _get_args,
        _SpecialForm as __SpecialForm
    )

__all__ = [

    "RscFlag",
    "RscOutParam",
    "RscEnumerator",

    "RscTpEnum",
    "RscTpIntEnum",
    "RscTpAnnotate",
    "RscTpTuple",
    "RscTpList",
    "RscTpDict",
    "RscTpSequence",
    "RscTpUnion",
    "RscTpGetOrigin",
    "RscTpGetArgs",
    "RscTpSpecialForm",
    "RscTpNamedTuple"
]

RscTpNamedTuple = _NamedTuple
RscOutParam = _Callable
RscTpEnum = _Enum
RscTpIntEnum = _IntEnum
RscTpAnnotate = _Annotated
RscTpTuple = _Tuple
RscTpList = _List
RscTpDict = _Dict
RscTpSequence = _Sequence
RscTpUnion = _Union
RscTpGetOrigin = _get_origin
RscTpGetArgs = _get_args
RscTpSpecialForm = __SpecialForm


class _FlagWithStatus(_IntFlag):
    @classmethod
    def _create_pseudo_member_(cls, value):
        if not hasattr(cls, "__STATE_MASK__"):
            return super()._create_pseudo_member_(value)
        if not hasattr(cls, "__FLAGS_MASK__"):
            raise TypeError("missing __FLAGS_MASK__ in " + str(cls))
        pseudo_member = cls._value2member_map_.get(value, None)
        if pseudo_member is None:
            need_to_create = [value]
            # get unaccounted for bits
            _, extra_flags_status = _FlagWithStatus._decompose(cls, value)

            extra_state_part = extra_flags_status & cls.__STATE_MASK__
            extra_flag_part = extra_flags_status & cls.__FLAGS_MASK__

            if extra_state_part:
                need_to_create.append(extra_state_part)

            while extra_flag_part:
                flag_value = 2 ** (extra_flag_part.bit_length() - 1)

                if flag_value not in cls._value2member_map_ and flag_value not in need_to_create:
                    need_to_create.append(flag_value)
                if extra_flag_part == -flag_value:
                    extra_flag_part = 0
                else:
                    extra_flag_part ^= flag_value

            for value in reversed(need_to_create):
                # construct singleton pseudo-members
                pseudo_member = int.__new__(cls, value)
                pseudo_member._name_ = None
                pseudo_member._value_ = value
                # use setdefault in case another thread already created a composite
                # with this value
                pseudo_member = cls._value2member_map_.setdefault(value, pseudo_member)
        return pseudo_member

    def __repr__(self):
        cls = self.__class__
        if self._name_ is not None:
            return '<%s.%s: %r>' % (cls.__name__, self._name_, self._value_)
        members, uncovered = _FlagWithStatus._decompose(cls, self._value_)
        return '<%s.%s: %r>' % (
            cls.__name__,
            '|'.join([str(m._name_ or m._value_) for m in members]),
            self._value_,
        )

    def __str__(self):
        cls = self.__class__
        if self._name_ is not None:
            return '%s.%s' % (cls.__name__, self._name_)
        members, uncovered = _FlagWithStatus._decompose(cls, self._value_)
        if len(members) == 1 and members[0]._name_ is None:
            return '%s.%r' % (cls.__name__, members[0]._value_)
        else:
            return '%s.%s' % (
                cls.__name__,
                '|'.join([str(m._name_ or m._value_) for m in members]),
            )

    def __invert__(self):
        members, uncovered = _FlagWithStatus._decompose(self.__class__, self._value_)
        inverted = self.__class__(0)
        for m in self.__class__:
            if m not in members and not (m._value_ & self._value_):
                inverted = inverted | m
        return self.__class__(inverted)

    @staticmethod
    def _decompose(flag, value):
        """Extract all members from the value."""
        if not hasattr(flag, '__STATE_MASK__'):
            return _normal_decompose(flag, value)
        not_covered = value
        negative = value < 0
        members = []
        state_part = value & flag.__STATE_MASK__
        flag_part = value & flag.__FLAGS_MASK__
        if state_part in flag._value2member_map_:
            state = flag._value2member_map_[state_part]
            members.append(state)
            not_covered &= ~state_part
        if not negative:
            not_covered_flag = flag_part
            while not_covered_flag:
                flag_value = 2 ** (not_covered_flag.bit_length() - 1)
                if flag_value in flag._value2member_map_:
                    members.append(flag._value2member_map_[flag_value])
                    not_covered &= ~flag_value
                not_covered_flag &= ~flag_value
        if not members and value in flag._value2member_map_:
            members.append(flag._value2member_map_[value])
        members.sort(key=lambda m: m._value_, reverse=False)
        if len(members) > 1 and members[-1].value == value:
            members.pop(0)
        return members, not_covered


RscFlag = _FlagWithStatus


class RscEnumerator(RscTpList):
    ...
