# -*- coding: utf-8 -*-
import sys
from importlib import import_module

from pydantic import ValidationError
from pydantic.error_wrappers import ErrorWrapper
from pydantic.fields import ModelField
from typing import Union, Text, Any, TypeVar, Generic, Type

# standard python types serializable by all libraries without and special processing
from pydantic.validators import dict_validator

StandardTypes = Union[None, bytes, str, tuple, list, dict, int, float, bool]


T = TypeVar('T')


class ClassPath(Generic[T]):
    """
    String which represents a path to class, contains module path and class name delimited by a colon.
    In Pydantic returns imported class

    !!! example
        `foo.bar:MyClass`
    """

    def __init__(self, cls: Type[T]):
        self._class = cls

    @property
    def type_(self) -> Type[T]:
        return self._class

    @classmethod
    def __get_validators__(cls):
        yield cls.import_class

    @classmethod
    def import_class(cls, v, field: ModelField):
        if isinstance(v, cls):
            return v

        if v.count(':') != 1:
            raise ValueError(f"'{v}' is not a valid path to class. Path should be a Python "
                             f"module and class name joined by colon, eg: foo.bar:MyClass")

        mod_name, class_name = v.split(':')
        try:
            mod = import_module(mod_name)
        except Exception as e:
            exc = ImportError(f'unable to import {mod_name}: {e.__class__.__name__}({e})')
            raise ValidationError([
                ErrorWrapper(exc=exc, loc='cls')
            ], cls)

        for module_name, module in sys.modules.items():
            # skip empty modules and ones without actual file
            if not module or not hasattr(module, '__file__'):
                continue

            if mod.__file__ == module.__file__:
                # if same module has been imported use imported one
                # this allows to use issubclass or isinstance checks on previously imported module and
                # class returned by this method (note: same class code imported in different way creates
                # different class types)
                if mod != module:
                    sys.modules.pop(mod.__name__)
                    mod = module
                break

        if not hasattr(mod, class_name):
            raise ValueError(f"module '{mod_name}' has no member '{class_name}'")

        imported_cls = getattr(mod, class_name)

        if field.sub_fields is not None:
            cls_f = field.sub_fields[0]
            imported_cls, error = cls_f.validate(imported_cls, {}, loc='cls')
            if error:
                raise ValidationError([error], cls)

        return cls(imported_cls)

    def __call__(self, *args, **kwargs) -> T:
        return self._class(*args, **kwargs)

    def __repr__(self):
        return f"ClassPath[{self._class.__module__}:{self._class.__name__}]"


class FuncPath:
    """
    String which represents a path to function, contains module path and class name delimited by a colon.
    In Pydantic returns imported function

    !!! example
        `foo.bar:my_func`
    """

    def __init__(self, fn):
        self._fn = fn

    @classmethod
    def __get_validators__(cls):
        yield cls.import_function

    @classmethod
    def import_function(cls, v, field: ModelField):
        if not isinstance(v, str):
            return v

        if v.count(':') != 1:
            raise ValueError(f"'{v}' is not a valid path to function. Path should be a Python "
                             f"module and member name joined by colon, eg: foo.bar:my_fn")

        mod_name, member_name = v.split(':')
        mod = import_module(mod_name)

        for module_name, module in sys.modules.items():
            # skip empty modules and ones without actual file
            if not module or not hasattr(module, '__file__'):
                continue

            if mod.__file__ == module.__file__:
                # if same module has been imported use imported one
                # this allows to use issubclass or isinstance checks on previously imported module and
                # class returned by this method (note: same class code imported in different way creates
                # different class types)
                if mod != module:
                    sys.modules.pop(mod.__name__)
                    mod = module
                break

        if not hasattr(mod, member_name):
            raise ValueError(f"module '{mod_name}' has no member '{member_name}'")

        member = getattr(mod, member_name)
        return cls(member)

    def __call__(self, *args, **kwargs):
        return self._fn(*args, **kwargs)

    def __repr__(self):
        return f"FuncPath[{self._fn.__module__}:{self._fn.__name__}]"


class LoggingConfig(dict):
    """
    Python `logging` module configuration.
    """

    __origin__ = dict
    __args__ = [Text, Any]  # type: ignore

    @classmethod
    def __get_validators__(cls):
        yield dict_validator
        yield cls.logging_config_validator

    @classmethod
    def logging_config_validator(cls, v):
        # TODO:
        return v
