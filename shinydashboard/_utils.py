from __future__ import annotations

from typing import Callable, List, Optional, TypeVar, Union

import htmltools as ht
from htmltools import tags

T = TypeVar("T")


def wrap_with_col(width: Optional[int], x: ht.TagChild) -> ht.Tag:
    return tags.div(x, class_=col_classes(width))


def col_classes(width: Optional[int]) -> str:
    if width is not None:
        return f"col col-sm-{width}"
    else:
        return "col"


# May be ht.TagChild or Optional[ht.TagChild]
TagInput = TypeVar("TagInput", bound=Optional[ht.TagChild])


def wrap_with_tag(
    x: TagInput, tag_func: Callable[[TagInput], ht.TagChild]
) -> Union[TagInput, ht.TagChild]:
    """If 'x' is a simple string, wrap it in the given tag"""
    # TODO: if raw HTML, just return
    if isinstance(x, str) and not isinstance(x, ht.HTML):
        return tag_func(x)
    else:
        return x


def bg_classes(color: str, gradient: bool = False) -> str:
    # TODO: Validate color
    return f"bg-{color}{' bg-gradient' if gradient else ''}"


def join(*args: Optional[str]) -> str:
    return " ".join([x for x in args if x])


def insert_dividers(lst: List[T], divider: T) -> List[T]:
    res: List[T] = []
    for el in lst:
        if len(res) > 0:
            res.append(divider)
        res.append(el)
    return res
