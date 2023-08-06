import datetime
from typing import Any, Callable, TypeVar, overload

from typing_extensions import ParamSpec

from huey import Huey
from huey.api import (
    Result,
    ResultGroup,
    Task,
    TaskLock,
    TaskWrapper,
    _OnShutdownHandler,
    _OnStartupHandler,
    _PostExecuteHandler,
    _PreExecuteHandler,
    _SignalHandler,
)
from huey.signals import _SIGNAL

HUEY: Huey

_T = TypeVar("_T")
_P = ParamSpec("_P")
_OnComplete = TypeVar("_OnComplete", bound=Task | None)

# When changing these functions, also change the corresponding functions in
# django_huey-stubs/__init__.pyi and
# huey-stubs/api.pyi
def task(
    retries: int = ...,
    retry_delay: int = ...,
    priority: int | None = ...,
    context: bool = ...,
    name: str | None = ...,
    expires: int | datetime.timedelta | datetime.datetime | None = ...,
    **kwargs: Any,
) -> Callable[[Callable[_P, _T]], TaskWrapper[_T, _P]]: ...
def periodic_task(
    validate_datetime,
    retries: int = ...,
    retry_delay: int = ...,
    priority: int | None = ...,
    context: bool = ...,
    name: str | None = ...,
    expires: int | datetime.timedelta | datetime.datetime | None = ...,
    **kwargs: Any,
) -> Callable[[Callable[_P, _T]], TaskWrapper[_T, _P]]: ...
def lock_task(lock_name: str) -> TaskLock: ...
@overload
def enqueue(task: Task[_T, None]) -> Result[_T, None]: ...
@overload
def enqueue(task: Task[_T, Task]) -> ResultGroup: ...
def restore(task: Task) -> bool: ...
def restore_all(task_class: type[Task]) -> bool: ...
def restore_by_id(id: str) -> bool: ...
def revoke(
    task: Task, revoke_until: datetime.datetime | None = ..., revoke_once: bool = ...
) -> None: ...
def revoke_all(
    task_class: type[Task],
    revoke_until: datetime.datetime | None = ...,
    revoke_once: bool = ...,
) -> None: ...
def revoke_by_id(
    id: str, revoke_until: datetime.datetime | None = ..., revoke_once: bool = ...
) -> None: ...
def is_revoked(
    task: Task | str, timestamp: datetime.datetime | None = ..., peek: bool = ...
) -> bool: ...
def result(
    id: str,
    blocking: bool = ...,
    timeout: int | None = ...,
    backoff: float = ...,
    max_delay: float = ...,
    revoke_on_timeout: bool = ...,
    preserve: bool = ...,
) -> Any: ...
def scheduled(limit: int | None = ...) -> list[Task]: ...
def on_startup(
    name: str | None = ...,
) -> Callable[[_OnStartupHandler], _OnStartupHandler]: ...
def on_shutdown(
    name: str | None = ...,
) -> Callable[[_OnShutdownHandler], _OnShutdownHandler]: ...
def pre_execute(
    name: str | None = ...,
) -> Callable[[_PreExecuteHandler], _PreExecuteHandler]: ...
def post_execute(
    name: str | None = ...,
) -> Callable[[_PostExecuteHandler], _PostExecuteHandler,]: ...

_H = TypeVar("_H", bound=_SignalHandler)

def signal(
    *signals: _SIGNAL,
) -> Callable[[_H], _H]: ...
def disconnect_signal(receiver: _SignalHandler, *signals: _SIGNAL) -> None: ...
def close_db(fn: Callable[_P, _T]) -> Callable[_P, _T]: ...
def db_task(
    retries: int = ...,
    retry_delay: int = ...,
    priority: int | None = ...,
    context: bool = ...,
    name: str | None = ...,
    expires: int | datetime.timedelta | datetime.datetime | None = ...,
    **kwargs: Any,
) -> Callable[[Callable[_P, _T]], TaskWrapper[_T, _P]]: ...
def db_periodic_task(
    validate_datetime,
    retries: int = ...,
    retry_delay: int = ...,
    priority: int | None = ...,
    context: bool = ...,
    name: str | None = ...,
    expires: int | datetime.timedelta | datetime.datetime | None = ...,
    **kwargs: Any,
) -> Callable[[Callable[_P, _T]], TaskWrapper[_T, _P]]: ...
