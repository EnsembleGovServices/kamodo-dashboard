import ast

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
from dash.exceptions import PreventUpdate
from kamodo import KamodoAPI, Kamodo
from plotly import graph_objects as go

from constants import PYSAT_URL

from utils.generate_2d_graph import create_2d_graph, update_2d_graph
from utils.generate_3d_graph import create_3d_graph, update_3d_graph

import logging

logger = logging.getLogger(__name__)

# WORKFLOW CARDS START


workflow_cards = html.Div(
    [
        html.Div([
            html.H2("Select a Workflow", className="workflow-title"),
        ], className="row justify-content-center"),
        html.Div([
            dbc.Card([
                dbc.Row([
                    dbc.Col(
                        [
                            dbc.CardImg(className="card-img-left workflow-card-img", src="assets/images/workflow1.png"),
                        ],
                        lg=6,
                    ),
                    dbc.Col(
                        [
                            dbc.CardBody(
                                [
                                    html.H3("Satellite Fly Through", className="workflow-header"),
                                ]
                            ),
                        ],
                        lg=6,
                    ),
                ])
            ], className="workflow-card"),
            dbc.Card([
                dbc.Row([
                    dbc.Col(
                        [
                            dbc.CardImg(className="card-img-left workflow-card-img", src="assets/images/workflow2.png"),
                        ],
                        lg=6,
                    ),
                    dbc.Col(
                        [
                            dbc.CardBody(
                                [
                                    html.H3("Model Coupling", className="workflow-header"),
                                ]
                            ),
                        ],
                        lg=6,
                    ),
                ])
            ], className="workflow-card"),

            dbc.Card([
                dbc.Row([
                    dbc.Col(
                        [
                            dbc.CardImg(className="card-img-left workflow-card-img", src="assets/images/workflow3.png"),
                        ],
                        lg=6,
                    ),
                    dbc.Col(
                        [
                            dbc.CardBody(
                                [
                                    html.H3("Data / Model Comparison", className="workflow-header"),
                                ]
                            ),
                        ],
                        lg=6,
                    ),
                ])
            ], className="workflow-card")
        ], className="row justify-content-center"),
    ],
    className="container workflow-section"

)

# WORKFLOW CARDS ENDS

# MODEL CARDS START


ctipe_details = html.Div([
    dbc.Row([
        html.P(
            'The Coupled Thermosphere Ionosphere Plasmasphere Electrodynamics Model (CTIPe) model consists of four distinct components:'),
        html.P(
            'A high-latitude ionosphere model; A mid and low-latitude ionosphere/plasmasphere model; An electrodynamical calculation of the global dynamo electric field.')
    ], className="justify-content-center"),
    dbc.Row([
        html.P('Model Developer(s) Timothy Fuller-Rowell, Mihail Codrescu, et al. NOAA Space Weather Prediction Center')
    ], className="justify-content-center"),
    dbc.Row([
        dbc.Input(id="ctipe-input-one", placeholder="Type something...", type="text", style={'margin': '3% 0'}),
    ], className="justify-content-center"),
    dbc.Row([
        dbc.Input(id="ctipe-input-two", placeholder="Type something...", type="text", style={'margin': '3% 0'}),
    ], className="justify-content-center")
], className="ctipe-details")


def get_model_types(model_name):
    if model_name == "CTIPe":
        return dbc.ListGroup(
            [
                dbc.ListGroupItem("Couple", className="model-type-name"),
                dbc.ListGroupItem("Thermosphere", className="model-type-name"),
                dbc.ListGroupItem("Lonosphere", className="model-type-name"),
                dbc.ListGroupItem("Plasmasphere", className="model-type-name"),
            ], className=f"model-types {model_name}-list-group")
    elif model_name == "GITM":
        return dbc.ListGroup(
            [
                dbc.ListGroupItem("Thermosphere", className="model-type-name"),
                dbc.ListGroupItem("Lonosphere", className="model-type-name"),
            ], className=f"model-types {model_name}-list-group")
    else:
        return dbc.ListGroup(
            [
                dbc.ListGroupItem("Lonosphere", className="model-type-name"),
            ], className=f"model-types {model_name}-list-group")


