import pandas as pd
import dash
from dash.dependencies import Input, Output, State
from dash import dcc
from dash import html
import random
from tabs import tab_1
import copy


df = pd.read_excel("data/Liste joueurs de foot.xlsx", skipfooter=2)
df.drop(labels='Unnamed: 1', axis=1, inplace=True)

columns_table =  [{"name": 'Joueur', "id": 'Joueur', "type":'text'}] + [{"name": i, "id": i, "type":'numeric'} for i in df.columns[1:]],

app = dash.Dash(__name__)
app.config['suppress_callback_exceptions'] = True

# Initial layout
app.layout = html.Div([
    dcc.Tabs(id="main-tab"),
    html.Div(id='tabs-content')
])


@app.callback(Output('tabs-content', 'children'),
              [Input('main-tab', 'value')])
def render_content(tab):
    """
    Main callback
    """
    return tab_1.tab_1_layout


@app.callback(
    Output('table', 'data'),
    Input('editing-rows-button', 'n_clicks'),
    Input('shuffle-data-button', 'n_clicks'),
    Input('classify-players','value'),
    State('table', 'data'),
    State('table', 'columns'))
def add_row(bt1, bt2, classify, rows, columns):
    """
    Callbacks of the main data_table
    """
    ctx = dash.callback_context

    if not ctx.triggered:
        button_id = 'No clicks yet'
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    # Adding new empty row to datatable
    if button_id == 'editing-rows-button':
        rows.insert(0,{c['id']: '' for c in columns})

    # Shuffle all values of datatable
    if button_id == 'shuffle-data-button':
        temp = copy.deepcopy(rows)
        for i in list(rows[0].keys()):
            numbers = [i for i in range(len(rows))]
            random_numbers = random.sample(numbers, len(numbers))
            for j in range(len(rows)):
                rows[j][i] = temp[random_numbers[j]][i]
    
    # Classify datatable depending on chosen classification
    if classify:
        temp = copy.deepcopy(rows)
        for i in range(len(rows)):
            if classify == '1':
                if rows[i]['Mins'] == '' or rows[i]['Buts'] == ''  : temp[i]['Classement'] = -1
                else: temp[i]['Classement'] = int(rows[i]['Buts']) / int(rows[i]['Mins'])
            if classify == '2':
                if rows[i]['Apps'] == '' or rows[i]['HdM'] == '': temp[i]['Classement'] = -1
                else: temp[i]['Classement'] = int(rows[i]['HdM']) / int(rows[i]['Apps'])
        classify_table = sorted(temp, key = lambda i: i['Classement'],reverse=True)
        return classify_table
    return rows


@app.callback(
    Output('teams-table', 'data'),
    Output('teams-table', 'columns'),
    Output('output-state', 'children'),
    Input('two-teams-button', 'n_clicks'),
    State('table', 'data'),
    State('table', 'columns'))
def create_teams(button,rows,columns):
    """
    Callback of the second data table regarding the two teams of 11 players
    """
    temp = copy.deepcopy(rows)
    if button > 0:
        # Adding players in case there are some missing
        while len(temp) < 22:
            temp.append({'Joueur': 'Random', 'Apps': None, 'Mins': None, 'Buts': None, 'P.Décisives': None, 'Jau': None, 'Rou': None, 'TpM': None, 'PR%': None, 'AériensGagnés': None, 'HdM': None, 'Classement': None})
        random.shuffle(temp)
        team1, team2 = temp[:11],temp[11:22]
        score1, score2 = 0,0
        team_table=[]

        # Evaluate the winning team according to the total number of goals scored by the players of a team
        for i in range(len(team1)):
            if isinstance(team1[i]['Buts'],int):
                score1 += team1[i]['Buts']
            if isinstance(team2[i]['Buts'],int):
                score2 += team2[i]['Buts']
            team_table.append({'Team1':team1[i]['Joueur'],'Team2':team2[i]['Joueur']})

        if score1 > score2:
            winner = u''' Le FC Barcelone a plus de chances de gagner le match en comparaison des buts inscrits par joueur par équipe'''
        elif score1 < score2:
            winner = u'''Le Real Madrid a plus de chances de gagner le match en comparaison des buts inscrits par joueur par équipe'''
        else:
            winner = u'''Egalité'''


        return team_table, [{"id": 'Team1', "name": "FC Barcelone"},{"id": 'Team2', "name": "Real Madrid"}], winner
    return None, None, None


if __name__ == '__main__':
    app.run_server(debug=True)