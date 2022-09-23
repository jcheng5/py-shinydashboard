from enum import Enum
from typing import List, Optional

import htmltools as ht
from htmltools import tags

from ._utils import insert_dividers


class MenuType(Enum):
    Messages = 1
    Notifications = 2
    # Tasks = 3


def menu_dropdown(
    type: MenuType,
    *args: ht.TagChild,
    badge_status: Optional[str] = "primary",
    icon: Optional[ht.TagChild] = None,
    header: Optional[ht.TagChild] = None,
) -> ht.TagChild:
    if icon is not None:
        pass
    elif type == MenuType.Notifications:
        icon = tags.i({"class": "far fa-bell"})
    elif type == MenuType.Messages:
        icon = tags.i({"class": "far fa-comments"})
    # elif type == MenuType.Tasks:
    #     icon = tags.i({"class": "far fa-list-check"})

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
            tags.span(
                {"class": f"navbar-badge badge bg-{badge_status}"},
                str(len(args)),
            ),
        ),
        tags.div(
            {"class": "dropdown-menu dropdown-menu-lg dropdown-menu-end"}, children
        ),
    )

    return menu


def item_message(
    sender: ht.TagChild,
    message: ht.TagChild,
    *,
    icon: Optional[ht.TagChild] = None,
    time: Optional[ht.TagChild] = None,
    href: Optional[str] = None,
):
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
    icon: Optional[ht.TagChild] = tags.i(
        {"class": "fas fa-exclamation-circle fa-fw me-2"},
    ),
    time: Optional[ht.TagChild] = None,
    href: Optional[str] = None,
):
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
