import htmltools as ht
from htmltools import tags
from htmltools._core import Tag, Tagifiable  # type: ignore


def body(*args: ht.TagChild) -> ht.Tag:
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
