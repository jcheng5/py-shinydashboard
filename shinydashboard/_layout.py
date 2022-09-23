from typing import List, Optional

import htmltools as ht
from htmltools import tags

from ._htmldeps import deps_adminlte


# TODO: Use all arguments
def page(
    header: ht.TagChildArg = None,
    sidebar: ht.TagChildArg = None,
    body: ht.TagChildArg = None,
    *,
    controlbar: ht.TagChildArg = None,
    footer: ht.TagChildArg = None,
    title: ht.TagChildArg = None,
    lang: Optional[str] = None,
) -> ht.Tag:
    return tags.html(
        _head(title=title),
        _body(
            header=header,
            sidebar=sidebar,
            body=body,
            controlbar=controlbar,
            footer=footer,
        ),
        lang=lang,
    )


def _head(*, title: ht.TagChildArg = None) -> ht.Tag:
    return tags.head(
        tags.meta(charset="utf-8"),
        tags.meta(
            name="viewport",
            content="width=device-width, initial-scale=1",
        ),
        tags.meta({"http-equiv": "x-ua-compatible", "content": "ie=edge"}),
        tags.title(title),
        deps_adminlte(),
        tags.link(
            rel="stylesheet",
            href="https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@5.15.4/css/all.min.css",
            integrity="sha256-mUZM63G8m73Mcidfrv5E+Y61y7a12O5mW4ezU3bxqW4=",
            crossorigin="anonymous",
        ),
        tags.script(
            {
                "src": "https://cdn.jsdelivr.net/npm/bootstrap@5.2.0/dist/js/bootstrap.bundle.min.js",
                "integrity": "sha384-A3rJD856KowSb7dwlZdYEkO39Gagi7vIsF0jrRAoQmDKKtQBHUuLZ9AsSv4jD4Xa",
                "crossorigin": "anonymous",
            }
        ),
    )


def _body(
    header: ht.TagChildArg = None,
    sidebar: ht.TagChildArg = None,
    body: ht.TagChildArg = None,
    *,
    controlbar: ht.TagChildArg = None,
    footer: ht.TagChildArg = None,
) -> ht.Tag:
    return tags.body(
        {"class": "layout-fixed"},
        tags.div(
            {"class": "wrapper"},
            header,
            sidebar,
            body,
            # TODO: controlbar?
            # TODO: footer?
        ),
    )


def header(
    *args: ht.TagChild,
    children: Optional[List[ht.TagChild]] = None,
    children_right: Optional[List[ht.TagChild]] = None,
) -> ht.Tag:
    # Navbar
    return tags.nav(
        {"class": "main-header navbar navbar-expand navbar-light"},
        tags.div(
            {"class": "container-fluid"},
            # Navbar links
            tags.ul(
                {"class": "navbar-nav"},
                tags.li(
                    {"class": "nav-item"},
                    tags.a(
                        {
                            "class": "nav-link",
                            "data-lte-toggle": "sidebar-full",
                            "href": "#",
                            "role": "button",
                        },
                        tags.i(class_="fas fa-bars"),
                    ),
                ),
                *args,
                children=children,
            ),
            # Drop-down menus
            tags.ul(
                {"class": "navbar-nav ms-auto"},
                children_right,
            ),
        ),
    )


def header_link(href: str, label: ht.TagChild) -> ht.Tag:
    return tags.li(
        {"class": "nav-item d-none d-md-block"},
        tags.a({"href": href, "class": "nav-link"}, label),
    )


