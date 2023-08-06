"""Main module for the site class"""
#! /usr/bin/env python

# Python imports
import sys
import os

# Module imports
import numpy as np
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd

# Local imports
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_PATH)
import visvasc

class Site:
    """Site class that handles the dash web app"""

    def __init__(self, input_dict_list, function, vessel_locs, **kwargs):
        """ Initialises a site to visualise a vasculature network.

        Args:
            input_list (list) : A list of dictionaries where each dictionary has the fields:
                name (str) : Name of variable to be displayed to site.
                id (str) : Name to be passed to the function (also used as ID).
                value (object) : Default value to be displayed to site.
                type (str) : Type of the value.
            function (object) : A function that takes a set of kwarg arguments and produces an
                output.
            vessel_locs (dict) : A dictionary of each vessels start, stop and number of samples.
                Expected as a dictionary with:
                    "vessel_name" : [start, end, num]
                for each vessel.
                The whole contents are passed directly to numpy.linspace and hence positional
                arguments can also be used.

        kwargs:
            t_max (float, optional) : The maximum time at which to evaluate the function.
                Defaults to 10.
            x_plot (function, optional) : The function to plot the static x graph.
                Defaults to visvasc.site._plot_x().
            t_plot (function, optional) : The function to plot the static t graph.
                Defaults to visvasc.site._plot_t().
        """

        # Loads keyword arguments
        self.t_max = kwargs.get('t_max', 10)
        self.x_plot = kwargs.get('x_plot', _plot_x)
        self.t_plot = kwargs.get('t_plot', _plot_t)

        self.app = Dash(__name__)
        self.input_dict_list = input_dict_list
        self.function = function
        self.vessel_locs = vessel_locs

        self.function_kwargs = get_kwargs(input_dict_list)

        vessels = list(vessel_locs.keys())
        vessel_dd_id = "vessel-dropdown"


        self.app.layout = html.Div([
            html.Div([
                html.H1("Inputs"),
                html.Div([
                    "Vessel: ",
                    dcc.Dropdown(vessels, vessels[0], id=vessel_dd_id),
                ]),
                html.Div([
                    "Max time (s): ",
                    dcc.Input(id="T_max", value=self.t_max, type="number"),
                ]),
                visvasc.layout.inputs_from_dict_list(
                    input_dict_list, style={'padding':10, 'flex':1}
                ),
            ], style={'padding':10, 'flex':1}),
            html.Div([
                html.H1("Graphs"),
                html.Div([
                    html.Label('X position'),
                    dcc.Slider(
                        min=0,
                        max=1,
                        value=0,
                        vertical=False,
                        id="slider-x",
                    ),
                    html.Div(id="slider-x-label"),
                ]),
                html.Div([
                    dcc.Graph(id='graph-x'),
                ]),
                html.Div([
                    html.Label('T position'),
                    dcc.Slider(
                        min=0,
                        max=self.t_max,
                        value=0,
                        vertical=False,
                        id="slider-t",
                    ),
                    html.Div(id="slider-t-label"),
                ]),
                html.Div([
                    dcc.Graph(id='graph-t'),
                ]),
            ], style={'padding':10, 'flex':1}),
        ], style={'display': 'flex', 'flex-direction': 'row'})

        inputs = [Input(item["id"], 'value') for item in input_dict_list]
        input_kwarg_keys = [item["id"] for item in input_dict_list]

        ### Callback functions ###
        @self.app.callback(
            Output('slider-x', 'min'),
            Output('slider-x', 'max'),
            Output('slider-x', 'value'),
            Input(vessel_dd_id, 'value'),
        )
        def _set_slider_range(vessel_key):
            v_start, v_end = get_relative_x(*vessel_locs[vessel_key][:2])
            v_mid = (v_end - v_start) / 2

            return v_start, v_end, v_mid

        @self.app.callback(
            Output('slider-x-label', 'children'),
            Input('slider-x', 'value'),
            Input(vessel_dd_id, 'value'),
        )
        def _update_slider(x_pos, vessel_key):
            v_start, v_end = get_relative_x(*vessel_locs[vessel_key][:2])
            x_percentage = (x_pos - v_start) / (v_end - v_start) * 100
            return f"x = {x_percentage:.0f}%"

        @self.app.callback(
            Output('graph-x', 'figure'),
            Input('slider-x', 'value'),
            Input('T_max', 'value'),
            *inputs,
        )
        def _get_figure_x(x, t_max, *input_kwarg_values): # pylint: disable=invalid-name
            """Plots the figure with up to date values"""

            # Updates internal variables
            self.update_kwargs(input_kwarg_keys, input_kwarg_values)
            self.x = x
            self.t_max = t_max

            return self.x_plot(self)

        @self.app.callback(
            Output('slider-t', 'max'),
            Input('T_max', 'value'),
        )
        def _set_t_slider_max(t_max):
            return t_max

        @self.app.callback(
            Output('slider-t-label', 'children'),
            Input('slider-t', 'value'),
            Input('T_max', 'value'),
        )
        def _update_slider(t, t_max):   # pylint: disable=invalid-name
            t_val = t if t < t_max else t_max
            return f"t = {t_val}"

        @self.app.callback(
            Output('graph-t', 'figure'),
            Input('slider-t', 'value'),
            Input(vessel_dd_id, 'value'),
            *inputs,
        )
        def _get_figure_t(t, vessel_key, *input_kwarg_values): # pylint: disable=invalid-name
            """Plots the figure with up to date values"""

            # Updates internal function_kwargs
            self.update_kwargs(input_kwarg_keys, input_kwarg_values)
            self.t = t
            self.vessel_key = vessel_key

            return self.t_plot(self)


    def update_kwargs(self, keys, values):
        """Updates the function kwargs dictionary

        Also updates internal property `self.function_kwargs`.

        Args:
            keys (list) : A list of function key word arguments.
            values (list) : A list of associated values.
                Expected to be in the same order as keys.

        Returns:
            function_kwargs (dict) : A dictionary of kwarg pairs.
        """

        function_kwargs = {}
        for i, key in enumerate(keys):
            function_kwargs[key] = values[i]

        self.function_kwargs = function_kwargs

        return function_kwargs

    def run(self, **kwargs):
        """Runs the server

        Key word arguments are directly passed to self.app.run_server()
        """
        return self.app.run_server(**kwargs)

