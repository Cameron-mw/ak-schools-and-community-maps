import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd

# Import CSV Data
df = pd.read_csv('data/Schools.csv')
schools = df['School'].unique()

# Mapbox Access Key
px.set_mapbox_access_token('pk.eyJ1IjoiY2FtZXJvbndvb2R3YXJkIiwiYSI6ImNsZ3BwcnBmbTByZGszZmxoMnR4aHpwY2UifQ.Tc8mGP995suKvJwI9wBxeg')
#px.set_mapbox_access_token(open('assets/mapbox_access_token','r'))

# Dash App Name
app = dash.Dash(__name__)

app.layout = html.Div([
    # Title
    html.Div(html.H1('Alaskan Schools'), style={'fontSize': 20, 'font-family': 'Optima', 'text-align': 'center'}),

    # Dropdown Menu
    dcc.Dropdown(
        id='category-dropdown',
        options=[
            {'label':'Schools','value':'School'},
            {'label':'Schools Scaled by Enrollment','value': 'TotalEnrollmentK12'},
            {'label':'Student Teacher Ratios by School','value': 'StudentTeacherRatio'},
            {'label':'High Schools','value': 'Is_HighSchool'},
            {'label':'High School Graduation Rates', 'value': 'Graduates'},
            {'label':'High School Graduation Rates Scaled by Enrollment','value': 'GraduationRate'}
        ],
        value='School', # Set as Default Selection
        style={'fontSize': 20, 'font-family': 'Optima','text-align': 'center', 'font-weight': 'bold'},
        searchable=False,
        multi=False
    ),

    # Search Bar
    dcc.Dropdown(
        id='search',
        options=[{'label': school,'value': school} for school in schools],
        placeholder='— Filter by School —',
        value=None, # Set as Default Selection
        style={'fontSize': 20, 'font-family': 'Optima','text-align': 'center', 'font-weight': 'bold', 'margin-top' : '5px'},
        searchable=True,
        multi=True
    ),

    # Map layout
    dcc.Graph(id='map',
              style={'font-family': 'Optima'}),

    # Text Box Layout
    html.Div(id='text_display', children=['text_display'],
             style={'fontSize': 20, 'font-family': 'Optima', 'margin-top' : '-20px', 'margin-left':'100px',
                    'text-align' : 'center', 'width' : '40%', "border":{"width":"2px", "color":"black"}}),

])

@app.callback(
    # Map Output
    [dash.dependencies.Output('map', 'figure'),
    # Text Output
    dash.dependencies.Output('text_display', 'children')],
    [dash.dependencies.Input('category-dropdown', 'value'),
     dash.dependencies.Input('search', 'value')]
)

