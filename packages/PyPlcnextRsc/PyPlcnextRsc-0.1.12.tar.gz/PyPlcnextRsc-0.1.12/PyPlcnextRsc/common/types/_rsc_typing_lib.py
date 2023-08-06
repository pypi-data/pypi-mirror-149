"""
This file is copied from typing.py (Python 3.9)
Its' purpose is to make sure the package can run at lower python version

For technology reason ,this file have been modified carefully for lower python version

"""
import collections
import collections.abc
import functools
import operator
import sys
import types
from abc import abstractmethod, ABCMeta

__all__ = [
    'Annotated',
    'Any',
    'Callable',
    'ClassVar',
    'Final',
    'ForwardRef',
    'Generic',
    'Literal',
    'Optional',
    'Protocol',
    'Tuple',
    'Type',
    'TypeVar',
    'Union',
    'AbstractSet',
    'ByteString',
    'Container',
    'Hashable',
    'ItemsView',
    'Iterable',
    'Iterator',
    'KeysView',
    'Mapping',
    'MappingView',
    'MutableMapping',
    'MutableSequence',
    'MutableSet',
    'Sequence',
    'Sized',
    'ValuesView',
    'Awaitable',
    'AsyncIterator',
    'AsyncIterable',
    'Coroutine',
    'Collection',
    'AsyncGenerator',
    'Reversible',
    'SupportsBytes',
    'SupportsComplex',
    'SupportsFloat',
    'SupportsIndex',
    'SupportsInt',
    'ChainMap',
    'Counter',
    'Deque',
    'Dict',
    'DefaultDict',
    'List',
    'OrderedDict',
    'Set',
    'FrozenSet',
    'NamedTuple',
    'TypedDict',
    'Generator',
    'AnyStr',
    'cast',
    'final',
    'get_args',
    'get_origin',
    'get_type_hints',
    'NewType',
    'no_type_check',
    'no_type_check_decorator',
    'NoReturn',
    'overload',
    'runtime_checkable',
    'Text',
    'TYPE_CHECKING',
    "_SpecialForm",
]


def _type_check(arg, msg, is_argument=True):
    invalid_generic_forms = (Generic, Protocol)
    if is_argument:
        invalid_generic_forms = invalid_generic_forms + (ClassVar, Final)

    if arg is None:
        return type(None)
    if isinstance(arg, str):
        return ForwardRef(arg)
    if (isinstance(arg, _GenericAlias) and
            arg.__origin__ in invalid_generic_forms):
        raise TypeError(f"{arg} is not valid as type argument")
    if arg in (Any, NoReturn):
        return arg
    if isinstance(arg, _SpecialForm) or arg in (Generic, Protocol):
        raise TypeError(f"Plain {arg} is not valid as type argument")
    if isinstance(arg, (type, TypeVar, ForwardRef)):
        return arg
    if not callable(arg):
        raise TypeError(f"{msg} Got {arg!r:.100}.")
    return arg


def _type_repr(obj):
    if isinstance(obj, type):
        if obj.__module__ == 'builtins':
            return obj.__qualname__
        return f'{obj.__module__}.{obj.__qualname__}'
    if obj is ...:
        return ('...')
    if isinstance(obj, types.FunctionType):
        return obj.__name__
    return repr(obj)


def _collect_type_vars(types):
    tvars = []
    for t in types:
        if isinstance(t, TypeVar) and t not in tvars:
            tvars.append(t)
        if isinstance(t, _GenericAlias):
            tvars.extend([t for t in t.__parameters__ if t not in tvars])
    return tuple(tvars)


def _check_generic(cls, parameters, elen):
    ...


def _deduplicate(params):
    # Weed out strict duplicates, preserving the first of each occurrence.
    all_params = set(params)
    if len(all_params) < len(params):
        new_params = []
        for t in params:
            if t in all_params:
                new_params.append(t)
                all_params.remove(t)
        params = new_params
        assert not all_params, all_params
    return params


def _remove_dups_flatten(parameters):
    params = []
    for p in parameters:
        if isinstance(p, _UnionGenericAlias):
            params.extend(p.__args__)
        elif isinstance(p, tuple) and len(p) > 0 and p[0] is Union:
            params.extend(p[1:])
        else:
            params.append(p)

    return tuple(_deduplicate(params))


def _flatten_literal_params(parameters):
    params = []
    for p in parameters:
        if isinstance(p, _LiteralGenericAlias):
            params.extend(p.__args__)
        else:
            params.append(p)
    return tuple(params)


_cleanups = []


def _tp_cache(func=None, typed=False):
    def decorator(func):
        cached = functools.lru_cache(typed=typed)(func)
        _cleanups.append(cached.cache_clear)

        @functools.wraps(func)
        def inner(*args, **kwds):
            try:
                return cached(*args, **kwds)
            except TypeError:
                pass
            return func(*args, **kwds)

        return inner

    if func is not None:
        return decorator(func)

    return decorator


def _eval_type(t, globalns, localns, recursive_guard=frozenset()):
    if isinstance(t, ForwardRef):
        return t._evaluate(globalns, localns, recursive_guard)
    if isinstance(t, _GenericAlias):
        ev_args = tuple(_eval_type(a, globalns, localns, recursive_guard) for a in t.__args__)
        if ev_args == t.__args__:
            return t
        else:
            return t.copy_with(ev_args)
    return t


