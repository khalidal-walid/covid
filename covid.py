import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

# Import data 
df = pd.read_csv("https://raw.githubusercontent.com/ynshung/covid-19-malaysia/master/covid-19-malaysia.csv")
df2 = pd.read_csv("https://raw.githubusercontent.com/ynshung/covid-19-malaysia/master/covid-19-my-states-cases.csv")
df3 = pd.read_csv("https://raw.githubusercontent.com/ynshung/covid-19-malaysia/master/covid-19-my-states-cases.csv")

# Creates a list of dictionaries
def get_options(list_player):
    player_list = []
    for i in list_player:
        player_list.append({'label': i, 'value': i})

    return player_list

# Initialise the app
app = dash.Dash(__name__)

# App layout
df3.transpose()
print(df3)
app.layout = html.Div([
  html.Div([
      html.Br(),
      html.H1('COVID-19 in Malaysia'),
      html.P(f"Last updated: {df2['date'].iloc[-1]}")
  ], className= 'title'),

  html.Div([
    html.Div([
        html.H1(children='Confirmed cases'),
        html.P(f"{df['cases'].iloc[-1]:,.0f}")
      ], className= 'info'),

    html.Div([
        html.H1(children='Discharged'),
        html.P(f"{df['discharged'].iloc[-1]:,.0f}")
    ], className= 'info'),

    html.Div([
        html.H1(children='Number of death'),
        html.P(f"{df['death'].iloc[-1]:,.0f}")
    ], className= 'info')

  ], className= 'main-info'),

  html.Div([
    html.Div([
      html.H1(children='Stats by state'),
      html.Div(
        className='div-for-dropdown',
                              children=[
                         dcc.Dropdown(id='player_selection', 
                                      # options=get_options(df3['date'].unique()),
                                      multi=False, 
                                      # value=[df2['date'].sort_values()[0]],
                                      style={'backgroundColor': '#1E1E1E'},
                                      className='player_selection'
                                      ),
                                ],
          # children=[
          #   dcc.Dropdown(id='state_selection', 
          #                 options = [
          #                   # {'label': 'R. Lewandowski', 'value': 'R. Lewandowski'},
          #                   {'label': 'Perlis', 'value': 'perlis'},
          #                   {'label': 'Kedah', 'value': 'kedah'},
          #                   {'label': 'Pulau Pinang', 'value': 'pulau-pinang'}],
          #                   multi=False, 
          #                   placeholder='Select state'
          #                   # value = 'R. Lewandowski',
          #   ),
          # ],
      ),
      # html.P(f"{df2['date'].iloc[-1]}")
      # html.P(f"{df2.loc[:-1, 'pulau-pinang']}")
    ], className= 'graph-1'),

    html.Div([
        html.H1(children='New Cases'),
        dcc.Graph(id = 'chart', figure = {})
    ], className= 'graph-2')

  ], className= 'main-graph')
])


# Run the App
if __name__ == '__main__':
  app.run_server(debug=True)
