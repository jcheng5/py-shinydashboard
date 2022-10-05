from typing import List
from htmltools import HTMLDependency
from . import __version__


def deps_adminlte() -> List[HTMLDependency]:
    return [
        HTMLDependency(
            "AdminLTE",
            "4.0.0-alpha.1",
            source={
                "package": "shinydashboard",
                "subdir": "www/adminlte",
            },
            script={"src": "js/adminlte.min.js"},
            stylesheet={"href": "css/adminlte.min.css"},
        ),
    ]


def deps_shinydashboard() -> List[HTMLDependency]:
    return [
        HTMLDependency(
            "shinydashboard",
            __version__,
            source={
                "package": "shinydashboard",
                "subdir": "shinydashboard",
            },
            script={"src": "js/shinydashboard.js"},
            stylesheet={"href": "css/shinydashboard.css"},
        )
    ]