class _Final:
    __slots__ = ('__weakref__',)

    def __init_subclass__(self, *args, **kwds):
        if '_root' not in kwds:
            raise TypeError("Cannot subclass special typing classes")


class _Immutable:
    __slots__ = ()

    def __copy__(self):
        return self

    def __deepcopy__(self, memo):
        return self


class _SpecialForm(_Final, _root=True):
    __slots__ = ('_name', '__doc__', '_getitem')

    def __init__(self, getitem):
        self._getitem = getitem
        self._name = getitem.__name__
        self.__doc__ = getitem.__doc__

    def __mro_entries__(self, bases):
        raise TypeError(f"Cannot subclass {self!r}")

    def __repr__(self):
        return 'typing.' + self._name

    def __reduce__(self):
        return self._name

    def __call__(self, *args, **kwds):
        raise TypeError(f"Cannot instantiate {self!r}")

    def __instancecheck__(self, obj):
        raise TypeError(f"{self} cannot be used with isinstance()")

    def __subclasscheck__(self, cls):
        raise TypeError(f"{self} cannot be used with issubclass()")

    @_tp_cache
    def __getitem__(self, parameters):
        return self._getitem(self, parameters)


class _LiteralSpecialForm(_SpecialForm, _root=True):
    @_tp_cache(typed=True)
    def __getitem__(self, parameters):
        return self._getitem(self, parameters)


@_SpecialForm
def Any(self, parameters):
    raise TypeError(f"{self} is not subscriptable")


@_SpecialForm
def NoReturn(self, parameters):
    raise TypeError(f"{self} is not subscriptable")


@_SpecialForm
def ClassVar(self, parameters):
    item = _type_check(parameters, f'{self} accepts only single type.')
    return _GenericAlias(self, (item,))


@_SpecialForm
def Final(self, parameters):
    item = _type_check(parameters, f'{self} accepts only single type.')
    return _GenericAlias(self, (item,))


@_SpecialForm
def Union(self, parameters):
    if parameters == ():
        raise TypeError("Cannot take a Union of no types.")
    if not isinstance(parameters, tuple):
        parameters = (parameters,)
    msg = "Union[arg, ...]: each arg must be a type."
    parameters = tuple(_type_check(p, msg) for p in parameters)
    parameters = _remove_dups_flatten(parameters)
    if len(parameters) == 1:
        return parameters[0]
    return _UnionGenericAlias(self, parameters)


@_SpecialForm
def Optional(self, parameters):
    arg = _type_check(parameters, f"{self} requires a single type.")
    return Union[arg, type(None)]


@_LiteralSpecialForm
def Literal(self, parameters):
    if not isinstance(parameters, tuple):
        parameters = (parameters,)

    parameters = _flatten_literal_params(parameters)

    try:
        parameters = tuple(p for p, _ in _deduplicate(list(_value_and_type_iter(parameters))))
    except TypeError:  # unhashable parameters
        pass

    return _LiteralGenericAlias(self, parameters)


class ForwardRef(_Final, _root=True):
    __slots__ = ('__forward_arg__', '__forward_code__',
                 '__forward_evaluated__', '__forward_value__',
                 '__forward_is_argument__')

    def __init__(self, arg, is_argument=True):
        if not isinstance(arg, str):
            raise TypeError(f"Forward reference must be a string -- got {arg!r}")
        try:
            code = compile(arg, '<string>', 'eval')
        except SyntaxError:
            raise SyntaxError(f"Forward reference must be an expression -- got {arg!r}")
        self.__forward_arg__ = arg
        self.__forward_code__ = code
        self.__forward_evaluated__ = False
        self.__forward_value__ = None
        self.__forward_is_argument__ = is_argument

    def _evaluate(self, globalns, localns, recursive_guard):
        if self.__forward_arg__ in recursive_guard:
            return self
        if not self.__forward_evaluated__ or localns is not globalns:
            if globalns is None and localns is None:
                globalns = localns = {}
            elif globalns is None:
                globalns = localns
            elif localns is None:
                localns = globalns
            type_ = _type_check(
                eval(self.__forward_code__, globalns, localns),
                "Forward references must evaluate to types.",
                is_argument=self.__forward_is_argument__,
            )
            self.__forward_value__ = _eval_type(
                type_, globalns, localns, recursive_guard | {self.__forward_arg__}
            )
            self.__forward_evaluated__ = True
        return self.__forward_value__

    def __eq__(self, other):
        if not isinstance(other, ForwardRef):
            return NotImplemented
        if self.__forward_evaluated__ and other.__forward_evaluated__:
            return (self.__forward_arg__ == other.__forward_arg__ and
                    self.__forward_value__ == other.__forward_value__)
        return self.__forward_arg__ == other.__forward_arg__

    def __hash__(self):
        return hash(self.__forward_arg__)

    def __repr__(self):
        return f'ForwardRef({self.__forward_arg__!r})'


