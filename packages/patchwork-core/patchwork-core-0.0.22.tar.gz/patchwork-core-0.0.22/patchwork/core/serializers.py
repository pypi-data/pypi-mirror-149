# -*- coding: utf-8 -*-

import json
from typing import Any


class Serializer:

    @classmethod
    def loads(cls, data: bytes) -> Any:
        raise NotImplementedError()

    @classmethod
    def dumps(cls, data: Any) -> bytes:
        raise NotImplementedError()


class NoOpSerializer(Serializer):

    @classmethod
    def loads(cls, data: Any) -> Any:
        return data

    @classmethod
    def dumps(cls, data: Any) -> Any:
        return data


class JSONSerializer(Serializer):

    @classmethod
    def loads(cls, data: bytes):
        return json.loads(data)

    @classmethod
    def dumps(cls, data: Any) -> bytes:
        return json.dumps(data).encode('utf-8')
