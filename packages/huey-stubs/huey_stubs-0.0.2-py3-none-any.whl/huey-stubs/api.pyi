import datetime
from functools import partial as partial
from logging import Logger
from types import TracebackType
from typing import Any, Callable, Generic, Iterable, Iterator, TypeVar, overload

from typing_extensions import ContextManager, ParamSpec

from huey.constants import EmptyData as EmptyData
from huey.consumer import Consumer as Consumer
from huey.exceptions import (
    CancelExecution as CancelExecution,
    ConfigurationError as ConfigurationError,
    HueyException as HueyException,
    RetryTask as RetryTask,
    TaskException as TaskException,
    TaskLockedException as TaskLockedException,
)
from huey.registry import Registry as Registry
from huey.serializer import Serializer as Serializer
from huey.signals import _SIGNAL
from huey.storage import (
    BaseStorage,
    BlackHoleStorage as BlackHoleStorage,
    FileStorage as FileStorage,
    MemoryStorage as MemoryStorage,
    PriorityRedisExpireStorage as PriorityRedisExpireStorage,
    PriorityRedisStorage as PriorityRedisStorage,
    RedisExpireStorage as RedisExpireStorage,
    RedisStorage as RedisStorage,
    SqliteStorage as SqliteStorage,
)
from huey.utils import (
    Error as Error,
    normalize_expire_time as normalize_expire_time,
    normalize_time as normalize_time,
    reraise_as as reraise_as,
    string_type as string_type,
    time_clock as time_clock,
    to_timestamp as to_timestamp,
)

logger: Logger

_T = TypeVar("_T")
_P = ParamSpec("_P")
_OnComplete = TypeVar("_OnComplete", bound=Task | None)

_OnStartupHandler = Callable[[], Any]
_OnShutdownHandler = Callable[[], Any]
_PreExecuteHandler = Callable[[Task], Any]
_PostExecuteHandler = Callable[[Task, Any | None, Exception | None], Any]
_SignalHandler = Callable[[str, Task], Any] | Callable[[str, Task, Exception], Any]
_H = TypeVar("_H", bound=_SignalHandler)

