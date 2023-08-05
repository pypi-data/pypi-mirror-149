from typing import Any, Callable, Generic, Iterable, List, TypeVar, Union

T = TypeVar("T")


class ClassBundle(Generic[T]):

    def __init__(self, objs: Iterable[T]) -> None:
        self._objs: List[T] = list(objs)

    def __passthrough__(self, __name: str) -> Union[List, Callable]:
        def func(*args, **kwargs):
            results = []
            for _o in self._objs:
                results.append(getattr(_o, __name)(*args, **kwargs))
            return results
        if all(callable(getattr(_o, __name)) for _o in self._objs):
            return func
        else:
            return [getattr(_o, __name) for _o in self._objs]

    def __getattribute__(self, __name: str) -> Any:
        try:
            return super().__getattribute__(__name)
        except AttributeError as e:
            if not all(getattr(_o, __name, None) for _o in self._objs):
                raise(e)
            return self.__passthrough__(__name)

    def append(self, obj: T) -> None:
        self._objs.append(obj)

    def append_all(self, obj_list: Iterable[T]) -> None:
        for o in obj_list:
            self._objs.append(o)
