import os
import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
from dotenv import load_dotenv

# Import CSV Data
df = pd.read_csv('data/Schools.csv')
schools = df['School'].unique()
high_schools = df[df['GraduationRate'].notnull()]['School'].unique()

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

    # Default Search Bar
    dcc.Dropdown(
        id='search',
        options=[{'label': school,'value': school} for school in schools],
        placeholder='— Filter by School —',
        value=None, # Set as Default Selection
        style={'fontSize': 20, 'font-family': 'Optima','text-align': 'center', 'font-weight': 'bold', 'margin-top' : '5px'},
        searchable=True,
        multi=True
    ),

    # High Schools Search Bar
    dcc.Dropdown(
        id='HSsearch',
        options=[{'label': school, 'value': school} for school in high_schools],
        placeholder='— Filter by School —',
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
             style={'fontSize': 24, 'font-family': 'Optima', 'line-height': 40, 'margin-top': '20px', 'padding-left': '250px', 'padding-right': '250px',
                    'text-align': 'center', 'position': 'relative'}),

    # Chart Layout
    dcc.Graph(id='chartA',
              style={'fontSize': 36, 'font-family': 'Optima', 'text-align': 'center', 'padding-top': '40px',
                      'padding-left': '20px', 'padding-right': '20px',
                      'position': 'relative', 'align-content': 'center', 'font-weight' : 'bold'})
])

# Default Search Bar Callback
@app.callback(
   dash.dependencies.Output(component_id='search', component_property='style'),
   [dash.dependencies.Input(component_id='category-dropdown', component_property='value')]
)
def show_hide_element(school):
    if school == 'Graduates' or school == 'GraduationRate':
        return {'fontSize': 20, 'font-family': 'Optima', 'text-align': 'center', 'font-weight': 'bold',
               'margin-top': '5px', 'display': 'none'}
    else:
        return {'fontSize': 20, 'font-family': 'Optima', 'text-align': 'center', 'font-weight': 'bold',
                'margin-top': '5px', 'display': 'block'}
# High School Search Bar Callback
@app.callback(
   dash.dependencies.Output(component_id='HSsearch', component_property='style'),
   [dash.dependencies.Input(component_id='category-dropdown', component_property='value')]
)
def show_hide_element(school):
    if school == 'Graduates' or school == 'GraduationRate':
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
     dash.dependencies.Output('chartA', 'figure')],
    # Search Bar Inputs
    [dash.dependencies.Input('category-dropdown', 'value'),
     dash.dependencies.Input('search', 'value'),
     dash.dependencies.Input('HSsearch', 'value')]
)