def make_model_card(model_name):
    return html.Div([dbc.Button(
        [
            dbc.Card([
                dbc.Row([
                    dbc.Col(
                        [
                            html.H1(f"{model_name}", className="model-header")
                        ],
                        lg=6,
                    ),
                    dbc.Col(
                        [
                            dbc.CardBody(
                                [
                                    get_model_types(model_name)
                                ]
                            ),
                        ],
                        lg=6,
                    ),
                ]),
            ], className=f"{model_name}-card model-card", id=f"{model_name}-card"),
        ],
        id=f"{model_name}-toggle",
        className=f"{model_name}-collapse-button",
        n_clicks=0,
    ),
        dbc.Collapse([
            ctipe_details
        ], id=f"collapse-{model_name}", className='container', is_open=False)
    ], className='model-accordion-card')


accordion = html.Div(
    [make_model_card('CTIPe'), make_model_card('GITM'), make_model_card('IRI')], className="accordion", id="accordion"
)

model_cards = html.Div(
    [
        html.Div([
            html.H2("Select a Model", className="model-title"),
        ], className="row justify-content-center"),
        html.Div([
            accordion
        ], className="row justify-content-center"),
    ], className="container model-section"
)


# MODEL CARDS END


# TESTING  START

# TESTING END


def update_menubar_details(active_tab):
    if active_tab == "workflow_tab":
        return workflow_cards
    elif active_tab == "models_tab":
        return model_cards
    elif active_tab == "datasets_tab":
        return "DATASETS TAB"
    elif active_tab == "editor_tab":
        return "EDITOR TAB"
    return html.P("This shouldn't ever be displayed...")


def toggle_model_cards_accordion(n1, n2, n3, is_open1, is_open2, is_open3):
    ctx = dash.callback_context

    if not ctx.triggered:
        return False, False, False
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if button_id == "CTIPe-toggle" and n1:
        return not is_open1, False, False
    elif button_id == "GITM-toggle" and n2:
        return False, not is_open2, False
    elif button_id == "IRI-toggle" and n3:
        return False, False, not is_open3
    return False, False, False


# PLOT DYNAMICALLY START #

k = KamodoAPI(PYSAT_URL)
empty_graph = dcc.Graph(
    id="my-graph-empty"
)


def get_selected_model_names(n_clicks):
    if n_clicks not in [0, None]:
        model_list = []
        i = 0  # only increment when there's a symbol without parenthesis
        for index in k:
            if '(' not in str(index):
                symbolic_fname = str(k.signatures[str(index)]['symbol'])
                fname = str(index)
                model_list.append(
                    dbc.ListGroupItem(
                        # symbolic_fname,
                        fname,
                        id={'type': 'model-plot-button', 'id': i},
                        n_clicks=0,
                        action=True
                    ),
                )
                i += 1

        return dbc.ListGroup(model_list, className="model-type-list")


def init_kamodo_graphs(children):
    if children is None:
        raise PreventUpdate
    graph_list = []
    for index, _ in enumerate(children['props']['children']):
        fname = _['props']['children']
        graph_list.append(
            dbc.ListGroupItem(
                html.Div(
                    id={'type': 'kamodo-plot', 'id': index}
                ),
                id={'type': 'kamodo-plot-area', 'id': index}, className='kamodo-plot-area', style={'display': 'none'})
        )
    print('initialized graphs')
    return graph_list


def plot_kamodo_graph(n_clicks, id):
    print(f'NCLICK VALUE : {n_clicks}, ID: {id}')
    if n_clicks in [None, 0]:
        raise PreventUpdate

    if n_clicks % 2 == 0:
        return {'display': 'none'}, False
    else:
        fsymbol = list(k.signatures.keys())[id['id']]
        new_graph = dcc.Graph(
            id="fsymbol-graph",
            figure=k.plot(fsymbol)
        )
        return {'display': 'block'}, new_graph


# PLOT DYNAMICALLY END


# CUSTOM FUNCTION PLOTTING START #