class TypeVar(_Final, _Immutable, _root=True):
    __slots__ = ('__name__', '__bound__', '__constraints__',
                 '__covariant__', '__contravariant__', '__dict__')

    def __init__(self, name, *constraints, bound=None,
                 covariant=False, contravariant=False):
        self.__name__ = name
        if covariant and contravariant:
            raise ValueError("Bivariant types are not supported.")
        self.__covariant__ = bool(covariant)
        self.__contravariant__ = bool(contravariant)
        if constraints and bound is not None:
            raise TypeError("Constraints cannot be combined with bound=...")
        if constraints and len(constraints) == 1:
            raise TypeError("A single constraint is not allowed")
        msg = "TypeVar(name, constraint, ...): constraints must be types."
        self.__constraints__ = tuple(_type_check(t, msg) for t in constraints)
        if bound:
            self.__bound__ = _type_check(bound, "Bound must be a type.")
        else:
            self.__bound__ = None
        try:
            def_mod = sys._getframe(1).f_globals.get('__name__', '__main__')
        except (AttributeError, ValueError):
            def_mod = None
        if def_mod != 'typing':
            self.__module__ = def_mod

    def __repr__(self):
        if self.__covariant__:
            prefix = '+'
        elif self.__contravariant__:
            prefix = '-'
        else:
            prefix = '~'
        return prefix + self.__name__

    def __reduce__(self):
        return self.__name__


def _is_dunder(attr):
    return attr.startswith('__') and attr.endswith('__')


class _BaseGenericAlias(_Final, _root=True):
    def __init__(self, origin, *, inst=True, name=None):
        self._inst = inst
        self._name = name
        self.__origin__ = origin
        self.__slots__ = None  # This is not documented.

    def __call__(self, *args, **kwargs):
        if not self._inst:
            raise TypeError(f"Type {self._name} cannot be instantiated; "
                            f"use {self.__origin__.__name__}() instead")
        result = self.__origin__(*args, **kwargs)
        try:
            result.__orig_class__ = self
        except AttributeError:
            pass
        return result

    def __mro_entries__(self, bases):
        res = []
        if self.__origin__ not in bases:
            res.append(self.__origin__)
        i = bases.index(self)
        for b in bases[i + 1:]:
            if isinstance(b, _BaseGenericAlias) or issubclass(b, Generic):
                break
        else:
            res.append(Generic)
        return tuple(res)

    def __getattr__(self, attr):
        if '__origin__' in self.__dict__ and not _is_dunder(attr):
            return getattr(self.__origin__, attr)
        raise AttributeError(attr)

    def __setattr__(self, attr, val):
        if _is_dunder(attr) or attr in ('_name', '_inst', '_nparams'):
            super().__setattr__(attr, val)
        else:
            setattr(self.__origin__, attr, val)

    def __instancecheck__(self, obj):
        return self.__subclasscheck__(type(obj))

    def __subclasscheck__(self, cls):
        raise TypeError("Subscripted generics cannot be used with"
                        " class and instance checks")


class _GenericAlias(_BaseGenericAlias, _root=True):
    def __init__(self, origin, params, *, inst=True, name=None):
        super().__init__(origin, inst=inst, name=name)
        if not isinstance(params, tuple):
            params = (params,)
        self.__args__ = tuple(... if a is _TypingEllipsis else
                              () if a is _TypingEmpty else
                              a for a in params)
        self.__parameters__ = _collect_type_vars(params)
        if not name:
            self.__module__ = origin.__module__

    def __eq__(self, other):
        if not isinstance(other, _GenericAlias):
            return NotImplemented
        return (self.__origin__ == other.__origin__
                and self.__args__ == other.__args__)

    def __hash__(self):
        return hash((self.__origin__, self.__args__))

    @_tp_cache
    def __getitem__(self, params):
        if self.__origin__ in (Generic, Protocol):
            raise TypeError(f"Cannot subscript already-subscripted {self}")
        if not isinstance(params, tuple):
            params = (params,)
        msg = "Parameters to generic types must be types."
        params = tuple(_type_check(p, msg) for p in params)
        _check_generic(self, params, len(self.__parameters__))

        subst = dict(zip(self.__parameters__, params))
        new_args = []
        for arg in self.__args__:
            if isinstance(arg, TypeVar):
                arg = subst[arg]
            elif isinstance(arg, _GenericAlias):
                subparams = arg.__parameters__
                if subparams:
                    subargs = tuple(subst[x] for x in subparams)
                    arg = arg[subargs]
            new_args.append(arg)
        return self.copy_with(tuple(new_args))

    def copy_with(self, params):
        return self.__class__(self.__origin__, params, name=self._name, inst=self._inst)

    def __repr__(self):
        if self._name:
            name = 'typing.' + self._name
        else:
            name = _type_repr(self.__origin__)
        args = ", ".join([_type_repr(a) for a in self.__args__])
        return f'{name}[{args}]'

    def __reduce__(self):
        if self._name:
            origin = globals()[self._name]
        else:
            origin = self.__origin__
        args = tuple(self.__args__)
        if len(args) == 1 and not isinstance(args[0], tuple):
            args, = args
        return operator.getitem, (origin, args)

    def __mro_entries__(self, bases):
        if self._name:
            return super().__mro_entries__(bases)
        if self.__origin__ is Generic:
            if Protocol in bases:
                return ()
            i = bases.index(self)
            for b in bases[i + 1:]:
                if isinstance(b, _BaseGenericAlias) and b is not self:
                    return ()
        return (self.__origin__,)


