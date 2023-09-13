import os
import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
from dotenv import load_dotenv

# Import CSV Data
df = pd.read_csv('data/Communities.csv')
comms = df['Community'].unique()

# Create Community Lists for Multiple Search Bars
essential_air_service_comms = df[df['Essential_Air_Service'] == 'Yes']['Community'].unique()
subsistence_use_comms = df[df['Subsistence_Use'] == 'Yes']['Community'].unique()
environmental_threat_comms = df[df['Environmentally_Threatened'] == 'Yes']['Community'].unique()
road_connection_comms = df[df['Road_Connection'].notnull()]['Community'].unique()

# Mapbox Access Key
load_dotenv()
px.set_mapbox_access_token(os.getenv('MAPBOX_ACCESS_TOKEN'))

# Dash App Name
app = dash.Dash(__name__)

app.layout = html.Div([
    # Link CSS Files
    html.Link(
        rel='stylesheet',
        href='/assets/styles.css'  # Update the path to your CSS file
    ),

    # Navigation Bar
    html.Div(className='navbar', children=[
        html.A("AK School & Community Maps", className='navbar-logo'),
        html.Div(className='navbar-item-container', children=[
            html.A("About", className='navbar-item'),
            html.A("Communities", className='navbar-item'),
            html.A("Schools", className='navbar-item'),
            html.A("Analysis", className='navbar-item'),
            html.A("Github", className='navbar-item', target="_blank"),
        ])
    ]),
    # Title
    html.Div(html.H1('Alaskan Communities'), style={'fontSize': 20, 'font-family': 'Optima', 'text-align': 'center'}),

    # Dropdown Menu
    dcc.Dropdown(
        id='category-dropdown',
        options=[
            {'label': 'All Communities', 'value': 'Community'},  # Default Selection
            {'label': 'Communities Scaled by Population', 'value': 'Population'},
            {'label': 'Incorporation Types', 'value': 'Incorporation_Type'},
            {'label': 'Subsistence Use Communities', 'value': 'Subsistence_Use'},
            {'label': 'Essential Air Service Communities', 'value': 'Essential_Air_Service'},
            {'label': 'Environmentally Threatened Communities', 'value': 'Environmentally_Threatened'},
            {'label': 'Road System Connection', 'value': 'Road_Connection'}
        ],
        value='Community',  # Set as Default Selection
        style={'fontSize': 20, 'font-family': 'Optima', 'text-align': 'center', 'font-weight': 'bold'},
        searchable=False,
        multi=False
    ),

    # Default Search Bar
    dcc.Dropdown(
        id='search',
        options=[{'label': comm, 'value': comm} for comm in comms],
        placeholder='— Filter by Community —',
        value=None,  # Set as Default Selection
        style={'fontSize': 20, 'font-family': 'Optima', 'text-align': 'center', 'font-weight': 'bold',
               'margin-top': '5px'},
        searchable=True,
        multi=True
    ),
    # EAS Communties Search Bar
    dcc.Dropdown(
        id='EASsearch',
        options=[{'label': comm, 'value': comm} for comm in essential_air_service_comms],
        placeholder='— Filter by Community —',
        value=None,  # Set as Default Selection
        style={'fontSize': 20, 'font-family': 'Optima', 'text-align': 'center', 'font-weight': 'bold',
               'margin-top': '5px'},
        searchable=True,
        multi=True
    ),
    # Subsistence Communities Search Bar
    dcc.Dropdown(
        id='SUCsearch',
        options=[{'label': comm, 'value': comm} for comm in subsistence_use_comms],
        placeholder='— Filter by Community —',
        value=None,  # Set as Default Selection
        style={'fontSize': 20, 'font-family': 'Optima', 'text-align': 'center', 'font-weight': 'bold',
               'margin-top': '5px'},
        searchable=True,
        multi=True
    ),

    # Environmental Threatened Communities Search Bar
    dcc.Dropdown(
        id='ETCsearch',
        options=[{'label': comm, 'value': comm} for comm in environmental_threat_comms],
        placeholder='— Filter by Community —',
        value=None,  # Set as Default Selection
        style={'fontSize': 20, 'font-family': 'Optima', 'text-align': 'center', 'font-weight': 'bold',
               'margin-top': '5px'},
        searchable=True,
        multi=True
    ),

    # Road Connection by Community Search Bar
    dcc.Dropdown(
        id='RCsearch',
        options=[{'label': comm, 'value': comm} for comm in road_connection_comms],
        placeholder='— Filter by Community —',
        value=None,  # Set as Default Selection
        style={'fontSize': 20, 'font-family': 'Optima', 'text-align': 'center', 'font-weight': 'bold',
               'margin-top': '5px'},
        searchable=True,
        multi=True
    ),

    # Map layout
    dcc.Graph(id='map',
              style={'font-family': 'Optima'}),

    # Text Box Layout
    html.Div(id='text_display', children=['text_display'],
             style={'fontSize': 24, 'font-family': 'Optima', 'line-height': 40, 'margin-top': '-30px', 'padding-left': '275px', 'padding-right': '275px',
                    'text-align': 'center', 'position': 'relative'}),

    # Chart Layout
    dcc.Graph(id='chart',
              style={'fontSize': 36, 'font-family': 'Optima', 'text-align': 'center', 'padding-top': '40px',
                      'position': 'relative', 'align-content': 'center', 'font-weight' : 'bold'})
])

