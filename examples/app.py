from pathlib import Path
from random import random
from shiny import Inputs, Outputs, Session, App, render, ui, reactive
import shinydashboard as sdb
import htmltools as ht

# TODO: I don't think the stretched-links are accessible if they don't have a visible
# element

app_ui = sdb.page(
    header=sdb.header(
        children=[sdb.header_link("https://posit.co", "Posit")],
        children_right=[
            sdb.menu_dropdown(
                sdb.MenuType.Messages,
                sdb.item_message(
                    "Joe Cheng",
                    "Hello, world!",
                    icon=ht.tags.i(class_="fs-2 text-info fa fas fa-info-circle"),
                    time="4 minutes ago",
                ),
                sdb.item_message(
                    "Winston Chang",
                    ht.TagList(
                        "I need a code review ", ht.strong("right now"), " please!"
                    ),
                    icon=ht.tags.i(
                        class_="fs-2 text-danger fa fas fa-exclamation-circle"
                    ),
                    time="4 minutes ago",
                    href="https://github.com/",
                ),
                header="Recent messages",
            ),
            sdb.menu_dropdown(
                sdb.MenuType.Notifications,
                sdb.item_notification(
                    "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
                    time="An hour ago",
                ),
                sdb.item_notification(
                    "Hello!",
                    time="An hour ago",
                ),
            ),
        ],
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
            sdb.sidebar_menu_link("Joe", href="http://www.joecheng.com"),
            sdb.sidebar_menu_link("Noah", href="http://www.noahcheng.com"),
            sdb.sidebar_submenu(
                "Pets",
                sdb.sidebar_menu_link(
                    "Otto", href="javascript:window.alert('Not implemented');"
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
                href="https://posit.co/",
            ),
            sdb.output_value_box("pipers"),
        ),
        ui.row(
            sdb.info_box(
                "Lords a-leaping",
                "10",
                subtitle="(That's a lot)",
                color="info",
            ),
            sdb.info_box(
                "Ladies dancing",
                "9",
                subtitle="(Also a lot)",
                color="danger",
                fill=True,
            ),
            sdb.output_info_box("maids"),
        ),
        ui.row(
            sdb.card(
                closeable=True,
                children=["This is cool I guess"],
            ),
            sdb.card(
                ht.TagList(
                    ht.tags.i(class_="fa fas fa-search me-1"),
                    "Hello",
                ),
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

    @output
    @sdb.render_value_box
    def pipers():
        reactive.invalidate_later(1)
        return sdb.value_box(
            "%1.3f" % (random() * 11),
            "Pipers piping",
            color="success",
            gradient=True,
        )

    @output
    @sdb.render_info_box
    async def maids():
        reactive.invalidate_later(1)
        return sdb.info_box(
            "Maids a-milking",
            "%1.1f" % (random() * 8),
            color="warning",
            gradient=True,
            fill=True,
            href="https://posit.co/",
        )


app_dir = Path(__file__).parent.resolve()

app = App(app_ui, server, static_assets=app_dir / "www")
