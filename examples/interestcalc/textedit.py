"""This module implements a title that can be clicked to edit."""

from typing import Callable
from shiny import Inputs, Outputs, Session, module, ui

# ============================================================
# Module: textedit
# ============================================================


@module.ui
def textedit_ui(initial_value: str) -> ui.Tag:
    return ui.span(
        ui.input_text("editbox", None, value=initial_value),
        class_="textedit-container d-flex align-items-start pe-3 pb-0",
    )


@module.server
def textedit_server(
    input: Inputs, output: Outputs, session: Session
) -> Callable[[], str]:
    return input.editbox


#     @reactive.Effect
#     @reactive.event(input.link)
#     def _():
#         ui.modal_show(
#             ui.modal(
#                 ui.input_text("new_value", None, value=value.get()),
#                 title="Edit title",
#                 footer=ui.TagList(
#                     ui.input_action_button("save", "Save", class_="btn-primary"),
#                     ui.input_action_button("cancel", "Cancel"),
#                 ),
#             )
#         )

#     @reactive.Effect
#     @reactive.event(input.save)
#     def save_handler():
#         value.set(input.new_value())
#         ui.modal_remove()

#     @reactive.Effect
#     @reactive.event(input.cancel)
#     def cancel_handler():
#         ui.modal_remove()
