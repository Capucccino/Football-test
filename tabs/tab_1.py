from dash import dash_table
from main import *


tab_1_layout = html.Div([
    html.H1('Football test'),
    html.Div([
        html.Button('Ajouter un joueur', id='editing-rows-button', n_clicks=0),
        html.Button('Melanger les données',
                    id='shuffle-data-button', n_clicks=0),
        dcc.Dropdown(
            id="classify-players",
            options=[
                {'label': 'Nombre de but par minutes jouées', 'value': '1'},
                {'label': 'Home du match par apparitions', 'value': '2'},
            ],
            placeholder='Classer les joueurs selon:',
    )
    ], style={'display': 'inline-block', 'margin': '10px','margin-left':'20px','margin-top': '10px', 'wdith': '50%'}),

    html.Div([
        dash_table.DataTable(
            id='table',
            data=df.to_dict('records'),
            columns=[{"name": 'Joueur', "id": 'Joueur', "type": 'text'}] +
            [{"name": i, "id": i, "type": 'numeric'} for i in df.columns[1:]],
            fixed_rows={'headers': True},
            style_table={'height': 200},
            style_cell={'textAlign': 'left'},
            style_cell_conditional=[
                {'if': {'column_id': 'Joueur'},
                 'width': '200px'}],
            row_deletable=True,
            editable=True,
            filter_action="native")
    ],style={'margin-left':'20px'}),


    html.Div([
        html.Button('Creer deux équipes', id='two-teams-button', n_clicks=0),
    ],style={'display': 'inline-block', 'margin-left':'20px','margin-top': '20px', 'wdith': '30%'}),


    html.Div([
        dash_table.DataTable(
            id='teams-table',
            data=[],
            fixed_rows={'headers': True},
            style_table={'height': 150},
            style_cell={'textAlign': 'left', 'width': '100px'},
        ),
    ], style={'display': 'block', 'margin-left':'20px','margin-top': '20px', 'wdith': '10%'}),
    
    html.Div(id='output-state',style={'margin-left':'20px','margin-top':'10px'},)

])