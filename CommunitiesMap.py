import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd

# Import CSV Data
df = pd.read_csv('data/Communities.csv')
comms = df['Community'].unique()

# Mapbox Access Key
px.set_mapbox_access_token(
    'pk.eyJ1IjoiY2FtZXJvbndvb2R3YXJkIiwiYSI6ImNsZ3BwcnBmbTByZGszZmxoMnR4aHpwY2UifQ.Tc8mGP995suKvJwI9wBxeg')
# px.set_mapbox_access_token(open('assets/mapbox_access_token','r'))

# Dash App Name
app = dash.Dash(__name__)

app.layout = html.Div([
    # Title
    html.Div(html.H1('Alaskan Communities'), style={'fontSize': 20, 'font-family': 'Optima', 'text-align': 'center'}),

    # Dropdown Menu
    dcc.Dropdown(
        id='category-dropdown',
        options=[
            {'label': 'All Communities', 'value': 'Communities'},  # Default Selection
            {'label': 'Communities Scaled by Population', 'value': 'Population'},
            {'label': 'Incorporation Types', 'value': 'Incorporation_Type'},
            {'label': 'Subsistence Use Communities', 'value': 'Subsistence_Use'},
            {'label': 'Essential Air Service Communities', 'value': 'Essential_Air_Service'},
            {'label': 'Environmentally Threatened Communities', 'value': 'Environmentally_Threatened'},
            {'label': 'Road System Connection', 'value': 'Road_Connection'}
        ],
        value='Communities',  # Set as Default Selection
        style={'fontSize': 20, 'font-family': 'Optima', 'text-align': 'center', 'font-weight': 'bold'},
        searchable=False,
        multi=False
    ),

    # Search Bar
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

    # Map layout
    dcc.Graph(id='map',
              style={'font-family': 'Optima'}),

    # Text Box Layout
    html.Div(id='text_display', children=['text_display'],
             style={'fontSize': 20, 'font-family': 'Optima', 'margin-top': '-20px', 'margin-left': '100px',
                    'text-align': 'center', 'width': '40%', "border": {"width": "2px", "color": "black"}}),

    # Pie Chart Layout
    dcc.Graph(id='chart',
              style={'fontSize': 24, 'font-family': 'Optima', 'text-align': 'center',
                     'width': '40%', 'padding-left': '50%', 'position': 'relative'})
])


# @app.callback(
#     [dash.dependencies.Output('search', 'options')],
#     [dash.dependencies.Input('category-dropdown', 'value')]
# )
# def update_search(selected_category):
#     print(selected_category)
#     if selected_category in ['Subsistence_Use', 'Essential_Air_Service', 'Environmentally_Threatened']:
#         filter_list = df[df[selected_category] == 'Yes']
#     else:
#         filter_list = df
#
#     return [{'label': comm, 'value': comm} for comm in filter_list]


