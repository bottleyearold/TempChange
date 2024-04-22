import pandas as pd
import numpy as np
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objs as go
from datetime import datetime, timedelta
import math
import dash_bootstrap_components as dbc

# Load the dataset
file_path = '/Users/fionamagee/Desktop/Temperature Change/dataset1.csv'
file_path2 = '/Users/fionamagee/Desktop/Temperature Change/dataset2.csv'
data = pd.read_csv(file_path)
data2 = pd.read_csv(file_path2)


# Drop unnecessary columns
columns_to_drop = ['ObjectId', 'ISO2', 'ISO3', 'Indicator', 'Unit', 'Source', 'CTS_Code', 'CTS_Name', 'CTS_Full_Descriptor']
data_cleaned = data.drop(columns=columns_to_drop)

# Rename columns
data_cleaned.rename(columns={'Country': 'country'}, inplace=True)

# Convert the dataset from wide format to long format
data_tidy = pd.melt(data_cleaned, id_vars=['country'], var_name='year', value_name='temperature_change')

# Remove 'F' from year
data_tidy['year'] = data_tidy['year'].str.replace('F', '')

start_date = datetime(2024, 4, 22, 12, 0)

# Calculate the end date from the start date
end_date = start_date + timedelta(days=(5 * 365) + 91, minutes=0)

year_columns = [col for col in data2 if col.startswith('F')]
years = [int(col.replace('F', '')) for col in year_columns]


# Create the base figure for the choropleth map
fig_choropleth = go.Figure()

# Add one trace for each year
for col in year_columns:
    fig_choropleth.add_trace(
        go.Choropleth(
            locations=data['ISO3'],
            z=data[col],
            text=data['Country'],
            colorscale='Plasma',
            autocolorscale=False,
            showscale=True,
            name=str(col).replace('F', ''),
            visible=(col == year_columns[-1])  # Show only the last year initially
        )
    )

# Make a slider for the years
steps = []
for i, year in enumerate(years):
    step = dict(
        method='update',
        args=[{'visible': [False] * len(years)}],
        label=str(year)
    )
    step['args'][0]['visible'][i] = True  # Toggle i-th trace to "visible"
    steps.append(step)

sliders = [dict(
    active=len(years) - 1,
    currentvalue={"prefix": "Year: "},
    pad={"t": 1},
    steps=steps
)]

# Update the layout of the choropleth map
fig_choropleth.update_layout(
    sliders=sliders,
    title=f'Global Annual Surface Temperature Change',
    geo=dict(
        showframe=False,
        showcoastlines=False,
        projection_type='equirectangular'
    )
)





# Create the Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, './assets/main.css'])

server = app.server

navbar = html.Div(
    [
        dbc.NavbarBrand("Information and Statistics", href="#", style={"color": "white", "width": "100%", "display": "block", "textAlign": "center", "padding-bottom": "8px", "padding-top": "10px","font-size": "20px", 'font-weight': '500'}),
        dbc.Nav(
            [
                dbc.NavItem(dbc.NavLink("Overview", href="#", style= {"padding-left": "35px", "padding-right": "35px"})),
                dbc.NavItem(dbc.NavLink("Result of Climate Change", href="#", style= {"padding-left": "35px", "padding-right": "35px"})),
                dbc.NavItem(dbc.NavLink("Temperature Change", href="https://finaldashboard-4.onrender.com", style= {"padding-left": "35px", "padding-right": "35px"})),
                dbc.NavItem(dbc.NavLink("More References", href="MoreReference.html", style= {"padding-left": "35px", "padding-right": "35px"})),
            ],
            className="ms-auto",
            navbar=True,
            style={"width": "100%", "display": "flex", "justifyContent": "center", "padding-bottom": "8px", 'border-bottom': '2px solid white'}
        ),
    ],
    style={
        "backgroundColor": "#132c48ff",
        "display": "flex",
        "flexDirection": "column",
        "justifyContent": "center",
        "width": "100%",
    }
)


