import dash_core_components
from plotly import graph_objs
from sympy import symbols, sympify
from sympy.plotting import plot

from utils.latexify import unicode_to_latex_convertor


def get_function(raw_func):
    try:
        func = sympify(raw_func)
    except:
        return
    else:
        return func


def get_data(data):
    axis_data = {}
    axis_data['xx'] = data[0].get_points()[0]
    axis_data['yy'] = data[0].get_points()[1]

    return axis_data


def get_layout(figure, raw_function_string):
    figure.update_layout(
        title='$'+unicode_to_latex_convertor(raw_function_string)+'$',
        width=700,
        height=500,
    )

    return figure


def create_2d_graph(raw_function_string):
    x = symbols('x')
    raw_func = raw_function_string
    func = get_function(raw_func)
    if func:
        data = plot(func, (x, -10, 10), show=False)
        axis_data = get_data(data)

        figure = graph_objs.Figure(
            graph_objs.Scatter(x=axis_data['xx'], y=axis_data['yy']),
        )

        figure = get_layout(figure, raw_function_string)

        return figure
    else:
        return


def update_2d_graph(range_value, raw_function_string):
    x = symbols('x')
    raw_func = raw_function_string
    func = get_function(raw_func)
    if func:
        data = plot(func, (x, range_value[0], range_value[1]), show=False)
        axis_data = get_data(data)

        figure = graph_objs.Figure(
            graph_objs.Scatter(x=axis_data['xx'], y=axis_data['yy']),
        )

        figure = get_layout(figure, raw_function_string)

        return figure
