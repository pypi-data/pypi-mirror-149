# -*- coding: utf-8 -*-
import os

import pytest
from pydantic import BaseSettings, BaseModel

from patchwork.core.pydantic import nested_env_settings


class SetEnv:
    def __init__(self):
        self.envars = set()

    def set(self, name, value):
        self.envars.add(name)
        os.environ[name] = value

    def clear(self):
        for n in self.envars:
            os.environ.pop(n)


@pytest.fixture
def env():
    setenv = SetEnv()

    yield setenv

    setenv.clear()


class Settings(BaseSettings):
    class Config:
        @classmethod
        def customise_sources(
            cls,
            init_settings,
            env_settings,
            file_secret_settings,
        ):
            return (
                init_settings,
                nested_env_settings,
                file_secret_settings,
            )


def test_nested_env_delimiter(env):
    class SubSubValue(BaseModel):
        v6: str

    class SubValue(BaseModel):
        v4: str
        v5: str
        sub_sub: SubSubValue

    class TopValue(Settings):
        v1: str
        v2: str
        v3: str
        sub: SubValue

    class Cfg(Settings):
        v0: str
        top: TopValue

        class Config:
            env_nested_delimiter = '__'

    env.set('top', '{"v1": "1", "v2": "2", "sub": {"v5": "xx"}}')
    env.set('v0', '0')
    env.set('top__v3', '3')
    env.set('top__sub', '{"sub_sub": {"v6": "6"}}')
    env.set('top__sub__v4', '4')
    env.set('top__sub__v5', '5')
    cfg = Cfg()
    assert cfg.dict() == {
        'v0': '0',
        'top': {
            'v1': '1',
            'v2': '2',
            'v3': '3',
            'sub': {
                'v4': '4',
                'v5': '5',
                'sub_sub': {
                    'v6': '6'
                }
            },
        },
    }