# When changing methods of this class, also change corresponding functions in
# django-huey-stubs/__init__.pyi and
# huey-stubs/contrib/djhuey/__init__.pyi
class Huey:
    _registry: Registry
    storage_class: type[BaseStorage]
    name: str
    results: bool
    store_none: bool
    utc: bool
    immediate_use_memory: bool
    serializer: Serializer
    storage_kwargs: dict[str, Any]
    storage: BaseStorage
    def __init__(
        self,
        name: str = ...,
        results: bool = ...,
        store_none: bool = ...,
        utc: bool = ...,
        immediate: bool = ...,
        serializer: Serializer | None = ...,
        compression: bool = ...,
        use_zlib: bool = ...,
        immediate_use_memory: bool = ...,
        always_eager: bool | None = ...,
        storage_class: type[BaseStorage] | None = ...,
        **storage_kwargs: Any,
    ) -> None: ...
    def create_storage(self) -> BaseStorage: ...
    def get_immediate_storage(self) -> MemoryStorage: ...
    def get_storage(self, **kwargs: Any) -> BaseStorage: ...
    @property
    def immediate(self) -> bool: ...
    @immediate.setter
    def immediate(self, value: bool) -> None: ...
    def create_consumer(self, **options: Any) -> Consumer: ...
    def task(
        self,
        retries: int = ...,
        retry_delay: int = ...,
        priority: int | None = ...,
        context: bool = ...,
        name: str | None = ...,
        expires: int | datetime.timedelta | datetime.datetime | None = ...,
        **kwargs: Any,
    ) -> Callable[[Callable[_P, _T]], TaskWrapper[_T, _P]]: ...
    def periodic_task(
        self,
        validate_datetime,
        retries: int = ...,
        retry_delay: int = ...,
        priority: int | None = ...,
        context: bool = ...,
        name: str | None = ...,
        expires: int | datetime.timedelta | datetime.datetime | None = ...,
        **kwargs: Any,
    ) -> Callable[[Callable[_P, _T]], TaskWrapper[_T, _P]]: ...
    def context_task(
        self,
        obj: ContextManager,
        as_argument: bool = ...,
        retries: int = ...,
        retry_delay: int = ...,
        priority: int | None = ...,
        context: bool = ...,
        name: str | None = ...,
        expires: int | datetime.timedelta | datetime.datetime | None = ...,
        **kwargs: Any,
    ) -> Callable[[Callable[_P, _T]], TaskWrapper[_T, _P]]: ...
    def pre_execute(
        self, name: str | None = ...
    ) -> Callable[[_PreExecuteHandler], _PreExecuteHandler]: ...
    def unregister_pre_execute(self, name: str | Callable) -> bool: ...
    def post_execute(
        self, name: str | None = ...
    ) -> Callable[[_PostExecuteHandler], _PostExecuteHandler,]: ...
    def unregister_post_execute(self, name: str | Callable) -> bool: ...
    def on_startup(
        self, name: str | None = ...
    ) -> Callable[[_OnStartupHandler], _OnStartupHandler]: ...
    def unregister_on_startup(self, name: str | Callable) -> bool: ...
    def on_shutdown(
        self, name: str | None = ...
    ) -> Callable[[_OnShutdownHandler], _OnShutdownHandler]: ...
    def unregister_on_shutdown(self, name: str | Callable | None = ...) -> bool: ...
    def notify_interrupted_tasks(self) -> None: ...
    def signal(self, *signals: _SIGNAL) -> Callable[[_H], _H]: ...
    def disconnect_signal(
        self, receiver: _SignalHandler, *signals: _SIGNAL
    ) -> None: ...
    def serialize_task(self, task: Task) -> bytes: ...
    def deserialize_task(self, data: bytes) -> Task: ...
    @overload
    def enqueue(
        self, task: Task[_T, None]
    ) -> Result[_T, None]: ...  # TODO: Could technically be None as well
    @overload
    def enqueue(
        self, task: Task[_T, Task]
    ) -> ResultGroup: ...  # TODO: Could technically be None as well
    def dequeue(self) -> Task | None: ...
    def put(self, key: str, data: Any) -> None: ...
    def put_result(self, key: str, data: Any) -> None: ...
    def put_if_empty(self, key: str, data: Any) -> bool: ...
    def get_raw(self, key: str, peek: bool = ...) -> bytes | type[EmptyData]: ...
    def get(self, key: str, peek: bool = ...) -> Any | None: ...
    def delete(self, key: str) -> bool: ...
    def execute(
        self, task: Task[_T, _OnComplete], timestamp: datetime.datetime | None = ...
    ) -> _T: ...
    def build_error_result(
        self, task: Task, exception: Exception
    ) -> dict[str, Any]: ...
    def revoke_all(
        self,
        task_class: type[Task],
        revoke_until: datetime.datetime | None = ...,
        revoke_once: bool = ...,
    ) -> None: ...
    def restore_all(self, task_class: type[Task]) -> bool: ...
    def revoke(
        self,
        task: Task,
        revoke_until: datetime.datetime | None = ...,
        revoke_once: bool = ...,
    ) -> None: ...
    def restore(self, task: Task) -> bool: ...
    def revoke_by_id(
        self,
        id: str,
        revoke_until: datetime.datetime | None = ...,
        revoke_once: bool = ...,
    ) -> None: ...
    def restore_by_id(self, id: str) -> bool: ...
    def is_revoked(
        self,
        task: Task | str,
        timestamp: datetime.datetime | None = ...,
        peek: bool = ...,
    ) -> bool: ...
    def add_schedule(self, task: Task) -> None: ...
    def read_schedule(
        self, timestamp: datetime.datetime | None = ...
    ) -> list[Task]: ...
    def read_periodic(self, timestamp: datetime.datetime) -> list[Task]: ...
    def ready_to_run(self, task: Task, timestamp: datetime.datetime | None = ...): ...
    def pending(self, limit: int | None = ...) -> list[Task]: ...
    def pending_count(self) -> int: ...
    def scheduled(self, limit: int | None = ...) -> list[Task]: ...
    def scheduled_count(self) -> int: ...
    def all_results(self) -> dict[str, Any]: ...
    def result_count(self) -> int: ...
    def __len__(self) -> int: ...
    def flush(self) -> None: ...
    def lock_task(self, lock_name: str) -> TaskLock: ...
    def flush_locks(self, *names: str) -> set[str]: ...
    def result(
        self,
        id: str,
        blocking: bool = ...,
        timeout: int | None = ...,
        backoff: float = ...,
        max_delay: float = ...,
        revoke_on_timeout: bool = ...,
        preserve: bool = ...,
    ) -> Any: ...

