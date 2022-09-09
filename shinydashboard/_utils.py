from typing import Callable, Optional, TypeVar, Union

import htmltools as ht
from htmltools import tags


def wrap_with_col(width: Union[int, bool, None], x: ht.TagChild) -> ht.TagChild:
    if width:
        if width is True:
            return tags.div(x, class_="col")
        else:
            return tags.div(x, class_=f"col col-sm-{width}")
    else:
        return x


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
