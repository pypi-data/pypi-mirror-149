#! /usr/bin/env python

# Module imports
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

def inputs_from_dict_list(input_list, style=None):
    """Gets an input layout from a list of dictionary

    Args: 
        input_list (list) : A list of dictionaries where each dictionary has the fields:
            name (str) : Name of variable to be displayed to site.
            id (str) : Name to be passed to the function (also used as ID).
            value (object) : Default value to be displayed to site.
            type (str) : Type of the value.
        style (dict) : The default style for the dash.html.Div object.
            Default to None.

    Returns:
        input_layout (Dash html object) : A Dash html div object.
    """

    input_fields = []
    for dict_item in input_list:
        field = html.Div([
            f"{dict_item['name']}: ",
            dcc.Input(id=dict_item["id"], value=dict_item["value"], type=dict_item["type"]),
        ])
        input_fields.append(field)

    return html.Div(input_fields, style=style)
