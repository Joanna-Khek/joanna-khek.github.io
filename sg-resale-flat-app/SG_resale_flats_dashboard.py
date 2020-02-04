# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 15:38:49 2019

@author: Joanna Khek Cuina
"""
# import libraries
import pandas as pd
import numpy as np
import dash
import dash_core_components as dcc # graph components
import dash_html_components as html # html components
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.express as px


full_data = pd.read_csv("full_resale_flat.csv")
full_data["date"] = pd.to_datetime(full_data["date"])
# ------------------------------- DATA ------------------------------ #
# date vs resale price
agg_date_resale = pd.DataFrame(full_data.groupby(["date", "town", "flat_type"])["resale_price"].mean())
agg_date_resale = agg_date_resale.reset_index()


# floor area vs resale price
agg_area_resale = pd.DataFrame(full_data.groupby(["flat_type"])["floor_area_sqm", "resale_price"].mean())
agg_area_resale = agg_area_resale.reset_index()


# floor vs resale price
agg_floor_resale = pd.DataFrame(full_data.groupby(["date", "storey_range"])["resale_price"].mean())
agg_floor_resale = agg_floor_resale.reset_index()


# town vs resale price
agg_town_resale = pd.DataFrame(full_data.groupby(["date", "town"])["resale_price"].mean())
agg_town_resale = agg_town_resale.reset_index()


# year vs floor area
agg_year_floor = pd.DataFrame(full_data.groupby(["date", "flat_type"])["floor_area_sqm"].mean())
agg_year_floor = agg_year_floor.reset_index()

# year vs town
agg_year_town = pd.DataFrame(full_data.groupby(["date", "year","town"])["resale_price"].mean())
agg_year_town = agg_year_town.reset_index()
agg_year_town = agg_year_town[agg_year_town["year"] == 2019]


# ----------------------------- FIGURES AND LAYOUTS ----------------------------- #
# FIGURE 1 (DATE VS RESALE PRICE)
fig1 = px.line(agg_date_resale, x="date", y="resale_price", color = "flat_type", facet_col="flat_type", 
               category_orders={"flat_type": ["1 ROOM", "2 ROOM", "3 ROOM", "4 ROOM", "5 ROOM", "EXECUTIVE"]}, width=1500, height=500)

for a in fig1.layout.annotations:
     a.text = a.text.split("=")[1]
 
fig1.update_layout(showlegend=False,
                   title="<b>Time Series of Resale Prices by Flat Type</b>",
                   xaxis_title="Year",
                   yaxis_title="Resale Price")
fig1.update_xaxes(title_text='Year')
fig1.update_layout(
    title={
        'y':1.0,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})


# FIGURE 2 (FLOOR AREA VS RESALE PRICE)
fig2 = px.scatter(full_data, x="floor_area_sqm", y="resale_price", color="flat_type",
                  category_orders={"flat_type": ["1 ROOM", "2 ROOM", "3 ROOM", "4 ROOM", "5 ROOM", "EXECUTIVE"]}, 
                  hover_data=['town'], width=1500, height=500)

fig2.update_layout(showlegend=False,
                          title="<b>Floor Area VS Resale Price by Flat Type</b>",
                          xaxis_title="Floor Area (sqm)",
                          yaxis_title="Resale Price")
fig2.update_layout(
    title={
        'y':1.0,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})

# FIGURE 3 (YEAR VS FLOOR AREA)
fig3 = px.line(agg_year_floor, x="date", y="floor_area_sqm", color="flat_type", facet_col="flat_type",
              category_orders={"flat_type": ["1 ROOM", "2 ROOM", "3 ROOM", "4 ROOM", "5 ROOM", "EXECUTIVE"]}, width=1500, height=600)

for a in fig3.layout.annotations:
     a.text = a.text.split("=")[1]
     
fig3.update_layout(showlegend=False,
                   title="<b>Time Series of Floor Area (sqm) by Flat Type</b>",
                   xaxis_title="Year",
                   yaxis_title="Floor Area (sqm)")
fig3.update_xaxes(title_text='Year')
fig3.update_layout(
        title={
                'y':1.0,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'})
    

# FIGURE 4 (TOWN VS RESALE PRICE)
fig4 = px.line(agg_year_town, x="date", y="resale_price", color = "town")

fig4.update_layout(showlegend=True,
                   title="<b>Resale Prices in 2019 by Town</b>",
                   yaxis_title="Resale Price")
fig4.update_layout(
    title={
        'y':1.0,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})
    


# ---------------------------- DASHBOARD ---------------------------- #
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.config.suppress_callback_exceptions = True
server = app.server

# CSS
tabs_styles = {
        "height": "44px"}

tab_style = {
        "borderBottom": "1px solid #d6d6d6",
        "padding": "5px",
        "fontWeight": "bold"
        }

tab_selected_style = {
        "borderTop": "1px solid #d6d6d6",
        "borderBottom": "1px solid #d6d6d6",
        "backgroundColor": "#119DFF",
        "color": "white",
        "padding": "6px"}

app.layout = html.Div([
        dcc.Tabs(id="tabs-styled-with-inline", value="tab-1", children=[
                dcc.Tab(label="Home Page", value="tab-1", style=tab_style, selected_style=tab_selected_style),
                dcc.Tab(label="Flat Type", value="tab-2", style=tab_style, selected_style=tab_selected_style),
                dcc.Tab(label="Town", value="tab-3", style=tab_style, selected_style=tab_selected_style)], style=tabs_styles),
        html.Div(id = "tabs-content-inline")
        ])

@app.callback(Output('tabs-content-inline', 'children'),
              [Input('tabs-styled-with-inline', 'value')])
        
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
                html.H1("Singapore Resale Flat Prices"),
                dcc.Markdown('''
                             ### Welcome!
                             
                             Hi I'm [Joanna Khek](https://www.linkedin.com/in/joannakhek/) and this is a personal visualisation with dash project i'm currently
                             working on.
                             
                             Housing prices are fluctuating every year and i wanted to have an overview of the housing situation here in Singapore.
                             I have created resale prices visualisations involving variables such as date, floor area, flat type and town.
                             
                             The full dataset is available and can be found [here](https://data.gov.sg/dataset/resale-flat-prices).
                             
                             Due to the limited memory space of this hosting site, only data from year 2000 ownwards was used.
                             
                             Click on the different tabs above to start exploring!    
                             
                             Last update: 6 Dec 2019
                             ''')])
    elif tab == "tab-2":
        return html.Div([
                html.H1("Overview"),
                dcc.Loading([
                    dcc.Markdown('''
                                 Please wait patiently while the plots are being loaded.   
                                 Hover over the plots for more information!
                                 '''),
                    dcc.Graph(id="first", figure=fig1),
                    dcc.Graph(id="second", figure=fig2),
                    dcc.Graph(id="third", figure=fig3),
                    #dcc.Graph(id="fourth", figure=fig4)
                    ])
                    ])
                
    elif tab == "tab-3":
        return html.Div([
                    html.H1("Town"),
                    html.Div([
                        html.Label(["Select a town to view the resale prices:", dcc.Dropdown(
                                id='town_selection', style={'height': '30px', 'width': '500px'},
                                options=[
                                        {'label': i, 'value': i} for i in full_data["town"].unique()],
                                value = 'ANG MO KIO'
                                )]),
                        ]),
    
                    html.Div([
                        html.Label(["Select a flat type to view the resale prices:", dcc.Dropdown(
                                id='flat_selection', style={'height': '30px', 'width': '500px'},
                                options=[
                                        {'label': "1 ROOM", 'value': "1 ROOM"},
                                        {'label': "2 ROOM", 'value': "2 ROOM"},
                                        {'label': "3 ROOM", 'value': "3 ROOM"},
                                        {'label': "4 ROOM", 'value': "4 ROOM"},
                                        {'label': "5 ROOM", 'value': "5 ROOM"},
                                        {'label': "EXECUTIVE", 'value': "EXECUTIVE"}],
                                        value= "5 ROOM"
                                        )]),
                        ]),
                    dcc.Graph(id="fourth", style={
                            'height':700}),
                    dcc.Graph(id='indicator-graphic'),
                    dcc.Graph(id="flat_type_graphic"),
# =============================================================================
#                     dcc.Slider(
#                             id='year--slider',
#                             min=full_data["year"].min(),
#                             max=full_data["year"].max(),
#                             value=full_data["year"].max(),
#                             marks={str(year):str(year) for year in full_data["year"].unique()},
#                             step=None
#                             )
# =============================================================================
                    ])
    

@app.callback(dash.dependencies.Output('fourth', 'figure'),
              [dash.dependencies.Input('flat_selection', 'value')])
def update_all_town(flat_selection_name):
    df = full_data[full_data["flat_type"] == flat_selection_name]
    agg_df = pd.DataFrame(df.groupby(["date", "year", "town"])["resale_price"].mean())
    agg_df = agg_df.reset_index()
    agg_df = agg_df[agg_df["year"] == 2019]
    
    traces = []
    for i in agg_df["town"].unique():
        df_by_town = agg_df[agg_df['town'] == i]
        traces.append(dict(
            x=df_by_town['date'],
            y=df_by_town['resale_price'],
            text=df_by_town['town'],
            name =i
        ))
        
    return{
            'data': traces,
            'layout': dict(
                    xaxis={'title': 'Year'},
                    yaxis={'title': 'Resale Price'},
                    margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                    hovermode='closest'
                    )
            }
    
@app.callback(dash.dependencies.Output('indicator-graphic', 'figure'),
              [dash.dependencies.Input('town_selection', 'value')])
                        
def update_graph(town_selection_name):
    dff = full_data[full_data["town"] == town_selection_name]
    agg_test = pd.DataFrame(dff.groupby(["date", "flat_type"])["resale_price"].mean())
    agg_test = agg_test.reset_index()


    return {
            'data': [dict(
                    x=agg_test["date"],
                    y=agg_test["resale_price"],
                    )],
            'layout': 
                go.Layout(
                        title="<b>Average Resale Prices by Town ({})</b>".format(town_selection_name))
                }
 

@app.callback(dash.dependencies.Output('flat_type_graphic', 'figure'),
              [dash.dependencies.Input('town_selection', 'value'),
               dash.dependencies.Input('flat_selection', 'value')])

def update_flat_graph(town_selection_name, flat_selection_name):
    df_flat = full_data[full_data["town"] == town_selection_name]
    df_flat = df_flat[df_flat["flat_type"] == flat_selection_name]
    agg_flat = pd.DataFrame(df_flat.groupby("date")["resale_price"].mean())
    agg_flat = agg_flat.reset_index()
    
    return {
            'data': [dict(
                    x=agg_flat["date"],
                    y=agg_flat["resale_price"],
                    )],
            'layout':
                go.Layout(
                        title="<b> Average Resale Prices by Town ({}) and Flat Type ({})</b>".format(town_selection_name, flat_selection_name))
                }
          
   

if __name__ == "__main__":
    app.run_server()

