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
# df = pd.read_pickle("data/master_usage.pkl")

df = pd.read_feather("data/master_usage.ftr", columns=None).set_index(['SubjectId'])
df.drop(columns=['index'], inplace=True)
df.reset_index(inplace=True)



dosages = ['1_mg/ml', '25_mg', '15_mg/ml', '50_mg/100ml', '75_mg', '150_mg', '300_mg', 'Other']
retailer_lst = ['All','Albertsons', 'Amazon','Costco','CVS','H_E_Butt','Cigna_Express_Scripts','Duane_Reed', 'Giant_Eagle', 'H_E_Butt', 'Humana_Pharmacy_Solutions','Hy-Vee', 'Kroger', 'Medicine_Shoppe', 'Publix','Rite_Aid', 'Shoprite_Supermarkets','Smith\'s_Food_and_Drug', 'Target', 'Walgreens','Walmart', 'Winn_Dixie']
retailer_options = [{'label':i.replace("_", ' '), 'value':i} for i in retailer_lst]
age_min = 0
age_max = 110

from app import app

#app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SUPERHERO])

retailer_dropdown = dcc.Dropdown(id='6-retailer-dd', multi=False, value=retailer_options[0]['value'] ,options=retailer_options, style={'width':'75%', 'color':'#000000'}, clearable=False)

status_radio = dbc.FormGroup(
    [
        dbc.Label("Client Status"),
        dbc.RadioItems(
            options=[],
            value=[],
            id="6-status-dd",
            inline=True
        ), html.Br(),
            html.P(id='6-status-text', children="", style={'margin-left': '5px'})
    ]
)

stats_card = dbc.Card(
    [
        dbc.CardBody(
            [
                html.P(f"General Statistics", style={'textAlign':'center'}),
                html.Hr(style={'color':'#ff8300'}),
                html.P(id='6-avg-age', children="", style={'textAlign':'right'}),
                html.P(id='6-avg-use', children="", style={'textAlign':'right'}),
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
                html.P(id='6-dataset-avg-age', children="", style={'textAlign':'right'}),
                html.P(id='6-dataset-avg-dur', children="", style={'textAlign':'right'}),
            ], 
        ),
    ],
    style={"width": "15rem"}, className='float-box'
)


graph_card = dbc.Card(
    dbc.CardBody(
        [
            html.H5("PRODUCT DATA", className="card-title"),
            
            html.P(id='6-graph-sub', children=""
            ),
            dcc.Graph(id='6-bar-fig', config={'displayModeBar':False}),
        ]
    ), className='float-box col-lg-9 mt-4, ml-4',
    
), 


graph_line = dbc.Card(
    dbc.CardBody(
        [
            html.H5("DATA OVER TIME", className="card-title"),
            
            # html.P(id='6-graph-sub', children=""
            # ),
            dcc.Graph(id='6-line-fig', config={'displayModeBar':False}),
        ]
    ), className='float-box',
    
), 


table_card = dbc.Card(
    dbc.CardBody(
        [
            html.H5(id='6-table-sub', children="", style={'text-align': 'center'}
            ),
            html.Div(id='6-data-table'),
        ]
    ), className='float-box col-lg-12 mt-5',
    
), 

""" page components in order top to bottom """

years_of_use_slider = dcc.RangeSlider(
        id='6-years-use-slider',
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
            html.P(id='6-years-use-header', children="", className="card-title", style={'text-align': 'center'}),
            years_of_use_slider,
        ]
    ), className='float-box col-lg-12 mt-7'
)

duration_of_use_slider = dcc.RangeSlider(
        id='6-dur-slider',
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
            html.P(id='6-dur-use-header', children="", className="card-title", style={'text-align': 'center'}),
            duration_of_use_slider,
        ]
    ), className='float-box col-lg-12 mt-3'
)

age_slider = dcc.RangeSlider(
        id='6-age-slider',
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
            html.P(id='6-age-header', children="", className="card-title", style={'text-align': 'center'}),
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
            id="7-form-check",inline=True, 
        )
    ]
)

