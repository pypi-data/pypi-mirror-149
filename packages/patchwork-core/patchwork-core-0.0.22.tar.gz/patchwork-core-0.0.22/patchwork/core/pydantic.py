# -*- coding: utf-8 -*-
# Note: this file is a port of pending PR on Pydantic (https://github.com/samuelcolvin/pydantic/pull/3159)
# about adding support for nested settings in ENV settings source
# https://github.com/samuelcolvin/pydantic/blob/1994a926bcdd14aac008dac00dcd779a37a61880/pydantic/env_settings.py

import sys

from pathlib import Path

import os

from pydantic import BaseSettings
from pydantic.typing import get_origin
from pydantic.env_settings import read_env_file, SettingsError
from typing import Optional, Mapping, Dict, Any, Type, Union


try:
    from typing import GenericAlias as TypingGenericAlias  # type: ignore
except ImportError:
    # python < 3.9 does not have GenericAlias (list[int], tuple[str, ...] and so on)
    TypingGenericAlias = ()


StrPath = Union[str, os.PathLike]


if sys.version_info < (3, 10):

    def is_union_origin(tp: Type[Any]) -> bool:
        return tp is Union

    WithArgsTypes = (TypingGenericAlias,)

else:
    import types
    import typing

    def is_union_origin(origin: Type[Any]) -> bool:
        return origin is Union or origin is types.UnionType  # noqa: E721

    WithArgsTypes = (typing._GenericAlias, types.GenericAlias, types.UnionType)


class NestedEnvSettingsSource:
    __slots__ = ('env_file', 'env_file_encoding', 'env_nested_delimiter')

    def __init__(
        self, env_file: Optional[StrPath], env_file_encoding: Optional[str], env_nested_delimiter: Optional[str]
    ):
        self.env_file: Optional[StrPath] = env_file
        self.env_file_encoding: Optional[str] = env_file_encoding
        self.env_nested_delimiter: Optional[str] = env_nested_delimiter

    def get_env_vars(self, settings: BaseSettings) -> Mapping[str, Optional[str]]:
        if settings.__config__.case_sensitive:
            env_vars: Mapping[str, Optional[str]] = os.environ
        else:
            env_vars = {k.lower(): v for k, v in os.environ.items()}

        if self.env_file is None:
            self.env_file = settings.__config__.env_file

        if self.env_file_encoding is None:
            self.env_file_encoding = settings.__config__.env_file_encoding

        if self.env_nested_delimiter is None:
            self.env_nested_delimiter = settings.__config__.env_nested_delimiter or '__'

        if self.env_file is not None:
            env_path = Path(self.env_file).expanduser()
            if env_path.is_file():
                env_vars = {
                    **read_env_file(
                        env_path, encoding=self.env_file_encoding, case_sensitive=settings.__config__.case_sensitive
                    ),
                    **env_vars,
                }
        return env_vars

    def explode_env_vars(self, settings: BaseSettings, env_vars: Mapping[str, Optional[str]]) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        for env_name, env_val in env_vars.items():
            keys = env_name.split(self.env_nested_delimiter)
            env_var = result
            for idx, key in enumerate(keys):
                if idx == len(keys) - 1:
                    try:
                        env_val = settings.__config__.json_loads(env_val)  # type: ignore
                    except (ValueError, TypeError):
                        ...
                    env_var[key] = env_val
                else:
                    env_var = env_var.setdefault(key, {})
        return result

    def __call__(self, settings: BaseSettings) -> Dict[str, Any]:
        """
        Build environment variables suitable for passing to the Model.
        """
        d: Dict[str, Optional[str]] = {}

        env_vars = self.get_env_vars(settings)
        if self.env_nested_delimiter is not None:
            env_vars = self.explode_env_vars(settings, env_vars)

        for field in settings.__fields__.values():
            env_val: Optional[str] = None
            for env_name in field.field_info.extra['env_names']:
                env_val = env_vars.get(env_name)
                if env_val is not None:
                    break

            if env_val is None:
                continue

            if field.is_complex():
                if isinstance(env_val, (str, bytes, bytearray)):
                    try:
                        env_val = settings.__config__.json_loads(env_val)
                    except ValueError as e:
                        raise SettingsError(f'error parsing JSON for "{env_name}"') from e
            elif (
                is_union_origin(get_origin(field.type_))
                and field.sub_fields
                and any(f.is_complex() for f in field.sub_fields)
            ):
                if isinstance(env_val, (str, bytes, bytearray)):
                    try:
                        env_val = settings.__config__.json_loads(env_val)
                    except ValueError:
                        pass
            d[field.alias] = env_val
        return d

    def __repr__(self) -> str:
        return f'NestedEnvSettingsSource(env_file={self.env_file!r}, env_file_encoding={self.env_file_encoding!r})'


nested_env_settings = NestedEnvSettingsSource(None, None, None)