def dummy2():
    return ht.TagList(
        # Navbar Search
        tags.li(
            {"class": "nav-item"},
            tags.a(
                {
                    "class": "nav-link",
                    "data-widget": "navbar-search",
                    "href": "#",
                    "role": "button",
                },
                tags.i({"class": "fas fa-search"}),
            ),
        ),
        # Messages Dropdown Menu
        tags.li(
            {"class": "nav-item dropdown"},
            tags.a(
                {"class": "nav-link", "data-bs-toggle": "dropdown", "href": "#"},
                tags.i(
                    {"class": "far fa-comments"},
                ),
                tags.span(
                    {"class": "navbar-badge badge bg-danger"},
                    "3",
                ),
            ),
            tags.div(
                {"class": "dropdown-menu dropdown-menu-lg dropdown-menu-end"},
                tags.a(
                    {"href": "#", "class": "dropdown-item"},
                    # Message Start
                    tags.div(
                        {"class": "d-flex"},
                        tags.div(
                            {"class": "flex-shrink-0"},
                            tags.img(
                                {
                                    "src": "./assets/img/user1-128x128.jpg",
                                    "alt": "User Avatar",
                                    "class": "img-size-50 img-circle me-3",
                                }
                            ),
                        ),
                        tags.div(
                            {"class": "flex-grow-1"},
                            tags.h3(
                                {"class": "dropdown-item-title"},
                                "Brad Diesel",
                                tags.span(
                                    {"class": "float-end fs-7 text-danger"},
                                    tags.i(
                                        {"class": "fas fa-star"},
                                    ),
                                ),
                            ),
                            tags.p(
                                {"class": "fs-7"},
                                "Call me whenever you can...",
                            ),
                            tags.p(
                                {"class": "fs-7 text-muted"},
                                tags.i(
                                    {"class": "far fa-clock me-1"},
                                ),
                                "4 Hours Ago",
                            ),
                        ),
                    ),
                    # Message End
                ),
                tags.div(
                    {"class": "dropdown-divider"},
                ),
                tags.a(
                    {"href": "#", "class": "dropdown-item"},
                    # Message Start
                    tags.div(
                        {"class": "d-flex"},
                        tags.div(
                            {"class": "flex-shrink-0"},
                            tags.img(
                                {
                                    "src": "./assets/img/user8-128x128.jpg",
                                    "alt": "User Avatar",
                                    "class": "img-size-50 img-circle me-3",
                                }
                            ),
                        ),
                        tags.div(
                            {"class": "flex-grow-1"},
                            tags.h3(
                                {"class": "dropdown-item-title"},
                                "John Pierce",
                                tags.span(
                                    {"class": "float-end fs-7 text-muted"},
                                    tags.i(
                                        {"class": "fas fa-star"},
                                    ),
                                ),
                            ),
                            tags.p(
                                {"class": "fs-7"},
                                "I got your message bro",
                            ),
                            tags.p(
                                {"class": "fs-7 text-muted"},
                                tags.i(
                                    {"class": "far fa-clock me-1"},
                                ),
                                "4 Hours Ago",
                            ),
                        ),
                    ),
                    # Message End
                ),
                tags.div(
                    {"class": "dropdown-divider"},
                ),
                tags.a(
                    {"href": "#", "class": "dropdown-item"},
                    # Message Start
                    tags.div(
                        {"class": "d-flex"},
                        tags.div(
                            {"class": "flex-shrink-0"},
                            tags.img(
                                {
                                    "src": "./assets/img/user3-128x128.jpg",
                                    "alt": "User Avatar",
                                    "class": "img-size-50 img-circle me-3",
                                },
                            ),
                        ),
                        tags.div(
                            {"class": "flex-grow-1"},
                            tags.h3(
                                {"class": "dropdown-item-title"},
                                "Nora Silvester",
                                tags.span(
                                    {"class": "float-end fs-7 text-warning"},
                                    tags.i(
                                        {"class": "fas fa-star"},
                                    ),
                                ),
                            ),
                            tags.p(
                                {"class": "fs-7"},
                                "The subject goes here",
                            ),
                            tags.p(
                                {"class": "fs-7 text-muted"},
                                tags.i(
                                    {"class": "far fa-clock me-1"},
                                ),
                                "4 Hours Ago",
                            ),
                        ),
                        # Message End
                    ),
                ),
                tags.div(
                    {"class": "dropdown-divider"},
                ),
                tags.a(
                    {"href": "#", "class": "dropdown-item dropdown-footer"},
                    "See All Messages",
                ),
            ),
            # Notifications Dropdown Menu
            tags.li(
                {"class": "nav-item dropdown"},
                tags.a(
                    {"class": "nav-link", "data-bs-toggle": "dropdown", "href": "#"},
                    tags.i(
                        {"class": "far fa-bell"},
                    ),
                    tags.span(
                        {"class": "navbar-badge badge bg-warning"},
                        "15",
                    ),
                ),
                tags.div(
                    {"class": "dropdown-menu dropdown-menu-lg dropdown-menu-end"},
                    tags.span(
                        {"class": "dropdown-item dropdown-header"},
                        "15 Notifications",
                    ),
                    tags.div(
                        {"class": "dropdown-divider"},
                    ),
                    tags.a(
                        {"href": "#", "class": "dropdown-item"},
                        tags.i(
                            {"class": "fas fa-envelope fa-fw me-2"},
                        ),
                        "4 new messages",
                        tags.span(
                            {"class": "float-end text-muted fs-7"},
                            "3 mins",
                        ),
                    ),
                    tags.div(
                        {"class": "dropdown-divider"},
                    ),
                    tags.a(
                        {"href": "#", "class": "dropdown-item"},
                        tags.i(
                            {"class": "fas fa-users fa-fw me-2"},
                        ),
                        "8 friend requests",
                        tags.span(
                            {"class": "float-end text-muted fs-7"},
                            "12 hours",
                        ),
                    ),
                    tags.div(
                        {"class": "dropdown-divider"},
                    ),
                    tags.a(
                        {"href": "#", "class": "dropdown-item"},
                        tags.i(
                            {"class": "fas fa-file fa-fw me-2"},
                        ),
                        "3 new reports",
                        tags.span(
                            {"class": "float-end text-muted fs-7"},
                            "2 days",
                        ),
                    ),
                    tags.div(
                        {"class": "dropdown-divider"},
                    ),
                    tags.a(
                        {"href": "#", "class": "dropdown-item dropdown-footer"},
                        "See All Notifications",
                    ),
                ),
            ),
            tags.li(
                {"class": "nav-item dropdown user-menu"},
                tags.a(
                    {
                        "href": "#",
                        "class": "nav-link dropdown-toggle",
                        "data-bs-toggle": "dropdown",
                    },
                    tags.img(
                        {
                            "src": "./assets/img/user2-160x160.jpg",
                            "class": "user-image img-circle shadow",
                            "alt": "User Image",
                        }
                    ),
                    tags.span(
                        {"class": "d-none d-md-inline"},
                        "Alexander Pierce",
                    ),
                ),
                tags.ul(
                    {"class": "dropdown-menu dropdown-menu-lg dropdown-menu-end"},
                    # User image
                    tags.li(
                        {"class": "user-header bg-primary"},
                        tags.img(
                            {
                                "src": "./assets/img/user2-160x160.jpg",
                                "class": "img-circle shadow",
                                "alt": "User Image",
                            }
                        ),
                        tags.p(
                            "Alexander Pierce - Web Developer",
                            tags.small("Member since Nov. 2012"),
                        ),
                    ),
                    # Menu Body
                    tags.li(
                        {"class": "user-body"},
                        tags.div(
                            {"class": "row"},
                            tags.div(
                                {"class": "col-4 text-center"},
                                tags.a(
                                    {"href": "#"},
                                    "Followers",
                                ),
                            ),
                            tags.div(
                                {"class": "col-4 text-center"},
                                tags.a(
                                    {"href": "#"},
                                    "Sales",
                                ),
                            ),
                            tags.div(
                                {"class": "col-4 text-center"},
                                tags.a(
                                    {"href": "#"},
                                    "Friends",
                                ),
                            ),
                        ),
                        # /.row
                    ),
                    # Menu Footer--,
                    tags.li(
                        {"class": "user-footer"},
                        tags.a(
                            {"href": "#", "class": "btn btn-default btn-flat"},
                            "Profile",
                        ),
                        tags.a(
                            {
                                "href": "#",
                                "class": "btn btn-default btn-flat float-end",
                            },
                            "Sign out",
                        ),
                    ),
                ),
            ),
            # TODO tackel in v4.1
            # tags.li({"class":"nav-item"},
            tags.a(
                {
                    "class": "nav-link",
                    "data-widget": "fullscreen",
                    "href": "#",
                    "role": "button",
                },
                tags.i(
                    {"class": "fas fa-expand-arrows-alt"},
                ),
            ),
        ),
        tags.li(
            {"class": "nav-item"},
            tags.a(
                {
                    "class": "nav-link",
                    "data-widget": "control-sidebar",
                    "data-slide": "true",
                    "href": "#",
                    "role": "button",
                },
                tags.i(
                    {"class": "fas fa-th-large"},
                ),
            ),
        ),
    )
