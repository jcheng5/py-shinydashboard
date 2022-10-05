shinydashboard
==============

This is the API documentation for shinydashboard for Python. TODO



API Reference
=============

.. currentmodule:: shinydashboard

Page and header
~~~~~~~~~~~~~~~
Functions for creating the top-level shinydashboard page, and the links in the header.

.. autosummary::
    :toctree: reference/

    page
    brand
    header
    header_link


Sidebar
~~~~~~~
Functions for creating the sidebar menu.

.. autosummary::
    :toctree: reference/

    sidebar
    sidebar_menu_tab
    sidebar_menu_link
    sidebar_submenu


Main body
~~~~~~~~~
Main body functions

.. autosummary::
    :toctree: reference/

    navset
    nav_content
    body
    card
    info_box
    value_box


Dropdown menus
~~~~~~~~~~~~~~
Functions for creating dropdown menus

.. autosummary::
    :toctree: reference/

    menu_dropdown
    item_message
    item_notification


Dynamic UI
~~~~~~~~~~
Shiny `output_*` and `render_*` methods for dynamically rendering items

.. autosummary::
    :toctree: reference/

    output_info_box
    output_menu_dropdown
    output_value_box
    render_info_box
    render_menu_dropdown
    render_value_box
