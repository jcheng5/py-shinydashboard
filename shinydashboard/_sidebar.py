from typing import Optional, Union
import htmltools as ht
from htmltools import tags
from ._utils import wrap_with_tag
from faicons import icon_svg

from htmltools._core import Tag, Tagifiable  # type: ignore


def brand(
    title: ht.TagChild,
    *,
    href: Optional[str] = None,
    img_src: Optional[str] = None,
    img_alt: Optional[str] = None,
    img_class: str = "brand-image shadow",
) -> ht.TagChild:
    """An element to hold the dashboard title and/or logo, for use in :func:`sidebar`.

    Parameters
    ----------
    title
        The main title of the dashboard. Usually a string, but can be any valid htmltools content.
    href
        A link target. Use ``None`` if no link is desired, or ``""`` to create a link that reloads the page.
    img_src
        An image URL; can be an absolute ``https`` URL, or a static file that's `served by Shiny <https://shiny.rstudio.com/py/docs/ui-static.html>`_. With the default ``img_class`` argument, the image will be displayed at a relatively small size, to the left of the title.
    img_alt
        A textual description of the image, for accessibility purposes.
    img_class
        CSS classes to apply to the ``<img>`` tag.

    Returns
    -------
        A :class:`Tag` object.
    """
    img = None
    if img_src:
        img = tags.img(
            {
                "src": img_src,
                "alt": img_alt,
                "class": img_class,
            },
        )

    container = tags.a if href is not None else tags.div

    return container(
        {"href": href, "class": "brand-link"},
        img,
        tags.span(
            {"class": "brand-text fw-light"},
            title,
        ),
    )


def sidebar_menu_tab(
    title: ht.TagChild,
    tab_name: str,
    *,
    icon: ht.TagChild = icon_svg("circle", style="regular"),
) -> ht.Tag:

    # id of the pane we're controlling
    content_id = f"shinydash-tab-{tab_name}"
    # id of the current element
    id = f"{content_id}-tab"

    return tags.li(
        {"class": "nav-item", "role": "presentation"},
        tags.a(
            {
                "class": "nav-link",
                "role": "tab",
                "id": id,
                "href": "#",
                "data-bs-toggle": "tab",
                "data-bs-target": f"#{content_id}",
            },
            icon,
            tags.p(
                title,
            ),
        ),
    )


def sidebar_menu_link(
    title: ht.TagChild,
    href: str,
    *,
    icon: ht.TagChild = icon_svg("circle", style="regular"),
) -> ht.Tag:

    return tags.li(
        {"class": "nav-item", "role": "presentation"},
        tags.a(
            {"class": "nav-link", "href": href},
            icon,
            tags.p(
                title,
            ),
        ),
    )


def nav_content(tab_name: str, *args: ht.TagChildArg, **kwargs: ht.TagAttrArg):
    id = f"shinydash-tab-{tab_name}"
    return ht.div(
        {
            "id": id,
            "class": "tab-pane",
            "role": "tabpanel",
            "aria-labelledby": id + "-tab",
        },
        *args,
        **kwargs,
    )


def navset(*tabs: ht.TagChildArg, **kwargs: ht.TagAttrArg):
    return ht.div(
        {
            "id": "shinydash-tab",
            "data-tabsetid": "shinydash-tab",
            "class": "tab-content",
        },
        *tabs,
        **kwargs,
    )


def sidebar_submenu(
    title: ht.TagChild,
    *args: ht.TagChild,
    icon: ht.TagChild = icon_svg("circle", style="solid"),
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
    """A collapsible sidebar, for use in :func:`page`. Contains :func:`brand` and a navigational menu.

    Parameters
    ----------
    title
        A title to be rendered at the top-left corner of the dashboard. You'll generally want to use :func:`brand` here (or just use a bare string, which we'll then automatically wrap in :func:`brand` for you).
    args
        A combination of any of the following:

        - :func:`sidebar_menu_tab` - For navigating to different tabs within the dashboard.
        - :func:`sidebar_menu_link` - For external links that navigate away from the dashboard.
        - :func:`sidebar_submenu` - For nested menus that contain tabs, external links, or yet another level of menus.

    Returns
    -------
        A :class:`Tag` object, ready to be used as the ``sidebar`` argument in :func:`page`.
    """
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