app.layout = html.Div([
    html.Div([
        navbar,

    # Main content area with graph, text boxes, and controls
    html.Div([
        # Graph, its associated text box, and controls
        html.Div([
            # Controls (Dropdown and Slider) placed side by side
            html.Div([
                html.Div([
                    html.Label('Dropdown'),
                    dcc.Dropdown(
                        id='country-dropdown',
                        options=[{'label': i, 'value': i} for i in np.sort(data_tidy['country'].unique())],
                        value='United States',
                        multi=True
                    ),
                ], className='control-group control-group-right'),

                html.Div([
                    html.Label('Slider'),
                    dcc.RangeSlider(
                        id='year-range-slider',
                        min=int(data_tidy['year'].min()),
                        max=int(data_tidy['year'].max()),
                        step=1,
                        value=[int(data_tidy['year'].min()), int(data_tidy['year'].max())],
                        marks=None,
                        tooltip={"placement": "bottom", "always_visible": True}
                    ),
                ], className='control-group control-group-left'),
            ], style={'width': '100%', 'margin-bottom': '20px'}),

            dcc.Graph(id='bar-chart', style={'height': '400px'}),
                html.H3('Increasing Temperatures', style={'padding-top': '20px', 'color': '#132c48ff'}),
                html.Div('This graph illistartes how global tempratures are rising in each country. The rising temperatures across the globe are a significant indicator of climate change, with far-reaching effects on both the environment and human societies. The upward trend in global temperatures is primarily attributed to the increase in greenhouse gases, such as carbon dioxide and methane, in the Earths atmosphere. These gases trap heat, leading to a gradual warming of the planet, known as the greenhouse effect.')
        ], className='graph-area', style= {'background-color': 'light blue','padding-left': '20px', 'padding-right': '20px' , 'padding-bottom': '20px', 'border-radius': '15px', 'padding-top': '50px' }),

        # Polar bear image, title, and its associated text box
        html.Div([
            html.Div([], style={'height': '20px'}),  # This empty div acts as a spacer
            html.H1('Temperature Change', style={'textAlign': 'left','font-family':'Arial', "font-weight": "520", "color": '#132c48ff'}),
            html.H2('The Danergous Effects of Our Rising Temperature', style={'font-size': "30px", "color": "#da7d88", "padding-bottom": "20px"}),
            html.Div("Temperature changes are a natural part of Earth's climate system, influenced by various factors including solar radiation, atmospheric composition, and ocean currents. Over geological timescales, temperatures have fluctuated, leading to ice ages and warmer interglacial periods.", style={'textAlign': 'left', 'padding-right': '20px','padding-left': '20px', 'padding-top': '20px', "padding-bottom": "20px" ,"background-color": "#d7dce1ff", "border-radius": "2%" , "margin-bottom":"20px"}),
            html.Div([
        html.H3('Countdown to Event', className='countdown-title', style={"height":"50px", "textAlign": "center", 'padding-top': '20px'}),
        html.Div("This is the time left to limit global warming to 1.5°C, and furthermore represents the point where climate change will be irreversibile", style={"textAlign": "center", 'font-size': '20px', 'padding-left': '10px', 'padding-right': '10px', 'padding-bottom': '10px'}),
        html.Div(id='countdown', className='countDOWN', style={"textAlign": "center","fontSize": "40px" }),
        dcc.Interval(id='interval-component', interval=1000, n_intervals=0)
    ], style={'textAlign': 'center', 'paddingBottom': "200px", 'background-color': '#d7dce1ff', 'margin-left': '10px', 'height': '300px'}),  # Ensure text alignment is set for the whole container
], className='polar-bear-area'),
        
    ], className='content-area'),
    html.H1('The Cost Of Climate Change', style={
            'textAlign': 'left', 
            'margin-top': '20px',
            'padding-left': '10px',
            'color': '#132c48ff', # Text color
            'font-weight': '500'
        }),
    html.Div('It is imperative that we halt the rise in global temperatures to avoid the severe and irreversible consequences of climate change. The stability of Earth’s climate underpins all aspects of human life, and as temperatures climb, we are confronted with more frequent and intense natural disasters, such as hurricanes, wildfires, and droughts, which not only endanger lives but also strain economies and lead to increased political instability. The delicate balance of ecosystems, upon which we rely for clean air, water, and food, is being disrupted. Species are being pushed to extinction faster than new ones can evolve, resulting in a loss of biodiversity that could take millions of years to recover. Warmer temperatures also contribute to the melting of polar ice caps, leading to sea-level rise, which threatens to submerge coastal cities and create millions of climate refugees. Moreover, agriculture, vital for human sustenance, is vulnerable to temperature changes. As regions become warmer, crop yields can decrease, and food security can become compromised, especially in areas that already face scarcity. In terms of health, heatwaves pose direct risks, while altering patterns of disease vectors can spread illness to new areas, potentially creating health crises. Halting the temperature increase is more than an environmental issue; it is about preserving our way of life, ensuring food and water security, protecting homes and economies, and safeguarding the health of current and future generations. It is about taking responsibility for our planets well-being and the legacy we leave for those who follow.', style={'padding-left':'30px', 'padding-right':'30px', 'padding-bottom': '30px'}),
    html.Div([
            dcc.Graph(id='choropleth-map', figure=fig_choropleth, style={'height': '600px', 'width':'1200px', 'padding-left': '250px', 'padding-bottom': '30px', 'left': '50%'}),
        ], className='graph-area'),

], style={'margin': '0', 'padding': '0', 'width': '100vw', 'height': '100vh'})
])

@app.callback(
    Output('bar-chart', 'figure'),
    [Input('country-dropdown', 'value'),
     Input('year-range-slider', 'value')]
)
def update_figure(selected_country, selected_year):
    if not isinstance(selected_country, list) or not selected_country:
        # If selected_country is not a list (e.g., it's 'Select' or None) or it's empty, initialize it with 'United States'.
        selected_country = ['United States']

    # Convert years to strings because the DataFrame has years as strings.
    selected_year = [str(y) for y in selected_year]

    # Filter the data based on selected years.
    filtered_data = data_tidy[(data_tidy['year'] >= selected_year[0]) & (data_tidy['year'] <= selected_year[1])]

    # If there are countries selected, further filter the data.
    if selected_country:
        filtered_data = filtered_data[filtered_data['country'].isin(selected_country)]

    # Now, create the figure with the filtered data.
    fig = px.bar(filtered_data, x='year', y='temperature_change', color='country',
                  title='Climate Change per Country and Year')

    fig.update_layout(
        xaxis_title='Years',
        yaxis_title='Temperature Change °C',
        legend_title='Countries',
        xaxis=dict(tickmode='linear', tick0=0, dtick=10, tickangle=-45),
        yaxis=dict(tickmode='auto', nticks=10),
    )
    return fig

@app.callback(
    Output('countdown', 'children'),
    Input('interval-component', 'n_intervals'))
def update_countdown(n):
    # Calculate the time difference between now and the end date
    time_left = end_date - datetime.now()

    # Extract days, hours, minutes, and seconds from the time difference
    days = time_left.days
    seconds = time_left.seconds
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    # Calculate years and remaining days
    years = days // 365
    remaining_days = days % 365  # Correctly accounts for remaining days after complete years

    # Format the countdown display
    return html.Div(
        f"{years} years, {remaining_days} days, {hours:02}:{minutes:02}:{seconds:02}",
        className='countdown'
    )

if __name__ == '__main__':
    app.run(jupyter_mode='tab', debug=True) 


    