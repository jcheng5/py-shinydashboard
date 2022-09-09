from typing import Optional, Union

import htmltools as ht
from htmltools import tags

from ._utils import bg_classes, join, wrap_with_col, wrap_with_tag


def value_box(
    value: ht.TagChild,
    subtitle: Optional[ht.TagChild] = None,
    *,
    icon: Optional[ht.TagChild] = None,
    color: str = "light",
    width: Optional[Union[int, bool]] = None,
    href: Optional[str] = None,
    footer: Optional[ht.TagChild] = None,
    gradient: bool = False,
    class_: Optional[str] = None,
) -> ht.TagChild:
    subtitle = wrap_with_tag(subtitle, tags.p)

    if icon is not None:
        icon = tags.div(
            {"class": "icon"},
            icon,
        )

    footer_tag: Optional[ht.Tag]
    if footer is not None:
        footer_tag = tags.div({"class": "small-box-footer"}, footer)
    else:
        footer_tag = None

    if href is None:
        container = tags.div
    else:
        container = tags.a

    box = container(
        {
            "class": join("small-box", bg_classes(color, gradient), class_),
            "href": href,
        },
        tags.div(
            {"class": "inner"},
            tags.h3(
                value,
            ),
            subtitle,
        ),
        icon,
        footer_tag,
    )

    return wrap_with_col(width, box)


def info_box(
    title: ht.TagChild,
    value: Optional[ht.TagChild] = None,
    *,
    subtitle: Optional[ht.TagChild] = None,
    icon: ht.TagChild = tags.i(class_="fas fa-thumbs-up"),
    color: str = "secondary",
    width: Optional[Union[int, bool]] = None,
    href: Optional[str] = None,
    fill: bool = False,
    gradient: bool = False,
    class_: Optional[str] = None,
) -> ht.TagChild:
    subtitle = wrap_with_tag(subtitle, tags.p)

    if href is None:
        container = tags.div
    else:
        container = tags.a

    box = container(
        {
            "class": join(
                "info-box",
                bg_classes(color, gradient) if fill else None,
                class_,
            ),
            "href": href,
        },
        tags.span(
            {
                "class": join(
                    "info-box-icon",
                    join("shadow-sm", bg_classes(color, gradient))
                    if not fill
                    else None,
                )
            },
            icon,
        ),
        tags.div(
            {"class": "info-box-content"},
            tags.span(
                {"class": "info-box-text"},
                title,
            ),
            tags.span(
                {"class": "info-box-number"},
                value,
            ),
            subtitle,
        ),
    )

    return wrap_with_col(width, box)
