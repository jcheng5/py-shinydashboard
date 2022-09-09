import htmltools as ht
from htmltools import tags


def body(*args: ht.TagChild) -> ht.TagChild:
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