@app.callback(
    # Map Output
    [dash.dependencies.Output('map', 'figure'),
     # Text Output
     dash.dependencies.Output('text_display', 'children'),
     # Pie Chart Output
     dash.dependencies.Output('chart', 'figure')],
    [dash.dependencies.Input('category-dropdown', 'value'),
     dash.dependencies.Input('search', 'value')],
    prevent_initial_call=False
)
def update_figure(selected_category, search):
    # if selected_category == 'Environmentally_Threatened':
    #     print('filtered')
    #     filter_list = df[df[selected_category] == 'Yes']
    #     options = [{'label': comm, 'value': comm} for comm in filter_list]
    #     return {'options': options}
    # else:
    #     print('not filtered')
    #     return [{'label': comm, 'value': comm} for comm in df]

    # Paramaters for map showing all Communities
    if selected_category == 'Communities':
        if search is None or len(search) == 0:
            filtered_df = df
        else:
            filtered_df = df[df['Community'].isin(search)]
        # filtered_df = df
        map_style = 'dark'
        color_scale = 'tealrose'  # Continuous color scale for map points scaled by population
        pie_title = 'Percentage of State Population per City Incorporation Type'
        pie_color = px.colors.qualitative.Prism
        pie_names = 'Incorporation_Type'  # name parameter for px.pie
        text_display = html.H2('Communities'), \
            'The points on this map represent a large sample of poplulated and unpopulated communities throughout the State of Alaska. ' \
            'The color scale shown by the legend on the right indicates population, with the green points representing populations ' \
            'less than 2000, white points populations between 2000 and 4000, and the rose colored points 4000 people and above. ' \
            'A community in this context may refer to an outpost, village, town, city, military base, research station, or historic site. ' \
            '"City incorporation" means the creation of a second class, first class, or home rule city government to ' \
            'provide services and facilities at the community level. ' \
            'This data was gathered from the State of Alaska Open Data Geoportal, and may not necessarily ' \
            'represent all Alaskan communities.'

    elif selected_category == 'Population':
        dff = pd.read_csv('data/Population_Counts.csv')
        if search is None or len(search) == 0:
            filtered_df = dff
        else:
            filtered_df = dff[dff['Community'].isin(search)]
        map_style = 'dark'
        color_scale = 'tealrose'  # Discrete Color Scale for Incorporation Type
        text_display = html.H2('Communities Relative Size'), \
            'A majority of Alaska`s population is concentrated near the cities and urban areas around Anchorage, Juneau, and Fairbanks. ' \
            'Here you can view each community`s data point sized proportionally by its population. Note that uninhabited communities will ' \
            'not be visible on the map. Population counts are approximate ' \
            'and may not be exact.'

    # Parameters for map showing all Communities by Incorporation Type
    elif selected_category == 'Incorporation_Type':
        if search is None or len(search) == 0:
            filtered_df = df
        else:
            filtered_df = df[df['Community'].isin(search)]
        # filtered_df = df
        map_style = 'dark'
        color_scale = px.colors.qualitative.Prism  # Discrete Color Scale for Incorporation Type
        pie_title = 'Percentage of State Population per City Incorporation Type'
        pie_color = px.colors.qualitative.Prism
        pie_names = 'Incorporation_Type'  # name parameter for px.pie
        text_display = html.H2('Communities by Incorporation Type'), \
            '\'City incorporation\' means the creation of a second class, first class, or home rule city government to ' \
            'provide services and facilities at the community level. ' \
            'Each class of city government has broad powers (AS 29.35) and every city also has certain general ' \
            'obligations (e.g., annual audits or financial reports, regular elections, codification of ordinances, ' \
            'regular meetings of the city council, etc.) '

    elif selected_category == 'Subsistence_Use':
        if search is None or len(search) == 0:
            filtered_df = df[df[selected_category] == 'Yes']
        else:
            filtered_df = df[df['Community'].isin(search)]
        # filtered_df = df[df[selected_category] == 'Yes'] # Only show communities that are subsistence use
        map_style = 'satellite'
        color_scale = 'oryel'  # Continuous color scale
        pie_title = 'Percentage of State Population Living in Subsistence Use Communities'
        pie_color = {'Yes': 'NavajoWhite ', 'No': 'LightSlateGray'}
        pie_names = selected_category  # name parameter for px.pie
        text_display = html.H2('Subsistence Use Communities'), \
            'Subsistence refers to the harvest, use, and sharing of wild, renewable plant and animal resources for food,' \
            ' shelter, fuel, clothing, tools, or transportation as part of long-standing practices that are an important' \
            ' foundation of Alaska Native cultures (bia.gov). Subsistence Use Communities in Alaska generally refer to ' \
            'areas where a portion of residents are either partially or fully dependent upon subsistence as a means of living. For many Alaskans, subsistence is ' \
            ' an integral part of the community, economy, culture, and way of life (gis.data.alaska.gov).'

    elif selected_category == 'Essential_Air_Service':
        filtered_df = df[df[selected_category] == 'Yes']  # Only show communities that are essential air service
        map_style = 'satellite'
        color_scale = 'oryel'  # Continuous color scale
        pie_title = 'Percentage of State Population Living in Essential Air Service Communities'
        pie_color = {'Yes': 'NavajoWhite ', 'No': 'LightSlateGray'}
        pie_names = selected_category  # name parameter for px.pie
        text_display = html.H2('Essential Air Service Communities'), \
            'These are the Alaskan communities that participate in the Essential Air Service program. ' \
            'The Essential Air Service (EAS) program was put into place to guarantee that small communities that were ' \
            'served by certificated air carriers before airline deregulation maintain a minimal level of scheduled air ' \
            'service. The United States Department of Transportation is mandated to provide eligible ' \
            'EAS communities with access to the National Air Transportation System. This is generally accomplished by ' \
            'subsidizing two round trips a day with 30- to 50-seat aircraft, or additional frequencies with aircraft ' \
            'with 9-seat or fewer, usually to a large- or medium-hub airport (transportation.gov).'

    elif selected_category == 'Environmentally_Threatened':
        filtered_df = df[df[selected_category] == 'Yes']  # Only show communities that are environmentally threatened
        map_style = 'satellite-streets'
        color_scale = 'oryel'  # Continuous color scale
        pie_title = 'Percentage of State Population Living living in Environmentally Threatened Communities'
        pie_color = {'Yes': 'NavajoWhite ', 'No': 'LightSlateGray'}
        pie_names = selected_category  # name parameter for px.pie
        text_display = html.H2('Environmentally Threatened Communities'), \
            'These are the Alaskan communities identified as highly vulnerable to erosion, flooding and permafrost ' \
            'degradation in the Denali Commissions 2019 Statewide Threat Assessment conducted by the US Army Corps of ' \
            'Engineers and the University of Alaska Fairbanks (gis.data.alaska.gov).'

    elif selected_category == 'Road_Connection':
        filtered_df = df[df[selected_category].notnull()]  # Don't include any null values in Road_Connection
        map_style = 'satellite-streets'
        pie_title = 'Percentage of State Population With Access to the Road System'
        pie_color = {'Yes': 'Orange', 'No': 'Crimson'}
        pie_names = selected_category
        text_display = html.H2('Road Connection by Community'), \
            'These are communities filtered by thier connection to the road system in Alaska. The "road system" in this case ' \
            'can be thought of as the roads which link communities with the highways in Alaska that reach all major ' \
            'population centers in the state. This also includes the Alcan Highway which passes into Canada and eventually' \
            'connects to the lower 48 states.'

    # Display Map
    # px.scatter_mapbox functions aren't combined because each as a unique color parameter
    if selected_category == 'Road_Connection':
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

    elif selected_category == 'Population':
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

    elif selected_category == 'Incorporation_Type':
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

    else:
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
                                            'Road_Connection'],
                                center={'lat': 63, 'lon': -152},
                                # size='Population_2021',
                                size_max=30,
                                zoom=3)
        fig.update_layout(mapbox_style=map_style, height=800)

    # Pie Chart for default dropdown selection
    if selected_category == 'Communities' or selected_category == 'Incorporation_Type':
        chart = px.pie(data_frame=df,
                       values='Population_2021',
                       names=pie_names,
                       color=pie_names,
                       labels={},
                       color_discrete_sequence=pie_color,  # Discrete plotly color sequence
                       title=pie_title,
                       hole=0.2)

    elif selected_category == 'Population':
        chart = px.line(data_frame=pd.read_csv('data/State_Population_22yr.csv'),
                        x="Year", y="Population", title="State Population 2000-2022")

    else:
        chart = px.pie(data_frame=df,
                       values='Population_2021',
                       names=pie_names,
                       color=pie_names,
                       labels={},
                       color_discrete_map=pie_color,  # Custom color dictionary
                       title=pie_title,
                       hole=0.2)

    return fig, text_display, chart


# Run App
if __name__ == '__main__':
    app.run_server(debug=True)
