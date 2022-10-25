import functools
from inspect import iscoroutinefunction
from typing import Awaitable, Callable, Optional, Union

import htmltools as ht
from faicons import icon_svg
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
    """A value box, for displaying key metrics in the :func:`body` of a dashboard.

    Intended to be used within a :func:`row`.

    Parameters
    ----------
    value
        The value to display in the box. Usually a number or short text.
    subtitle
        Subtitle text, usually describing the value.
    icon
        An icon to display prominently, likely from :func:`icon_svg`.
    color
        A `Bootstrap color <https://getbootstrap.com/docs/5.2/customize/color/>`_, e.g.
        ``"light"`` (the default), ``"dark"``, ``"success"``, etc.
    width
        How wide the card should be, in `Bootstrap grid
        <https://getbootstrap.com/docs/5.2/layout/grid/>`_ columns; must be an integer
        between 1 and 12, inclusive. If ``None``, then the card's width will be
        automatically determined based on the amount of space available.
    href, optional
        If not ``None``, treats the entire value box as a clickable link to the
        specified URL.
    footer
        Optional content to insert into a band at the bottom of the box.
    gradient
        Whether to apply a subtle gradient effect to the background color.
    class_
        A string specifying additional CSS class(es) to apply to the value box element.
        Multiple classes should be space-separated.

    Returns
    -------
        A :class:`Tag` object, suitable for inclusion in a :func:`row`.
    """
    subtitle = wrap_with_tag(subtitle, tags.p)

    if icon is not None:
        icon = tags.div(
            {"class": "icon"},
            tags.div(
                {"class": "icon-inner"},
                icon,
            ),
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
        icon,
        tags.div(
            {"class": "inner"},
            tags.h3(
                value,
            ),
            subtitle,
        ),
        tags.div(class_="clearfix") if icon is not None else None,
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
    value: ht.TagChild,
    *,
    subtitle: Optional[ht.TagChild] = None,
    icon: ht.TagChild = icon_svg("thumbs-up"),
    color: str = "secondary",
    width: Optional[int] = None,
    href: Optional[str] = None,
    fill: bool = False,
    gradient: bool = False,
    class_: Optional[str] = None,
) -> ht.Tag:
    """An info box, for displaying secondary metrics in the :func:`body` of a dashboard.

    Intended to be used within a :func:`row`.

    Compared to :func:`value_box`, :func:`info_box` is smaller, and less colorful
    (unless ``fill=True``). It also has a title that appears above the value plus a
    subtitle that appears below the value, while :func:`value_box` only has a subtitle
    that appears below the value.

    Parameters
    ----------
    title
        Title text, usually describing the value. Appears above the value.
    value
        The value to display in the box. Usually a number or short text.
    subtitle
        Explanatory text that appears below the value.
    icon
        An icon to display prominently, likely from :func:`icon_svg`. The default is a
        thumbs-up icon.
    color
        A `Bootstrap color <https://getbootstrap.com/docs/5.2/customize/color/>`_, e.g.
        ``"light"`` (the default), ``"dark"``, ``"success"``, etc.
    width, optional
        How wide the card should be, in `Bootstrap grid
        <https://getbootstrap.com/docs/5.2/layout/grid/>`_ columns; must be an integer
        between 1 and 12, inclusive. If ``None``, then the card's width will be
        automatically determined based on the amount of space available.
    href, optional
        If not ``None``, treats the entire value box as a clickable link to the
        specified URL.
    fill, optional
        If ``True``, the specified color fills the entire info box; if ``False`` (the
        default), the color is only applied in a box surrounding the icon.
    gradient, optional
        Whether to apply a subtle gradient effect to the background color.
    class_, optional
        A string specifying additional CSS class(es) to apply to the value box element.
        Multiple classes should be space-separated.

    Returns
    -------
        A :class:`Tag` object, suitable for inclusion in a :func:`row`.
    """
    subtitle = wrap_with_tag(subtitle, tags.div)

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