class _SpecialGenericAlias(_BaseGenericAlias, _root=True):
    def __init__(self, origin, nparams, *, inst=True, name=None):
        if name is None:
            name = origin.__name__
        super().__init__(origin, inst=inst, name=name)
        self._nparams = nparams
        if origin.__module__ == 'builtins':
            self.__doc__ = f'A generic version of {origin.__qualname__}.'
        else:
            self.__doc__ = f'A generic version of {origin.__module__}.{origin.__qualname__}.'

    @_tp_cache
    def __getitem__(self, params):
        if not isinstance(params, tuple):
            params = (params,)
        msg = "Parameters to generic types must be types."
        params = tuple(_type_check(p, msg) for p in params)
        _check_generic(self, params, self._nparams)
        return self.copy_with(params)

    def copy_with(self, params):
        return _GenericAlias(self.__origin__, params,
                             name=self._name, inst=self._inst)

    def __repr__(self):
        return 'typing.' + self._name

    def __subclasscheck__(self, cls):
        if isinstance(cls, _SpecialGenericAlias):
            return issubclass(cls.__origin__, self.__origin__)
        if not isinstance(cls, _GenericAlias):
            return issubclass(cls, self.__origin__)
        return super().__subclasscheck__(cls)

    def __reduce__(self):
        return self._name


class _CallableGenericAlias(_GenericAlias, _root=True):
    def __repr__(self):
        assert self._name == 'Callable'
        if len(self.__args__) == 2 and self.__args__[0] is Ellipsis:
            return super().__repr__()
        return (f'typing.Callable'
                f'[[{", ".join([_type_repr(a) for a in self.__args__[:-1]])}], '
                f'{_type_repr(self.__args__[-1])}]')

    def __reduce__(self):
        args = self.__args__
        if not (len(args) == 2 and args[0] is ...):
            args = list(args[:-1]), args[-1]
        return operator.getitem, (Callable, args)


class _CallableType(_SpecialGenericAlias, _root=True):
    def copy_with(self, params):
        return _CallableGenericAlias(self.__origin__, params,
                                     name=self._name, inst=self._inst)

    def __getitem__(self, params):
        if not isinstance(params, tuple) or len(params) != 2:
            raise TypeError("Callable must be used as "
                            "Callable[[arg, ...], result].")
        args, result = params
        if args is Ellipsis:
            params = (Ellipsis, result)
        else:
            if not isinstance(args, list):
                raise TypeError(f"Callable[args, result]: args must be a list."
                                f" Got {args}")
            params = (tuple(args), result)
        return self.__getitem_inner__(params)

    @_tp_cache
    def __getitem_inner__(self, params):
        args, result = params
        msg = "Callable[args, result]: result must be a type."
        result = _type_check(result, msg)
        if args is Ellipsis:
            return self.copy_with((_TypingEllipsis, result))
        msg = "Callable[[arg, ...], result]: each arg must be a type."
        args = tuple(_type_check(arg, msg) for arg in args)
        params = args + (result,)
        return self.copy_with(params)


class _TupleType(_SpecialGenericAlias, _root=True):
    @_tp_cache
    def __getitem__(self, params):
        if params == ():
            return self.copy_with((_TypingEmpty,))
        if not isinstance(params, tuple):
            params = (params,)
        if len(params) == 2 and params[1] is ...:
            msg = "Tuple[t, ...]: t must be a type."
            p = _type_check(params[0], msg)
            return self.copy_with((p, _TypingEllipsis))
        msg = "Tuple[t0, t1, ...]: each t must be a type."
        params = tuple(_type_check(p, msg) for p in params)
        return self.copy_with(params)


class _UnionGenericAlias(_GenericAlias, _root=True):
    def copy_with(self, params):
        return Union[params]

    def __eq__(self, other):
        if not isinstance(other, _UnionGenericAlias):
            return NotImplemented
        return set(self.__args__) == set(other.__args__)

    def __hash__(self):
        return hash(frozenset(self.__args__))

    def __repr__(self):
        args = self.__args__
        if len(args) == 2:
            if args[0] is type(None):
                return f'typing.Optional[{_type_repr(args[1])}]'
            elif args[1] is type(None):
                return f'typing.Optional[{_type_repr(args[0])}]'
        return super().__repr__()


def _value_and_type_iter(parameters):
    return ((p, type(p)) for p in parameters)


class _LiteralGenericAlias(_GenericAlias, _root=True):

    def __eq__(self, other):
        if not isinstance(other, _LiteralGenericAlias):
            return NotImplemented

        return set(_value_and_type_iter(self.__args__)) == set(_value_and_type_iter(other.__args__))

    def __hash__(self):
        return hash(frozenset(_value_and_type_iter(self.__args__)))


