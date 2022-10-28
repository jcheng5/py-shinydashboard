from __future__ import annotations

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

    Use ``value_box`` directly within your Shiny UI definition if the contents and
    appearance of the value box are intended to be static (i.e. they do not change
    during the execution of the app). If the contents need to be reactive, use
    :func:`output_value_box`/:func:`render_value_box` instead.

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
    """The UI side of a dynamically rendered :func:`value_box`.

    Put an ``output_value_box`` in your Shiny UI definition, instead of an ordinary
    :func:`value_box`, if you want the value box to be dynamic (that is, to re-render in
    reponse to changing inputs and other sources of reactivity).

    See also :func:`render_value_box` for info about providing the server logic for a
    dynamic value box.

    Parameters
    ----------
    id
        The identifier for the output; must match the name of your corresponding
        server-side rendering function (see :func:`render_value_box`).
    width
        How wide the card should be, in `Bootstrap grid
        <https://getbootstrap.com/docs/5.2/layout/grid/>`_ columns; must be an integer
        between 1 and 12, inclusive. If ``None``, then the card's width will be
        automatically determined based on the amount of space available.

    Returns
    -------
        A :class:`Tag` object, to be included somewhere in the :func:`body`.
    """
    return ui.output_ui(
        id,
        container=ht.div,
        class_="value-box-output " + col_classes(width),
    )


def render_value_box(
    fn: Callable[[], Union[Optional[ht.Tag], Awaitable[Optional[ht.Tag]]]]
):
    """A Shiny render decorator for dynamic :func:`value_box` outputs.

    Here's an example of an value box renderer that would go into the Shiny server
    function::

        @output
        @sdb.render_value_box
        def valueBox1():
            current_time = datetime.datetime.now().astimezone()

            # datetime.now() isn't inherently reactive, so explicitly
            # tell Shiny to consider this output dirty 1 second from now
            reactive.invalidate_later(1)

            return sdb.value_box(
                current_time.strftime("%I:%M:%S %p"),
                "Current time",
                icon=faicons.icon_svg("clock"),
                color="success",
            )

    Note that like all Shiny render decorators, ``@render_value_box`` must be *below*
    (or maybe you think of it as *inside*) the ``@output`` decorator.

    This example would require a matching ``output_value_box("valueBox1")`` to appear in
    the Shiny UI definition. See :func:`output_value_box` for more information.

    Parameters
    ----------
    fn
        A user-defined function to decorate; its name should match with the
        corresponding :func:`output_value_box` in the UI. The function should return
        either a :func:`value_box` object, or ``None``.

    Returns
    -------
        A decorated function that must be further decorated with ``@output``.
    """
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

    Use ``info_box`` directly within your Shiny UI definition if the contents and
    appearance of the info box are intended to be static (i.e. they do not change during
    the execution of the app). If the contents need to be reactive, use
    :func:`output_info_box`/:func:`render_info_box` instead.

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
    width
        How wide the card should be, in `Bootstrap grid
        <https://getbootstrap.com/docs/5.2/layout/grid/>`_ columns; must be an integer
        between 1 and 12, inclusive. If ``None``, then the card's width will be
        automatically determined based on the amount of space available.
    href
        If not ``None``, treats the entire value box as a clickable link to the
        specified URL.
    fill
        If ``True``, the specified color fills the entire info box; if ``False`` (the
        default), the color is only applied in a box surrounding the icon.
    gradient
        Whether to apply a subtle gradient effect to the background color.
    class_
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
    """Create an output container for a dynamically rendered :func:`info_box`.

    Put an ``output_info_box`` in your Shiny UI definition, instead of an ordinary
    :func:`info_box`, if you want the info box to be dynamic (that is, to re-render in
    reponse to changing inputs and other sources of reactivity).

    See also :func:`render_info_box` for info about providing the server logic for a
    dynamic info box.

    Parameters
    ----------
    id
        The identifier for the output; must match the name of your corresponding
        server-side rendering function (see :func:`render_info_box`).
    width
        How wide the card should be, in `Bootstrap grid
        <https://getbootstrap.com/docs/5.2/layout/grid/>`_ columns; must be an integer
        between 1 and 12, inclusive. If ``None``, then the card's width will be
        automatically determined based on the amount of space available.

    Returns
    -------
        A :class:`Tag` object, to be included somewhere in the :func:`body`.
    """
    return ui.output_ui(
        id,
        container=ht.div,
        class_="info-box-output " + col_classes(width),
    )


def render_info_box(
    fn: Callable[[], Union[Optional[ht.Tag], Awaitable[Optional[ht.Tag]]]]
):
    """A Shiny render decorator for dynamic :func:`info_box` outputs.

    Here's an example of an info box renderer that would go into the Shiny server
    function::

        @output
        @sdb.render_info_box
        def infoBox1():
            current_time = datetime.datetime.now().astimezone()

            # datetime.now() isn't inherently reactive, so explicitly
            # tell Shiny to consider this output dirty 1 second from now
            reactive.invalidate_later(1)

            return sdb.info_box(
                "Current time",
                current_time.strftime("%I:%M:%S %p"),
                subtitle=str(current_time.tzinfo),
                icon=faicons.icon_svg("clock"),
                color="warning",
            )

    Note that like all Shiny render decorators, ``@render_info_box`` must be *below* (or
    maybe you think of it as *inside*) the ``@output`` decorator.

    This example would require a matching ``output_info_box("infoBox1")`` to appear in
    the Shiny UI definition. See :func:`output_info_box` for more information.

    Parameters
    ----------
    fn
        A user-defined function to decorate; its name should match with the
        corresponding :func:`output_info_box` in the UI. The function should return
        either an :func:`info_box` object, or ``None``.

    Returns
    -------
        A decorated function that must be further decorated with ``@output``.
    """
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
