from typing import Optional, Union
import htmltools as ht
from htmltools import tags

from ._utils import wrap_with_tag


def brand(
    title: ht.TagChild,
    *,
    href: Optional[str] = None,
    img_src: Optional[str] = None,
    img_alt: Optional[str] = None,
    img_class: str = "brand-image opacity-80 shadow",
) -> ht.TagChild:
    if href is None:
        href = "javascript:;"

    img = None
    if img_src:
        img = tags.img(
            {
                "src": img_src,
                "alt": img_alt,
                "class": img_class,
            },
        )

    return tags.a(
        {"href": href, "class": "brand-link"},
        img,
        tags.span(
            {"class": "brand-text fw-light"},
            title,
        ),
    )


def sidebar_menu_link(
    title: ht.TagChild,
    href: str,
    *,
    icon: ht.TagChild = tags.i(
        {"class": "nav-icon far fa-circle"},
    ),
) -> ht.Tag:
    return tags.li(
        {"class": "nav-item"},
        tags.a(
            {
                "href": href,
                "class": "nav-link",
            },
            icon,
            tags.p(
                title,
            ),
        ),
    )


def sidebar_submenu(
    title: ht.TagChild,
    *args: ht.TagChild,
    icon: ht.TagChild = tags.i({"class": "nav-icon fas fa-circle"}),
    expanded: bool = False,
) -> ht.Tag:
    return tags.li(
        {"class": "nav-item" + (" menu-open" if expanded else "")},
        tags.a(
            {"href": "javascript:;", "class": "nav-link"},
            icon,
            tags.p(
                title,
                tags.i(
                    {"class": "end fas fa-angle-right"},
                ),
            ),
        ),
        tags.ul(
            {"class": "nav nav-treeview"},
            *args,
        ),
    )


def sidebar(title: Union[str, ht.TagChild], *args: ht.TagChild) -> ht.Tag:
    title = wrap_with_tag(title, brand)

    # Main Sidebar Container
    return tags.aside(
        {"class": "main-sidebar sidebar-bg-dark sidebar-color-primary shadow"},
        tags.div(
            {"class": "brand-container"},
            title,
            tags.a(
                {
                    "class": "pushmenu mx-1",
                    "data-lte-toggle": "sidebar-mini",
                    "href": "javascript:;",
                    "role": "button",
                },
                tags.i(
                    {"class": "fas fa-angle-double-left"},
                ),
            ),
        ),
        # Sidebar
        tags.div(
            {"class": "sidebar"},
            tags.nav(
                {"class": "mt-2"},
                # Sidebar Menu
                tags.ul(
                    {
                        "class": "nav nav-pills nav-sidebar flex-column",
                        "data-lte-toggle": "treeview",
                        "role": "menu",
                        "data-accordion": "false",
                    },
                    *args,
                ),
            ),
        ),
        # /.sidebar
    )