# Default Search Bar Callback
@app.callback(
   dash.dependencies.Output(component_id='search', component_property='style'),
   [dash.dependencies.Input(component_id='category-dropdown', component_property='value')]
)
def show_hide_element(community):
    if community == 'Essential_Air_Service' \
            or community == 'Subsistence_Use' \
            or community == 'Environmentally_Threatened' \
            or community == 'Road_Connection':
        return {'fontSize': 20, 'font-family': 'Optima', 'text-align': 'center', 'font-weight': 'bold',
               'margin-top': '5px', 'display': 'none'}
    else:
        return {'fontSize': 20, 'font-family': 'Optima', 'text-align': 'center', 'font-weight': 'bold',
                'margin-top': '5px', 'display': 'block'}

# EAS Communties Search Bar Callback
@app.callback(
   dash.dependencies.Output(component_id='EASsearch', component_property='style'),
   [dash.dependencies.Input(component_id='category-dropdown', component_property='value')]
)
def show_hide_element(community):
    if community == 'Essential_Air_Service':
        return {'fontSize': 20, 'font-family': 'Optima', 'text-align': 'center', 'font-weight': 'bold',
                'margin-top': '5px', 'display': 'block'}
    else:
        return {'fontSize': 20, 'font-family': 'Optima', 'text-align': 'center', 'font-weight': 'bold',
                'margin-top': '5px', 'display': 'none'}

# Subsistence Communities Search Bar Callback
@app.callback(
   dash.dependencies.Output(component_id='SUCsearch', component_property='style'),
   [dash.dependencies.Input(component_id='category-dropdown', component_property='value')]
)
def show_hide_element(community):
    if community == 'Subsistence_Use':
        return {'fontSize': 20, 'font-family': 'Optima', 'text-align': 'center', 'font-weight': 'bold',
                'margin-top': '5px', 'display': 'block'}
    else:
        return {'fontSize': 20, 'font-family': 'Optima', 'text-align': 'center', 'font-weight': 'bold',
                'margin-top': '5px', 'display': 'none'}

# Environmental Threatened Communities Search Bar Callback
@app.callback(
   dash.dependencies.Output(component_id='ETCsearch', component_property='style'),
   [dash.dependencies.Input(component_id='category-dropdown', component_property='value')]
)
def show_hide_element(community):
    if community == 'Environmentally_Threatened':
        return {'fontSize': 20, 'font-family': 'Optima', 'text-align': 'center', 'font-weight': 'bold',
                'margin-top': '5px', 'display': 'block'}
    else:
        return {'fontSize': 20, 'font-family': 'Optima', 'text-align': 'center', 'font-weight': 'bold',
                'margin-top': '5px', 'display': 'none'}

