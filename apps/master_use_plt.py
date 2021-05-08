import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from dash_core_components.RadioItems import RadioItems
import csv
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
from datetime import datetime
import time
from datetime import date
now = pd.to_datetime('now')
#Dash Stuff
import plotly.express as px
from dash.dependencies import Input, Output
import dash_table

""" DATA AND VARIABLES """
df = pd.read_pickle("/Users/johntaylor/cloud_upload_2/dashboard_4_13_21/design_redo/data/master_usage.pkl")
dosages = ['1_mg/ml', '25_mg', '15_mg/ml', '50_mg/100ml', '75_mg', '150_mg', '300_mg', 'Other']

#create firm list
initial_lst = ['All']
firm_lst = sorted(list(set(df['Firm'])))
# firm_lst.remove("nan")
final_firms = initial_lst + firm_lst

firm_options = [{'label':i, 'value':i} for i in final_firms]
age_min = 0
age_max = 110

from app import app

#app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SUPERHERO])

firm_dropdown = dcc.Dropdown(id='9-firm-dd', multi=False, value=firm_options[0]['value'] ,options=firm_options, style={'width':'75%', 'color':'#000000'}, clearable=False)

status_radio = dbc.FormGroup(
    [
        dbc.Label("Client Status"),
        dbc.RadioItems(
            options=[],
            value=[],
            id="9-status-dd",
            inline=True
        ), html.Br(),
            html.P(id='9-status-text', children="", style={'margin-left': '5px'})
    ]
)

stats_card = dbc.Card(
    [
        dbc.CardBody(
            [
                html.P(f"General Statistics", style={'textAlign':'center'}),
                html.Hr(style={'color':'#ff8300'}),
                html.P(id='9-avg-age', children="", style={'textAlign':'right'}),
                html.P(id='9-avg-use', children="", style={'textAlign':'right'}),
            ], 
        ),
    ],
    style={"width": "15rem"}, className='float-box'
)

dataset_stats = dbc.Card(
    [
        dbc.CardBody(
            [
                html.P(f"Dataset Statistics", style={'textAlign':'center'}),
                html.Hr(style={'color':'#ff8300'}),
                html.P(id='9-dataset-avg-age', children="", style={'textAlign':'right'}),
                html.P(id='9-dataset-avg-dur', children="", style={'textAlign':'right'}),
            ], 
        ),
    ],
    style={"width": "15rem"}, className='float-box'
)


graph_card = dbc.Card(
    dbc.CardBody(
        [
            html.H5("PRODUCT DATA", className="card-title"),
            
            html.P(id='9-graph-sub', children=""
            ),
            dcc.Graph(id='9-bar-fig', config={'displayModeBar':False}),
        ]
    ), className='float-box col-lg-9 mt-4, ml-4',
    
), 


graph_line = dbc.Card(
    dbc.CardBody(
        [
            html.H5("DATA OVER TIME", className="card-title"),
            
            # html.P(id='9-graph-sub', children=""
            # ),
            dcc.Graph(id='9-line-fig', config={'displayModeBar':False}),
        ]
    ), className='float-box',
    
), 


table_card = dbc.Card(
    dbc.CardBody(
        [
            html.H5(id='9-table-sub', children="", style={'text-align': 'center'}
            ),
            html.Div(id='9-data-table'),
        ]
    ), className='float-box col-lg-12 mt-5',
    
), 

""" page components in order top to bottom """

years_of_use_slider = dcc.RangeSlider(
        id='9-years-use-slider',
        min=0,
        max=10,
        step=1,
        value=[],
        marks={},
        # dots=True,
        tooltip = {'always_visible':False, 'placement':'bottom'}     
        )

years_of_use_card = dbc.Card(
    dbc.CardBody(
        [
            html.P(id='9-years-use-header', children="", className="card-title", style={'text-align': 'center'}),
            years_of_use_slider,
        ]
    ), className='float-box col-lg-12 mt-7'
)

duration_of_use_slider = dcc.RangeSlider(
        id='9-dur-slider',
        min=0,
        max=40,
        step=1,
        value=[0,40],
        marks={i:{'label': str(i),'style': {'color':'#ffffff'}} for i in range(0, 41, 10)},
        # dots=True,
        tooltip = {'always_visible':False, 'placement':'bottom'}     
        )