formulation_dose = dbc.FormGroup(
    [
        dbc.Label("Dosage"),
        dbc.Checklist(
            options=[],
            value=[],
            id="6-dosage-check",inline=True, 
        )
    ]
)

delivery = dbc.FormGroup(
    [
        dbc.Label("Delivery"),
        dbc.Checklist(
            options=[],
            value=[],
            id="6-delivery-method",inline=True, 
        )
    ]
)

# """ Setup the layout here with simple row and column lines"""

layout = dbc.Container([
                        dbc.Row([
                                dbc.Col(html.H1('Master Usage Data - Retailers'))
                                 ], className="row justify-content-center"),
                                html.Br(), 
                                html.Br(),
                        dbc.Row([
                                dbc.Col([
                                    dbc.Row(retailer_dropdown),
                                    html.Br(), 
                                    dbc.Row(status_radio),
                                        ], className='mt-2 col-lg-3, ml-3'), 
                                dbc.Col(stats_card, className='mt-2', width=9),
                                # dbc.Col(graph_line, width=3),
                                ]),
                        dbc.Row([
                            dbc.Col([
                                dbc.Row(years_of_use_card), 
                                dbc.Row(duration_of_use_card), 
                                dbc.Row(age_card),
                                    ], xs=12, sm=12, md=12, lg=3, xl=3, className='mt-9, ml-2'), 
                            dbc.Col([
                                dbc.Row(formulation_check, className='ml-5'), 
                                dbc.Row(formulation_dose, className='ml-5'), 
                                dbc.Row(delivery, className='ml-5'), 
                                dbc.Row(graph_card, className='ml-4'),
                                dbc.Row(),
                                    ]),
                                ]),
                        # dbc.Row(table_card),


                            ], fluid=True)

# """ Callback Functions """
# """ for the status dropdown """
@app.callback(
    Output('6-status-dd', 'options'),
    Output('6-status-dd', 'value'),
    Input('6-retailer-dd', 'value'))
def set_status_options(selected_retailer):
    if selected_retailer == 'All':
        retailer_choice = df
        status_lst = ['All', 'Living', 'Deceased']
    else:
        retailer_choice = df[df['retailers'].str.contains(selected_retailer)]
        # initial_lst = ['All'] 
        radio_lst = ['All', 'Living', 'Deceased']
        other_lst = list(set(retailer_choice['deceased']))
        # clean_lst = [x for x in other_lst if x in radio_lst]
        # print(f'clean lst {clean_lst}')
        status_lst = list(set([x for x in other_lst if x in radio_lst]))
        # print(f'selected_retailer = {selected_retailer}')
        # print(f'status_lst {status_lst}')
        if len(status_lst) > 1:
            status_lst = sorted(status_lst, reverse=True)
            status_lst.insert(0,'All')
    # print(f'other_lst {other_lst}')
    value = status_lst[0]  #makes the default value the first option in the status_lst
    return [{'label': i, 'value': i} for i in status_lst], value

# """for the formulation checklist """
# @app.callback(
#     Output("7-form-check", 'options'),
#     Output("7-form-check", 'value'),
#     Input('6-retailer-dd', 'value'))
# def set_checklist_options(selected_retailer):
#     if selected_retailer == 'All':
#         retailer_choice = df
#     else:
#         retailer_choice = df[df['retailers'].str.contains(selected_retailer)]
#     form_lst = sorted(list(set(retailer_choice['formulation'])), reverse=True)

#     if 'Other' in form_lst:
#         form_lst.remove('Other')
#         form_lst.append('Other')
#     value = form_lst  #makes the default value the first option in the status_lst
#     return [{'label': i, 'value': i} for i in form_lst], value




# Formulation options dictated by inputs from retailer, status, 
@app.callback(
    Output("7-form-check", 'options'),
    Output("7-form-check", 'value'),
    Input('6-retailer-dd', 'value'), 
    Input('6-status-dd', 'value'))