class Generic:
    __slots__ = ()
    _is_protocol = False

    @_tp_cache
    def __class_getitem__(cls, params):
        if not isinstance(params, tuple):
            params = (params,)
        if not params and cls is not Tuple:
            raise TypeError(
                f"Parameter list to {cls.__qualname__}[...] cannot be empty")
        msg = "Parameters to generic types must be types."
        params = tuple(_type_check(p, msg) for p in params)
        if cls in (Generic, Protocol):
            if not all(isinstance(p, TypeVar) for p in params):
                raise TypeError(
                    f"Parameters to {cls.__name__}[...] must all be type variables")
            if len(set(params)) != len(params):
                raise TypeError(
                    f"Parameters to {cls.__name__}[...] must all be unique")
        else:
            _check_generic(cls, params, len(cls.__parameters__))
        return _GenericAlias(cls, params)

    def __init_subclass__(cls, *args, **kwargs):
        super().__init_subclass__(*args, **kwargs)
        tvars = []
        if '__orig_bases__' in cls.__dict__:
            error = Generic in cls.__orig_bases__
        else:
            error = Generic in cls.__bases__ and cls.__name__ != 'Protocol'
        if error:
            raise TypeError("Cannot inherit from plain Generic")
        if '__orig_bases__' in cls.__dict__:
            tvars = _collect_type_vars(cls.__orig_bases__)
            gvars = None
            for base in cls.__orig_bases__:
                if (isinstance(base, _GenericAlias) and
                        base.__origin__ is Generic):
                    if gvars is not None:
                        raise TypeError(
                            "Cannot inherit from Generic[...] multiple types.")
                    gvars = base.__parameters__
            if gvars is not None:
                tvarset = set(tvars)
                gvarset = set(gvars)
                if not tvarset <= gvarset:
                    s_vars = ', '.join(str(t) for t in tvars if t not in gvarset)
                    s_args = ', '.join(str(g) for g in gvars)
                    raise TypeError(f"Some type variables ({s_vars}) are"
                                    f" not listed in Generic[{s_args}]")
                tvars = gvars
        cls.__parameters__ = tuple(tvars)


class _TypingEmpty:
    """"""


class _TypingEllipsis:
    """"""


_TYPING_INTERNALS = ['__parameters__', '__orig_bases__', '__orig_class__',
                     '_is_protocol', '_is_runtime_protocol']
_SPECIAL_NAMES = ['__abstractmethods__', '__annotations__', '__dict__', '__doc__',
                  '__init__', '__module__', '__new__', '__slots__',
                  '__subclasshook__', '__weakref__', '__class_getitem__']
EXCLUDED_ATTRIBUTES = _TYPING_INTERNALS + _SPECIAL_NAMES + ['_MutableMapping__marker']


def _get_protocol_attrs(cls):
    attrs = set()
    for base in cls.__mro__[:-1]:  # without object
        if base.__name__ in ('Protocol', 'Generic'):
            continue
        annotations = getattr(base, '__annotations__', {})
        for attr in list(base.__dict__.keys()) + list(annotations.keys()):
            if not attr.startswith('_abc_') and attr not in EXCLUDED_ATTRIBUTES:
                attrs.add(attr)
    return attrs


def _is_callable_members_only(cls):
    return all(callable(getattr(cls, attr, None)) for attr in _get_protocol_attrs(cls))


def _no_init(self, *args, **kwargs):
    if type(self)._is_protocol:
        raise TypeError('Protocols cannot be instantiated')


def _allow_reckless_class_cheks():
    try:
        return sys._getframe(3).f_globals['__name__'] in ['abc', 'functools']
    except (AttributeError, ValueError):  # For platforms without _getframe().
        return True


_PROTO_WHITELIST = {
    'collections.abc': [
        'Callable', 'Awaitable', 'Iterable', 'Iterator', 'AsyncIterable',
        'Hashable', 'Sized', 'Container', 'Collection', 'Reversible',
    ],
    'contextlib': ['AbstractContextManager', 'AbstractAsyncContextManager'],
}


class _ProtocolMeta(ABCMeta):
    def __instancecheck__(cls, instance):
        if ((not getattr(cls, '_is_protocol', False) or
             _is_callable_members_only(cls)) and
                issubclass(instance.__class__, cls)):
            return True
        if cls._is_protocol:
            if all(hasattr(instance, attr) and
                   # All *methods* can be blocked by setting them to None.
                   (not callable(getattr(cls, attr, None)) or
                    getattr(instance, attr) is not None)
                   for attr in _get_protocol_attrs(cls)):
                return True
        return super().__instancecheck__(instance)


class Protocol(Generic, metaclass=_ProtocolMeta):
    __slots__ = ()
    _is_protocol = True
    _is_runtime_protocol = False

    def __init_subclass__(cls, *args, **kwargs):
        super().__init_subclass__(*args, **kwargs)
        if not cls.__dict__.get('_is_protocol', False):
            cls._is_protocol = any(b is Protocol for b in cls.__bases__)

        def _proto_hook(other):
            if not cls.__dict__.get('_is_protocol', False):
                return NotImplemented
            if not getattr(cls, '_is_runtime_protocol', False):
                if _allow_reckless_class_cheks():
                    return NotImplemented
                raise TypeError("Instance and class checks can only be used with"
                                " @runtime_checkable protocols")
            if not _is_callable_members_only(cls):
                if _allow_reckless_class_cheks():
                    return NotImplemented
                raise TypeError("Protocols with non-method members"
                                " don't support issubclass()")
            if not isinstance(other, type):
                raise TypeError('issubclass() arg 1 must be a class')
            for attr in _get_protocol_attrs(cls):
                for base in other.__mro__:
                    if attr in base.__dict__:
                        if base.__dict__[attr] is None:
                            return NotImplemented
                        break
                    annotations = getattr(base, '__annotations__', {})
                    if (isinstance(annotations, collections.abc.Mapping) and
                            attr in annotations and
                            issubclass(other, Generic) and other._is_protocol):
                        break
                else:
                    return NotImplemented
            return True

        if '__subclasshook__' not in cls.__dict__:
            cls.__subclasshook__ = _proto_hook
        if not cls._is_protocol:
            return
        for base in cls.__bases__:
            if not (base in (object, Generic) or
                    base.__module__ in _PROTO_WHITELIST and
                    base.__name__ in _PROTO_WHITELIST[base.__module__] or
                    issubclass(base, Generic) and base._is_protocol):
                raise TypeError('Protocols can only inherit from other'
                                ' protocols, got %r' % base)
        cls.__init__ = _no_init


