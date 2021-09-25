from plotly import graph_objs
from sympy import symbols, sympify
from sympy.plotting import plot3d

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
    axis_data['xx'] = data[0].get_meshes()[0]
    axis_data['yy'] = data[0].get_meshes()[1][:, 0]
    axis_data['zz'] = data[0].get_meshes()[2]

    return axis_data


def get_layout(figure, raw_function_string):
    figure.update_layout(
        title='$' + unicode_to_latex_convertor(raw_function_string) + '$',
        width=700,
        height=500,
    )

    return figure


def create_3d_graph(raw_function_string):
    x, y = symbols('x y')
    raw_func = raw_function_string
    try:
        func = sympify(raw_func)
    except:
        return
    else:
        data = plot3d(func, (x, -5, 5), (y, -5, 5), show=False)
        axis_data = get_data(data)

        figure = graph_objs.Figure(
            graph_objs.Surface(x=axis_data['xx'], y=axis_data['yy'], z=axis_data['zz'])
        )

        figure = get_layout(figure, raw_function_string)

        return figure


def update_3d_graph(range_value_x, range_value_y, raw_function_string):
    x, y = symbols('x y')
    raw_func = raw_function_string
    try:
        func = sympify(raw_func)
    except:
        return
    else:
        data = plot3d(func, (x, range_value_x[0], range_value_x[1]), (y, range_value_y[0], range_value_y[1]),
                      show=False)
        axis_data = get_data(data)

        figure = graph_objs.Figure(
            graph_objs.Surface(x=axis_data['xx'], y=axis_data['yy'], z=axis_data['zz'])
        )

        figure = get_layout(figure, raw_function_string)

        return figure
