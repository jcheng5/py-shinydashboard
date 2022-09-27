from inspect import iscoroutinefunction
from typing import Awaitable, Callable, Optional, Union
import functools
import htmltools as ht
from htmltools import tags
from shiny import render, ui

from ._utils import bg_classes, col_classes, join, wrap_with_col, wrap_with_tag


def value_box(
    value: ht.TagChild,
    subtitle: Optional[ht.TagChild] = None,
    *,
    icon: Optional[ht.TagChild] = None,
    color: str = "light",
    width: Optional[int] = None,
    href: Optional[str] = None,
    footer: Optional[ht.TagChild] = None,
    gradient: bool = False,
    class_: Optional[str] = None,
) -> ht.Tag:
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


def output_value_box(id: str, width: Optional[int] = None) -> ht.Tag:
    return ui.output_ui(
        id,
        container=ht.div,
        class_="value-box-output " + col_classes(width),
    )


def render_value_box(
    fn: Callable[[], Union[Optional[ht.Tag], Awaitable[Optional[ht.Tag]]]]
):
    return render_children(fn)


def info_box(
    title: ht.TagChild,
    value: Optional[ht.TagChild] = None,
    *,
    subtitle: Optional[ht.TagChild] = None,
    icon: ht.TagChild = tags.i(class_="fas fa-thumbs-up"),
    color: str = "secondary",
    width: Optional[int] = None,
    href: Optional[str] = None,
    fill: bool = False,
    gradient: bool = False,
    class_: Optional[str] = None,
) -> ht.Tag:
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


def output_info_box(id: str, width: Optional[int] = None) -> ht.Tag:
    return ui.output_ui(
        id,
        container=ht.div,
        class_="info-box-output " + col_classes(width),
    )


def render_info_box(
    fn: Callable[[], Union[Optional[ht.Tag], Awaitable[Optional[ht.Tag]]]]
):
    return render_children(fn)


def render_children(
    fn: Callable[[], Union[Optional[ht.Tag], Awaitable[Optional[ht.Tag]]]]
):
    if iscoroutinefunction(fn) or (
        hasattr(fn, "__call__") and iscoroutinefunction(getattr(fn, "__call__"))
    ):

        @functools.wraps(fn)
        async def fn_async() -> Optional[ht.TagChildArg]:
            res: Optional[ht.Tag] = await fn()  # type: ignore
            if res is None:
                return res
            else:
                return res.children

        return render.ui(fn_async)
    else:

        @functools.wraps(fn)
        def fn_sync() -> Optional[ht.TagList]:
            res: Optional[ht.Tag] = fn()  # type: ignore
            if res is None:
                return res
            else:
                return res.children

        return render.ui(fn_sync)