class _AnnotatedAlias(_GenericAlias, _root=True):
    def __init__(self, origin, metadata):
        if isinstance(origin, _AnnotatedAlias):
            metadata = origin.__metadata__ + metadata
            origin = origin.__origin__
        super().__init__(origin, origin)
        self.__metadata__ = metadata

    def copy_with(self, params):
        assert len(params) == 1
        new_type = params[0]
        return _AnnotatedAlias(new_type, self.__metadata__)

    def __repr__(self):
        return "typing.Annotated[{}, {}]".format(
            _type_repr(self.__origin__),
            ", ".join(repr(a) for a in self.__metadata__)
        )

    def __reduce__(self):
        return operator.getitem, (
            Annotated, (self.__origin__,) + self.__metadata__
        )

    def __eq__(self, other):
        if not isinstance(other, _AnnotatedAlias):
            return NotImplemented
        return (self.__origin__ == other.__origin__
                and self.__metadata__ == other.__metadata__)

    def __hash__(self):
        return hash((self.__origin__, self.__metadata__))


class Annotated:
    __slots__ = ()

    def __new__(cls, *args, **kwargs):
        raise TypeError("Type Annotated cannot be instantiated.")

    @_tp_cache
    def __class_getitem__(cls, params):
        if not isinstance(params, tuple) or len(params) < 2:
            raise TypeError("Annotated[...] should be used "
                            "with at least two arguments (a type and an "
                            "annotation).")
        msg = "Annotated[t, ...]: t must be a type."
        origin = _type_check(params[0], msg)
        metadata = tuple(params[1:])
        return _AnnotatedAlias(origin, metadata)

    def __init_subclass__(cls, *args, **kwargs):
        raise TypeError(
            "Cannot subclass {}.Annotated".format(cls.__module__)
        )


def runtime_checkable(cls):
    if not issubclass(cls, Generic) or not cls._is_protocol:
        raise TypeError('@runtime_checkable can be only applied to protocol classes,'
                        ' got %r' % cls)
    cls._is_runtime_protocol = True
    return cls


def cast(typ, val):
    return val


def _get_defaults(func):
    try:
        code = func.__code__
    except AttributeError:
        # Some built-in functions don't have __code__, __defaults__, etc.
        return {}
    pos_count = code.co_argcount
    arg_names = code.co_varnames
    arg_names = arg_names[:pos_count]
    defaults = func.__defaults__ or ()
    kwdefaults = func.__kwdefaults__
    res = dict(kwdefaults) if kwdefaults else {}
    pos_offset = pos_count - len(defaults)
    for name, value in zip(arg_names[pos_offset:], defaults):
        assert name not in res
        res[name] = value
    return res


_allowed_types = (types.FunctionType, types.BuiltinFunctionType,
                  types.MethodType, types.ModuleType,
                  )


def get_type_hints(obj, globalns=None, localns=None, include_extras=False):
    if getattr(obj, '__no_type_check__', None):
        return {}
    # Classes require a special treatment.
    if isinstance(obj, type):
        hints = {}
        for base in reversed(obj.__mro__):
            if globalns is None:
                base_globals = sys.modules[base.__module__].__dict__
            else:
                base_globals = globalns
            ann = base.__dict__.get('__annotations__', {})
            for name, value in ann.items():
                if value is None:
                    value = type(None)
                if isinstance(value, str):
                    value = ForwardRef(value, is_argument=False)
                value = _eval_type(value, base_globals, localns)
                hints[name] = value
        return hints if include_extras else {k: _strip_annotations(t) for k, t in hints.items()}

    if globalns is None:
        if isinstance(obj, types.ModuleType):
            globalns = obj.__dict__
        else:
            nsobj = obj
            # Find globalns for the unwrapped object.
            while hasattr(nsobj, '__wrapped__'):
                nsobj = nsobj.__wrapped__
            globalns = getattr(nsobj, '__globals__', {})
        if localns is None:
            localns = globalns
    elif localns is None:
        localns = globalns
    hints = getattr(obj, '__annotations__', None)
    if hints is None:
        # Return empty annotations for something that _could_ have them.
        if isinstance(obj, _allowed_types):
            return {}
        else:
            raise TypeError('{!r} is not a module, class, method, '
                            'or function.'.format(obj))
    defaults = _get_defaults(obj)
    hints = dict(hints)
    for name, value in hints.items():
        if value is None:
            value = type(None)
        if isinstance(value, str):
            value = ForwardRef(value)
        value = _eval_type(value, globalns, localns)
        if name in defaults and defaults[name] is None:
            value = Optional[value]
        hints[name] = value
    return hints if include_extras else {k: _strip_annotations(t) for k, t in hints.items()}


