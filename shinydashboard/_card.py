from typing import List, Optional

import htmltools as ht
from faicons import icon_svg
from htmltools import tags

from ._utils import join, wrap_with_col


def card(
    title: Optional[ht.TagChild] = None,
    *args: ht.TagChild,
    color: str = "light",
    width: Optional[int] = None,
    # Having issues with `collapsed` right now; the plus/minus sign management is done
    # via CSS, which doesn't work well with SVG
    # collapsed: Optional[bool] = None,
    closeable: bool = False,
    maximizable: bool = False,
) -> ht.TagChild:
    """A bordered card container, for visually grouping related UI elements in the
    :func:`body` of a dashboard.

    Intended to be used within a :func:`row`.

    Parameters
    ----------
    title
        A title to show at the top of the card.
    color
        A `Bootstrap color <https://getbootstrap.com/docs/5.2/customize/color/>`_, e.g.
        ``"light"`` (the default), ``"dark"``, ``"success"``, etc.
    width
        How wide the card should be, in `Bootstrap grid
        <https://getbootstrap.com/docs/5.2/layout/grid/>`_ columns; must be an integer
        between 1 and 12, inclusive. If ``None``, then the card's width will be
        automatically determined based on the amount of space available.
    closeable
        Whether to include an "X" button in the header that removes the card.
    maximizable
        Whether to include a button in the header that temporarily resizes the card to
        fill the browser window.

    Returns
    -------
        A :class:`Tag` object.
    """

    tools: List[ht.TagChild] = []
    # if collapsed is not None:
    #     tools.append(
    #         tags.button(
    #             {
    #                 "type": "button",
    #                 "class": "btn btn-tool",
    #                 "data-lte-toggle": "card-collapse",
    #             },
    #             # icon_svg("plus" if collapsed else "minus"),
    #             tags.i(
    #                 {"class": f"fas fa-{'plus' if collapsed else 'minus'}"},
    #             ),
    #         )
    #     )

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
        {"class": f"card card-{color}"},
        # {"class": "collapsed-card" if collapsed else None},
        title_tag,
        tags.div(
            {"class": "card-body"},
            *args,
        ),
    )

    return wrap_with_col(width, card_tag)
