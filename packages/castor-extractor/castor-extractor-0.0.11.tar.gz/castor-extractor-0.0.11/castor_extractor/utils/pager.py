from itertools import chain
from typing import (
    Callable,
    Generic,
    Iterator,
    List,
    Optional,
    Sequence,
    TypeVar,
)

_DEFAULT_PER_PAGE = 100

T = TypeVar("T")


class PagerLogger:
    def on_page(self, page: int, count: int):
        pass

    def on_success(self, page: int, total: int):
        pass


class Pager(Generic[T]):
    def __init__(
        self,
        callback: Callable[[int, int], Sequence[T]],
        logger: Optional[PagerLogger] = None,
    ):
        self._callback = callback
        self._logger = logger or PagerLogger()

    def all(self, per_page: int = _DEFAULT_PER_PAGE) -> List[T]:
        """Returns all data provided by the callback as a list"""
        return list(chain.from_iterable(self.iterator(per_page=per_page)))

    def iterator(
        self, per_page: int = _DEFAULT_PER_PAGE
    ) -> Iterator[Sequence[T]]:
        """Yields data provided by the callback as a list page by page"""
        page = 1
        total_results = 0

        while True:
            results = self._callback(page, per_page)
            nb_results = len(results)

            self._logger.on_page(page, nb_results)

            if nb_results == 0:
                break

            yield results

            total_results += nb_results
            page += 1

        self._logger.on_success(page, total_results)
