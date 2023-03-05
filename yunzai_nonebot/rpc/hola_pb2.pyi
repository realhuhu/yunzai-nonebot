from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class OptionCode(_message.Message):
    __slots__ = ["code"]
    CODE_FIELD_NUMBER: _ClassVar[int]
    code: int
    def __init__(self, code: _Optional[int] = ...) -> None: ...

class Request(_message.Message):
    __slots__ = ["request", "self_id"]
    REQUEST_FIELD_NUMBER: _ClassVar[int]
    SELF_ID_FIELD_NUMBER: _ClassVar[int]
    request: int
    self_id: str
    def __init__(self, self_id: _Optional[str] = ..., request: _Optional[int] = ...) -> None: ...

class Response(_message.Message):
    __slots__ = ["response"]
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    response: int
    def __init__(self, response: _Optional[int] = ...) -> None: ...
