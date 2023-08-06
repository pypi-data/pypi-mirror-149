# -*- coding: utf-8 -*-

from pydantic import BaseSettings, BaseModel, ValidationError
from pydantic.fields import ModelField
from typing import TypeVar, Generic, Type, Union, Mapping

from patchwork.core import Component, AsyncPublisher, AsyncSubscriber
from patchwork.core.config.providers import json_config_settings_source
from patchwork.core.pydantic import nested_env_settings
from patchwork.core.typing import ClassPath


class ImproperlyConfigured(Exception):
    """
    Invalid configuration detected
    """
    pass


ClassType = TypeVar("ClassType", bound=Type[object])


class ClassConfig(Generic[ClassType]):

    engine: ClassPath[ClassType]
    options: Mapping = {}

    def __init__(self, engine: ClassType, options: Mapping = None):
        self.engine = engine
        self.options = options or {}

    @classmethod
    def __get_validators__(cls):
        yield cls.dependency_validator

    @classmethod
    def dependency_validator(cls, v, field: ModelField):
        if isinstance(v, cls):
            return v

        engine_field = ModelField(name='engine', type_=ClassPath[ClassType],
                                  class_validators=None, model_config=field.model_config)
        engine, error = engine_field.validate(v.pop('engine', None), {}, loc='engine')
        if error:
            raise ValidationError([error], cls)

        # TODO: it will be nice to have validate options against constructor arguments
        opts = v
        return cls(engine=engine.type_, options=opts)

    def instantiate(self, **init_kwargs):
        return self.engine(**self.options, **init_kwargs)


ComponentType = TypeVar("ComponentType", bound=Type[Component])


class ComponentConfig(Generic[ComponentType]):
    """
    pydantic custom type for Dependencies.
    A dependency is a configuration of another component. Configuration must have at least `engine`
    defined which points to class and optionally may have a dict of `options` which will be passed
    to the engine. Options must follow engine `Settings`.
    """

    engine: ClassPath[ComponentType]
    options: BaseModel = BaseModel()

    def __init__(self, engine: ComponentType, options: Union[BaseModel, dict] = None):
        self.engine = engine
        if options is None:
            options = engine.Config()
        elif isinstance(options, dict):
            options = engine.Config(**options)
        else:
            assert isinstance(options, engine.Config), \
                f"model config for {engine} must be an instance of the component config"
        self.options = options

    @classmethod
    def __get_validators__(cls):
        yield cls.dependency_validator

    @classmethod
    def dependency_validator(cls, v, field: ModelField):
        if isinstance(v, cls):
            return v

        engine_field = ModelField(name='engine', type_=ClassPath[ComponentType],
                                  class_validators=None, model_config=field.model_config)
        engine, error = engine_field.validate(v.pop('engine', None), {}, loc='engine')
        if error:
            raise ValidationError([error], cls)

        options_field = getattr(engine.type_, 'Config', None)
        if options_field is not None:
            opts = options_field.validate(v)
        else:
            opts = {}
        return cls(engine=engine.type_, options=opts)

    def instantiate(self, parent=None, **init_kwargs):
        return self.engine(**({"parent": parent} if parent is not None else {}), **self.options.dict(), **init_kwargs)


PublisherConfig = ComponentConfig[Type[AsyncPublisher]]
SubscriberConfig = ComponentConfig[Type[AsyncSubscriber]]


class PatchworkConfig(BaseSettings):

    class Config:
        env_prefix = 'patchwork_'
        env_file = '.env'
        env_file_encoding = 'utf-8'
        json_file = 'settings.json'
        secrets_dir = None

        @classmethod
        def customise_sources(
            cls,
            init_settings,
            env_settings,
            file_secret_settings,
        ):
            return (
                init_settings,
                json_config_settings_source,
                nested_env_settings,
                env_settings,
                file_secret_settings,
            )
