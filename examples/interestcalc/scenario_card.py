# pyright: reportUnknownMemberType=false

import math
from dataclasses import dataclass
from typing import Any, Callable, Optional

import numpy as np
import pandas as pd
import shinydashboard as sdb
from faicons import icon_svg
from numpy._typing import NDArray
from shiny import Inputs, Outputs, Session, module, reactive, render, ui
from shiny.types import SilentCancelOutputException

from textedit import textedit_ui, textedit_server

# ============================================================
# Module: scenario
# ============================================================


@module.ui
def scenario_ui(
    scenario_name: str, width: int = 4, default_code: str = "0"
) -> ui.TagChildArg:
    return ui.column(
        width,
        sdb.card(
            ui.h6(
                ui.input_action_link(
                    "close",
                    None,
                    icon=icon_svg("xmark", style="solid"),
                    class_="float-end",
                    title="Remove scenario",
                ),
                textedit_ui("scenario_name", scenario_name),
                class_="m-0",
            ),
            ui.input_numeric("interest", "Interest (%)", 7),
            ui.input_text_area("code", "Annual savings logic", default_code, rows=4),
            ui.output_ui("message", class_="text-danger fs-6"),
            # Card width
        ),
        id=module.resolve_id("card"),
    )


@dataclass
class ScenarioResults:
    data: Callable[[], pd.DataFrame]
    title: Callable[[], str]


@module.server
def scenario_server(
    input: Inputs,
    output: Outputs,
    session: Session,
    start_age: Callable[[], int],
    end_age: Callable[[], int],
    on_close: Callable[[], None],
) -> ScenarioResults:
    title = textedit_server("scenario_name")

    error_message: reactive.Value[Optional[str]] = reactive.Value(None)

    def contrib_for_age(age: int) -> float:
        index = age - start_age()
        result = eval(input.code(), {"math": math}, {"index": index, "age": age})
        if result is None:
            return 0
        return float(result)

    @reactive.Calc
    def data() -> pd.DataFrame:
        ages: NDArray[np.signedinteger[Any]] = np.arange(
            start_age(), end_age() + 1, step=1
        )
        try:
            contributions = [contrib_for_age(age) for age in ages]
            error_message.set(None)
        except Exception as e:
            error_message.set(str(e))
            raise SilentCancelOutputException()

        interest = 1 + input.interest() / 100
        balances = [0]
        for contrib in contributions:
            balances.append(balances[-1] * interest + contrib)
        balances.pop(0)

        return pd.DataFrame(
            {"age": ages, "savings": contributions, "balance": balances}
        )

    @output
    @render.ui
    def message():
        msg = error_message.get()
        if msg is not None:
            return ui.TagList(ui.strong("Error:"), msg)

    @reactive.Effect
    @reactive.event(input.close)
    def close_card():
        # Remove UI
        ui.remove_ui(f"#{module.resolve_id('card')}", immediate=False)

        # Destroy observers
        close_card.destroy()  # type: ignore

        # Notify parent
        on_close()

    return ScenarioResults(data=data, title=title)
