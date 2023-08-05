from types import TracebackType
from typing import Any
from typing import Callable
from typing import Dict
from typing import Iterable
from typing import List
from typing import Tuple

WSGICallable = Callable[[Dict[str, Any], Callable], Iterable[bytes]]
ExcInfoTuple = Tuple[type, BaseException, TracebackType]
HeadersList = List[Tuple[str, str]]
