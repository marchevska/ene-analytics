# ENE Analytics app
# Copyright 2020 Olga Marchevska
#
# Dash application to compare unemployment by age groups: 1 - clusters with dynamics, 2 - box charts for all age ranges

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
        html.H1('Unemployment Rate By Age',
                style={'textAlign': 'center'}),

        # A fullscreen spinner is shown when the data is loaded from the database
        # So far, this is the only way to deactive interactive page contents during the long DB query
        dcc.Loading(id="loading", type='circle', fullscreen=True, style={'opacity': 0.5},
                    children=[html.Div('', id='loading_div'), html.Div('', id='loading_div1')]),
        html.Div('', id='page_data'),
    ])


ene_unemployment_app = Dash(__name__, server=app, routes_pathname_prefix='/dash/unemployment_by_age/',
                         external_stylesheets=['/static/css/dash_style.css'])
ene_unemployment_app.layout = serve_dash_app_layout
ene_unemployment_app.config['suppress_callback_exceptions'] = True


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


def generate_unemployment_by_age_chart_figure(region_list=[0], gender=0, date_range=None):
    src_data = pd.read_csv('data/csv/agg_by_gender_age_month_region.zip').reset_index()
    age_ranges = dict(pd.read_csv('data/csv/age_ranges.csv', index_col='range', squeeze=True))

    if region_list != [0]:
        src_data = src_data[src_data.region.isin(region_list)]

    # Monthly aggregate data
    month_data = pd.DataFrame()
    for range, label in age_ranges.items():
        temp = src_data[src_data.tramo_edad.isin(eval(range))].drop(['region', 'tramo_edad'], axis='columns').groupby(
            ['year', 'month']).sum()
        if gender == 0:
            month_data[label] = 1.0 * (temp.male_unemployed + temp.female_unemployed)/temp.is_workforce
        elif gender == 1:
            month_data[label] = 1.0 * temp.male_unemployed/temp.male_workforce
        else:
            month_data[label] = 1.0 * temp.female_unemployed/temp.female_workforce
    month_data = month_data.reset_index()

    # Quarterly aggregate data
    month_data['quarter'] = month_data.apply(calc_quarter, axis=1)
    q_data = month_data.reset_index().drop(['year', 'month'], axis='columns').groupby('quarter').mean().sort_values(
        by='index').reset_index()

    if date_range is None:
        date_range = [0, len(q_data) - 1]
    temp = q_data.iloc[date_range[0]:date_range[1] + 1]

    # Chart formatting
    regions = dict(pd.read_csv('data/csv/regions.csv', index_col='id', squeeze=True))
    region_name = regions[str(region_list).replace(' ', '')]
    gender_str = {0: 'all population', 1: 'male', 2: 'female'}[gender]

    chart_mode = 'lines' if len(temp) > 10 else 'lines+markers'
    x_range = [-1, len(temp)] if len(temp) > 10 else [-0.1*len(temp), len(temp) - 1 + 0.1*len(temp)]
    max_unemployment_rate = max([temp[label].max() for label in age_ranges.values()])
    y_range = [-0.02 * max_unemployment_rate, 1.1 * max_unemployment_rate]

    return {
        'data': [
            {'x': temp.quarter, 'y': temp[label], 'mode': chart_mode, 'name': label,
             'line': {'width': 3}} for label in age_ranges.values()
        ],
        'layout': {'title': {'text': f'''Unemployment rate for {gender_str}, {region_name}'''},
                   'xaxis': {'showgrid': False, 'range': x_range},
                   'yaxis': {'tickformat': ',.0%', 'range': y_range},
                   'legend': {'x': 1.01, 'y': 0.5, 'orientation': 'v'},
                   'margin': {'t': 80}
                   }
    }


@ene_unemployment_app.callback(
    [Output('loading_div', 'children'), Output('page_data', 'children')],
    [Input('url', 'pathname')],
    []
)
def display_page(*args, **kwargs):
    ctx = callback_context
    if ctx.inputs['url.pathname'] is None:
        raise dash.exceptions.PreventUpdate

    # Unemployment rate, dynamics
    regions = dict(pd.read_csv('data/csv/regions.csv', index_col='id', squeeze=True))
    quarters = get_quarters()

    page_data_div = html.Div([
        html.Table([
            html.Tr([
                html.Td(
                    [
                        html.P('Unemployment rate is defined as a percentage of workforce who are currently '
                               'unemployed.'),
                        html.P('Unemployment rate is the highest for the age group 15-24 years, and is dropping '
                               'with the age. For age group 60+ years, unemployment rate is lowest, which is '
                               'partially due to leaving the workforce'),
                    ],
                    style={'width': '300px'}),
                html.Td(
                    dcc.Graph(
                        id='unemployment_dynamics',
                        figure=generate_unemployment_by_age_chart_figure(),
                        style={'width': '800px', 'height': '430px'},
                        ),
                    style={'width': '800px'}
                ),
            ]),
            html.Tr([
                html.Td('Region or zone:', className='label'),
                html.Td(
                    dcc.Dropdown(id='region_select',
                                 options=[{'label': value, 'value': key} for key, value in regions.items()],
                                 value='[0]',
                                 style={'width': '300px'},
                                 ),
                    className='input',
                ),
                ],
                style={'height': '80px'}
            ),
            html.Tr([
                html.Td('Gender:', className='label'),
                html.Td(
                    html.Div(
                        dcc.RadioItems(
                            id='gender_select',
                            options=[
                                {'label': 'All population', 'value': 0},
                                {'label': 'Male', 'value': 1},
                                {'label': 'Female', 'value': 2},
                            ],
                            value=0,
                            labelStyle={'marginRight': '10px'},
                        ),
                        style={'width': '600px', 'height': '60px'},
                    ),
                    className='input',
                ),
                ],
                style={'height': '60px'}
            ),
            html.Tr([
                html.Td('Time period:', className='label'),
                html.Td(
                    html.Div(
                        dcc.RangeSlider(
                            id='unemployment_date_range',
                            min=0,
                            max=len(quarters) - 1,
                            step=1,
                            value=[0, len(quarters) - 1],
                            marks={i: {'label': quarters[i], 'style': {'width': '30px'}}
                                   for i in set(range(0, len(quarters), 4)) | {len(quarters) - 1}},
                        ),
                        style={'width': '600px', 'height': '60px', 'marginLeft': '20px'}
                    ),
                    className='input',
                ),
                ],
                style={'height': '60px'}
            ),
        ]),
    ],
    )

    return '', page_data_div


@ene_unemployment_app.callback(
    [Output('loading_div1', 'children'), Output('unemployment_dynamics', 'figure')],
    [Input('region_select', 'value'), Input('gender_select', 'value'), Input('unemployment_date_range', 'value')]

)
def update_unemployment_chart(*args, **kwargs):
    ctx = callback_context
    if len(ctx.triggered) != 1:
        raise dash.exceptions.PreventUpdate

    regions = eval(ctx.inputs['region_select.value'])
    gender = ctx.inputs['gender_select.value']
    date_range = ctx.inputs['unemployment_date_range.value']

    return '', generate_unemployment_by_age_chart_figure(regions, gender, date_range)
