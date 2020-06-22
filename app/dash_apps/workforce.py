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
        html.H1('Workforce Participation in Chile',
                style={'textAlign': 'center'}),

        # A fullscreen spinner is shown when the data is loaded from the database
        # So far, this is the only way to deactive interactive page contents during the long DB query
        dcc.Loading(id="loading", type='circle', fullscreen=True, style={'opacity': 0.5},
                    children=[html.Div('', id='loading_div'), html.Div('', id='loading_div1')]),
        html.Div('', id='page_data'),
    ])


ene_workforce_app = Dash(__name__, server=app, routes_pathname_prefix='/dash/workforce/',
                         external_stylesheets=['/static/css/dash_style.css'])
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

    # Monthly aggregate data
    month_data = src_data.drop(['region', 'tramo_edad'], axis='columns').groupby(
        ['year', 'month']).sum().reset_index()
    month_data['perc_workforce'] = 1.0 * month_data.is_workforce/month_data.total
    month_data['perc_workforce_m'] = 1.0 * month_data.male_workforce/month_data.male
    month_data['perc_workforce_f'] = 1.0 * month_data.female_workforce/month_data.female

    # Quarterly aggregate data
    month_data['quarter'] = month_data.apply(calc_quarter, axis=1)
    q_data = month_data.drop(['year', 'month'], axis='columns').groupby('quarter').mean().sort_values(
        by='index').reset_index()

    if date_range is None:
        date_range = [0, len(q_data) - 1]
    temp = q_data.iloc[date_range[0]:date_range[1] + 1]

    # Chart formatting
    regions = dict(pd.read_csv('data/csv/regions.csv', index_col='id', squeeze=True))
    region_name = regions[str(region_list).replace(' ', '')]
    age_str = get_age_str(age_range[0], age_range[1])

    chart_mode = 'lines' if len(temp) > 10 else 'lines+markers'
    x_range = [-1, len(temp)] if len(temp) > 10 else [-0.1*len(temp), len(temp) - 1 + 0.1*len(temp)]

    return {
        'data': [
            {'x': temp.quarter, 'y': temp.perc_workforce, 'mode': chart_mode, 'name': 'all population',
             'line': {'color': 'rgb(153, 0, 102)', 'width': 4}, 'legendgroup': 'group'},
            {'x': temp.quarter, 'y': temp.perc_workforce_m, 'mode': chart_mode, 'name': 'male',
             'line': {'color': 'rgb(0, 153, 153)', 'width': 3}, 'legendgroup': 'group1'},
            {'x': temp.quarter, 'y': temp.perc_workforce_f, 'mode': chart_mode, 'name': 'female',
             'line': {'color': 'rgb(255, 153, 0)', 'width': 3}, 'legendgroup': 'group2'},
            {'x': temp.quarter, 'y': [temp.perc_workforce.mean()] * len(temp), 'mode': 'lines',
             'line': {'color': 'rgba(153, 153, 153, 0.5)', 'width': 2, 'dash': 'dot'},
             'name': 'average', 'legendgroup': 'group3'},
            {'x': temp.quarter, 'y': [temp.perc_workforce_m.mean()] * len(temp), 'mode': 'lines',
             'line': {'color': 'rgba(153, 153, 153, 0.5)', 'width': 2, 'dash': 'dot'},
             'name': 'average', 'legendgroup': 'group3', 'showlegend': False},
            {'x': temp.quarter, 'y': [temp.perc_workforce_f.mean()] * len(temp), 'mode': 'lines',
             'line': {'color': 'rgba(153, 153, 153, 0.5)', 'width': 2, 'dash': 'dot'},
             'name': 'average', 'legendgroup': 'group3', 'showlegend': False},
        ],
        'layout': {'title': {'text': f'''Region: {region_name}, age: {age_str}'''},
                   'xaxis': {'showgrid': False, 'range': x_range},
                   'yaxis': {'tickformat': ',.0%', 'range': [-0.02, 1.005]},
                   'legend': {'x': 1.01, 'y': 0.5, 'orientation': 'v'},
                   'margin': {'t': 80}
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
        html.Table([
            html.Tr([
                html.Td(
                    [
                        html.P('Workforce participation is the percentage of the population of working age '
                        '(older than 15 years in Chile) who either have an employment or temporarily '
                        'are unemployed.'),
                        html.P('In general, women participation was growing during period 2010-2020, especially '
                               'in its first half, but the gap between male and female job activity still remains '
                               'in the majority of age ranges and geografies.'),
                    ],
                    style={'width': '300px'}),
                html.Td(
                    dcc.Graph(
                        id='workforce_dynamics',
                        figure=generate_workforce_chart_figure(),
                        style={'width': '800px', 'height': '430px'}
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
                                 style={'width': '300px'}
                                 ),
                    className='input',
                ),
                ],
                style={'height': '80px'}
            ),
            html.Tr([
                html.Td('Age range:', className='label'),
                html.Td(
                    html.Div(
                        dcc.RangeSlider(
                            id='age_range',
                            min=1,
                            max=12,
                            step=1,
                            value=[1, 12],
                            marks={i: get_age_str(i, i) for i in range(1, 13)},
                        ),
                        style={'width': '600px', 'height': '60px', 'marginLeft': '10px'}
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
                            id='workforce_date_range',
                            min=0,
                            max=len(quarters) - 1,
                            step=1,
                            value=[0, len(quarters) - 1],
                            marks={i: {'label': quarters[i], 'style': {'width': '30px'}}
                                   for i in set(range(0, len(quarters), 4)) | {len(quarters) - 1}},
                        ),
                        style={'width': '600px', 'height': '60px', 'marginLeft': '10px'}
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


@ene_workforce_app.callback(
    [Output('loading_div1', 'children'), Output('workforce_dynamics', 'figure')],
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

    return '', generate_workforce_chart_figure(regions, ages, date_range)
