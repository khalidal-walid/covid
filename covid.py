import datetime
import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

# Import data 
df = pd.read_csv("https://raw.githubusercontent.com/MoH-Malaysia/covid19-public/main/epidemic/cases_malaysia.csv")
df2 = pd.read_csv("https://raw.githubusercontent.com/MoH-Malaysia/covid19-public/main/epidemic/cases_state.csv")
df3 = pd.read_csv("https://raw.githubusercontent.com/MoH-Malaysia/covid19-public/main/epidemic/deaths_malaysia.csv")
df4 = pd.read_csv("https://raw.githubusercontent.com/MoH-Malaysia/covid19-public/main/epidemic/hospital.csv")
df5 = pd.read_csv("https://raw.githubusercontent.com/MoH-Malaysia/covid19-public/main/epidemic/tests_malaysia.csv")

# Creates a list of dictionaries
def get_options(list_state):
    state_list = []
    for i in list_state:
        state_list.append({'label': i, 'value': i})

    return state_list


# percentage calculation
death_percentage = df3['deaths_new'].sum(axis=0) / df['cases_new'].sum(axis=0) * 100

discharge_percentage = df4['discharged_total'].sum(axis=0) / df['cases_new'].sum(axis=0) * 100

rtk_percentage = df['cases_new'].iloc[-1] / df5['rtk-ag'].iloc[-1] * 100

pcr_percentage = df['cases_new'].iloc[-1] / df5['pcr'].iloc[-1] * 100


# format date
df['date'] = pd.to_datetime(df['date']).dt.strftime('%d %b %Y')


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
        html.H1(children='Kes baharu'),
        html.H2(f"{df['cases_new'].iloc[-1]}"),
        html.P(f"Jumlah kes: {df['cases_new'].sum(axis=0)}")
      ], className= 'info'),

    html.Div([
        html.H1(children='Kes sembuh baharu'),
        html.H2(f"{df4['discharged_total'].groupby(df4['date']).sum().iloc[-1]}"),
        html.P(f"Jumlah kes sembuh: {df4['discharged_total'].sum(axis=0)}"),
    ], className= 'info'),

    html.Div([
        html.H1(children='Kes kematian baharu'),
        html.H2(f"{df3['deaths_new'].iloc[-1]}"),
        html.P(f"Jumlah kes kematian: {df3['deaths_new'].sum(axis=0)}")
    ], className= 'info')

  ], className= 'main-info'),

  html.Div([
    html.Div([
      html.H1(children='Statistik semasa'),

      html.P(f"Peratus sembuh: {round(discharge_percentage, 2)}%"),
      dbc.Progress(value=discharge_percentage, max=100, striped=True, style={"height": "40px", 'margin': '1em'}),

      html.P(f"Kes dikesan dari ujian RTK-AG: {round(rtk_percentage, 2)}%"),
      dbc.Progress(value=pcr_percentage, max=100, striped=True, style={"height": "40px", 'margin': '1em'}), 

      html.P(f"Kes dikesan dari ujian PCR: {round(pcr_percentage, 2)}%"),
      dbc.Progress(value=pcr_percentage, max=100, striped=True, style={"height": "40px", 'margin': '1em'}), 

      html.P(f"Peratus kematian: {round(death_percentage,2)}%"),
      dbc.Progress(value=death_percentage, max=100, striped=True, style={"height": "40px", 'margin': '1em'})      
    ], className= 'graph-1'),

    html.Div([
        html.H1(children='Kes mengikut negeri'),
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
    y ='cases_new'
  )

  figure.update_layout(
    showlegend=False,
    plot_bgcolor= 'rgba(0, 0, 0, 0)',
    paper_bgcolor= '#1B233F',
    xaxis=dict(linecolor='gray'),
    yaxis=dict(linecolor='gray'),
    font_color='lightgray'
  )

  figure.update_xaxes(title_text='Tarikh',showticklabels=False, showgrid=False)
  figure.update_yaxes(title_text='Kes baharu', showticklabels=False, showgrid=False)

  return figure


# Run the App
if __name__ == '__main__':
  # app.run_server(debug=True)
  app.run_server()
