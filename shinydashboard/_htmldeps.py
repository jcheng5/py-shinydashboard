from typing import List
from htmltools import HTMLDependency


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
