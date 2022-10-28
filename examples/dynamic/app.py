import datetime

import faicons
from shiny import App, Inputs, Outputs, Session, reactive, ui

import shinydashboard as sdb

# By putting a reactive value outside of the server function, it's shared by all
# sessions within this Python process
click_count = reactive.Value(0)

app_ui = sdb.page(
    body=sdb.body(
        ui.row(
            sdb.card(
                "Controls",
                ui.input_action_button("click", "Click", class_="btn-primary"),
                ui.input_action_button("reset", "Reset", class_="btn-light"),
                width=4,
            ),
        ),
        ui.row(
            sdb.output_value_box("valueBox1", width=4),
        ),
        ui.row(
            sdb.output_info_box("infoBox1", width=4),
        ),
    )
)


def server(input: Inputs, output: Outputs, session: Session) -> None:
    @output
    @sdb.render_value_box
    def valueBox1():
        """Shows the current click count in a value_box."""

        return sdb.value_box(
            str(click_count()),
            "clicks",
            color="success",
            icon=faicons.icon_svg("arrow-pointer"),
        )

    @output
    @sdb.render_info_box
    def infoBox1():
        """Shows the current time in an info_box()."""

        current_time = datetime.datetime.now().astimezone()

        # datetime.now() isn't inherently reactive, so explicitly tell Shiny to consider
        # this output dirty 1 second from now
        reactive.invalidate_later(1)

        return sdb.info_box(
            "Current time",
            current_time.strftime("%I:%M:%S %p"),
            subtitle=str(current_time.tzinfo),
            icon=faicons.icon_svg("clock"),
            color="warning",
        )

    @reactive.Effect
    @reactive.event(input.click)
    def on_click():
        click_count.set(click_count.get() + 1)

    @reactive.Effect
    @reactive.event(input.reset)
    def on_reset():
        click_count.set(0)


app = App(app_ui, server)