def update_figure(selected_category, search, HSsearch):
    # Paramaters for map showing all Schools
    global pie_names

    StudentSums = pd.read_csv('data/TotalStudentCounts.csv')

    y = ['Kindergarten', 'First Grade', 'Second Grade',
         'Third Grade', 'Fourth Grade', 'Fifth Grade', 'Sixth Grade',
         'Seventh Grade', 'Eighth Grade', 'Ninth Grade', 'Tenth Grade',
         'Eleventh Grade', 'Twelfth Grade']

    col_labels = {'SchoolDistrict': 'School District', 'In_Cohort': 'In Cohort', 'GraduationRate': 'Graduation Rate',
                  'K8Enrollment': 'K-8 Enrollment', 'HSEnrollment': '9-12 Enrollment',
                  'TotalEnrollmentK12': 'K-12 Total Enrollment', 'Is_HighSchool': 'Is High School?',
                  'TotalTeacherCount': 'Total Teacher Count', 'StudentTeacherRatio': 'Student Teacher Ratio'}

    if selected_category == 'School':
        if search is None or len(search) == 0:
            filtered_df = df
        else:
            filtered_df = df[df['School'].isin(search)]
        map_style = 'dark'
        color_scale = px.colors.qualitative.Light24
        pie_names = 'SchoolDistrict'  # name parameter for px.pie
        text_display = html.H2('Alaskan Schools'),\
            'The points on this map represent a large sample of the public schools on record in Alaska during the given year, categorized by school district. ' \
            'The \'Year\' varibale here corresponds to the year in which an academic year is concluded. For example, \'2013\' refers to the 2012-2013 school year. The schools represented on this map ' \
            'are either primary (elementary) schools, intermediate (middle) schools, secondary (high) schools, or some ' \
            'combination of the three, and are color coded by their respective school districts. Note that school district data is not complete for all schools.', \
            html.Br(), html.Br(), \
            'There are many schools in rural or remote communities in Alaska whose students ' \
            'range in grade from Kindergarten through eighth grade or through twelth grade. The large student age-range in schools like these this might ' \
            'be considered a unique feature of rural communities compared to more populated areas, and because of this we will consider a school to be a high school if has a nonzero grade 9-12 Enrollment number. ' \
            'This data was gathered from the \"Enrollment Counts by School\" and \"Teacher Counts by School\" tables on the State of Alaska Open Data Geoportal, and does not ' \
            'represent all Alaskan schools.', \
            html.Br(), html.Br(), \
            'The chart \"Student Enrollment by School District\" below shows the total year-to-year K-12 enrollment for Alaskan school districts relative to eachother. Drag the mouse over an area on the graph to zoom in on that selected area, ' \
            'or double click on a school district in the legend to isolate that district\'s enrollment data in the graph.'
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
                                hover_data=['Community', 'SchoolDistrict', 'Year', 'K8Enrollment', 'HSEnrollment',
                                            'TotalEnrollmentK12', 'TotalTeacherCount', 'StudentTeacherRatio'],
                                center={'lat': 63, 'lon': -152},
                                zoom=3)
        fig.update_layout(mapbox_style=map_style, height=800)

        chart = px.line(data_frame=pd.read_csv('data/DistrictEnrollment.csv'),
                        x='Year',
                        y='District Enrollment',
                        color='School District',
                        title='Student Enrollment by School District (K-12); 2013-2021',
                        hover_name='School District',
                        hover_data=['Year', 'School District', 'District Enrollment'],
                        labels={},
                        color_discrete_sequence=px.colors.qualitative.Light24,
                        markers=True)
        chart.update_layout(title_x=0.5, height=700, title_font_size=24,
                            legend_title='School District', legend_font_size=16, legend_font_family='Optima')

    elif selected_category == 'TotalEnrollmentK12':
        if search is None or len(search) == 0:
            filtered_df = df[df[selected_category].notnull()]
        else:
            filtered_df = df[df['School'].isin(search)]

        map_style = 'dark'
        color_scale = 'tealrose'
        text_display = html.H2('Schools Relative Size'), \
        'The points on this map represent a large sample of the public schools on record in Alaska during the given year where ' \
        'point-size is scaled by K-12 enrollment, and color is assigned by school district. This data was gathered from the \"Enrollment Counts by School\" table on the State of Alaska Open Data Geoportal, and does not ' \
        'represent all Alaskan schools.', \
        html.Br(), html.Br(), \
        'The chart \"Total State Student Enrollment by Grade (K-12)\" below shows the change in total K-12 student enrollment across the state from 2013-2022 ' \
        'according to the \"Enrollment Counts by School\" table. Note that each data point specifies the number of schools the overall enrollment was taken from each year.'

        fig = px.scatter_mapbox(filtered_df,
                                lat='Latitude',
                                lon='Longitude',
                                color='SchoolDistrict',
                                color_continuous_scale=color_scale,  # Unique color parameter
                                size='TotalEnrollmentK12',
                                animation_frame='Year',
                                animation_group='Year',
                                range_color=[0, 2000],
                                labels=col_labels,
                                hover_name='School',
                                hover_data=['Community', 'SchoolDistrict', 'Year', 'K8Enrollment', 'HSEnrollment',
                                            'TotalEnrollmentK12', 'TotalTeacherCount'],
                                center={'lat': 63, 'lon': -152},
                                zoom=3)
        fig.update_layout(mapbox_style=map_style, height=800)

        chart = px.line(data_frame=StudentSums,
                        x='Year',
                        y=y,
                        title='Total State Student Enrollment by Grade (K-12); 2013-2022',
                        hover_data=['Year', 'TotalSchoolCount'],
                        labels={'value': 'Total Enrollment',
                                'TotalSchoolCount': 'Total Number of Schools Counted From'},
                        markers=True)
        chart.update_layout(title_x=0.5, height=700, title_font_size=24,
                            legend_title='Grade', legend_font_size=16, legend_font_family='Optima')


    elif selected_category == 'StudentTeacherRatio':
        if search is None or len(search) == 0:
            filtered_df = df[df[selected_category].notnull()]
        else:
            filtered_df = df[df['School'].isin(search)]

        map_style = 'light'
        color_scale = 'Rainbow'
        text_display = html.H2('Student Teacher Ratios by School'), \
        'The points on this map represent a large sample of the public schools on record in Alaska during the given year where ' \
        'point-color is determined by student teacher ratio. Student teacher ratio is defined as the total number of students divided by the total number of teachers in a given school. ' \
        'This data was gathered from the \"Enrollment Counts by School\" table on the State of Alaska Open Data Geoportal, and does not ' \
        'represent all Alaskan schools.', \
        html.Br(), html.Br(), \
        'The chart \"Teacher Count vs. K-12 Enrollment by School\" is a scatter plot visualziation of the student-teacher ratio as defined above for the selected year. ' \
        'Use the cursor to highlight an area on the chart to zoom in on the points in that selected area.'

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
                                hover_data=['Community', 'SchoolDistrict', 'StudentTeacherRatio', 'Year',
                                            'K8Enrollment', 'HSEnrollment', 'TotalEnrollmentK12', 'TotalTeacherCount'],
                                center={'lat': 63, 'lon': -152},
                                zoom=3)
        fig.update_layout(mapbox_style=map_style, height=800)

        chart = px.scatter(data_frame=filtered_df,
                           x='TotalEnrollmentK12',
                           y='TotalTeacherCount',
                           title='Teacher Count vs. K-12 Enrollment by School; 2013-2021',
                           hover_data=['Community', 'School', 'SchoolDistrict', 'TotalEnrollmentK12', 'Year'],
                           labels={},
                           color='StudentTeacherRatio',
                           color_continuous_scale='Rainbow',
                           range_color=[0, 50],
                           animation_frame='Year')
        chart.update_layout(title_x=0.5, height=700, title_font_size=24)


    elif selected_category == 'Is_HighSchool':
        if search is None or len(search) == 0:
            filtered_df = df[df[selected_category].notnull()]
        else:
            filtered_df = df[df['School'].isin(search)]

        map_style = 'dark'
        color_scale = 'tealrose'
        text_display = html.H2('Schools with Grade 9-12 Enrollment'), \
        'The points on this map differentiate between schools with high school (grade 9-12) enrollment, and those with only grades K-8 enrollment ' \
        'for the given year. Due to the age diversity present in many Alaskan schools, we will consider a school to be a high school if has a nonzero 9-12 Enrollment.', \
        html.Br(), html.Br(), \
        'The chart \"Total State High School Enrollment by Grade\" below shows the change in total high school (grades 9-12) enrollment across the state from 2013-2022 ' \
        'according to the \"Enrollment Counts by School\" table.'

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
                                hover_data=['Community', 'SchoolDistrict', 'Year', 'K8Enrollment', 'HSEnrollment',
                                            'TotalEnrollmentK12', 'Is_HighSchool', 'TotalTeacherCount'],
                                center={'lat': 63, 'lon': -152},
                                zoom=3)
        fig.update_layout(mapbox_style=map_style, height=800)

        chart = px.line(data_frame=StudentSums,
                        x='Year',
                        y=['Ninth Grade', 'Tenth Grade', 'Eleventh Grade', 'Twelfth Grade'],
                        title='Total State High School Student Enrollment by Grade; 2013-2022',
                        labels={'value': 'Total Enrollment'},
                        markers=True)
        chart.update_layout(title_x=0.5, height=700, title_font_size=24,
                            legend_title='Grade', legend_font_size=16, legend_font_family='Optima')

    elif selected_category == 'Graduates':
        if HSsearch is None or len(HSsearch) == 0:
            filtered_df = df[df['GraduationRate'].notnull()]
        else:
            dff = df[df['School'].isin(HSsearch)]
            filtered_df = dff[dff['GraduationRate'].notnull()]

        map_style = 'dark'
        color_scale = 'rdbu'
        text_display = html.H2('High School Graduation Rates'), \
        'The points on this map represent schools that have a four-year high school gradution rate during the given year, and are color-scaled by this rate. ' \
        'According to the Department of Education (ed.gov), \"The four-year graduation rate is calculated by dividing the number of students who graduate in four years or less with a regular high school diploma by the number of students who form the adjusted cohort for that graduating class.\" ' \
        'For example, if ten seniors at a particular school graduate out of a total of 20 students who entered the ninth grade four years earliers (In Cohort), then the school\'s graduation rate would be 0.5, or 50% for that given year. ' \
        'The cohort number is also adjusted up or down to account for students who transfer in, transfer out, emigrate, or die. ', \
        html.Br(), html.Br(), \
        'The chart \"Four-Year Graduation Rates vs. Student Teacher Ratio by School\" below plots the relationship between four-year graduation rates and Student Teacher Ratio (student count divided by teacher count) by school. ' \
        'Note that many Alaskan communities combine elementary/middle and high school programs at single school locations, so the teacher count used in the Student Teacher Ratio calculation is not exclusive to high school teachers. ' \
        'This data was gathered from the \"High School Graduation Rate: Four Year\" and \"Teacher Counts by School\" tables.'

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
                                hover_data=['Community', 'SchoolDistrict', 'Year', 'In_Cohort', 'Graduates',
                                            'GraduationRate', 'K8Enrollment', 'HSEnrollment', 'TotalEnrollmentK12',
                                            'TotalTeacherCount', 'StudentTeacherRatio'],
                                center={'lat': 63, 'lon': -152},
                                zoom=3)
        fig.update_layout(mapbox_style=map_style, height=800)

        chart = px.scatter(data_frame=filtered_df,
                           x='StudentTeacherRatio',
                           y='GraduationRate',
                           title='Four-Year Graduation Rates vs. Student Teacher Ratio by School; 2015-2021',
                           hover_name='School',
                           hover_data=['SchoolDistrict', 'Graduates', 'In_Cohort', 'Year', 'GraduationRate',
                                       'StudentTeacherRatio'],
                           labels={},
                           color='GraduationRate',
                           color_continuous_scale='agsunset',
                           animation_frame='Year')
        chart.update_layout(title_x=0.5, height=700, title_font_size=24)

    elif selected_category == 'GraduationRate':
        if HSsearch is None or len(HSsearch) == 0:
            filtered_df = df[df[selected_category].notnull()]
        else:
            dff = df[df['School'].isin(HSsearch)]
            filtered_df = dff[dff['GraduationRate'].notnull()]

        map_style = 'dark'
        color_scale = 'rdbu'
        text_display = html.H2('High School Graduation Rates with Relative Size'), \
        'The points on this map represent a large sample of the public schools on record in Alaska during the given year where ' \
        'point color is scaled by four-year high school graduation rate and size is scaled by high school enrollment; gathered from the \"High School Graduation Rate: Four Year\" table.', \
        html.Br(), html.Br(), \
        'The chart \"Four-Year Graduation Rates vs. Students In-Cohort by School\" below plots the relationship between four-year graduation rates and students in-cohort by school. ' \
        'This relationship visualizes a \'weight\' attribute of a school\'s gradution rate directly proportional to its number of students in-cohort. ' \
        'The farther to the right on the graph a school appears, the higher its in-cohort enrollment pool is from which the gradution rate is calculated. ' \
        'This data was gathered from the \"High School Graduation Rate: Four Year\" table.'

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
                            hover_data=['Community', 'SchoolDistrict', 'Year', 'In_Cohort', 'Graduates',
                                        'GraduationRate', 'K8Enrollment', 'HSEnrollment', 'TotalEnrollmentK12',
                                        'TotalTeacherCount'],
                            center={'lat': 63, 'lon': -152},
                            zoom=3)
        fig.update_layout(mapbox_style=map_style, height=800)

        chart = px.scatter(data_frame=filtered_df,
                           x='In_Cohort',
                           y='GraduationRate',
                           title='Four-Year Graduation Rates vs. Students In-Cohort by School; 2015-2021',
                           hover_name='School',
                           hover_data=['SchoolDistrict', 'Graduates', 'In_Cohort', 'Year', 'GraduationRate'],
                           labels={},
                           color='GraduationRate',
                           color_continuous_scale='phase',
                           animation_frame='Year')
        chart.update_layout(title_x=0.5, height=700, title_font_size=24)


    return fig, text_display, chart

    # Run App
if __name__ == '__main__':
    app.run_server(debug=True)
