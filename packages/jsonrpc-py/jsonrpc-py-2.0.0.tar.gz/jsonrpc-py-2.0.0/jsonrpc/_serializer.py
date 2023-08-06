# Pure zero-dependency JSON-RPC 2.0 implementation.
# Copyright © 2022 Andrew Malchuk. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from abc import ABCMeta, abstractmethod
from json.decoder import JSONDecoder
from json.encoder import JSONEncoder
from typing import Any, Final

from ._errors import Error, ErrorEnum

__all__: Final[list[str]] = ["JSONSerializer"]

# Ensure to output JSON as a strict JavaScript subset:
_JSON_ESCAPE_TABLE: Final[dict[int, str]] = {
    0x2028: "\\u2028",
    0x2029: "\\u2029"
}


class BaseSerializer(metaclass=ABCMeta):
    __slots__: tuple[str, ...] = ()

    @abstractmethod
    def serialize(self, obj: Any, /) -> bytes:
        raise NotImplementedError

    @abstractmethod
    def deserialize(self, obj: bytes, /) -> Any:
        raise NotImplementedError


class JSONSerializer(BaseSerializer):
    """
    Simple class for JSON serialization and deserialization.
    Combines the :py:class:`json.JSONEncoder` and :py:class:`json.JSONDecoder` objects.
    Primarily used by the :class:`jsonrpc.WSGIHandler` instance for (de)serialization the requests and responses.
    """
    __slots__: list[str] = ["_encoder", "_decoder"]

    def __init__(self) -> None:
        self._encoder: Final[JSONEncoder] = JSONEncoder(ensure_ascii=False, separators=("\x2C", "\x3A"))
        self._decoder: Final[JSONDecoder] = JSONDecoder(strict=False)

    def __repr__(self) -> str:
        return f"<{__package__}.{self.__class__.__name__}()>"

    def serialize(self, obj: Any, /) -> bytes:
        """
        Returns the JSON representation of a value.

        :param obj: An any type of object that must be JSON serializable.
        :raises jsonrpc.Error: If any exception has occurred due the serialization or/and encoding to :py:class:`bytes`.
        :returns: The :py:class:`bytes` object containing the serialized Python data structure.
        """
        try:
            return self._encoder.encode(obj).translate(_JSON_ESCAPE_TABLE).encode("utf-8", "surrogatepass")
        except Exception as exc:
            raise Error(code=ErrorEnum.PARSE_ERROR, message="Failed to serialize object to JSON") from exc

    def deserialize(self, obj: bytes, /) -> Any:
        """
        Returns the value encoded in JSON in appropriate Python type.

        :param obj: The :py:class:`bytes` object containing the serialized JSON document.
        :raises jsonrpc.Error: If any exception has occurred due the deserialization or/and decoding from :py:class:`bytes`.
        :returns: An any type of object containing the deserialized Python data structure.
        """
        try:
            return self._decoder.decode(obj.decode("utf-8", "surrogatepass"))
        except Exception as exc:
            raise Error(code=ErrorEnum.PARSE_ERROR, message="Failed to deserialize object from JSON") from exc