def set_checklist_options(selected_retailer, status):
    if selected_retailer == 'All' and status == 'All':
        retailer_choice = df
    elif selected_retailer != 'All' and status == 'All':
        retailer_choice = df[df['retailers'].str.contains(selected_retailer)]
    elif selected_retailer == 'All' and status != 'All':
        retailer_choice = df[df['deceased'] == status]
    else:
        retailer_choice = df[(df['deceased'] == status) & (df['retailers'].str.contains(selected_retailer))]
    
    form_lst = sorted(list(set(retailer_choice['formulation'])), reverse=True)

    if 'Other' in form_lst:
        form_lst.remove('Other')
        form_lst.append('Other')
    value = form_lst  #makes the default value the first option in the status_lst
    return [{'label': i, 'value': i} for i in form_lst], value

# # """for the dose checklist """
@app.callback(
    Output("6-dosage-check", 'options'),
    Output("6-dosage-check", 'value'),
    Input("7-form-check", 'value'))
def set_checklist_options(formulation):
    dosage_df = df[df['formulation'].isin(formulation)]
    # dosage_df = df[df['formulation'].apply(lambda x: set(x).intersection(formulation)).astype(bool)]
    dosage_lst = list(set(dosage_df['dosage']))
    final_lst =  [i for i in dosage_lst if i in dosages]
    # if '0ther' in final_lst:
    #     final_lst.remove('Other')
    #     # final_lst.sort(key = lambda x: x != 'Other' int(x.split('_')[0]))
    # final_lst = final_lst.sort(key = lambda x: int(x.split('_')[0]) if x != 'Other' else x)
    #     # final_lst.append('Other')
    # else:
        # final_lst.sort(key = lambda x: int(x.split('_')[0]))
    # print(f'dosage final lst {final_lst}')
    # print(f'dosage final lst ordered {final_lst_ordered}')


    # print(f'final list {final_lst}')
    value = final_lst #makes the default value the first option in the status_lst)
    return [{'label': i, 'value': i} for i in final_lst], value

# # """for the delivery checklist """
@app.callback(
    Output("6-deliver-method", "options"),
    Output("6-delivery-method", "value"),
    Input("7-form-check", "value"),
    Input("6-dosage-check", "value"))
def set_formulation_options(formulation, dosage):
    admin_df = df[(df['formulation'].isin(formulation)) & (df['dosage'].isin(dosage))]
    deliv_meth = list(set(admin_df['admin_method']))
    deliv_meth_fin = sorted(deliv_meth, reverse=True)
    value = deliv_meth_fin  #makes the default value the first option in the status_lst
    return [{'label': i, 'value': i} for i in deliv_meth_fin], value

# # # """ Setting the Use Years Slider """
@app.callback(
    Output('6-years-use-slider', 'value'), #sets starting value for the slider
    Output('6-years-use-slider', 'marks'), #sets the marks for the length of the slider
    Output('6-years-use-slider', 'min'), #sets the marks for the length of the slider
    Output('6-years-use-slider', 'max'), #sets the marks for the length of the slider
    Input('6-retailer-dd', 'value'))
def set_year_options(selected_retailer):
    if selected_retailer == 'All':
        retailer_choice = df
    else:
        retailer_choice = df[df['retailers'].str.contains(selected_retailer)]
    
    start_yr_lst = list(set(retailer_choice['use_years'].str[0].astype('int')))
    end_yr_lst = list(set(retailer_choice['use_years'].str[1].astype('int')))
    final_st_lst = [x for x in start_yr_lst if x >= 1980]
    final_end_lst = [x for x in end_yr_lst if x <= 2020]

    min_yr = min(final_st_lst)
    max_yr = max(final_end_lst)
    years_use_value = [min_yr, max_yr]
    years_use_marks = {i:{'label': str(i),'style': {'color':'#ffffff'}} for i in range(min_yr, max_yr+1, 5)}
    return years_use_value, years_use_marks, min_yr, max_yr

# # # """ Setting the client age slider  """
@app.callback(
    Output('6-age-slider', 'value'), #sets starting value for the slider
    Output('6-age-slider', 'marks'), #sets the marks for the length of the slider
    Output('6-age-slider', 'min'), #sets the marks for the length of the slider
    Output('6-age-slider', 'max'), #sets the marks for the length of the slider
    Input('6-retailer-dd', 'value'))
