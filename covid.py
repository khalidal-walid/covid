import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

# Import data 
# df = pd.read_csv("https://raw.githubusercontent.com/khalidal-walid/covid/main/covid-19%20malaysia.csv")
# df2 = pd.read_csv("https://raw.githubusercontent.com/khalidal-walid/covid/main/covid-19%20state.csv")

df = pd.read_csv("/Users/tengku/Project/Covid/covid-19 malaysia.csv")
df2 = pd.read_csv("/Users/tengku/Project/Covid/covid-19 state.csv")

# Creates a list of dictionaries
def get_options(list_state):
    state_list = []
    for i in list_state:
        state_list.append({'label': i, 'value': i})

    return state_list

# Initialise the app
app = dash.Dash(
  __name__,
  meta_tags=[
      {"name": "viewport", "content": "width=device-width, initial-scale=1"}
  ],
  external_stylesheets=[dbc.themes.BOOTSTRAP]
)

# App layout
app.layout = html.Div([
  html.Div([
      html.Br(),
      html.H1('COVID-19 di Malaysia'),
      html.P(f"Tarikh kemaskini: {df['date'].iloc[-1]}")
  ], className= 'title'),

  html.Div([
    html.Div([
        html.H1(children='Jumlah kes keseluruhan'),
        html.H2(f"{df['total cases'].iloc[-1]:,.0f}"),
        html.P(f"Kes baharu: {df['new cases'].iloc[-1]}")
      ], className= 'info'),

    html.Div([
        html.H1(children='Jumlah kes sembuh'),
        html.H2(f"{df['total discharged'].iloc[-1]:,.0f}"),
        html.P(f"Kes sembuh baharu: {df['new discharged'].iloc[-1]}")
    ], className= 'info'),

    html.Div([
        html.H1(children='Jumlah kes kematian'),
        html.H2(f"{df['total death'].iloc[-1]:,.0f}"),
        html.P(f"Kes kematian baharu: {df['new death'].iloc[-1]}")
    ], className= 'info')

  ], className= 'main-info'),

  html.Div([
    html.Div([
      html.H1(children='Statistik semasa'),

      html.P(f"Peratus sudah menerima dos pertama: {df['% 1st dose'].iloc[-1]}"),
      dbc.Progress(value=11.68, max=100, striped=True, color="success", style={"height": "40px", 'margin': '1em'}),

      html.P(f"Peratus sudah menerima dos kedua: {df['% 2nd dose'].iloc[-1]}"),
      # dbc.Progress(children=["0.06%"], value=1, max=100, striped=True, color="success", style={"height": "40px", 'margin': '1em'}), 
      dbc.Progress(value=7.23, max=100, striped=True, color="success", style={"height": "40px", 'margin': '1em'}), 

      html.P(f"Peratus sembuh: {df['% discharged'].iloc[-1]}"),
      dbc.Progress(value=90.63, max=100, striped=True, color="success", style={"height": "40px", 'margin': '1em'}),

      html.P(f"Peratus kematian: {df['% death'].iloc[-1]}"),
      dbc.Progress(value=0.39, max=100, striped=True, color="danger", style={"height": "40px", 'margin': '1em'})      
    ], className= 'graph-1'),

    html.Div([
        html.H1(children='Kes mengikut negeri (Mei 2021)'),
              html.Div(
                className='div-for-dropdown',
                children=[
                  dcc.Dropdown (id='state_selection', 
                  options=get_options(df2['state'].unique()),
                  multi=False, 
                  # style={'background-color': '#1E1E1E'},
                  # value=[df3['date'].sort_values()[0]],
                  value='Johor',
                  className='state_selection'
                  ),
                ], 
              ),
        dcc.Graph(id = 'line-chart')
    ], className= 'graph-2')

  ], className= 'main-graph')
])

# app callback
@app.callback(
  Output('line-chart', 'figure'),
  [Input('state_selection', 'value')]
)

def update_line_chart(state_selection):
  # print(state_selection)

  dff = df2.copy()
  dff = dff[dff["state"] == state_selection]

  figure = px.line(
    data_frame = dff,
    x = 'date',
    y ='total cases'
  )

  figure.update_layout(
    showlegend=False,
    plot_bgcolor= 'rgba(0, 0, 0, 0)',
    paper_bgcolor= '#1B233F',
    xaxis=dict(linecolor='gray'),
    # yaxis=dict(linecolor='gray'),
    font_color='lightgray'
  )

  figure.update_xaxes(title_text='Tarikh',showticklabels=False, showgrid=False, showline=True)
  figure.update_yaxes(title_text='Kes baharu', showticklabels=False, showgrid=False)

  return figure


# Run the App
if __name__ == '__main__':
  # app.run_server(debug=True)
  app.run_server()