duration_of_use_card = dbc.Card(
    dbc.CardBody(
        [
            html.P(id='9-dur-use-header', children="", className="card-title", style={'text-align': 'center'}),
            duration_of_use_slider,
        ]
    ), className='float-box col-lg-12 mt-3'
)

age_slider = dcc.RangeSlider(
        id='9-age-slider',
        min=age_min,
        max=age_max,
        step=2,
        value=[],
        marks={},
        # dots=True,
        tooltip = {'always_visible':False, 'placement':'bottom'}
        )

age_card = dbc.Card(
    dbc.CardBody(
        [
            html.P(id='9-age-header', children="", className="card-title", style={'text-align': 'center'}),
            age_slider,
        ]
    ), className='float-box col-lg-12 mt-3'
)

formulation_check = dbc.FormGroup(
    [
        dbc.Label("Formulation"),
        dbc.Checklist(
            options=[],
            value=[],
            id="9-form-check",inline=True, 
        )
    ]
)

formulation_dose = dbc.FormGroup(
    [
        dbc.Label("Dosage"),
        dbc.Checklist(
            options=[],
            value=[],
            id="9-dosage-check",inline=True, 
        )
    ]
)

delivery = dbc.FormGroup(
    [
        dbc.Label("Delivery"),
        dbc.Checklist(
            options=[],
            value=[],
            id="9-delivery-method",inline=True, 
        )
    ]
)

# """ Setup the layout here with simple row and column lines"""

layout = dbc.Container([
                        dbc.Row([
                                dbc.Col(html.H1('Master Usage Data - Plaintiffs'))
                                 ], className="row justify-content-center"),
                                html.Br(), 
                                # html.Br(),
                        dbc.Row([
                                dbc.Col([
                                    dbc.Row(firm_dropdown),
                                    html.Br(), 
                                    dbc.Row(status_radio),
                                        ], xs=12, sm=12, md=12, lg=3, xl=3, className='mt-2 ml-3'), 
                                dbc.Col(stats_card, xs=12, sm=12, md=12, lg=3, xl=3),
                                dbc.Col([
                                    dbc.Row(formulation_check), 
                                    dbc.Row(formulation_dose), 
                                    dbc.Row(delivery), 
                                        ], xs=12, sm=12, md=12, lg=5, xl=5),
                                        # ], className='mt-2 col-lg-3'),
                                ]),
                        dbc.Row([
                            dbc.Col([
                                dbc.Row(years_of_use_card), 
                                dbc.Row(duration_of_use_card), 
                                dbc.Row(age_card),
                                    ], xs=12, sm=12, md=12, lg=3, xl=3, className='mt-2 ml-2'), 
                            dbc.Col([
                                # dbc.Row(formulation_check, className='ml-5'), 
                                # dbc.Row(formulation_dose, className='ml-5'), 
                                # dbc.Row(delivery, className='ml-5'), 
                                dbc.Row(graph_card, className='ml-2'),
                                dbc.Row(),
                                    ]),
                                ]),
                        dbc.Row(table_card),


                            ], fluid=True)

# """ Callback Functions """
# """ for the status dropdown """
@app.callback(
    Output('9-status-dd', 'options'),
    Output('9-status-dd', 'value'),
    Input('9-firm-dd', 'value'))
def set_status_options(selected_firm):
    if selected_firm == 'All':
        firm_choice = df
        status_lst = ['All', 'Living', 'Deceased']
    else:
        firm_choice = df[df['Firm'] == selected_firm]
        radio_lst = ['All', 'Living', 'Deceased']
        other_lst = list(set(firm_choice['deceased']))
        
        status_lst = list(set([x for x in other_lst if x in radio_lst]))
    
        if len(status_lst) > 1:
            status_lst = sorted(status_lst, reverse=True)
            status_lst.insert(0,'All')
    # print(f'other_lst {other_lst}')
    value = status_lst[0]  #makes the default value the first option in the status_lst
    return [{'label': i, 'value': i} for i in status_lst], value

# Formulation options dictated by inputs from retailer, status, 
@app.callback(
    Output("9-form-check", 'options'),
    Output("9-form-check", 'value'),
    Input('9-firm-dd', 'value'), 
    Input('9-status-dd', 'value'))
