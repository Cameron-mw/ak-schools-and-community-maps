import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd

# Import CSV Data
df = pd.read_csv("data/Communities.csv")

# Mapbox Access Key
px.set_mapbox_access_token("pk.eyJ1IjoiY2FtZXJvbndvb2R3YXJkIiwiYSI6ImNsZ3BwcnBmbTByZGszZmxoMnR4aHpwY2UifQ.Tc8mGP995suKvJwI9wBxeg")
#px.set_mapbox_access_token(open('assets/Access_token.py','r'))

# Dash App Name
app = dash.Dash(__name__)

app.layout = html.Div([
    # Title
    html.H1('Alaskan Communities'),
    # Dropdown Menu
    dcc.Dropdown(
        id='category-dropdown',
        options=[
            {'label':'All Communities','value':'Communities'}, # Default Selection
            {'label':'Subsistence Use Communities','value':'Subsistence_Use'},
            {'label':'Essential Air Service Communities','value':'Essential_Air_Service'},
            {'label':'Environmentally Threatened Communities','value':'Environmentally_Threatened'}
        ],
        value='Communities', # Set as Default Selection
        multi=False
    ),
    # Display Map
    dcc.Graph(id='map'),
    # Display Text
    html.Div(id='text_display', children=['text_display'], style={'fontSize': 20,
            'margin-top' : '-30px', 'text-align' : 'center', 'width' : '40%'}) # Text Beneath Map
])

@app.callback(
    # Map Output
    [dash.dependencies.Output('map', 'figure'),
    # Text Output
    dash.dependencies.Output('text_display', 'children')],
    [dash.dependencies.Input('category-dropdown', 'value')],
    prevent_initial_call=False
)

def update_figure(selected_category):
    if selected_category == 'Communities': # Default Map showing all Communities
        filtered_df = df
        text_display = html.H2('All Communities'),\
            'The points on this map represent both poplulated and unpopulated communities throughout the state of Alaska. ' \
            'A community in this context may refer to an outpost, village, town, city, military base, or historic site. ' \
            'Many rural Alaskan communities are not connected to the Alaska Highway system. ' \
            'This data was gathered from the State of Alaska Open Data Geoportal, and is not not necessarily representative ' \
            'of all Alaskan communities, but rather a sample of them.'

    elif selected_category == 'Subsistence_Use':
        filtered_df = df[df[selected_category] == 1] # Only show communities that are subsistence use
        text_display = html.H2('Subsistence Use Communities'), \
            'Subsistence refers to the harvest, use, and sharing of wild, renewable plant and animal resources for food,' \
            ' shelter, fuel, clothing, tools, or transportation as part of long-standing practices that are an important' \
            ' foundation of Alaska Native cultures (bia.gov). Subsistence Communities refer to areas that are ' \
            'dependent upon subsistence as an integral part of the community, economy, culture, and way of life (gis.data.alaska.gov).' \

    elif selected_category == 'Essential_Air_Service':
        filtered_df = df[df[selected_category] == 1] # Only show communities that are essential air service
        text_display = html.H2('Essential Air Service Communities'), \
            'These are the Alaskan communities that participate in the Essential Air Service program. ' \
            'The Essential Air Service (EAS) program was put into place to guarantee that small communities that were ' \
            'served by certificated air carriers before airline deregulation maintain a minimal level of scheduled air ' \
            'service. The United States Department of Transportation is mandated to provide eligible ' \
            'EAS communities with access to the National Air Transportation System. This is generally accomplished by ' \
            'subsidizing two round trips a day with 30- to 50-seat aircraft, or additional frequencies with aircraft ' \
            'with 9-seat or fewer, usually to a large- or medium-hub airport (transportation.gov).'

    elif selected_category == 'Environmentally_Threatened':
        filtered_df = df[df[selected_category] == 1] # Only show communities that are environmentally threatened
        text_display = html.H2('Environmentally Threatened Communities'), \
            'These are the Alaskan communities identified as highly vulnerable to erosion, flooding and permafrost ' \
            'degradation in the Denali Commissions 2019 Statewide Threat Assessment conducted by the US Army Corps of ' \
            'Engineers and the University of Alaska Fairbanks (gis.data.alaska.gov).'

    # Display Map
    fig = px.scatter_mapbox(filtered_df,
                            lat="Latitude",
                            lon="Longitude",
                            hover_name="Community",
                            hover_data=["2021_Population","Borough_Census_Area","Incorporation_Type"],
                            center={'lat': 63, 'lon': -152},
                            zoom=3)
    fig.update_layout(mapbox_style="dark", height=750)

    return fig, text_display

if __name__=='__main__':
    app.run_server(debug=True)

