# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Load the data using pandas
# data = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv")

# Read the SpaceX launch data into a pandas dataframe
spacex_df = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    
    # TASK 1: Add a Launch Site Drop-down Input Component
    dcc.Dropdown(
        id='site-dropdown',
        options=[
            {'label': 'All Sites', 'value': 'ALL'},
            {'label': 'Cape Canaveral Launch Complex 40 (CAFS LC-40)', 'value': 'CCAFS LC-40'},
            {'label': 'Cape Canaveral Space Launch Complex 40 (CCAFS SLC-40)', 'value': 'CCAFS SLC-40'},
            {'label': 'Kennedy Space Center Launch Complex 39A (KSC LC-39A)', 'value': 'KSC LC-39A'},
            {'label': 'Vandenberg Air Force Base Space Launch Complex (VAFB SLC-4E)', 'value': 'VAFB SLC-4E'}
        ],
        value='ALL',
        placeholder="Select a Launch Site here",
        searchable=True
    ),

    html.Br(),

    # TASK 2: Placeholder for the pie chart
    dcc.Graph(id='success-pie-chart'),

    
    # TASK 3: Add a Range Slider to Select Payload
    dcc.RangeSlider(
        id='payload-slider',
        min=0, 
        max=10000, 
        step=1000,
        marks={i: f'{i}' for i in range(0, 10001, 1000)},
        value=[min_payload, max_payload]
    ),

    html.Br(),

    
    # Placeholder for the scatter plot
    dcc.Graph(id='success-payload-scatter-chart'),
    
    
])

# TASK 2: Add a callback function to render success-pie-chart based on selected site dropdown
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(filtered_df, 
                     names='Launch Site', 
                     values='class', 
                     title='Total Successful Launches by Site')
    else:
        # Filter dataframe to include only the selected site data
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        fig = px.pie(filtered_df, 
                     names='class', 
                     title=f'Total Successful Launches for site {entered_site}')
    return fig

# TASK 4: Add a callback function to render success-payload-scatter-chart based on selected site and payload range
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value'),
    Input(component_id='payload-slider', component_property='value')
)
def update_scatter_chart(entered_site, payload_range):
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload_range[0]) &
                            (spacex_df['Payload Mass (kg)'] <= payload_range[1])]
    if entered_site == 'ALL':
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', 
                         color='Booster Version Category',
                         title='Correlation between Payload and Success for all Sites')
    else:
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', 
                         color='Booster Version Category',
                         title=f'Correlation between Payload and Success for site {entered_site}')
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
