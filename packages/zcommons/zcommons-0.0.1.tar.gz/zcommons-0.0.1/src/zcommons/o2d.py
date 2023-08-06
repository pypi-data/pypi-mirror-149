__all__ = [
    "asdict",
    "asobj"
]

import dataclasses
import typing


_BUILTIN_BASE_TYPES = [type(None), bool, int, float, str, bytes]
_BUILTIN_CONTAIN_TYPES = [tuple, list, set, dict]


def asdict(obj, *, dict_factory=dict):
    if dataclasses.is_dataclass(obj):
        return dataclasses.asdict(obj, dict_factory=dict_factory)
    # return itself directly if obj is base type
    if type(obj) in _BUILTIN_BASE_TYPES:
        return obj
    # traverse container and check the sameness of elements in container
    if type(obj) in _BUILTIN_CONTAIN_TYPES:
        key_type, val_type = None, None
        if type(obj) is dict:
            ret = dict_factory()
            for k, v in obj.items():
                if key_type is None:
                    key_type, val_type = type(k), type(v)
                else:
                    if key_type != type(k) or val_type != type(v):
                        raise TypeError(f"asdict() should be called on container with the same element type")

                ret[asdict(k)] = asdict(v)
            return ret
        else:
            ret = []
            for k in obj:
                if key_type is None:
                    key_type = type(k)
                else:
                    if key_type != type(k):
                        raise TypeError(f"asdict() should be called on container with the same element type")

                ret.append(asdict(k))
            return type(obj)(ret)


def asobj(_cls, d):
    if not isinstance(_cls, type):
        raise TypeError(f"asobj() should be called on type")
    if dataclasses.is_dataclass(_cls):
        init_params = {}
        set_attrs = {}

        for f in getattr(_cls, dataclasses._FIELDS).values():
            # Only consider normal fields
            if f._field_type in [dataclasses._FIELD_CLASSVAR, dataclasses._FIELD_INITVAR]:
                continue

            v = None
            if f.name in d:
                v = asobj(f.type, d[f.name])
            else:
                if f.default is dataclasses._MISSING_TYPE and f.default_factory is dataclasses._MISSING_TYPE:
                    raise ValueError(f"Field {f.name} is required, but its value is missing")

            if f.init:
                init_params[f.name] = v
            else:
                set_attrs[f.name] = v

        ret = _cls(**init_params)
        for k, v in set_attrs.items():
            setattr(ret, k, v)
        return ret

    if isinstance(_cls, typing.GenericMeta):
        if _cls.__dict__["__args__"] is None:
            raise TypeError(f"asobj() should be called on container which specified element type")
        orig_base = _cls.__dict__["__extra__"]
        if orig_base is dict:
            key_type, val_type = _cls.__dict__["__args__"]
            if type(d) is not dict:
                raise TypeError(f"the type of d is not {_cls}")
            ret = _cls()
            for k, v in d.item():
                ret[asobj(key_type, k)] = asobj(val_type, v)
            return ret
        if orig_base in [tuple, list, set]:
            key_type, = _cls.__dict__["__args__"]
            ret = []
            # let it raises
            for k in d:
                ret.append(asobj(key_type, k))
            return orig_base(ret)

    if _cls in _BUILTIN_BASE_TYPES:
        return _cls(d)

    if _cls in _BUILTIN_CONTAIN_TYPES:
        raise TypeError(f"asobj() should be called on container which specified element type")
    raise TypeError(f"unsupport type {_cls}")


def _is_typing_container(_cls):
    return isinstance(_cls, typing.GenericMeta) and _cls.__dict__["__extra__"] in _BUILTIN_CONTAIN_TYPES
