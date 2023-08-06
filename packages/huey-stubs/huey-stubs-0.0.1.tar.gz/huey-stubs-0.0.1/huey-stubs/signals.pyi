import sys
from typing import Any

from typing_extensions import Literal, TypeAlias

if sys.version_info[0] < 3:
    Incomplete: TypeAlias = Any
else:
    from _typeshed import Incomplete

SIGNAL_CANCELED: Literal["canceled"]
SIGNAL_COMPLETE: Literal["complete"]
SIGNAL_ERROR: Literal["error"]
SIGNAL_EXECUTING: Literal["executing"]
SIGNAL_EXPIRED: Literal["expired"]
SIGNAL_LOCKED: Literal["locked"]
SIGNAL_RETRYING: Literal["retrying"]
SIGNAL_REVOKED: Literal["revoked"]
SIGNAL_SCHEDULED: Literal["scheduled"]
SIGNAL_INTERRUPTED: Literal["interrupted"]
_SIGNAL = Literal[
    "canceled",
    "complete",
    "error",
    "executing",
    "expired",
    "locked",
    "retrying",
    "revoked",
    "scheduled",
    "interrupted",
]

class Signal:
    receivers: Incomplete
    def __init__(self) -> None: ...
    def connect(self, receiver, *signals) -> None: ...
    def disconnect(self, receiver, *signals) -> None: ...
    def send(self, signal, task, *args, **kwargs) -> None: ...
