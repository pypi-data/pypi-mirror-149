from typing_extensions import Literal

WORKER_THREAD: Literal["thread"]
WORKER_GREENLET: Literal["greenlet"]
WORKER_PROCESS: Literal["process"]
WORKER_TYPES: tuple[Literal["thread"], Literal["greenlet"], Literal["process"]]

class EmptyData: ...