def _strip_annotations(t):
    if isinstance(t, _AnnotatedAlias):
        return _strip_annotations(t.__origin__)
    if isinstance(t, _GenericAlias):
        stripped_args = tuple(_strip_annotations(a) for a in t.__args__)
        if stripped_args == t.__args__:
            return t
        return t.copy_with(stripped_args)
    return t


def get_origin(tp):
    if isinstance(tp, _AnnotatedAlias):
        return Annotated
    if hasattr(tp, '__origin__'):
        return tp.__origin__
    if tp is Generic:
        return Generic
    return None


def get_args(tp):
    if isinstance(tp, _AnnotatedAlias):
        return (tp.__origin__,) + tp.__metadata__
    if isinstance(tp, _GenericAlias):
        res = tp.__args__
        if tp.__origin__ is collections.abc.Callable and res[0] is not Ellipsis:
            res = (list(res[:-1]), res[-1])
        return res

    if hasattr(tp, "__args__"):
        return tp.__args__
    return ()


def no_type_check(arg):
    if isinstance(arg, type):
        arg_attrs = arg.__dict__.copy()
        for attr, val in arg.__dict__.items():
            if val in arg.__bases__ + (arg,):
                arg_attrs.pop(attr)
        for obj in arg_attrs.values():
            if isinstance(obj, types.FunctionType):
                obj.__no_type_check__ = True
            if isinstance(obj, type):
                no_type_check(obj)
    try:
        arg.__no_type_check__ = True
    except TypeError:
        pass
    return arg


def no_type_check_decorator(decorator):
    @functools.wraps(decorator)
    def wrapped_decorator(*args, **kwds):
        func = decorator(*args, **kwds)
        func = no_type_check(func)
        return func

    return wrapped_decorator


def _overload_dummy(*args, **kwds):
    raise NotImplementedError(
        "You should not call an overloaded function. "
        "A series of @overload-decorated functions "
        "outside a stub module should always be followed "
        "by an implementation that is not @overload-ed.")


def overload(func):
    return _overload_dummy


def final(f):
    return f


T = TypeVar('T')
KT = TypeVar('KT')
VT = TypeVar('VT')
T_co = TypeVar('T_co', covariant=True)
V_co = TypeVar('V_co', covariant=True)
VT_co = TypeVar('VT_co', covariant=True)
T_contra = TypeVar('T_contra', contravariant=True)
CT_co = TypeVar('CT_co', covariant=True, bound=type)
AnyStr = TypeVar('AnyStr', bytes, str)
_alias = _SpecialGenericAlias
Hashable = _alias(collections.abc.Hashable, 0)  # Not generic.
Awaitable = _alias(collections.abc.Awaitable, 1)
Coroutine = _alias(collections.abc.Coroutine, 3)
AsyncIterable = _alias(collections.abc.AsyncIterable, 1)
AsyncIterator = _alias(collections.abc.AsyncIterator, 1)
Iterable = _alias(collections.abc.Iterable, 1)
Iterator = _alias(collections.abc.Iterator, 1)
Reversible = _alias(collections.abc.Reversible, 1)
Sized = _alias(collections.abc.Sized, 0)  # Not generic.
Container = _alias(collections.abc.Container, 1)
Collection = _alias(collections.abc.Collection, 1)
Callable = _CallableType(collections.abc.Callable, 2)
Callable.__doc__ = "Callable"
AbstractSet = _alias(collections.abc.Set, 1, name='AbstractSet')
MutableSet = _alias(collections.abc.MutableSet, 1)
# NOTE: Mapping is only covariant in the value type.
Mapping = _alias(collections.abc.Mapping, 2)
MutableMapping = _alias(collections.abc.MutableMapping, 2)
Sequence = _alias(collections.abc.Sequence, 1)
MutableSequence = _alias(collections.abc.MutableSequence, 1)
ByteString = _alias(collections.abc.ByteString, 0)  # Not generic
# Tuple accepts variable number of parameters.
Tuple = _TupleType(tuple, -1, inst=False, name='Tuple')
Tuple.__doc__ = "Tuple"
List = _alias(list, 1, inst=False, name='List')
Deque = _alias(collections.deque, 1, name='Deque')
Set = _alias(set, 1, inst=False, name='Set')
FrozenSet = _alias(frozenset, 1, inst=False, name='FrozenSet')
MappingView = _alias(collections.abc.MappingView, 1)
KeysView = _alias(collections.abc.KeysView, 1)
ItemsView = _alias(collections.abc.ItemsView, 2)
ValuesView = _alias(collections.abc.ValuesView, 1)
Dict = _alias(dict, 2, inst=False, name='Dict')
DefaultDict = _alias(collections.defaultdict, 2, name='DefaultDict')
OrderedDict = _alias(collections.OrderedDict, 2)
Counter = _alias(collections.Counter, 1)
ChainMap = _alias(collections.ChainMap, 2)
Generator = _alias(collections.abc.Generator, 3)
AsyncGenerator = _alias(collections.abc.AsyncGenerator, 2)
Type = _alias(type, 1, inst=False, name='Type')
Type.__doc__ = "Type"


@runtime_checkable
class SupportsInt(Protocol):
    __slots__ = ()

    @abstractmethod
    def __int__(self) -> int:
        pass


@runtime_checkable
class SupportsFloat(Protocol):
    __slots__ = ()

    @abstractmethod
    def __float__(self) -> float:
        pass


