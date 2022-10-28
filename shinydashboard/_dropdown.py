from __future__ import annotations

from typing import List, Literal, Optional, Union

import htmltools as ht
from faicons import icon_svg
from htmltools import tags
from shiny import render

from ._utils import insert_dividers


def menu_dropdown(
    icon: ht.TagChild,
    *args: ht.TagChild,
    badge_value: Optional[Union[int, Literal["auto"]]] = "auto",
    badge_status: Optional[str] = "primary",
    header: Optional[ht.TagChild] = None,
) -> ht.TagChild:
    """A drop-down menu, designed to be used as part of a :func:`header`'s
    ``children_right`` argument, and intended to be filled with :func:`item_message` and
    :func:`item_notification` objects.

    Parameters
    ----------
    icon
        An icon to display, that can be clicked to reveal the menu items.
    args
        One or more items to display in the dropdown menu; see :func:`item_message` and
        :func:`item_notification`.
    badge_value
        An optional number to display on a badge that overlays the icon. By default, the
        value will be calculated based on `len(args)`. Pass ``None`` to omit the badge.
    badge_status
        The color to use for the badge background. Must be a `Bootstrap color
        <https://getbootstrap.com/docs/5.2/customize/color/>`_, e.g. ``"light"`` (the
        default), ``"dark"``, ``"success"``, etc.
    header
        Content to display when the menu is dropped down, in a region above the menu
        items.

    Returns
    -------
        A :class:`Tag` object, suitable for inclusion in :func:`header`'s ``children_right`` argument.
    """

    if badge_value == "auto":
        badge_value = len(args)

    children: List[ht.TagChild] = []
    if header is not None:
        children.append(
            tags.span(
                {"class": "dropdown-item dropdown-header"},
                header,
            )
        )
    children += args
    children = insert_dividers(
        children,
        tags.div(
            {"class": "dropdown-divider"},
        ),
    )

    menu = tags.li(
        {"class": "nav-item dropdown"},
        tags.a(
            {"class": "nav-link", "data-bs-toggle": "dropdown", "href": "#"},
            icon,
            (
                tags.span(
                    {"class": f"navbar-badge badge bg-{badge_status}"},
                    str(badge_value),
                )
                if badge_value is not None and badge_status is not None
                else None
            ),
        ),
        tags.div(
            {"class": "dropdown-menu dropdown-menu-lg dropdown-menu-end"}, children
        ),
    )

    return menu


def output_menu_dropdown(id: str) -> ht.Tag:
    return tags.li(id=id, class_="shinydashboard-menu-output")


render_menu_dropdown = render.ui


def item_message(
    sender: ht.TagChild,
    message: ht.TagChild,
    *,
    icon: Optional[ht.TagChild] = None,
    time: Optional[ht.TagChild] = None,
    href: Optional[str] = None,
):
    """A menu item for :func:`menu_dropdown`, representing a message.

    Parameters
    ----------
    sender
        A string or :class:`Tag` to be displayed as the sender.
    message
        A string or :class:`Tag` for the message.
    icon
        An icon to display to the left of the message.
    time
        A string or :class:`Tag` indicating the time of the message.
    href, optional
        If provided, turns the entire menu item into a link to this URL.

    Returns
    -------
        A :class:`Tag` object, suitable for inclusion in :func:`menu_dropdown`.
    """

    child = tags.div(
        {"class": "d-flex"},
        (
            tags.div(
                {"class": "flex-shrink-0 me-3"},
                icon,
            )
            if icon
            else None
        ),
        tags.div(
            {"class": "flex-grow-1"},
            tags.h3(
                {"class": "dropdown-item-title"},
                sender,
            ),
            tags.p(
                {"class": "fs-7"},
                message,
            ),
            tags.p(
                {"class": "fs-7 text-muted"},
                tags.i(
                    {"class": "far fa-clock me-1"},
                ),
                time,
            )
            if time
            else None,
        ),
    )

    if href is not None:
        container = tags.a(child, href=href, class_="dropdown-item")
    else:
        container = tags.div(child, class_="dropdown-item")

    return container


def item_notification(
    message: ht.TagChild,
    *,
    icon: Optional[ht.TagChild] = icon_svg(
        "circle-exclamation", fill="var(--bs-secondary)"
    ),
    time: Optional[ht.TagChild] = None,
    href: Optional[str] = None,
):
    """A menu item for :func:`menu_dropdown`, representing a generic notification.

    Parameters
    ----------
    message
        A string or :class:`Tag` for the message.
    icon, optional
        An icon to display to the left of the message; by default, an exclamation point
        icon will be displayed.
    time, optional
        A string or :class:`Tag` indicating the time of the notification.
    href, optional
        If provided, turns the entire menu item into a link to this URL.

    Returns
    -------
        A :class:`Tag` object, suitable for inclusion in :func:`menu_dropdown`.
    """
    child = tags.div(
        {"class": "d-flex"},
        (
            tags.div(
                {"class": "flex-grow-0 flex-shrink-0 me-1"},
                icon,
            )
            if icon
            else None
        ),
        tags.div(
            {"class": "flex-grow-1 text-wrap"},
            (
                tags.span(
                    {"class": "text-muted text-nowrap fs-8 ms-1 float-end"},
                    time,
                )
                if time
                else None
            ),
            message,
        ),
    )

    if href is not None:
        container = tags.a(child, href=href, class_="dropdown-item")
    else:
        container = tags.div(child, class_="dropdown-item")

    return container