def update_figure(selected_category, search):
    # Paramaters for map showing all Schools
    if selected_category == 'School':
        if search is None or len(search) == 0:
            filtered_df = df
        else:
            filtered_df = df[df['School'].isin(search)]
        # filtered_df = df
        map_style = 'dark'
        color_scale = px.colors.qualitative.Prism
        #color_scale = 'tealrose' # Continuous color scale for map points scaled by population
        text_display = html.H2('Alaskan Schools'),\
            'The points on this map represent a large sample of the public schools on record in Alaska during a given year. The \'Year\' varibale here corresponds to the year in which an academic year is concluded. For example, \'2013\' refers to the 2012-2013 school year. The schools represented on this map ' \
            'are either primary (elementary) schools, intermediate (middle) schools, secondary (high) schools, or some ' \
            'combination of the three, and are color coded by their respective school districts. There are many schools in rural or remote communities in Alaska whose student bodies ' \
            'range in grade from Kindergarten through eighth grade or through twelth grade. The large student age-range in schools like these this might ' \
            'be considered a unique feature of rural communities compared to more populated areas, and because of this we will consider a school to be a high school if has a nonzero 9-12 Enrollment number. ' \
            'This data was gathered from the State of Alaska Open Data Geoportal, and does not ' \
            'represent all Alaskan schools.'

    elif selected_category == 'TotalEnrollmentK12':
        if search is None or len(search) == 0:
            filtered_df = df[df[selected_category].notnull()]
        else:
            filtered_df = df[df['School'].isin(search)]
        #filtered_df = df[df[selected_category].notnull()]
        map_style = 'dark'
        color_scale = 'tealrose'
        text_display = html.H2('Schools Relative Size'), \
        'The points on this map represent a large sample of the public schools on record in Alaska during a given year where ' \
        'point-size and color are scaled by K-12 Enrollment.'

    elif selected_category == 'StudentTeacherRatio':
        if search is None or len(search) == 0:
            filtered_df = df[df[selected_category].notnull()]
        else:
            filtered_df = df[df['School'].isin(search)]
        #filtered_df = df[df[selected_category].notnull()]
        map_style = 'light'
        color_scale = 'Rainbow'
        text_display = html.H2('Student Teacher Ratios by School'), \
        'The points on this map represent a large sample of the public schools on record in Alaska during a given year where ' \
        'point-color is scaled by Student Teacher Ratio. Student Teacher Ratio is defined as the total number of students divided by the total number of teachers in a given school.'

    elif selected_category == 'Is_HighSchool':
        if search is None or len(search) == 0:
            filtered_df = df[df[selected_category].notnull()]
        else:
            filtered_df = df[df['School'].isin(search)]
        #filtered_df = df[df[selected_category].notnull()]
        map_style = 'dark'
        color_scale = 'tealrose'
        text_display = html.H2('Schools with Grade 9-12 Enrollment'), \
        'The points on this map differentiate between schools with high school (9-12) enrollment, and those with only K-8 enrollment ' \
        'for the given year. Due to the age diversity present in many Alaskan schools, we will consider a school to be a high school if has a nonzero 9-12 Enrollment.'

    elif selected_category == 'Graduates':
        if search is None or len(search) == 0:
            filtered_df = df[df['GraduationRate'].notnull()]
        else:
            dff = df[df['School'].isin(search)]
            filtered_df = dff[dff['GraduationRate'].notnull()]
        #filtered_df = df[df['GraduationRate'].notnull()]
        map_style = 'dark'
        color_scale = 'rdbu'
        text_display = html.H2('High School Graduation Rates'), \
        'The points on this map represent schools that have a high school gradution rate during the given year, and are color scaled by graduation rate.'

    elif selected_category == 'GraduationRate':
        if search is None or len(search) == 0:
            filtered_df = df[df[selected_category].notnull()]
        else:
            dff = df[df['School'].isin(search)]
            filtered_df = dff[dff['GraduationRate'].notnull()]
        #filtered_df = df[df[selected_category].notnull()]
        map_style = 'dark'
        color_scale = 'rdbu'
        text_display = html.H2('High School Graduation Rates with Relative Size'), \
        'The points on this map represent a large sample of the public schools on record in Alaska during a given year where' \
        'point color is scaled by high school graduation rate and size is scaled by high school enrollment.'

    col_labels = {'SchoolDistrict': 'School District', 'In_Cohort':'In Cohort','GraduationRate':'Graduation Rate',
                  'K8Enrollment':'K-8 Enrollment', 'HSEnrollment':'9-12 Enrollment',
                  'TotalEnrollmentK12':'K-12 Total Enrollment', 'Is_HighSchool':'Is High School?',
                  'TotalTeacherCount':'Total Teacher Count', 'StudentTeacherRatio':'Student Teacher Ratio'}

    if selected_category == 'School':
        fig = px.scatter_mapbox(filtered_df,
                                lat='Latitude',
                                lon='Longitude',
                                color='SchoolDistrict',
                                color_discrete_sequence=color_scale,  # Unique color parameter
                                animation_frame='Year',
                                animation_group='Year',
                                range_color=[0, 2000],
                                labels=col_labels,
                                hover_name='School',
                                hover_data=['Community', 'SchoolDistrict', 'Year', 'K8Enrollment', 'HSEnrollment', 'TotalEnrollmentK12', 'TotalTeacherCount'],
                                center={'lat': 63, 'lon': -152},
                                zoom=3)
        fig.update_layout(mapbox_style=map_style, height=800)

    elif selected_category == 'TotalEnrollmentK12':
        fig = px.scatter_mapbox(filtered_df,
                                lat='Latitude',
                                lon='Longitude',
                                color='TotalEnrollmentK12',
                                color_continuous_scale=color_scale,  # Unique color parameter
                                size='TotalEnrollmentK12',
                                animation_frame='Year',
                                animation_group='Year',
                                range_color=[0, 2000],
                                labels=col_labels,
                                hover_name='School',
                                hover_data=['Community', 'SchoolDistrict', 'Year', 'K8Enrollment', 'HSEnrollment', 'TotalEnrollmentK12','TotalTeacherCount'],
                                center={'lat': 63, 'lon': -152},
                                zoom=3)
        fig.update_layout(mapbox_style=map_style, height=800)

    elif selected_category == 'StudentTeacherRatio':
        fig = px.scatter_mapbox(filtered_df,
                                lat='Latitude',
                                lon='Longitude',
                                color='StudentTeacherRatio',
                                color_continuous_scale=color_scale,  # Unique color parameter
                                animation_frame='Year',
                                animation_group='Year',
                                range_color=[0, 50],
                                labels=col_labels,
                                hover_name='School',
                                hover_data=['Community', 'SchoolDistrict','StudentTeacherRatio', 'Year','K8Enrollment', 'HSEnrollment', 'TotalEnrollmentK12', 'TotalTeacherCount'],
                                center={'lat': 63, 'lon': -152},
                                zoom=3)
        fig.update_layout(mapbox_style=map_style, height=800)

    elif selected_category == 'Is_HighSchool':
        fig = px.scatter_mapbox(filtered_df,
                                lat='Latitude',
                                lon='Longitude',
                                color='Is_HighSchool',
                                color_discrete_map={'Yes': 'Orange ', 'No': 'Gray'},  # Unique color parameter
                                animation_frame='Year',
                                animation_group='Year',
                                range_color=[0, 2000],
                                labels=col_labels,
                                hover_name='School',
                                hover_data=['Community', 'SchoolDistrict', 'Year', 'K8Enrollment', 'HSEnrollment', 'TotalEnrollmentK12', 'Is_HighSchool', 'TotalTeacherCount'],
                                center={'lat': 63, 'lon': -152},
                                zoom=3)
        fig.update_layout(mapbox_style=map_style, height=800)

    elif selected_category == 'Graduates':
        fig = px.scatter_mapbox(filtered_df,
                                lat='Latitude',
                                lon='Longitude',
                                color='GraduationRate',
                                color_continuous_scale=color_scale,  # Unique color parameter
                                animation_frame='Year',
                                animation_group='Year',
                                range_color=[0, 1],
                                labels=col_labels,
                                hover_name='School',
                                hover_data=['Community', 'SchoolDistrict', 'Year', 'In_Cohort','Graduates','GraduationRate','K8Enrollment', 'HSEnrollment', 'TotalEnrollmentK12', 'TotalTeacherCount'],
                                center={'lat': 63, 'lon': -152},
                                zoom=3)
        fig.update_layout(mapbox_style=map_style, height=800)

    elif selected_category == 'GraduationRate':
        fig = px.scatter_mapbox(filtered_df,
                                lat='Latitude',
                                lon='Longitude',
                                color='GraduationRate',
                                color_continuous_scale=color_scale,  # Unique color parameter
                                size='HSEnrollment',
                                animation_frame='Year',
                                animation_group='Year',
                                range_color=[0, 1],
                                labels=col_labels,
                                hover_name='School',
                                hover_data=['Community', 'SchoolDistrict', 'Year', 'In_Cohort','Graduates','GraduationRate','K8Enrollment', 'HSEnrollment', 'TotalEnrollmentK12', 'TotalTeacherCount'],
                                center={'lat': 63, 'lon': -152},
                                zoom=3)
        fig.update_layout(mapbox_style=map_style, height=800)
    return fig, text_display

    # Run App
if __name__ == '__main__':
    app.run_server(debug=True)
