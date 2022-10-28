from collections.abc import MutableMapping
from typing import Iterator, Optional, Tuple, TypeVar, cast

from shiny import reactive

Key = TypeVar("Key")
Value = TypeVar("Value")


class ReactiveValues(MutableMapping[Key, Value]):
    def __init__(self):
        self._items: dict[Key, reactive.Value[Value]] = dict()
        self._has_item: dict[Key, reactive.Value[bool]] = dict()
        self._keys: reactive.Value[Tuple[Key, ...]] = reactive.Value(())

    def _update_keys(self):
        self._keys.set(tuple(self._items.keys()))

    def _contains_key(self, key: Key, value: Optional[bool] = None) -> bool:
        if key not in self._has_item:
            self._has_item[key] = reactive.Value(key in self._items)

        if value is not None:
            self._has_item[key].set(value)
            return value
        else:
            return self._has_item[key].get()

    def __setitem__(self, key: Key, value: Value):
        if key not in self._items:
            self._contains_key(key, True)
            self._items[key] = reactive.Value(value)
            self._update_keys()
        else:
            self._items[key].set(value)

    def __getitem__(self, key: Key) -> Value:
        if key not in self._items:
            # Attempting to read an item that isn't present. This will fail, but we
            # also want to take a reactive dependency so that if the desired item is
            # added later, that will trigger reactivity in the reader.
            self._contains_key(key)

        # Attempt to read, even if the key wasn't present; we want the same error as the
        # underlying dict would throw, so, just let it throw
        return self._items[key].get()

    def __contains__(self, key: object) -> bool:
        # Same as `key in self._items`, except this way it's also reactive
        return self._contains_key(cast(Key, key))

    def __delitem__(self, key: Key) -> None:
        if key in self._items:
            self._contains_key(key, False)
            self._items[key].unset()
            self._update_keys()

        # Attempt to del, even if the key wasn't present; we want the same error as the
        # underlying dict would throw, so, just let it throw
        del self._items[key]

    def __iter__(self) -> Iterator[Key]:
        # Take a reactive dependency on the current set of keys
        self._keys.get()
        return self._items.__iter__()

    def __len__(self) -> int:
        # Take a reactive dependency on the current set of keys
        self._keys.get()
        return self._items.__len__()


T = TypeVar("T")


def _maybe_set(rv: reactive.Value[T], value: T):
    with reactive.isolate():
        if rv.get() != value:
            rv.set(value)
            return True
        else:
            return False
