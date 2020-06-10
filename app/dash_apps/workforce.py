# ENE Analytics app
# Copyright 2020 Olga Marchevska
#
# Dash application for workforce analysis

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
        html.H1('Workforce'),

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


@ene_workforce_app.callback(
    [Output('loading_div', 'children'), Output('page_data', 'children')],
    [Input('url', 'pathname')],
    []
)
def display_page(*args, **kwargs):
    ctx = callback_context
    if ctx.inputs['url.pathname'] is None:
        raise dash.exceptions.PreventUpdate

    # Read data from DB
    con = db.connect()

    # Workforce participation percentage, dynamics
    stmt = '''
        select ano_trimestre as "year", 
            mes_central as "month", 
            count(*) as "total", 
            sum(case when activ is null then 1 else 0 end) as "under_15", 
            sum(case when activ is not null then 1 else 0 end) as "over_15", 
            sum(case when activ is not null and sexo = 1 then 1 else 0 end) as "male_over_15", 
            sum(case when activ is not null and sexo = 2 then 1 else 0 end) as "female_over_15", 
            sum(case when activ=1 then 1 else 0 end) as "employed", 
            sum(case when activ=2 then 1 else 0 end) as "unemployed", 
            sum(case when activ in (1, 2) then 1 else 0 end) as "is_workforce",
            sum(case when activ in (1, 2) and sexo = 1 then 1 else 0 end) as "male_workforce",
            sum(case when activ in (1, 2) and sexo = 2 then 1 else 0 end) as "female_workforce",
            sum(case when activ=3 then 1 else 0 end) as "not_workforce"
        from ene 
        group by ano_trimestre, mes_central
    '''
    src_data = pd.read_sql_query(stmt, con).reset_index()
    src_data['quarter'] = src_data.apply(calc_quarter, axis=1)
    src_data['perc_workforce'] = 1.0 * src_data.is_workforce/src_data.over_15
    src_data['perc_workforce_m'] = 1.0 * src_data.male_workforce/src_data.male_over_15
    src_data['perc_workforce_f'] = 1.0 * src_data.female_workforce/src_data.female_over_15
    src_data['perc_gender_m'] = 1.0 * src_data.male_workforce/(src_data.male_workforce + src_data.female_workforce)
    src_data['perc_gender_f'] = 1.0 * src_data.female_workforce/(src_data.male_workforce + src_data.female_workforce)

    q_data = src_data[['quarter', 'index', 'perc_workforce', 'perc_workforce_m', 'perc_workforce_f',
                       'perc_gender_m', 'perc_gender_f']].groupby(
        'quarter').mean().reset_index().sort_values(by='index')

    # Workforce participation percentage by region
    stmt = '''
        select ene_agg.*, ene_region_15.region_15_name as "region_name"
        from  
            (select ano_trimestre as "year", 
                mes_central as "month",
                region_15 as "region", 
                count(*) as "total", 
                sum(case when activ is null then 1 else 0 end) as "under_15", 
                sum(case when activ is not null then 1 else 0 end) as "over_15", 
                sum(case when activ is not null and sexo = 1 then 1 else 0 end) as "male_over_15", 
                sum(case when activ is not null and sexo = 2 then 1 else 0 end) as "female_over_15", 
                sum(case when activ=1 then 1 else 0 end) as "employed", 
                sum(case when activ=2 then 1 else 0 end) as "unemployed", 
                sum(case when activ in (1, 2) then 1 else 0 end) as "is_workforce",
                sum(case when activ in (1, 2) and sexo = 1 then 1 else 0 end) as "male_workforce",
                sum(case when activ in (1, 2) and sexo = 2 then 1 else 0 end) as "female_workforce",
                sum(case when activ=3 then 1 else 0 end) as "not_workforce"
            from ene 
            group by ano_trimestre, mes_central, region_15) as ene_agg
        left join ene_region_15 on ene_agg.region = ene_region_15.id
    '''
    src_data_region = pd.read_sql_query(stmt, con).reset_index()

    src_data_region['quarter'] = src_data_region.apply(calc_quarter, axis=1)
    src_data_region['perc_workforce'] = 1.0 * src_data_region.is_workforce/src_data_region.over_15
    src_data_region['perc_workforce_m'] = 1.0 * src_data_region.male_workforce/src_data_region.male_over_15
    src_data_region['perc_workforce_f'] = 1.0 * src_data_region.female_workforce/src_data_region.female_over_15

    q_data_region = src_data_region[['quarter', 'index', 'region', 'perc_workforce', 'perc_workforce_m',
                              'perc_workforce_f']].groupby(['quarter', 'region']).mean().\
        reset_index().sort_values(by='index')

    q_data_region_avg = src_data_region[['region_name', 'perc_workforce', 'perc_workforce_m', 'perc_workforce_f']].groupby(
        'region_name').mean().reset_index().sort_values(by='perc_workforce', ascending=False)

    page_data_div = html.Div([
        html.Div(id='src_data', children=str(src_data), hidden=True),

        html.Table([
            html.Tr([
                html.Td(
                    dcc.Graph(
                        figure={
                            'data': [
                                {'x': q_data.quarter, 'y': q_data.perc_workforce, 'mode': 'lines', 'name': 'total'},
                                {'x': q_data.quarter, 'y': q_data.perc_workforce_m, 'mode': 'lines', 'name': 'male'},
                                {'x': q_data.quarter, 'y': q_data.perc_workforce_f, 'mode': 'lines', 'name': 'female'},
                            ],
                            'layout': {'title': 'Workforce participation in population over 15 years',
                                       'yaxis': {'tickformat': ',.0%', 'range': [0, 1.02]},
                                       },
                        },
                        style={'width': '500px', 'height': '400px'}
                    ),
                ),
                html.Td(
                    dcc.Graph(
                        figure={
                            'data': [
                                {'x': q_data.quarter, 'y': q_data.perc_gender_m, 'mode': 'lines', 'name': 'male'},
                                {'x': q_data.quarter, 'y': q_data.perc_gender_f, 'mode': 'lines', 'name': 'female'},
                            ],
                            'layout': {'title': 'Gender shares in workforce',
                                       'yaxis': {'tickformat': ',.0%', 'range': [0, 1.02]},
                                       },
                        },
                        style={'width': '500px', 'height': '400px'}
                    ),
                ),
            ]),
            html.Tr([
                html.Td(
                    dcc.Graph(
                        figure={
                            'data': [
                                {'x': q_data_region[q_data_region.region == reg].quarter,
                                 'y': q_data_region[q_data_region.region == reg].perc_workforce,
                                 'mode': 'lines', 'name': f'''{reg}'''} for reg in q_data_region.region.unique()
                            ],
                            'layout': {'title': 'Workforce participation in population over 15 years',
                                       'yaxis': {'tickformat': ',.0%', 'range': [0, 1.02]},
                                       },
                        },
                        style={'width': '500px', 'height': '400px'}
                    ),
                ),
                html.Td(
                    dcc.Graph(
                        figure={
                            'data': [
                                go.Bar(y=q_data_region_avg.region_name, x=q_data_region_avg.perc_workforce,
                                       orientation='h', name='all population'),
                                go.Bar(y=q_data_region_avg.region_name, x=q_data_region_avg.perc_workforce_m,
                                       orientation='h', name='male'),
                                go.Bar(y=q_data_region_avg.region_name, x=q_data_region_avg.perc_workforce_f,
                                       orientation='h', name='female'),
                            ],
                            'layout': {'title': 'Average participation by region',
                                       'xaxis': {'tickformat': ',.0%', 'range': [0, 1.02]},
                                       # 'yaxis': {'range': [0, 16]},
                                       },
                        },
                        style={'width': '500px', 'height': '600px'}
                    ),

                ),
            ]),
        ]),

    ])

    return '', page_data_div