def set_age_options(selected_retailer):
    if selected_retailer == 'All':
        retailer_choice = df
    else:
        retailer_choice = df[df['retailers'].str.contains(selected_retailer)]
    initial_age_lst = sorted(list(set(retailer_choice['age'])))
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
    Output('6-bar-fig', 'figure'),
    Output('6-status-text', 'children'),  
    Output('6-avg-age', 'children'),  
    Output('6-avg-use', 'children'),  
    Output('6-years-use-header', 'children'),  
    Output('6-dur-use-header', 'children'),  
    Output('6-age-header', 'children'),
    # Output('6-line-fig', 'figure'),
    # Output('6-data-table', 'children'),
    # Output('6-graph-sub', 'children'), 
    # Output('6-table-sub', 'children'),
    # Output('6-dataset-avg-age', 'children'),
    # Output('6-dataset-avg-dur', 'children'),
    # Output('page-title', 'children'),
    Input('6-retailer-dd', 'value'),
    Input('6-status-dd', 'value'),
    Input('6-years-use-slider', 'value'),
    Input('6-dur-slider', 'value'),
    Input('6-age-slider', 'value'),
    Input("7-form-check", 'value'),
    Input("6-dosage-check", 'value'),
    Input("6-delivery-method", 'value'),

)

# def update_graph(selected_retailer, status, years, duration, age, formulation, dosage, delivery):
def update_graph(selected_retailer, status, use_years, duration, age, formulation, dosage, delivery):
    if selected_retailer == 'All' and status == 'All':
        main_df = df
    elif selected_retailer == 'All' and status != 'All':
        main_df = df[(df['deceased'] == status)]
    elif selected_retailer != 'All' and status == 'All':
        main_df = df[df['retailers'].str.contains(selected_retailer)]
    else: 
        main_df = df[(df['retailers'].str.contains(selected_retailer)) &
                    (df['deceased'] == status)]  
    
    # print(f'main df{main_df}')

    # print(f'formulation is {formulation}')
    # print(f'dosage is {dosage}')
    # print(f'delivery is {delivery}')

    #setting the results with the use_years value
    use_years_range = list(range(use_years[0], use_years[1] +1)) #create list of all values in the range to use to constrict the data
    main_df = main_df[main_df.use_years_lst.apply(lambda x: set(x).intersection(use_years_range)).astype(bool)]
    #duration used
    final_df = main_df[ (main_df['total_use_years'].between(duration[0], duration[1])) &
                        (main_df['age'].between(age[0], age[1])) & 
                        (main_df['formulation'].isin(formulation)) &
                        (main_df['dosage'].isin(dosage)) & 
                        (main_df['admin_method'].isin(delivery))
                        ]    
    
    # final_data_line = final_df.groupby(['formulation','use_years'])['SubjectId'].count().reset_index()
    # final_data_line = final_data_line.rename(columns={'use_years':'Year', 'SubjectId':'Total'})
    # final_data_line = final_data_line[final_data_line.Total >0]
    # print(f'final_data head {final_data.head()}')
    # print(form_choice)
    # line_fig = px.scatter(final_data_line, 
    #     x="Year", y="Total", color='formulation').update_traces(mode='lines+markers')
    # line_fig.update_layout(
    #     title={
    #         'text': "<br><br><b>Total Products</b> in Use by Year",
    #         'y':1.0,
    #         'x':0.5,
    #         'xanchor': 'center',
    #         'yanchor': 'top'})

    final_df.drop_duplicates(subset=['SubjectId', 'formulation'], inplace=True) #to avoid double counting of subject IDs
    final_data = final_df.groupby('formulation')['SubjectId'].count().reset_index()
    final_data = final_data.rename(columns={'SubjectId':'Total'})
    final_data = final_data[final_data['Total'] >0]
    
    # print(f' final_data head {final_data.head()}')

    """ CONTENT FOR ALL THE TEXT FIELDS """
    master_status_number = final_df.SubjectId.nunique()
    if status == 'All':
        master_status_text = f'All {master_status_number} Clients' 
    else:
        master_status_text = f'{master_status_number} {status} Clients'

    #average age stats
    if selected_retailer == 'All':
        master_retailer = final_df
    else:
        master_retailer = final_df[final_df['retailers'].str.contains(selected_retailer)]
    master_avg_age_retailer = round(master_retailer['age'].mean(), 1)
    master_avg_age_retailer_text = f'Average Age:  {master_avg_age_retailer}'
    # #average duration text
    master_avg_dur = round(master_retailer['total_use_years'].mean(),1)
    master_avg_dur_text = f'Average Years of Use:  {master_avg_dur}'
    #Use years text
    master_years_use_header = f"Years Used {use_years[0]} to {use_years[1]}"
    #duration header text
    master_dur_use_header = f'Duration Used {duration[0]} to {duration[1]} years'

    # if selected_retailer == 'All':
    #     master_retailer_avg = df
    # else:
    #     master_retailer_avg = df[df['retailers'].str.contains(selected_retailer)]
    # #Average Age Stats
    
    
    # #dataset averages
    # master_dataset_avg_age = round(filtered_retailer['age'].mean(),1)
    # master_dataset_avg_age_text = f'Average Age:  {master_dataset_avg_age}'
    # master_dataset_avg_dur = round(filtered_retailer['total_use_years'].mean(),1)
    # master_dataset_avg_dur_text = f'Average Years of Use:  {master_dataset_avg_dur}'
    # #totals for status chosen
    
   
    
    # #age header text
    master_age_header = f'Clients  {age[0]} to {age[1]} years old'
    # #the graph header
    # master_graph_header = f'{master_status_text} using any Product {years[0]} - {years[1]}, from {duration[0]} - {duration[1]} years duration, ages {age[0]} - {age[1]}'
    # master_table_header = f'{master_status_text} using any Product {years[0]} - {years[1]}, from {duration[0]} - {duration[1]} years duration, ages {age[0]} - {age[1]}'

    # final_data = filtered_retailer.groupby(['formulation'])['SubjectId'].count().reset_index()
    # final_data.drop_duplicates(columns=['SubjectId'], inplace=True)
    # final_data = final_data.rename(columns={'SubjectId':'Total'})
    # final_data = final_data[final_data['Total'] >0]
    # print(f'final data rows = {final_data.shape[0]}')
    # print(f'final data head {final_data.head()}')
    # print(final_data.head())
    master_product_fig=px.bar(final_data,
                    text='Total',  #puts direct label on bar graph
                    x='formulation', y='Total', color="formulation", labels=dict(Year="Year of Product Use", Total="Clients Using Each Product", formulation="Product Type", hover_data=["SubjectID", "formulation"]),
                    title='')
    master_product_fig.update_layout(showlegend=False)
    # master_table_fig =html.Div([dash_table.DataTable
    #             (id='table',
    #             style_header={'backgroundColor': '#df691a', 'color': '#ffffff'},
	# 			columns=[{"name": i, "id": i} for i in filtered_retailer.   columns if i != 'retailers'],
	# 			page_size=10,
    #             style_as_list_view=True,
	# 			data=filtered_retailer.to_dict("records"),
    #             # export_format="csv",
    #             export_format="xlsx",
    #             filter_action="native",
    #             sort_action="native",
	# 			style_cell={'width': '300px',
    #                         'height': '20px',
    #                         'textAlign': 'left', 
    #                         'backgroundColor': 'rgb(43, 62, 80)',
    #                         'color': 'white'}
    #             ),
    #                     ])
    # # page_title = 'Master Usage Data'
    # return master_product_fig, master_avg_age_text_retailer, master_avg_dur_text, master_status_text, master_years_use_header, master_dur_use_header, master_age_header, master_table_fig, master_graph_header, master_table_header, master_dataset_avg_age_text, master_dataset_avg_dur_text

    # return master_product_fig, master_avg_age_text_retailer, master_avg_dur_text, master_status_text, master_years_use_header, master_dur_use_header, master_age_header, master_graph_header, master_dataset_avg_age_text, master_dataset_avg_dur_text

    return master_product_fig, master_status_text, master_avg_age_retailer_text, master_avg_dur_text, master_years_use_header, master_dur_use_header, master_age_header

if __name__ == '__main__':
    app.run_server(debug=True)