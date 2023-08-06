# -*- coding: utf-8 -*-
from typing import Type
from pydantic import BaseModel

from patchwork.core.typing import ClassPath


class Test:
    pass


def test_without_type():
    class M(BaseModel):
        path: ClassPath

    m = M(path='tests.core.test_classpath:Test')


def test_with_type():
    class M(BaseModel):
        path: ClassPath[Type[Test]]

    m = M(path='tests.core.test_classpath:Test')


def test_default():
    class M(BaseModel):
        path: ClassPath[Type[Test]] = ClassPath(Test)

    m = M()
    assert issubclass(m.path.type_, Test)