@runtime_checkable
class SupportsComplex(Protocol):
    __slots__ = ()

    @abstractmethod
    def __complex__(self) -> complex:
        pass


@runtime_checkable
class SupportsBytes(Protocol):
    __slots__ = ()

    @abstractmethod
    def __bytes__(self) -> bytes:
        pass


@runtime_checkable
class SupportsIndex(Protocol):
    __slots__ = ()

    @abstractmethod
    def __index__(self) -> int:
        pass


def _make_nmtuple(name, types, module, defaults=()):
    fields = [n for n, t in types]
    types = {n: _type_check(t, f"field {n} annotation must be a type")
             for n, t in types}
    nm_tpl = collections.namedtuple(name, fields,
                                    defaults=defaults, module=module)
    nm_tpl.__annotations__ = nm_tpl.__new__.__annotations__ = types
    return nm_tpl


_prohibited = frozenset({'__new__', '__init__', '__slots__', '__getnewargs__',
                         '_fields', '_field_defaults',
                         '_make', '_replace', '_asdict', '_source'})
_special = frozenset({'__module__', '__name__', '__annotations__'})


class NamedTupleMeta(type):

    def __new__(cls, typename, bases, ns):
        assert bases[0] is _NamedTuple
        types = ns.get('__annotations__', {})
        default_names = []
        for field_name in types:
            if field_name in ns:
                default_names.append(field_name)
            elif default_names:
                raise TypeError(f"Non-default namedtuple field {field_name} "
                                f"cannot follow default field"
                                f"{'s' if len(default_names) > 1 else ''} "
                                f"{', '.join(default_names)}")
        nm_tpl = _make_nmtuple(typename, types.items(),
                               defaults=[ns[n] for n in default_names],
                               module=ns['__module__'])
        # update from user namespace without overriding special namedtuple attributes
        for key in ns:
            if key in _prohibited:
                raise AttributeError("Cannot overwrite NamedTuple attribute " + key)
            elif key not in _special and key not in nm_tpl._fields:
                setattr(nm_tpl, key, ns[key])
        return nm_tpl


def NamedTuple(typename, fields=None, **kwargs):
    if fields is None:
        fields = kwargs.items()
    elif kwargs:
        raise TypeError("Either list of fields or keywords"
                        " can be provided to NamedTuple, not both")
    try:
        module = sys._getframe(1).f_globals.get('__name__', '__main__')
    except (AttributeError, ValueError):
        module = None
    return _make_nmtuple(typename, fields, module=module)


_NamedTuple = type.__new__(NamedTupleMeta, 'NamedTuple', (), {})


def _namedtuple_mro_entries(bases):
    if len(bases) > 1:
        raise TypeError("Multiple inheritance with NamedTuple is not supported")
    assert bases[0] is NamedTuple
    return (_NamedTuple,)


NamedTuple.__mro_entries__ = _namedtuple_mro_entries


class _TypedDictMeta(type):
    def __new__(cls, name, bases, ns, total=True):
        for base in bases:
            if type(base) is not _TypedDictMeta:
                raise TypeError('cannot inherit from both a TypedDict type '
                                'and a non-TypedDict base class')
        tp_dict = type.__new__(_TypedDictMeta, name, (dict,), ns)

        annotations = {}
        own_annotations = ns.get('__annotations__', {})
        own_annotation_keys = set(own_annotations.keys())
        msg = "TypedDict('Name', {f0: t0, f1: t1, ...}); each t must be a type"
        own_annotations = {
            n: _type_check(tp, msg) for n, tp in own_annotations.items()
        }
        required_keys = set()
        optional_keys = set()

        for base in bases:
            annotations.update(base.__dict__.get('__annotations__', {}))
            required_keys.update(base.__dict__.get('__required_keys__', ()))
            optional_keys.update(base.__dict__.get('__optional_keys__', ()))

        annotations.update(own_annotations)
        if total:
            required_keys.update(own_annotation_keys)
        else:
            optional_keys.update(own_annotation_keys)

        tp_dict.__annotations__ = annotations
        tp_dict.__required_keys__ = frozenset(required_keys)
        tp_dict.__optional_keys__ = frozenset(optional_keys)
        if not hasattr(tp_dict, '__total__'):
            tp_dict.__total__ = total
        return tp_dict

    __call__ = dict  # static method

    def __subclasscheck__(cls, other):
        raise TypeError('TypedDict does not support instance and class checks')

    __instancecheck__ = __subclasscheck__


def TypedDict(typename, fields=None, total=True, **kwargs):
    if fields is None:
        fields = kwargs
    elif kwargs:
        raise TypeError("TypedDict takes either a dict or keyword arguments,"
                        " but not both")

    ns = {'__annotations__': dict(fields), '__total__': total}
    try:
        ns['__module__'] = sys._getframe(1).f_globals.get('__name__', '__main__')
    except (AttributeError, ValueError):
        pass
    return _TypedDictMeta(typename, (), ns)


_TypedDict = type.__new__(_TypedDictMeta, 'TypedDict', (), {})
TypedDict.__mro_entries__ = lambda bases: (_TypedDict,)


def NewType(name, tp):
    def new_type(x):
        return x

    new_type.__name__ = name
    new_type.__supertype__ = tp
    return new_type


Text = str
TYPE_CHECKING = False