class Task(Generic[_T, _OnComplete]):
    default_expires: None
    default_priority: None
    default_retries: int
    default_retry_delay: int
    name: str
    args: tuple[Any, ...]
    kwargs: dict[str, Any]
    id: str
    revoke_id: str
    eta: datetime.datetime | None
    retries: int
    retry_delay: int
    priority: int | None
    expires: int | datetime.timedelta | datetime.datetime | None
    expires_resolved: datetime.datetime
    on_complete: _OnComplete
    on_error: Task | None
    def __init__(
        self,
        args: tuple[Any, ...] | None = ...,
        kwargs: dict[str, Any] | None = ...,
        id: str | None = ...,
        eta: datetime.datetime | None = ...,
        retries: int | None = ...,
        retry_delay: int | None = ...,
        priority: int | None = ...,
        expires: int | datetime.timedelta | datetime.datetime | None = ...,
        on_complete: Task | None = ...,
        on_error: Task | None = None,
        expires_resolved: datetime.datetime | None = ...,
    ) -> None: ...
    @property
    def data(self) -> tuple[tuple[Any, ...], dict[str, Any]]: ...
    def __hash__(self) -> int: ...
    def create_id(self) -> str: ...
    def resolve_expires(self, utc: bool = ...) -> datetime.datetime: ...
    def extend_data(self, data: Any) -> None: ...
    def then(
        self, task: TaskWrapper[Any, _P], *args: _P.args, **kwargs: _P.kwargs
    ) -> Task[_T, Task]: ...
    def error(
        self, task: TaskWrapper[Any, _P], *args: _P.args, **kwargs: _P.kwargs
    ) -> Task[_T, _OnComplete]: ...
    def execute(self) -> _T: ...
    def __eq__(self, rhs: Any) -> bool: ...

class PeriodicTask(Task[_T, _OnComplete]):
    def validate_datetime(self, timestamp: datetime.datetime) -> bool: ...

class TaskWrapper(Generic[_T, _P]):  # TODO: Reorder the generics?
    task_base: type[Task]
    __doc__: str
    huey: Huey
    func: Callable
    retries: int | None
    retry_delay: int | None
    context: bool
    name: str | None
    settings: dict[str, Any]
    task_class: type[Task]
    def __init__(
        self,
        huey: Huey,
        func: Callable[_P, _T],
        retries: int | None = ...,
        retry_delay: int | None = ...,
        context: bool = ...,
        name: str | None = ...,
        task_base: type[Task] | None = ...,
        **settings: Any,
    ) -> None: ...
    def unregister(self) -> bool: ...
    def create_task(
        self,
        func: Callable,
        context: bool = ...,
        name: str | None = ...,
        **settings: Any,
    ) -> type[Task]: ...
    def is_revoked(
        self, timestamp: datetime.datetime | None = ..., peek: bool = ...
    ) -> bool: ...
    def revoke(
        self, revoke_until: datetime.datetime | None = ..., revoke_once: bool = ...
    ) -> None: ...
    def restore(self) -> bool: ...
    def schedule(
        self,
        args: tuple[Any, ...] | None = ...,
        kwargs: dict[str, Any] | None = ...,
        eta: datetime.datetime | None = ...,
        delay: int | None = ...,
        priority: int | None = ...,
        retries: int | None = ...,
        retry_delay: int | None = ...,
        expires: int | datetime.timedelta | datetime.datetime | None = ...,
        id: str | None = ...,
    ): ...
    def map(self, it: Iterable) -> ResultGroup: ...
    def __call__(
        self, *args: _P.args, **kwargs: _P.kwargs
    ) -> Result[_T, None]: ...  # TODO: Could technically be None as well
    def call_local(self, *args: _P.args, **kwargs: _P.kwargs) -> _T: ...
    def s(self, *args: _P.args, **kwargs: _P.kwargs) -> Task[_T, None]: ...

