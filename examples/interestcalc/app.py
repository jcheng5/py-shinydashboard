# pyright: reportUnknownMemberType=false,reportUnknownArgumentType=false
from typing import Callable, Sequence, Tuple
import pathlib
import pandas as pd
import shinydashboard as sdb
from examples.interestcalc.scenario_card import ScenarioResults
from faicons import icon_svg
from htmltools import tags
from shiny import App, Inputs, Outputs, Session, reactive, render, req, ui
import numpy as np
from reactive_values import ReactiveValues
from scenario_card import scenario_server, scenario_ui

CARD_COLUMN_WIDTH = 4

app_ui = sdb.page(
    header=None,
    sidebar=sdb.sidebar(
        "Compound interest",
        {"class": "text-light"},
        ui.input_numeric("start_age", "Starting age", value=19),
        ui.input_numeric("end_age", "Ending age", value=70),
    ),
    body=sdb.body(
        # tags.h2(
        #     "Compound interest: The eighth wonder of the world", class_="text-center"
        # ),
        ui.tags.head(
            ui.tags.link(rel="stylesheet", href="textedit.css"),
            ui.tags.script(src="textedit.js"),
        ),
        ui.navset_tab_card(
            ui.nav(
                "Plot",
                ui.output_plot("plot"),
                tags.div(
                    ui.input_slider(
                        "playhead",
                        None,
                        min=0,
                        max=1,
                        step=1,
                        value=0,
                        animate=ui.AnimationOptions(interval=250, loop=False),
                    ),
                    class_="d-flex flex-row justify-content-center",
                ),
            ),
            ui.nav(
                "Table",
                tags.div(
                    ui.output_table("all_table"),
                    style="height: 450px; overflow: auto;",
                ),
            ),
        ),
        ui.row(
            scenario_ui(
                "scenario1", "Scenario 1", CARD_COLUMN_WIDTH, "2000 if age <= 30 else 0"
            ),
            scenario_ui(
                "scenario2", "Scenario 2", CARD_COLUMN_WIDTH, "2000 if age > 30 else 0"
            ),
            ui.column(
                CARD_COLUMN_WIDTH,
                ui.input_action_button(
                    "add",
                    "Add scenario",
                    icon=icon_svg("plus"),
                ),
                id="add_container",
            ),
        ),
    ),
)


def server(input: Inputs, output: Outputs, session: Session):
    scenarios = Scenarios(input.start_age, input.end_age)

    scenarios.add_scenario()
    scenarios.add_scenario()

    @reactive.Effect
    def sync_playhead_limits():
        ui.update_slider(
            "playhead",
            min=input.start_age(),
            max=input.end_age(),
            value=input.start_age(),
        )

    @reactive.Effect
    @reactive.event(input.add)
    def add_scenario():
        ui.update_slider("playhead", value=input.start_age())
        mod_id, scenario_name = scenarios.add_scenario()
        ui.insert_ui(
            scenario_ui(mod_id, scenario_name, CARD_COLUMN_WIDTH, "0"),
            "#add_container",
            "beforeBegin",
        )

    @reactive.Calc
    def all_results() -> pd.DataFrame:
        """One big data frame with [age, (scenario) name, savings, balance] columns"""

        all_titles = [scenario_res.title() for _, scenario_res in scenarios.items()]
        titles, counts = np.unique(all_titles, return_counts=True)
        duplicate_titles = titles[counts > 1]
        if len(duplicate_titles) > 0:
            raise ValueError(
                f"Duplicate scenario names detected ({', '.join(duplicate_titles)}). "
                "Please ensure each scenario name is unique!"
            )

        # Create a table for each scenario; it's just the scenario data, plus a "name"
        # column that's just the scenario name, repeated
        tables: list[pd.DataFrame] = [
            scenario_res.data().assign(id=scenario_id, name=scenario_res.title())
            for scenario_id, scenario_res in scenarios.items()
        ]

        req(len(tables) > 0)

        # Bind all the table rows together
        result = pd.concat(tables)
        # Convert name column to categorical, so grouping preserves their original order
        result["name"] = pd.Categorical(result["name"], all_titles)
        return result

    @output
    @render.table(index=True)
    def all_table():
        """Formatted table showing all of the scenario results"""

        pivoted = all_results().pivot(
            index="age", columns="name", values=["savings", "balance"]
        )
        return pivoted.style.format("${0:,.2f}").set_table_attributes(
            'class="dataframe shiny-table table w-auto"'
        )

    @output
    @render.plot
    def plot():
        df: pd.DataFrame = all_results()

        df_filtered = df.loc[df["age"] <= input.playhead(), :]

        # Abort unless there's data worth plotting
        req(df_filtered.shape[0] > 0)

        df_pivot = df_filtered.pivot(index="age", columns="name", values="balance")

        ax = df_pivot.plot.line(linewidth=2.5)
        ax.legend(title="", loc="upper left")
        ax.set_xlim((df["age"].min(), df["age"].max()))
        ax.set_ylim(bottom=min(0, df["balance"].min()), top=df["balance"].max())
        ax.yaxis.set_major_formatter("${x:1,.0f}")
        ax.yaxis.set_tick_params(which="major", labelleft=False, labelright=True)


class Scenarios:
    def __init__(
        self, start_age: Callable[[], int], end_age: Callable[[], int]
    ) -> None:
        self._counter = 0
        self._start_age = start_age
        self._end_age = end_age
        self._scenarios: ReactiveValues[str, ScenarioResults] = ReactiveValues()

    def _new_id(self) -> int:
        self._counter += 1
        return self._counter

    def add_scenario(self) -> Tuple[str, str]:
        id = self._new_id()
        module_id = f"scenario{id}"
        module_label = f"Scenario {id}"
        res = scenario_server(
            module_id,
            self._start_age,
            self._end_age,
            lambda: self.remove_handler(module_id),
        )
        self._scenarios[module_id] = res
        return module_id, module_label

    def remove_handler(self, id: str) -> None:
        del self._scenarios[id]

    def items(self) -> Sequence[Tuple[str, ScenarioResults]]:
        return list(self._scenarios.items())


app = App(app_ui, server, static_assets=pathlib.Path(__file__).parent / "www")