# Road Connection by Community Search Bar Callback
@app.callback(
   dash.dependencies.Output(component_id='RCsearch', component_property='style'),
   [dash.dependencies.Input(component_id='category-dropdown', component_property='value')]
)
def show_hide_element(community):
    if community == 'Road_Connection':
        return {'fontSize': 20, 'font-family': 'Optima', 'text-align': 'center', 'font-weight': 'bold',
                'margin-top': '5px', 'display': 'block'}
    else:
        return {'fontSize': 20, 'font-family': 'Optima', 'text-align': 'center', 'font-weight': 'bold',
                'margin-top': '5px', 'display': 'none'}

@app.callback(
    # Map Output
    [dash.dependencies.Output('map', 'figure'),
     # Text Output
     dash.dependencies.Output('text_display', 'children'),
     # Chart Output
     dash.dependencies.Output('chart', 'figure')],
    # Search Bar Inputs
    [dash.dependencies.Input('category-dropdown', 'value'),
     dash.dependencies.Input('search', 'value'),
     dash.dependencies.Input('EASsearch', 'value'),
     dash.dependencies.Input('SUCsearch', 'value'),
     dash.dependencies.Input('ETCsearch', 'value'),
     dash.dependencies.Input('RCsearch', 'value')],
    prevent_initial_call=False
)
def update_figure(selected_category, search, EASsearch, SUCsearch, ETCsearch, RCsearch):

    # Paramaters for Default Communities Category
    if selected_category == 'Community':
        # Show Communties in search bar or show all if nothing is selected in search
        if search is None or len(search) == 0:
            filtered_df = df
        else:
            filtered_df = df[df['Community'].isin(search)]

        map_style = 'dark'
        color_scale = 'tealrose'  # Continuous color scale for map points scaled by population
        text_display = html.H2('Communities'), \
            'The points on this map represent a large sample of poplulated and unpopulated communities throughout the State of Alaska. ' \
            'A community in this context may refer to an outpost, village, town, city, military base, research station, or historic site. ' \
            'The color scale shown by the legend on the right indicates population, with the green points representing populations ' \
            'less than 2000, white points populations between 2000 and 4000, and the rose colored points 4000 people and above. ' \
            'This data was gathered from the \"Community Regions Overview\" table on the State of Alaska Open Data Geoportal, and does not necessarily ' \
            'represent all Alaskan communities. ', \
            html.Br(), html.Br(), \
            'The figure \"Counts of Populated and Unpopulated Communities by Year; 2011-2021\" below tallies the total number of communities on record each given year as recorded in the \"DCCED Certified Population Counts (All Locations)\" table, ' \
            'with counts subdivided between populated and unpopulated communities. ' \
            'Overall there is not a significant change in the recorded number of communities from year to year (This indicates relative completeness of the data) with the exception of 2019, where we can see that most uninhabited communities are absent from the count. ' \
            'It is unlikely that all these places suddenly disappered for a single year only to return the next year. It turns out these communities were not included in the 2019 data, decreasing the overall number of communities on record. ' \
            'This is an example of how most raw data does not come in fully complete or comprehensive forms.'
        # Mapbox Parameters
        fig = px.scatter_mapbox(filtered_df,
                                lat='Latitude',
                                lon='Longitude',
                                color='Population_2021',
                                range_color=[0, 5000],
                                color_continuous_scale=color_scale,  # Unique color parameter
                                labels={'Population_2021': 'Population (2021)', 'Borough_Census_Area': 'Borough',
                                        'Incorporation_Type': 'Incorporation Type',
                                        'Road_Connection': 'Road Connection'},
                                hover_name='Community',
                                hover_data=['Population_2021', 'Borough_Census_Area', 'Incorporation_Type',
                                            'Road_Connection', 'Essential_Air_Service'],
                                center={'lat': 63, 'lon': -152},
                                # size='Population_2021',
                                size_max=30,
                                zoom=3)
        fig.update_layout(mapbox_style=map_style, height=800)

        # Chart Parameters
        chart = px.bar(data_frame=pd.read_csv('data/UninhabitedComms.csv'),
                       x='Year',
                       y='Community Count',
                       color='Status',
                       labels={'Count': 'Community Count', 'Status': 'Population Category'},
                       color_discrete_map={'Uninhabited': 'rgb(204,204,204)',
                                           'Under One Hundred (1-99)': 'rgb(141,211,199)',
                                           'Under One Thousand (100-999)': 'rgb(68,170,153)',
                                           'Over One Thousand (1000+)': 'rgb(204,102,119)'},
                       category_orders={
                           'Status': ['Uninhabited', 'Under One Hundred (1-99)', 'Under One Thousand (100-999)',
                                      'Over One Thousand (1000+)']},
                       title='Counts of Populated and Unpopulated Communities by Year; 2011-2021')
        chart.update_layout(title_x=0.5, title_font_size=22, legend_font_size=16, legend_font_family='Optima')


    elif selected_category == 'Population':
        dff = pd.read_csv('data/Population_Counts.csv')
        if search is None or len(search) == 0:
            filtered_df = dff
        else:
            filtered_df = dff[dff['Community'].isin(search)]
        map_style = 'dark'
        color_scale = 'tealrose'  # Discrete Color Scale for Incorporation Type
        text_display = html.H2('Communities Relative Size'), \
            'The points on this map represent a large sample of poplulated communities in Alaska scaled by their population. A majority of Alaska\'s population is concentrated near the cities and urban areas around Anchorage, Juneau, and Fairbanks. ' \
            'Here you can view each community\'s data point sized proportionally by its population during the given year. Note that uninhabited communities will ' \
            'not be visible on the map. This data was gathered from the \"DCCED Certified Population Counts (All Locations)\" table; population counts are approximate. The chart \"State Population 2000-2022\" below ' \
            'shows the change in the overall state population over the last two decades according to the Census Bureau (census.gov).'

        fig = px.scatter_mapbox(filtered_df,
                                lat='Latitude',
                                lon='Longitude',
                                color='Population',
                                color_continuous_scale=color_scale,  # Unique color parameter
                                size='Population',
                                range_color=[0, 20000],
                                animation_group='Year',
                                animation_frame='Year',
                                labels={'IncorporationType': 'Incorporation Type'},
                                hover_name='Community',
                                hover_data=['Population', 'IncorporationType', 'Source'],
                                center={'lat': 63, 'lon': -152},
                                zoom=3)
        fig.update_layout(mapbox_style=map_style, height=800)

        chart = px.line(data_frame=pd.read_csv('data/State_Population_22yr.csv'),
                        x="Year", y="Population", title="State Population 2000-2022")
        chart.update_layout(title_x=0.5, title_font_size=22, legend_font_size=16, legend_font_family='Optima')

    elif selected_category == 'Incorporation_Type':
        if search is None or len(search) == 0:
            filtered_df = df
        else:
            filtered_df = df[df['Community'].isin(search)]
        map_style = 'dark'
        color_scale = px.colors.qualitative.Prism  # Discrete Color Scale for Incorporation Type
        pie_title = 'Percentage of State Population per City Incorporation Type (2021)'
        pie_color = px.colors.qualitative.Prism
        pie_names = 'Incorporation_Type'  # name parameter for px.pie
        text_display = html.H2('Communities by Incorporation Type'), \
            'The points on this map represent a large sample of communities categorized by their incorporation type. \'City incorporation\' means the creation of a second class, first class, or home rule city government to ' \
            'provide services and facilities at the community level. Click on the incorporation types in the map legend to filter by communities of that type. ' \
            'According to the State of Alaska, \"Each class of city government has broad powers (AS 29.35) and every city also has certain general ' \
            'obligations (e.g., annual audits or financial reports, regular elections, codification of ordinances, ' \
            'regular meetings of the city council, etc.).\" This data was gathered from the \"Community Regions Overview\" table on the State of Alaska Open Data Geoportal. ', \
            html.Br(), html.Br(), \
            'The pie chart \"Percentage of State Population per City Incorporation Type\" below displays the population ' \
            'percentages of Alaskan residents living in communities of each incorporation type (as of 2021) gathered from the \"Community Regions Overview\" table.'

        fig = px.scatter_mapbox(filtered_df,
                                lat='Latitude',
                                lon='Longitude',
                                color='Incorporation_Type',
                                color_discrete_sequence=color_scale,  # Unique color parameter
                                labels={'Population_2021': 'Population (2021)', 'Borough_Census_Area': 'Borough',
                                        'Incorporation_Type': 'Incorporation Type',
                                        'Road_Connection': 'Road Connection'},
                                hover_name='Community',
                                hover_data=['Population_2021', 'Borough_Census_Area', 'Incorporation_Type',
                                            'Road_Connection'],
                                center={'lat': 63, 'lon': -152},
                                zoom=3)
        fig.update_layout(mapbox_style=map_style, height=800)

        chart = px.pie(data_frame=df,
                       values='Population_2021',
                       names=pie_names,
                       color=pie_names,
                       labels={},
                       color_discrete_sequence=pie_color,  # Discrete plotly color sequence
                       title=pie_title,
                       hole=0.2)
        chart.update_layout(title_x=0.5, title_font_size=20, legend_font_size=16, legend_font_family='Optima')

    elif selected_category == 'Subsistence_Use':
        if SUCsearch is None or len(SUCsearch) == 0:
            filtered_df = df[df[selected_category] == 'Yes'] # Only show communities that are subsistence use
        else:
            filtered_df = df[df['Community'].isin(SUCsearch)]
        map_style = 'satellite'
        color_scale = 'Tealgrn'  # Continuous color scale
        pie_title = 'Percentage of State Population Living in Subsistence Use Communities (2021)'
        pie_color = {'Yes': 'NavajoWhite ', 'No': 'LightSlateGray'}
        pie_names = selected_category  # name parameter for px.pie
        text_display = html.H2('Subsistence Use Communities'), \
            'The points on the map represent the Alaskan communities designated as subsistence use according to the table \"Subsistence Use Communities\" as of 2017. ' \
            'Subsistence refers to the harvest, use, and sharing of wild, renewable plant and animal resources for food, ' \
            'shelter, fuel, clothing, tools, or transportation as part of long-standing practices that are an important ' \
            'foundation of Alaska Native cultures (bia.gov). Subsistence Use Communities in Alaska generally refer to ' \
            'areas where a portion of residents are either partially or fully dependent upon subsistence as a means of living. For many Alaskans, subsistence is ' \
            ' an integral part of the community, economy, culture, and way of life (gis.data.alaska.gov). The map style has been changed to a satellite imagery map to add geographical context to this category.', \
            html.Br(), html.Br(), \
            'The pie chart \"Percentage of State Population Living in Subsistence Use Communities\" below displays the percentage of Alaskans ( 2021 population) living in subsistence use communities gathered from the \"Subsistence Use Communities\" table.'

        fig = px.scatter_mapbox(filtered_df,
                                lat='Latitude',
                                lon='Longitude',
                                color='Population_2021',
                                range_color=[0, 5000],
                                color_continuous_scale=color_scale,  # Unique color parameter
                                labels={'Population_2021': 'Population (2021)', 'Borough_Census_Area': 'Borough',
                                        'Incorporation_Type': 'Incorporation Type',
                                        'Road_Connection': 'Road Connection'},
                                hover_name='Community',
                                hover_data=['Population_2021', 'Borough_Census_Area', 'Incorporation_Type',
                                            'Road_Connection', 'Essential_Air_Service'],
                                center={'lat': 63, 'lon': -152},
                                # size='Population_2021',
                                size_max=30,
                                zoom=3)
        fig.update_layout(mapbox_style=map_style, height=800)

        chart = px.pie(data_frame=df,
                       values='Population_2021',
                       names=pie_names,
                       color=pie_names,
                       labels={},
                       color_discrete_map=pie_color,  # Custom color dictionary
                       title=pie_title,
                       hole=0.2)
        chart.update_layout(title_x=0.5, title_font_size=22, legend_font_size=16, legend_font_family='Optima')


    elif selected_category == 'Essential_Air_Service':
        if EASsearch is None or len(EASsearch) == 0:
            filtered_df = df[df[selected_category] == 'Yes'] # Only show communities that are subsistence use
        else:
            filtered_df = df[df['Community'].isin(EASsearch)]
        # filtered_df = df[df[selected_category] == 'Yes']  # Only show communities that are essential air service
        map_style = 'satellite'
        color_scale = 'oryel'  # Continuous color scale
        pie_title = 'Percentage of State Population Living in Essential Air Service Communities (2018)'
        pie_color = {'Yes': 'NavajoWhite ', 'No': 'LightSlateGray'}
        pie_names = selected_category  # name parameter for px.pie
        text_display = html.H2('Essential Air Service Communities'), \
            'The points on the map represent Alaskan communities that participate in the Essential Air Service program as of 2018 according to the \"Essential Air Service Communities\" table. ' \
            'The Essential Air Service (EAS) program was put into place to guarantee that small communities that were ' \
            'served by certificated air carriers before airline deregulation maintain a minimal level of scheduled air ' \
            'service. The United States Department of Transportation is mandated to provide eligible ' \
            'EAS communities with access to the National Air Transportation System. This is generally accomplished by ' \
            'subsidizing two round trips a day with 30- to 50-seat aircraft, or additional frequencies with aircraft ' \
            'with 9-seat or fewer, usually to a large- or medium-hub airport (transportation.gov). The map style has been changed to a satellite imagery map to add geographical context to this category.', \
            html.Br(), html.Br(), \
            'The pie chart \"Percentage of State Population Living in Essential Air Service Communities\" below displays the percentage of Alaskans living in EAS communities as of 2018 according to the \"Essential Air Service Communities\".'

        fig = px.scatter_mapbox(filtered_df,
                                lat='Latitude',
                                lon='Longitude',
                                color='Population_2021',
                                range_color=[0, 5000],
                                color_continuous_scale=color_scale,  # Unique color parameter
                                labels={'Population_2021': 'Population (2021)', 'Borough_Census_Area': 'Borough',
                                        'Incorporation_Type': 'Incorporation Type',
                                        'Road_Connection': 'Road Connection'},
                                hover_name='Community',
                                hover_data=['Population_2021', 'Borough_Census_Area', 'Incorporation_Type',
                                            'Road_Connection', 'Essential_Air_Service'],
                                center={'lat': 63, 'lon': -152},
                                # size='Population_2021',
                                size_max=30,
                                zoom=3)
        fig.update_layout(mapbox_style=map_style, height=800)

        chart = px.pie(data_frame=df,
                       values='Population_2021',
                       names=pie_names,
                       color=pie_names,
                       labels={},
                       color_discrete_map=pie_color,  # Custom color dictionary
                       title=pie_title,
                       hole=0.2)
        chart.update_layout(title_x=0.5, title_font_size=22, legend_font_size=16, legend_font_family='Optima')


    elif selected_category == 'Environmentally_Threatened':
        dff = pd.read_csv('data/ThreatenedComms.csv')
        if ETCsearch is None or len(ETCsearch) == 0:
            filtered_df = dff # Only show communities that are subsistence use
        else:
            filtered_df = dff[dff['Community'].isin(ETCsearch)]
        #filtered_df = pd.read_csv('data/ThreatenedComms.csv')  # Only show communities that are environmentally threatened
        map_style = 'satellite-streets'
        color_scale = 'Tealgrn'  # Continuous color scale
        pie_title = 'Percentage of State Population Living living in Environmentally Threatened Communities (2021)'
        pie_color = {'Yes': 'NavajoWhite ', 'No': 'LightSlateGray'}
        pie_names = selected_category  # name parameter for px.pie
        text_display = html.H2('Environmentally Threatened Communities'), \
            'The points on the map represent Alaskan communities identified as highly vulnerable to erosion, flooding and permafrost ' \
            'degradation in the Denali Commissions 2019 Statewide Threat Assessment conducted by the US Army Corps of ' \
            'Engineers and the University of Alaska Fairbanks (gis.data.alaska.gov). Where available, each threatened community has individual rankings for erosion, flooding, and permafrost degradation risk, along with a summary of hazards. ' \
            'This data was gathered from the \"Environmentally Threatened Communities\" table on the State of Alaska Open Data Geoportal. The map style has been changed to a satellite imagery map to add geographical context to this category.', \
            html.Br(), html.Br(), \
            'The pie chart \"Percentage of State Population Living living in Environmentally Threatened Communities\" below displays the percentage of Alaskans living in environmentally threatened communities as of 2020. '

        fig = px.scatter_mapbox(filtered_df,
                                lat='Latitude',
                                lon='Longitude',
                                color='2021_Population',
                                color_continuous_scale=color_scale,
                                labels={'2021_Population': 'Population (2021)', 'Borough_Census_Area': 'Borough',
                                        'Incorporation_Type': 'Incorporation Type',
                                        'Road_Connection': 'Road Connection'},
                                hover_name='Community',
                                hover_data=['2021_Population', 'Borough_Census_Area', 'Incorporation_Type',
                                            'Road_Connection', 'Erosion Ranking', 'Flood Ranking', 'Permafrost Ranking',
                                            'Key Hazard Threat'],
                                center={'lat': 63, 'lon': -152},
                                zoom=3)
        fig.update_layout(mapbox_style=map_style, height=800)

        chart = px.pie(data_frame=df,
                       values='Population_2021',
                       names=pie_names,
                       color=pie_names,
                       labels={},
                       color_discrete_map=pie_color,  # Custom color dictionary
                       title=pie_title,
                       hole=0.2)
        chart.update_layout(title_x=0.5, title_font_size=22, legend_font_size=16, legend_font_family='Optima')


    elif selected_category == 'Road_Connection':
        if RCsearch is None or len(RCsearch) == 0:
            filtered_df = df[df['Road_Connection'].notnull()]
        else:
            filtered_df = df[df['Community'].isin(RCsearch)]
        map_style = 'satellite-streets'
        pie_title = 'Percentage of State Population With Access to the Road System (2021)'
        pie_color = {'Yes': 'Orange', 'No': 'Crimson'}
        pie_names = selected_category
        text_display = html.H2('Road Connection by Community'), \
            'The points on the map represent Alaskan communities categorized by their access to the state road system as designated in the \"Road Connection in Community\" table. The \'road system\' in this case ' \
            'refers to the state roads which link communities to all major ' \
            'population centers in the state. This road system also includes the Alcan Highway which passes into Canada and eventually' \
            ' connects Alaska to Canada and the lower 48 states. Air, sea, and river are the main alternative modes of access to communities without road connection. The map style has been changed to a satellite imagery map to add geographical context.', \
            html.Br(), html.Br(), \
            'The pie chart \"Percentage of State Population With Access to the Road System\" below displays the percentage of Alaskans living in communities with access to the road system (as of 2021). '

        fig = px.scatter_mapbox(filtered_df,
                                lat='Latitude',
                                lon='Longitude',
                                color='Road_Connection',
                                color_discrete_map={'Yes': 'Orange ', 'No': 'Crimson'},  # Unique color parameter
                                labels={'Population_2021': 'Population (2021)', 'Borough_Census_Area': 'Borough',
                                        'Incorporation_Type': 'Incorporation Type',
                                        'Road_Connection': 'Road Connection'},
                                hover_name='Community',
                                hover_data=['Population_2021', 'Borough_Census_Area', 'Incorporation_Type',
                                            'Road_Connection'],
                                center={'lat': 63, 'lon': -152},
                                zoom=3)
        fig.update_layout(mapbox_style=map_style, height=800)

        chart = px.pie(data_frame=df,
                       values='Population_2021',
                       names=pie_names,
                       color=pie_names,
                       labels={},
                       color_discrete_map=pie_color,  # Custom color dictionary
                       title=pie_title,
                       hole=0.2)
        chart.update_layout(title_x=0.5, title_font_size=22, legend_font_size=16, legend_font_family='Optima')
    # Display Map
    # px.scatter_mapbox functions aren't combined because each as a unique color parameter

    return fig, text_display, chart


# Run App
if __name__ == '__main__':
    app.run_server(debug=True)
