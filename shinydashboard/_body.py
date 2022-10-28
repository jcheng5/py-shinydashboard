from __future__ import annotations

import htmltools as ht
from htmltools import tags
from htmltools._core import Tag, Tagifiable  # type: ignore


def body(*args: ht.TagChild) -> ht.Tag:
    """A container object that must be used to wrap the main contents of the dashboard,
    and passed as the ``body`` argument of :func:`page`.

    Parameters
    ----------
    args
        HTML objects. Common functions to use here are
        :func:`navset`/:func:`nav_content` and :func:`row`/:func:`column`.

    Returns
    -------
        A :class:`Tag` object, ready to be used as the ``body`` argument of :func:`page`.
    """
    return tags.main(
        {"class": "content-wrapper pt-4"},
        tags.div(
            {"class": "content"},
            tags.div(
                {"class": "container-fluid"},
                *args,
            ),
        ),
    )
