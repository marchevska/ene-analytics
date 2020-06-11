# ENE Analytics app
# Copyright 2020 Olga Marchevska
#
# Dash application for workforce dynamics analysis, split by region, gender, and age

import datetime as dt

import flask
import dash
from dash import Dash, callback_context
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import pandas as pd

from app import app, db


# Functional layout for a Dash app
def serve_dash_app_layout(*args, **kwargs):
    return html.Div([
        dcc.Location(id='url', refresh=False),
        html.H1('Workforce Participation Dynamics In Population Over 15 Years'),

        # A fullscreen spinner is shown when the data is loaded from the database
        # So far, this is the only way to deactive interactive page contents during the long DB query
        dcc.Loading(id="loading", type='circle', fullscreen=True, style={'opacity': 0.5},
                    children=html.Div('', id='loading_div')),
        html.Div('', id='page_data'),
    ])


ene_workforce_app = Dash(__name__, server=app, routes_pathname_prefix='/dash/workforce/',
                         external_stylesheets=[])
ene_workforce_app.layout = serve_dash_app_layout
ene_workforce_app.config['suppress_callback_exceptions'] = True


# -------------------------------------------------------------------------------------
# Load page data
# -------------------------------------------------------------------------------------

def calc_quarter(row):
    return f'''Q{pd.Timestamp(dt.date(int(row['year']), int(row['month']), 1)).quarter} {int(row['year'])}'''


def get_quarters():
    src_data = pd.read_csv('data/csv/agg_by_gender_age_month_region.zip')
    src_data['quarter'] = src_data.apply(calc_quarter, axis=1)
    return src_data['quarter'].unique()


def get_age_str(min_age, max_age):
    if min_age == 12:
        return '70+'
    elif max_age == 12:
        return f'''{10 + min_age * 5}-70+'''
    else:
        return f'''{10 + min_age * 5}-{15 + max_age * 5}'''


def generate_workforce_chart_figure(region_list=[0], age_range=[1, 12], date_range=None):
    src_data = pd.read_csv('data/csv/agg_by_gender_age_month_region.zip').reset_index()

    if region_list != [0]:
        src_data = src_data[src_data.region.isin(region_list)]
    src_data = src_data[(age_range[0] <= src_data.tramo_edad) & (src_data.tramo_edad <= age_range[1])]

    regions = dict(pd.read_csv('data/csv/regions.csv', index_col='id', squeeze=True))
    region_name = regions[str(region_list).replace(' ', '')]
    age_str = get_age_str(age_range[0], age_range[1])

    # Quarterly aggregate data
    src_data['quarter'] = src_data.apply(calc_quarter, axis=1)
    q_data = src_data[['total', 'male', 'female', 'is_workforce',
       'male_workforce', 'female_workforce', 'quarter']].groupby('quarter').sum().merge(
        src_data[['index', 'quarter']].groupby('quarter').mean(), left_index=True, right_index=True).sort_values(
        by='index').reset_index()
    q_data['perc_workforce'] = 1.0 * q_data.is_workforce/q_data.total
    q_data['perc_workforce_m'] = 1.0 * q_data.male_workforce/q_data.male
    q_data['perc_workforce_f'] = 1.0 * q_data.female_workforce/q_data.female

    if date_range is None:
        date_range = [0, len(q_data) - 1]
    return {
        'data': [
            {'x': q_data.quarter.iloc[date_range[0]:date_range[1] + 1],
                'y': q_data.perc_workforce.iloc[date_range[0]:date_range[1] + 1],
                'mode': 'lines', 'name': 'all population'},
            {'x': q_data.quarter.iloc[date_range[0]:date_range[1] + 1],
                'y': q_data.perc_workforce_m.iloc[date_range[0]:date_range[1] + 1],
                'mode': 'lines', 'name': 'male'},
            {'x': q_data.quarter.iloc[date_range[0]:date_range[1] + 1],
                'y': q_data.perc_workforce_f.iloc[date_range[0]:date_range[1] + 1],
                'mode': 'lines', 'name': 'female'},
        ],
        'layout': {'title': f'''Region: {region_name}, age: {age_str}''',
                   'yaxis': {'tickformat': ',.0%', 'range': [0, 1]},
                   }
    }


@ene_workforce_app.callback(
    [Output('loading_div', 'children'), Output('page_data', 'children')],
    [Input('url', 'pathname')],
    []
)
def display_page(*args, **kwargs):
    ctx = callback_context
    if ctx.inputs['url.pathname'] is None:
        raise dash.exceptions.PreventUpdate

    # Workforce participation percentage, dynamics
    regions = dict(pd.read_csv('data/csv/regions.csv', index_col='id', squeeze=True))
    quarters = get_quarters()

    page_data_div = html.Div([
        html.Div(
            dcc.Graph(
                id='workforce_dynamics',
                # figure=generate_workforce_chart_figure(src_data),
                figure=generate_workforce_chart_figure(),
                style={'width': '800px', 'height': '400px'}
            ),
            style={'width': '100%', 'align-items': 'center', 'justify-content': 'center', 'display': 'flex'}
        ),

        html.Div(
            html.Div(
                dcc.RangeSlider(
                    id='workforce_date_range',
                    min=0,
                    max=len(quarters) - 1,
                    step=1,
                    value=[0, len(quarters) - 1],
                    marks={i: {'label': quarters[i], 'style': {'width': '30px'}}
                           for i in set(range(0, len(quarters), 4)) | {len(quarters) - 1}},
                ),
                style={'width': '600px', 'height': '100px'}
            ),
            style={'width': '100%', 'align-items': 'center', 'justify-content': 'center', 'display': 'flex'}
        ),

        dcc.Dropdown(id='region_select',
                     options=[{'label': value, 'value': key} for key, value in regions.items()],
                     value='[0]',
                     style={'width': '300px'}
        ),

        html.Div(
            html.Div(
                dcc.RangeSlider(
                    id='age_range',
                    min=1,
                    max=12,
                    step=1,
                    value=[1, 12],
                    marks={i: get_age_str(i, i) for i in range(1, 13)},
                ),
                style={'width': '600px', 'height': '100px'}
            ),
            style={'width': '100%', 'align-items': 'center', 'justify-content': 'center', 'display': 'flex'}
        ),

    ])

    return '', page_data_div


@ene_workforce_app.callback(
    Output('workforce_dynamics', 'figure'),
    [Input('region_select', 'value'), Input('age_range', 'value'), Input('workforce_date_range', 'value')],
    [State('region_select', 'value'), State('age_range', 'value'), State('workforce_date_range', 'value')]

)
def update_workforce_chart(*args, **kwargs):
    ctx = callback_context
    if len(ctx.triggered) != 1:
        raise dash.exceptions.PreventUpdate

    regions = eval(ctx.states['region_select.value'])
    ages = ctx.states['age_range.value']
    date_range = ctx.inputs['workforce_date_range.value']

    return generate_workforce_chart_figure(regions, ages, date_range)