def set_form_list_options(selected_firm, status):
    if selected_firm == 'All' and status == 'All':
        firm_choice = df
    elif selected_firm != 'All' and status == 'All':
        firm_choice = df[df['Firm'] == selected_firm]
    elif selected_firm == 'All' and status != 'All':
        firm_choice = df[df['deceased'] == status]
    else:
        firm_choice = df[(df['deceased'] == status) & (df['Firm'] == selected_firm)]
    
    form_lst = sorted(list(set(firm_choice['formulation'])))

    # print(f'form lst {form_lst}')


    if 'Other' in form_lst:
        form_lst.remove('Other')
        form_lst.append('Other')
    value = form_lst  #makes the default value the first option in the status_lst
    return [{'label': i, 'value': i} for i in form_lst], value

# # """for the dose checklist """
@app.callback(
    Output("9-dosage-check", "options"),
    Output("9-dosage-check", "value"),
    Input("9-form-check", "value"))
def set_checklist_options(formulation):
    dosage_df = df[df['formulation'].isin(formulation)]
    # dosage_df = df[df['formulation'].apply(lambda x: set(x).intersection(formulation)).astype(bool)]
    dosage_lst = list(set(dosage_df['dosage']))
    final_lst =  [i for i in dosage_lst if i in dosages]    
    value = final_lst #makes the default value the first option in the status_lst)
    return [{'label': i, 'value': i} for i in final_lst], value

# # """for the delivery checklist """
@app.callback(
    Output("9-delivery-method", 'options'),
    Output("9-delivery-method", 'value'),
    Input("9-form-check", 'value'),
    Input("9-dosage-check", 'value'))
def set_delivery_list_options(formulation, dosage):
    admin_df = df[(df['formulation'].isin(formulation)) & (df['dosage'].isin(dosage))]
    deliv_meth = list(set(admin_df['admin_method']))
    deliv_meth_fin = sorted(deliv_meth, reverse=True)
    value = deliv_meth_fin  #makes the default value the first option in the status_lst
    return [{'label': i, 'value': i} for i in deliv_meth_fin], value

# # # """ Setting the Use Years Slider """
@app.callback(
    Output('9-years-use-slider', 'value'), #sets starting value for the slider
    Output('9-years-use-slider', 'marks'), #sets the marks for the length of the slider
    Output('9-years-use-slider', 'min'), #sets the marks for the length of the slider
    Output('9-years-use-slider', 'max'), #sets the marks for the length of the slider
    Input('9-firm-dd', 'value'))
def set_year_options(selected_firm):
    if selected_firm == 'All':
        firm_choice = df
    else:
        firm_choice = df[df['Firm'] == selected_firm]
    
    start_yr_lst = list(set(firm_choice['use_years'].str[0].astype('int')))
    end_yr_lst = list(set(firm_choice['use_years'].str[1].astype('int')))
    final_st_lst = [x for x in start_yr_lst if x >= 1980]
    final_end_lst = [x for x in end_yr_lst if x <= 2020]

    min_yr = min(final_st_lst)
    max_yr = max(final_end_lst)
    years_use_value = [min_yr, max_yr]
    years_use_marks = {i:{'label': str(i),'style': {'color':'#ffffff'}} for i in range(min_yr, max_yr+1, 10)}
    return years_use_value, years_use_marks, min_yr, max_yr

# # # """ Setting the client age slider  """
@app.callback(
    Output('9-age-slider', 'value'), #sets starting value for the slider
    Output('9-age-slider', 'marks'), #sets the marks for the length of the slider
    Output('9-age-slider', 'min'), #sets the marks for the length of the slider
    Output('9-age-slider', 'max'), #sets the marks for the length of the slider
    Input('9-firm-dd', 'value'))
def set_age_options(selected_firm):
    if selected_firm == 'All':
        firm_choice = df
    else:
        firm_choice = df[df['Firm'] == selected_firm]
    initial_age_lst = sorted(list(set(firm_choice['age'])))
    age_lst = [x for x in initial_age_lst if x >=0]
    age_min=int(age_lst[0])
    if age_min < 0:
        age_min == 0
    try:
        age_max=int(age_lst[-1])
    except:
        age_max=int(age_lst[0])
    age_value = [age_min, age_max]
    
    age_marks = {i:{'label':str(i), 'style':{'color':'#ffffff'}} for i in range(age_min, age_max+1, 10)}
    
    return age_value, age_marks, age_min, age_max