def get_kwargs(input_dict_list):
    """Gets a dict of kwarg from a list of dictionaries

    Args:
        input_dict_list (list) : A list of dictionaries with the format "id" : "value".

    Returns:
        kwarg_dict (dict) : A dictionary of kwarg pairs.
    """

    kwarg_dict = {}
    for item in input_dict_list:
        key, value = item["id"], item["value"]
        kwarg_dict[key] = value

    return kwarg_dict

def get_relative_x(start, end):
    """Gets the relative distance between a start and an end"""
    return 0, end - start

def _plot_x(site):
    """ Plots the graph with fixed x

    Args:
        site (visvasc.site.Site object) : Used for containing internal variables.
    
    Returns:
        fig (plotly figure) : Figure to displayed to the site.
    """

    t = np.linspace(0, site.t_max, 100)                     # pylint: disable=invalid-name
    y = site.function(site.x, t, **site.function_kwargs)    # pylint: disable=invalid-name
    data = pd.DataFrame({
        "Time (s)" : t,
        "Predicted" : y,
    })
    fig = px.line(data, x="Time (s)", y="Predicted", title="Fixed x")

    return fig

def _plot_t(site):
    """ Plots the graph with fixed t

    Args:
        site (visvasc.site.Site object) : Used for containing internal variables.
    
    Returns:
        fig (plotly figure) : Figure to displayed to the site.
    """

    x = np.linspace(*site.vessel_locs[site.vessel_key])     # pylint: disable=invalid-name
    y = site.function(x, site.t, **site.function_kwargs)    # pylint: disable=invalid-name

    x_rel = np.linspace(*get_relative_x(*site.vessel_locs[site.vessel_key][:2]), len(x))
    data = pd.DataFrame({
        "Axial position (cm)" : x_rel,
        "Predicted" : y,
    })
    fig = px.line(data, x="Axial position (cm)", y="Predicted", title="Fixed t")
    return fig
