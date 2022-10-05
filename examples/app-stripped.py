from pathlib import Path
from random import random
from shiny import Inputs, Outputs, Session, App, render, ui, reactive
import shinydashboard as sdb
import htmltools as ht
import matplotlib.pyplot as plt
import numpy as np
from faicons import icon_svg

# TODO: I don't think the stretched-links are accessible if they don't have a visible
# element

app_ui = sdb.page(
    header=sdb.header(
        children=[sdb.header_link("https://posit.co", "Posit")],
        children_right=[
            sdb.output_menu_dropdown("comments"),
            sdb.menu_dropdown(
                icon_svg("bell"),
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
                "A simple plot",
                ui.output_plot("plot"),
                closeable=True,
            ),
            sdb.card(
                ht.TagList(
                    icon_svg("magnifying-glass"),
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

    @output
    @render.plot
    def plot():
        N = 5
        menMeans = (20, 35, 30, 35, -27)
        womenMeans = (25, 32, 34, 20, -25)
        menStd = (2, 3, 4, 1, 2)
        womenStd = (3, 5, 2, 3, 3)
        ind = np.arange(N)  # the x locations for the groups
        width = 0.35  # the width of the bars: can also be len(x) sequence

        fig, ax = plt.subplots()

        p1 = ax.bar(ind, menMeans, width, yerr=menStd, label="Men")
        p2 = ax.bar(
            ind, womenMeans, width, bottom=menMeans, yerr=womenStd, label="Women"
        )

        ax.axhline(0, color="grey", linewidth=0.8)
        ax.set_ylabel("Scores")
        ax.set_title("Scores by group and gender")
        ax.set_xticks(ind, labels=["G1", "G2", "G3", "G4", "G5"])
        ax.legend()

        # Label with label_type 'center' instead of the default 'edge'
        ax.bar_label(p1, label_type="center")
        ax.bar_label(p2, label_type="center")
        ax.bar_label(p2)

        return fig

    @output
    @sdb.render_menu_dropdown
    def comments():
        return sdb.menu_dropdown(
            icon_svg("comments"),
            sdb.item_message(
                "Joe Cheng",
                "Hello, world!",
                icon=icon_svg("circle-info", height="2em", fill="var(--bs-info)"),
                time="2 minutes ago",
            ),
            sdb.item_message(
                "Winston Chang",
                ht.TagList("I need a code review ", ht.strong("right now"), " please!"),
                icon=icon_svg(
                    "circle-exclamation", height="2em", fill="var(--bs-danger)"
                ),
                time="4 minutes ago",
                href="https://github.com/",
            ),
            header="Recent messages",
        )


app_dir = Path(__file__).parent.resolve()

app = App(app_ui, server, static_assets=app_dir / "www")