def range_slider_2d_graph(min_value, max_value):
    range_slider = dcc.RangeSlider(
        id='my-range-slider-2d',
        className='my-range-slider-2d',
        min=int(min_value),
        max=int(max_value),
        step=0.5,
        value=[-5, 5],
    )
    range_slider_area = html.Div([
        dbc.Row(
            [
                dbc.Col([
                    html.H4(
                        f'{min_value}'
                    )
                ], className='range-min-value', width=1),
                dbc.Col([
                    range_slider
                ], width=10),
                dbc.Col([
                    html.H4(
                        f'{max_value}'
                    )
                ], className='range-max-value', width=1),
            ]
        ),
    ], id='my-range-slider-area', className='my-range-slider-area')

    return range_slider_area


def range_slider_3d_graph(min_value, max_value):
    range_slider_x = dcc.RangeSlider(
        id='my-range-slider-3d-x',
        className='my-range-slider-3d-x',
        min=int(min_value),
        max=int(max_value),
        step=0.5,
        value=[-5, 5],
    )

    range_slider_y = dcc.RangeSlider(
        id='my-range-slider-3d-y',
        className='my-range-slider-3d-y',
        min=int(min_value),
        max=int(max_value),
        step=0.5,
        value=[-5, 5],
    )


    range_slider_area = html.Div([
        dbc.Row(
            [
                dbc.Col([
                    html.H4(
                        f'{min_value}'
                    )
                ], className='range-min-value', width=1),
                dbc.Col([
                    range_slider_x
                ], width=10),
                dbc.Col([
                    html.H4(
                        f'{max_value}'
                    )
                ], className='range-max-value', width=1),
            ]
        ),
        dbc.Row(
            [
                dbc.Col([
                    html.H4(
                        f'{min_value}'
                    )
                ], className='range-min-value', width=1),
                dbc.Col([
                    range_slider_y
                ], width=10),
                dbc.Col([
                    html.H4(
                        f'{max_value}'
                    )
                ], className='range-max-value', width=1),
            ]
        ),
    ], id='my-range-slider-area', className='my-range-slider-area')

    return range_slider_area


def plot_custom_2d_graph(figure):
    new_graph = dcc.Graph(
        id='my-graph-custom-2d',
        figure=figure,
    )
    return new_graph


def plot_custom_3d_graph(figure):
    new_graph = dcc.Graph(
        id='my-graph-custom-3d',
        figure=figure,
    )
    return new_graph


def plot_custom_function(function_value, min_value, max_value):
    if not min_value:
        min_value = -10
    if not max_value:
        max_value = 10

    if function_value and min_value and max_value:
        function = function_value.split('=')[1]
        if (function.__contains__('x') or function.__contains__('X')) and (
                function.__contains__('y') or function.__contains__('Y')):
            figure = create_3d_graph(function)
            if figure:
                new_graph = plot_custom_3d_graph(figure)
                range_slider_area = range_slider_3d_graph(min_value, max_value)
                new_graph_area = html.Div([
                    new_graph,
                    range_slider_area
                ], id='my-graph-custom-area', className='my-graph-custom-area')
                return new_graph_area
            else:
                return dbc.Alert("Input valid function only...", color="danger")
        else:
            figure = create_2d_graph(function)
            if figure:
                new_graph = plot_custom_2d_graph(figure)
                range_slider_area = range_slider_2d_graph(min_value, max_value)
                new_graph_area = html.Div([
                    new_graph,
                    range_slider_area
                ], id='my-graph-custom-area', className='my-graph-custom-area')
                return new_graph_area
            else:
                return dbc.Alert("Input valid function only...", color="danger")
    return False


# CUSTOM FUNCTION PLOTTING END #

# UPDATE CUSTOM FUNCTION GRAPH START #

def update_custom_function_2d_graph(range_value, function_value):
    print(f"RANGE 2D : {range_value}")
    function = function_value.split('=')[1]
    new_figure = update_2d_graph(range_value, function)
    return new_figure


def update_custom_function_3d_graph(range_value_x, range_value_y, function_value):
    print(f"RANGE 3D : X {range_value_x} Y {range_value_y} ")
    function = function_value.split('=')[1]
    new_figure = update_3d_graph(range_value_x, range_value_y, function)
    return new_figure

# UPDATE CUSTOM FUNCTION GRAPH END #
