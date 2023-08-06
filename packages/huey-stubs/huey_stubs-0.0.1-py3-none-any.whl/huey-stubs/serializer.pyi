import gzip
import sys
from typing import Any

from typing_extensions import TypeAlias

if sys.version_info[0] < 3:
    Incomplete: TypeAlias = Any
else:
    from _typeshed import Incomplete

from huey.exceptions import ConfigurationError as ConfigurationError
from huey.utils import encode as encode

logger: Incomplete
if sys.version_info[0] > 2:
    gzip_compress = gzip.compress
    gzip_decompress = gzip.decompress
else:
    def gzip_compress(data: Incomplete, comp_level: Incomplete): ...
    def gzip_decompress(data: Incomplete): ...

def is_compressed(data): ...

class Serializer:
    comp: Incomplete
    comp_level: Incomplete
    use_zlib: Incomplete
    pickle_protocol: Incomplete
    def __init__(
        self,
        compression: bool = ...,
        compression_level: int = ...,
        use_zlib: bool = ...,
        pickle_protocol=...,
    ) -> None: ...
    def serialize(self, data): ...
    def deserialize(self, data): ...

def constant_time_compare(s1, s2): ...

class SignedSerializer(Serializer):
    secret: Incomplete
    salt: Incomplete
    separator: bytes
    def __init__(
        self, secret: Incomplete | None = ..., salt: str = ..., **kwargs
    ) -> None: ...
