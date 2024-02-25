# Import required libraries
import pandas as pd
import dash
#import dash_html_components as html
#import dash_core_components as dcc
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px




# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
#print('Min= ', min_payload, 'Max= ',max_payload)




# Create a dash application
app = dash.Dash(__name__)




# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                      style={'textAlign': 'center', 'color': '#503D36',
                                             'font-size': 40}),
                              # TASK 1: Add a dropdown list to enable Launch Site selection
                              # The default select value is for ALL sites
                              html.Div(dcc.Dropdown(id='site-dropdown',
                                                    options=[{'label':'All Sites', 'value':'All'},
                                                             {'label':'CCAFS LC40', 'value':'CCAFS LC-40'},
                                                             {'label':'VAFB', 'value':'VAFB SLC-4E'},
                                                             {'label':'KSC', 'value':'KSC LC-39A'},
                                                             {'label':'CCAFS SLC40', 'value':'CCAFS SLC-40'}
                                                            ],
                                                    value='All',
                                                    placeholder='Select a Launch Site here',
                                                    searchable=True                      
                                                   )
                                      ),
                              html.Br(),




                              # TASK 2: Add a pie chart to show the total successful launches count for all sites
                              # If a specific launch site was selected, show the Success vs. Failed counts for the site
                              html.Div(dcc.Graph(id='success-pie-chart')),
                              html.Br(),




                              html.P("Payload range (Kg):"),
                              # TASK 3: Add a slider to select payload range
                              html.Div(dcc.RangeSlider(id='payload-slider',
                                                       min=0, max=10000, step=1000,
                                                       marks={0:'0',
                                                              1000:'1000', 2000:'2000',
                                                              3000:'3000', 4000:'4000',
                                                              5000:'5000', 6000:'6000',
                                                              7000:'7000', 8000:'8000',
                                                              9000:'9000', 10000:'10000'},
                                                       value=[min_payload, max_payload]
                                                      )
                                       #html.Div(id='output-payload-slider')
                                       ),




                              # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                              html.Div(dcc.Graph(id='success-payload-scatter-chart'))
                              ])




# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
            Input(component_id='site-dropdown', component_property='value')
           )




def get_pie_chart(entered_site):
  filtered_df = spacex_df
# print('Entered Site= ', entered_site)
  if entered_site == 'All':
     filtered_df = spacex_df.groupby('Launch Site')['class'].sum().reset_index()
     fig = px.pie(filtered_df, values=filtered_df['class'],
                  names=filtered_df['Launch Site'],
                  title='The Success Rate for All sites'
                 )
     return fig
#        print('All Sites= ', entered_site)
  else:
     filtered_df = spacex_df[spacex_df['Launch Site']==entered_site]
     vc = filtered_df.value_counts('class').reset_index()
     fig = px.pie(vc, values=vc.iloc[:,1],
                  names=vc['class'],
                  title=('The Success Rate for site {}'.format(entered_site))
                 )
     return fig
    # print('Entered Site= ', entered_site)
     # return the outcomes piechart for a selected site




# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [
               Input(component_id='site-dropdown',component_property='value'),
               Input(component_id='payload-slider',component_property='value')
              ]
           )




def get_scatter_chart(entered_site, selected_payload):
  filtered_df = spacex_df
#   print('Entered Site= ', entered_site)
#   print('Selected Payload Range1= ', selected_payload[1])
  if entered_site == 'All':
     f1_df = filtered_df[filtered_df['Payload Mass (kg)']>=selected_payload[0]]
     f2_df = f1_df[f1_df['Payload Mass (kg)']<=selected_payload[1]]
     fig = px.scatter(f2_df,
                      x='Payload Mass (kg)',
                      y='class',
                      color='Booster Version Category',
                      title='The Payload vs Success Rate at all launch sites'
                 )
     return fig
#        print('All Sites= ', entered_site)
  else:
     filtered_df = spacex_df[spacex_df['Launch Site']==entered_site]
     f1_df = filtered_df[filtered_df['Payload Mass (kg)']>=selected_payload[0]]
     f2_df = f1_df[f1_df['Payload Mass (kg)']<=selected_payload[1]]
     fig = px.scatter(f2_df,
                      x='Payload Mass (kg)',
                      y='class',
                      color='Booster Version Category',
                      title=('The Payload "{}" vs Success Rate for site {}'.format(selected_payload, entered_site))
                 )
     return fig




# Run the app
if __name__ == '__main__':
  app.run_server()

