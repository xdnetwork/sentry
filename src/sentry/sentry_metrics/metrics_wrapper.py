from collections import ChainMap
from typing import MutableMapping, Optional, Union

from sentry.metrics.base import MetricsBackend

Tags = MutableMapping[str, str]


class MetricsWrapper(MetricsBackend):
    def __init__(
        self,
        backend: MetricsBackend,
        name: Optional[str] = None,
        tags: Optional[Tags] = None,
    ) -> None:
        self.__backend = backend
        self.__name = name
        self.__tags = tags

    def __merge_name(self, name: str) -> str:
        if self.__name is None:
            return name
        else:
            return f"{self.__name}.{name}"

    def __merge_tags(self, tags: Optional[Tags]) -> Optional[Tags]:
        if self.__tags is None:
            return tags
        elif tags is None:
            return self.__tags
        else:
            return ChainMap(tags, self.__tags)

    def increment(
        self, name: str, value: Union[int, float] = 1, tags: Optional[Tags] = None
    ) -> None:
        # sentry metrics backend uses `incr` instead of `increment`
        self.__backend.incr(self.__merge_name(name), value, self.__merge_tags(tags))  # type: ignore[no-untyped-call]

    def gauge(self, name: str, value: Union[int, float], tags: Optional[Tags] = None) -> None:  # type: ignore[override]
        self.__backend.gauge(self.__merge_name(name), value, self.__merge_tags(tags))  # type: ignore[no-untyped-call]

    def timing(self, name: str, value: Union[int, float], tags: Optional[Tags] = None) -> None:  # type: ignore[override]
        self.__backend.timing(self.__merge_name(name), value, self.__merge_tags(tags))  # type: ignore[no-untyped-call]