# # """ Main callbacks """
@app.callback(
    Output('9-bar-fig', 'figure'),
    Output('9-status-text', 'children'),  
    Output('9-avg-age', 'children'),  
    Output('9-avg-use', 'children'),  
    Output('9-years-use-header', 'children'),  
    Output('9-dur-use-header', 'children'),  
    Output('9-age-header', 'children'),
 
    Input('9-firm-dd', 'value'),
    Input('9-status-dd', 'value'),
    Input('9-years-use-slider', 'value'),
    Input('9-dur-slider', 'value'),
    Input('9-age-slider', 'value'),
    Input("9-form-check", 'value'),
    Input("9-dosage-check", 'value'),
    Input("9-delivery-method", 'value'),

)

# def update_graph(selected_firm, status, years, duration, age, formulation, dosage, delivery):
def update_graph(selected_firm, status, use_years, duration, age, formulation, dosage, delivery):
    if selected_firm == 'All' and status == 'All':
        main_df = df
    elif selected_firm == 'All' and status != 'All':
        main_df = df[df['deceased'] == status]
    elif selected_firm != 'All' and status == 'All':
        main_df = df[df['Firm'] == selected_firm]
    else: 
        main_df = df[(df['Firm'] == selected_firm) &
                    (df['deceased'] == status)]  
    
    # print(f'use years {use_years}')
    # print(f'duration {duration}')
    # print(f'age {age}')
    # print(f'formulation {formulation}')
    # print(f'dosage {dosage}')


    #setting the results with the use_years value
    use_years_range = list(range(use_years[0], use_years[1] +1)) #create list of all values in the range to use to constrict the data
    main_df = main_df[main_df.use_years_lst.apply(lambda x: set(x).intersection(use_years_range)).astype(bool)]
    #duration used
    final_df = main_df[(main_df['total_use_years'].between(duration[0], duration[1])) &
                        (main_df['age'].between(age[0], age[1])) & 
                        (main_df['formulation'].isin(formulation)) &
                        (main_df['dosage'].isin(dosage)) & 
                        (main_df['admin_method'].isin(delivery))
                        ]    
    
    final_df.drop_duplicates(subset=['SubjectId', 'formulation'], inplace=True) #to avoid double counting of subject IDs
    final_data = final_df.groupby('formulation')['SubjectId'].count().reset_index()
    final_data = final_data.rename(columns={'SubjectId':'Total'})
    final_data = final_data[final_data['Total'] >0]

    # print(f'final df head {final_df.head()}')


    """ CONTENT FOR ALL THE TEXT FIELDS """
    master_status_number = final_df.SubjectId.nunique()
    if status == 'All':
        master_status_text = f'All {master_status_number} Clients' 
    else:
        master_status_text = f'{master_status_number} {status} Clients'

    #average age stats
    if selected_firm == 'All':
        master_firm = final_df
    else:
        master_firm = final_df[final_df['Firm'] == selected_firm]
    master_avg_age_retailer = round(master_firm['age'].mean(), 1)
    master_avg_age_retailer_text = f'Average Age:  {master_avg_age_retailer}'
    # #average duration text
    master_avg_dur = round(master_firm['total_use_years'].mean(),1)
    master_avg_dur_text = f'Average Years of Use:  {master_avg_dur}'
    #Use years text
    master_years_use_header = f"Years Used {use_years[0]} to {use_years[1]}"
    #duration header text
    master_dur_use_header = f'Duration Used {duration[0]} to {duration[1]} years'

    # #age header text
    master_age_header = f'Clients  {age[0]} to {age[1]} years old'


    master_product_fig=px.bar(final_data,
                    text='Total',  #puts direct label on bar graph
                    x='formulation', y='Total', color="formulation", labels=dict(Year="Year of Product Use", Total="Clients Using Each Product", formulation="Product Type", hover_data=["SubjectID", "formulation"]),
                    title='')

    master_product_fig.update_layout(showlegend=False)
   

    return master_product_fig, master_status_text, master_avg_age_retailer_text, master_avg_dur_text, master_years_use_header, master_dur_use_header, master_age_header

if __name__ == '__main__':
    app.run_server(debug=True)