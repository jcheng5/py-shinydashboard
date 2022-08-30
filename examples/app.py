from asyncio import shield
from os import stat
from pathlib import Path
from shiny import Inputs, Outputs, Session, App, reactive, render, req, ui
import shinydashboard as sdb
from shinydashboard._layout import menu_dropdown

app_ui = sdb.page(
    sdb.header(children_right=menu_dropdown(), title="My sidebar"),
)


def server(input: Inputs, output: Outputs, session: Session):
    @output
    @render.text
    def txt():
        return f"n*2 is {input.n() * 2}"


app_dir = Path(__file__).parent.resolve()

app = App(app_ui, server, static_assets=app_dir / "www")
