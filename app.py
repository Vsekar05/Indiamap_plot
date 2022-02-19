import os
import dash
import dash_auth
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import json

india_states=json.load(open("states_india.geojson","r"))

state_id_map = {}
for feature in india_states['features']:
  feature['id'] = feature['properties']['state_code']
  state_id_map[feature['properties']['st_nm']] = feature['id']
 
USERNAME_PASSWORD_PAIRS = [
    ['nethu', '12345'],['guvi', 'guvi'],['vignesh','vignesh']
]
app = dash.Dash()
auth = dash_auth.BasicAuth(app,USERNAME_PASSWORD_PAIRS)
server = app.server

colors = {
   'background': '#111111',
   'text': '#FC0101'
}

Data=pd.read_csv("https://raw.githubusercontent.com/nikhilkumarsingh/choropleth-python-tutorial/master/india_census.csv")
Data['Density'] = Data['Density[a]'].apply(lambda x: int(x.split("/")[0].replace(",","")))
Data['id']=Data['State or union territory'].apply(lambda x:state_id_map[x])
Data.head()

fig = px.choropleth(Data,locations="id",geojson=india_states,color="Density")
fig.update_geos(fitbounds='locations',visible=False)
 
fig.update_layout(
   plot_bgcolor=colors['background'],
   paper_bgcolor=colors['background'],
   font_color=colors['text']
)
 
app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
   html.H1(
       children='India Map',
       style={
           'textAlign': 'center',
           'color': colors['text']
       }
   ),
 
   html.Div(children='The color depicts the population for each state', style={
       'textAlign': 'center',
       'color': colors['text']
   }),
 
   dcc.Graph(
       id='example-graph-2',
       figure=fig
   )
])
 

 
if __name__ == '__main__':
    app.run_server(debug=True)
