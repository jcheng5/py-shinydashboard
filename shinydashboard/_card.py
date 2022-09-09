from typing import List, Optional, Union
import htmltools as ht
from htmltools import tags

from ._utils import join, wrap_with_col


def card(
    title: Optional[ht.TagChild] = None,
    *args: ht.TagChild,
    color: str = "light",
    width: Optional[Union[int, bool]] = None,
    collapsed: Optional[bool] = None,
    closeable: bool = False,
    maximizable: bool = False,
    children: List[ht.TagChild] = [],
) -> ht.TagChild:

    tools: List[ht.TagChild] = []
    if collapsed is not None:
        tools.append(
            tags.button(
                {
                    "type": "button",
                    "class": "btn btn-tool",
                    "data-lte-toggle": "card-collapse",
                },
                tags.i(
                    {"class": f"fas fa-{'plus' if collapsed else 'minus'}"},
                ),
            )
        )

    if maximizable:
        tools.append(
            tags.button(
                {
                    "type": "button",
                    "class": "btn btn-tool",
                    "data-lte-toggle": "card-maximize",
                },
                tags.i(
                    {"class": "fas fa-expand"},
                ),
            )
        )
    if closeable:
        tools.append(
            tags.button(
                {
                    "type": "button",
                    "class": "btn btn-tool",
                    "data-lte-dismiss": "card-remove",
                },
                tags.i(
                    {"class": "fas fa-times"},
                ),
            )
        )

    title_tag: Optional[ht.Tag] = None
    if title is not None or len(tools) > 0:
        title_tag = tags.div(
            {"class": "card-header"},
            tags.h3(
                {"class": "card-title"},
                title,
            ),
            tags.div(
                {"class": "card-tools"},
                tools,
            ),
        )

    card_tag = tags.div(
        {"class": join(f"card card-{color}", "collapsed-card" if collapsed else None)},
        title_tag,
        tags.div(
            {"class": "card-body"},
            *args,
            children,
        ),
    )

    return wrap_with_col(width, card_tag)
