from __future__ import annotations

from typing import List, Optional

import htmltools as ht
from htmltools import tags
from htmltools._core import Tag, Tagifiable, TagList, TagChildArg  # type: ignore

from ._htmldeps import deps_adminlte, deps_shinydashboard


def page(
    header: Optional[ht.Tag] = None,
    sidebar: Optional[ht.Tag] = None,
    body: Optional[ht.Tag] = None,
    *,
    title: ht.TagChildArg = None,
    lang: Optional[str] = None,
) -> ht.Tag:
    """A shinydashboard page, for use as a Shiny app's UI.

    Parameters
    ----------

    header
        The top navigation bar, as returned by :func:`header`.
    sidebar
        The side navigation bar, as returned by :func:`sidebar`.
    body
        The main content area of the page, as returned by :func:`body`.
    title
        The contents of the ``<title>`` tag, which is used by the browser to label browser tabs and bookmarks.
    lang
        The ``lang`` attribute of the ``<html>`` tag; for example, ``"en"`` for English.

    Returns
    -------
        A :class:`Tag` object representing the HTML page.

    Examples
    --------
    >>> import shinydashboard as sdb
    >>> app_ui = sdb.page(
    ...     header = sdb.header(),
    ...     sidebar = sdb.sidebar(),
    ...     body = sdb.body(),
    ...     title = "Example dashboard"
    ... )
    """

    return tags.html(
        _head(title=title),
        _body(
            header=header,
            sidebar=sidebar,
            body=body,
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
        deps_shinydashboard(),
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
) -> ht.Tag:
    return tags.body(
        {"class": "layout-fixed"},
        {"class": "remove-sidebar"} if sidebar is None else None,
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
    children: Optional[List[ht.TagChildArg]] = None,
    children_right: Optional[List[ht.TagChildArg]] = None,
) -> ht.Tag:
    """A header, for use in :func:`page`.

    The header for a dashboard, suitable for use as the ``header`` argument of :func:`page`.

    Note that shinydashboard headers do not include the logo or tab navigation; instead, those are in the sidebar.

    Parameters
    ----------
    children
        A list of items to display on the left side of the header, like :func:`header_link`.
    children_right
        A list of items to display on the right side of the header, like :func:`menu_dropdown`.

    Returns
    -------
        A :class:`Tag` object.
    """
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
    """A link, for use in :func:`header`.

    Parameters
    ----------
    href
        A URL to link to.
    label
        A string or htmltools HTML to use as a label.

    Returns
    -------
        A :class:`Tag` object.
    """
    return tags.li(
        {"class": "nav-item d-none d-md-block"},
        tags.a({"href": href, "class": "nav-link"}, label),
    )