class TaskLock:
    def __init__(self, huey: Huey, name: str) -> None: ...
    def __call__(self, fn: Callable[_P, _T]) -> Callable[_P, _T]: ...
    def __enter__(self) -> None: ...
    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None: ...
    def clear(self) -> bool: ...

class Result(Generic[_T, _OnComplete]):
    huey: Huey
    task: Task[_T, _OnComplete]
    def __init__(self, huey: Huey, task: Task[_T, _OnComplete]) -> None: ...
    @property
    def id(self) -> str: ...
    def __call__(
        self,
        blocking: bool = ...,
        timeout: int | None = ...,
        backoff: float = ...,
        max_delay: float = ...,
        revoke_on_timeout: bool = ...,
        preserve: bool = ...,
    ) -> _T: ...
    def get_raw_result(
        self,
        blocking: bool = ...,
        timeout: int | None = ...,
        backoff: float = ...,
        max_delay: float = ...,
        revoke_on_timeout: bool = ...,
        preserve: bool = ...,
    ) -> _T | Error: ...
    def get(
        self,
        blocking: bool = ...,
        timeout: int | None = ...,
        backoff: float = ...,
        max_delay: float = ...,
        revoke_on_timeout: bool = ...,
        preserve: bool = ...,
    ) -> _T: ...
    def is_revoked(self) -> bool: ...
    def revoke(self, revoke_once: bool = ...) -> None: ...
    def restore(self) -> bool: ...
    @overload
    def reschedule(
        self: Result[_T, None],
        eta: datetime.datetime | None = ...,
        delay: int | None = ...,
        expires: int | datetime.timedelta | datetime.datetime | None = ...,
    ) -> Result[_T, None]: ...  # TODO: Could technically be None as well
    @overload
    def reschedule(
        self: Result[_T, Task],
        eta: datetime.datetime | None = ...,
        delay: int | None = ...,
        expires: int | datetime.timedelta | datetime.datetime | None = ...,
    ) -> ResultGroup: ...  # TODO: Could technically be None as well
    def reset(self) -> None: ...

class ResultGroup:
    def __init__(self, results: Iterable[Result]) -> None: ...
    def get(
        self,
        blocking: bool = ...,
        timeout: int | None = ...,
        backoff: float = ...,
        max_delay: float = ...,
        revoke_on_timeout: bool = ...,
        preserve: bool = ...,
    ) -> list[Any]: ...
    def __call__(
        self,
        blocking: bool = ...,
        timeout: int | None = ...,
        backoff: float = ...,
        max_delay: float = ...,
        revoke_on_timeout: bool = ...,
        preserve: bool = ...,
    ) -> list[Any]: ...
    def __getitem__(self, idx: int) -> Any: ...
    def __iter__(self) -> Iterator[Result]: ...
    def __len__(self) -> int: ...

def crontab(
    minute: str = ...,
    hour: str = ...,
    day: str = ...,
    month: str = ...,
    day_of_week: str = ...,
    strict: bool = ...,
) -> Callable[[datetime.datetime], bool]: ...

class BlackHoleHuey(Huey):
    storage_class: type[BlackHoleStorage]

class MemoryHuey(Huey):
    storage_class: type[MemoryStorage]

class SqliteHuey(Huey):
    storage_class: type[SqliteStorage]

class RedisHuey(Huey):
    storage_class: type[RedisStorage]

class RedisExpireHuey(Huey):
    storage_class: type[RedisExpireStorage]

class PriorityRedisHuey(Huey):
    storage_class: type[PriorityRedisStorage]

class PriorityRedisExpireHuey(Huey):
    storage_class: type[PriorityRedisExpireStorage]

class FileHuey(Huey):
    storage_class: type[FileStorage]
