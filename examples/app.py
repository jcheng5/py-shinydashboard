from pathlib import Path
from shiny import Inputs, Outputs, Session, App, render, ui
import shinydashboard as sdb
from shinydashboard._layout import menu_dropdown, header_link
import htmltools as ht

# TODO: I don't think the stretched-links are accessible if they don't have a visible
# element

app_ui = sdb.page(
    header=sdb.header(
        children=[header_link("https://posit.co", "Posit")],
        children_right=[menu_dropdown()],
    ),
    sidebar=sdb.sidebar(
        sdb.brand("Hello World"),
        sdb.sidebar_submenu(
            ht.TagList(
                "The Chengs",
                ht.tags.span(
                    {"class": "badge bg-info float-end me-3"},
                    "3",
                ),
            ),
            sdb.sidebar_menu_link("Joe", "http://www.joecheng.com"),
            sdb.sidebar_menu_link("Noah", "http://www.noahcheng.com"),
            sdb.sidebar_submenu(
                "Pets",
                sdb.sidebar_menu_link(
                    "Otto", "javascript:window.alert('Not implemented');"
                ),
            ),
        ),
    ),
    body=sdb.body(
        ui.row(
            sdb.value_box(
                "12",
                "Drummers drumming",
                color="primary",
                gradient=True,
                width=True,
                href="https://posit.co/",
            ),
            sdb.value_box(
                "11", "Pipers piping", color="success", gradient=True, width=True
            ),
        ),
        ui.row(
            sdb.info_box(
                "Lords a-leaping",
                "10",
                subtitle="(That's a lot)",
                color="info",
                width=True,
            ),
            sdb.info_box(
                "Ladies dancing",
                "9",
                subtitle="(Also a lot)",
                color="danger",
                width=True,
                fill=True,
            ),
            sdb.info_box(
                "Maids a-milking",
                "8",
                color="warning",
                gradient=True,
                fill=True,
                width=True,
                href="https://posit.co/",
            ),
        ),
        ui.row(
            sdb.card(
                width=True,
                closeable=True,
                children=["This is cool I guess"],
            ),
            sdb.card(
                [ht.tags.i(class_="fa fas fa-search me-1"), "Hello"],
                width=True,
                collapsed=False,
                maximizable=True,
                closeable=True,
            ),
        ),
    ),
)


def server(input: Inputs, output: Outputs, session: Session):
    @output
    @render.text
    def txt():
        return f"n*2 is {input.n() * 2}"


app_dir = Path(__file__).parent.resolve()

app = App(app_ui, server, static_assets=app_dir / "www")
