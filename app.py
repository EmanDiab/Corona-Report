# bar chart for death recovered confirmed
import plotly.graph_objects as go
import plotly as py
from plotly.subplots import make_subplots
import requests
import json

# ============ Global =====================

url_g = "https://covid19.mathdro.id/api"
response_g = requests.get(url_g)
data_g = response_g.text
main_parsed_g = json.loads(data_g)

confirmed_g = main_parsed_g['confirmed']['value']
recovered_g = main_parsed_g['recovered']['value']
deaths_g = main_parsed_g['deaths']['value']

import plotly.express as px

df = px.data.tips()
fig1 = px.pie(df, values=[confirmed_g, recovered_g, deaths_g], title='إصابات الكورونا في العالم',
              names=['الحالات المؤكدة', 'المتعافين', 'معدل الوفاة'], color=['confirmed', 'recovered', 'deaths'],
              color_discrete_map={'confirmed': 'mediumseagreen',
                                  'recovered': 'springgreen',
                                  'deaths': 'darkgreen'})

# =============== In Egypt =================

url = "https://covid19.mathdro.id/api/countries/EG"
response = requests.get(url)
data = response.text
main_parsed = json.loads(data)

confirmed = main_parsed['confirmed']['value']
recovered = main_parsed['recovered']['value']
deaths = main_parsed['deaths']['value']

import plotly.express as px

data_canada = px.data.gapminder()
fig2 = px.bar(data_canada, title='إصابات الكورونا في مصر ', x=['الحالات المؤكدة', 'المتعافين', 'المتوفين'],
              y=[confirmed, recovered, deaths])

# ========= Table of top countries ============
L = ["confirmed", "recovered", "deaths"]

url_t = "https://covid19.mathdro.id/api/recovered"
response_t = requests.get(url_t)
data_t = response_t.text
main_parsed_t = json.loads(data_t)

# ==========
# countries and confirmed citizens to put it in the table
countries = []
confirmed_citizens = []

# sorting the dictionary of the main_parsed_t which contains the country, region ,confirmed cases
Sorted_country = sorted(main_parsed_t, key=lambda k: k['confirmed'], reverse=True)

for Dic in Sorted_country:
    countries.append((Dic['countryRegion'], Dic['provinceState']))
    confirmed_citizens.append((Dic['confirmed']))

import plotly.graph_objects as go

fig3 = go.Figure(data=[go.Table(

    header=dict(values=['اسم البلد ', 'عدد الحالات المصابة'],
                line_color='seagreen',
                fill_color='#61d4b3',
                align='right'),
    cells=dict(values=[countries,  # 1st column
                       confirmed_citizens],  # 2nd column
               line_color='darkslategray',
               fill_color='mediumspringgreen',
               align='right'))
])

# ========= Plotting as Dash =============================
import dash
import dash_core_components as dcc
import dash_html_components as html

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server


colors = {
    'background': '#111111',
    'text': '#2b580c'
}

app.layout = html.Div(children=[
    html.H1(
        children='إحصائيات كورونا',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
    dcc.Graph(
        id='corona_world',
        figure=fig1
    ),
    dcc.Graph(
        id='corona_egypt',
        figure=fig2

    ),
    dcc.Graph(
        id='corona_top countries',
        figure=fig3
    )
])

if __name__ == '__main__':
    app.run_server(debug=False)