def rubbish():
    return [
        tags.li(
            {"class": "nav-item menu-open"},
            tags.a(
                {
                    "href": "javascript:;",
                    "class": "nav-link active",
                },
                tags.i(
                    {"class": "nav-icon fas fa-circle"},
                ),
                tags.p(
                    "Dashboard",
                    tags.i(
                        {"class": "end fas fa-angle-right"},
                    ),
                ),
            ),
            tags.ul(
                {"class": "nav nav-treeview"},
                tags.li(
                    {"class": "nav-item"},
                    tags.a(
                        {
                            "href": "./index.html",
                            "class": "nav-link active",
                        },
                        tags.i(
                            {"class": "nav-icon far fa-circle"},
                        ),
                        tags.p(
                            "Dashboard v1",
                        ),
                    ),
                ),
                tags.li(
                    {"class": "nav-item"},
                    tags.a(
                        {
                            "href": "./index2.html",
                            "class": "nav-link ",
                        },
                        tags.i(
                            {"class": "nav-icon far fa-circle"},
                        ),
                        tags.p(
                            "Dashboard v2",
                        ),
                    ),
                ),
                tags.li(
                    {"class": "nav-item"},
                    tags.a(
                        {
                            "href": "./index3.html",
                            "class": "nav-link ",
                        },
                        tags.i(
                            {"class": "nav-icon far fa-circle"},
                        ),
                        tags.p(
                            "Dashboard v3",
                        ),
                    ),
                ),
            ),
        ),
        tags.li(
            {"class": "nav-item "},
            tags.a(
                {"href": "javascript:;", "class": "nav-link "},
                tags.i(
                    {"class": "nav-icon fas fa-circle"},
                ),
                tags.p(
                    "Widgets",
                    tags.i(
                        {"class": "end fas fa-angle-right"},
                    ),
                ),
            ),
            tags.ul(
                {"class": "nav nav-treeview"},
                tags.li(
                    {"class": "nav-item"},
                    tags.a(
                        {
                            "href": "./pages/widgets/small-box.html",
                            "class": "nav-link ",
                        },
                        tags.i(
                            {"class": "nav-icon far fa-circle"},
                        ),
                        tags.p(
                            "Small Box",
                        ),
                    ),
                ),
                tags.li(
                    {"class": "nav-item"},
                    tags.a(
                        {
                            "href": "./pages/widgets/info-box.html",
                            "class": "nav-link ",
                        },
                        tags.i(
                            {"class": "nav-icon far fa-circle"},
                        ),
                        tags.p(
                            "info Box",
                        ),
                    ),
                ),
                tags.li(
                    {"class": "nav-item"},
                    tags.a(
                        {
                            "href": "./pages/widgets/cards.html",
                            "class": "nav-link ",
                        },
                        tags.i(
                            {"class": "nav-icon far fa-circle"},
                        ),
                        tags.p(
                            "Cards",
                        ),
                    ),
                ),
            ),
        ),
        tags.li(
            {"class": "nav-item "},
            tags.a(
                {"href": "javascript:;", "class": "nav-link "},
                tags.i(
                    {"class": "nav-icon fas fa-circle"},
                ),
                tags.p(
                    "Layout Options",
                    tags.span(
                        {"class": "badge bg-info float-end me-3"},
                        "6",
                    ),
                    tags.i(
                        {"class": "end fas fa-angle-right"},
                    ),
                ),
            ),
            tags.ul(
                {"class": "nav nav-treeview"},
                tags.li(
                    {"class": "nav-item"},
                    tags.a(
                        {
                            "href": "./pages/layout/fixed-sidebar.html",
                            "class": "nav-link ",
                        },
                        tags.i(
                            {"class": "nav-icon far fa-circle"},
                        ),
                        tags.p(
                            "Fixed Sidebar",
                        ),
                    ),
                ),
            ),
        ),
        tags.li(
            {"class": "nav-item "},
            tags.a(
                {"href": "javascript:;", "class": "nav-link "},
                tags.i(
                    {"class": "nav-icon fas fa-circle"},
                ),
                tags.p(
                    "Forms",
                    tags.i(
                        {"class": "end fas fa-angle-right"},
                    ),
                ),
            ),
            tags.ul(
                {"class": "nav nav-treeview"},
                tags.li(
                    {"class": "nav-item"},
                    tags.a(
                        {
                            "href": "./pages/forms/general.html",
                            "class": "nav-link ",
                        },
                        tags.i(
                            {"class": "nav-icon far fa-circle"},
                        ),
                        tags.p(
                            "General Elements",
                        ),
                    ),
                ),
            ),
        ),
        tags.li(
            {"class": "nav-item "},
            tags.a(
                {"href": "javascript:;", "class": "nav-link "},
                tags.i(
                    {"class": "nav-icon fas fa-circle"},
                ),
                tags.p(
                    "Tables",
                    tags.i(
                        {"class": "end fas fa-angle-right"},
                    ),
                ),
            ),
            tags.ul(
                {"class": "nav nav-treeview"},
                tags.li(
                    {"class": "nav-item"},
                    tags.a(
                        {
                            "href": "./pages/tables/simple.html",
                            "class": "nav-link ",
                        },
                        tags.i(
                            {"class": "nav-icon far fa-circle"},
                        ),
                        tags.p(
                            "Simple Tables",
                        ),
                    ),
                ),
            ),
        ),
        tags.li(
            {"class": "nav-header"},
            "MULTI LEVEL EXAMPLE",
        ),
        tags.li(
            {"class": "nav-item"},
            tags.a(
                {"href": "javascript:;", "class": "nav-link"},
                tags.i(
                    {"class": "nav-icon fas fa-circle"},
                ),
                tags.p(
                    "Level 1",
                ),
            ),
        ),
        tags.li(
            {"class": "nav-item"},
            tags.a(
                {"href": "javascript:;", "class": "nav-link"},
                tags.i(
                    {"class": "nav-icon fas fa-circle"},
                ),
                tags.p(
                    "Level 1",
                    tags.i(
                        {"class": "end fas fa-angle-right"},
                    ),
                ),
            ),
            tags.ul(
                {"class": "nav nav-treeview"},
                tags.li(
                    {"class": "nav-item"},
                    tags.a(
                        {
                            "href": "javascript:;",
                            "class": "nav-link",
                        },
                        tags.i(
                            {"class": "nav-icon far fa-circle"},
                        ),
                        tags.p(
                            "Level 2",
                        ),
                    ),
                ),
                tags.li(
                    {"class": "nav-item"},
                    tags.a(
                        {
                            "href": "javascript:;",
                            "class": "nav-link",
                        },
                        tags.i(
                            {"class": "nav-icon far fa-circle"},
                        ),
                        tags.p(
                            "Level 2",
                            tags.i(
                                {"class": "end fas fa-angle-right"},
                            ),
                        ),
                    ),
                    tags.ul(
                        {"class": "nav nav-treeview"},
                        tags.li(
                            {"class": "nav-item"},
                            tags.a(
                                {
                                    "href": "javascript:;",
                                    "class": "nav-link",
                                },
                                tags.i(
                                    {"class": "nav-icon far fa-dot-circle"},
                                ),
                                tags.p(
                                    "Level 3",
                                ),
                            ),
                        ),
                        tags.li(
                            {"class": "nav-item"},
                            tags.a(
                                {
                                    "href": "javascript:;",
                                    "class": "nav-link",
                                },
                                tags.i(
                                    {"class": "nav-icon far fa-dot-circle"},
                                ),
                                tags.p(
                                    "Level 3",
                                ),
                            ),
                        ),
                        tags.li(
                            {"class": "nav-item"},
                            tags.a(
                                {
                                    "href": "javascript:;",
                                    "class": "nav-link",
                                },
                                tags.i(
                                    {"class": "nav-icon far fa-dot-circle"},
                                ),
                                tags.p(
                                    "Level 3",
                                ),
                            ),
                        ),
                    ),
                ),
                tags.li(
                    {"class": "nav-item"},
                    tags.a(
                        {
                            "href": "javascript:;",
                            "class": "nav-link",
                        },
                        tags.i(
                            {"class": "nav-icon far fa-circle"},
                        ),
                        tags.p(
                            "Level 2",
                        ),
                    ),
                ),
            ),
        ),
        tags.li(
            {"class": "nav-item"},
            tags.a(
                {"href": "javascript:;", "class": "nav-link"},
                tags.i(
                    {"class": "nav-icon fas fa-circle"},
                ),
                tags.p(
                    "Level 1",
                ),
            ),
        ),
        tags.li(
            {"class": "nav-header"},
            "LABELS",
        ),
        tags.li(
            {"class": "nav-item"},
            tags.a(
                {"href": "javascript:;", "class": "nav-link"},
                tags.i(
                    {"class": "nav-icon far fa-circle text-danger"},
                ),
                tags.p(
                    {"class": "text"},
                    "Important",
                ),
            ),
        ),
        tags.li(
            {"class": "nav-item"},
            tags.a(
                {"href": "javascript:;", "class": "nav-link"},
                tags.i(
                    {"class": "nav-icon far fa-circle text-warning"},
                ),
                tags.p(
                    "Warning",
                ),
            ),
        ),
        tags.li(
            {"class": "nav-item"},
            tags.a(
                {"href": "javascript:;", "class": "nav-link"},
                tags.i(
                    {"class": "nav-icon far fa-circle text-info"},
                ),
                tags.p(
                    "Informational",
                ),
            ),
        ),
    ]
