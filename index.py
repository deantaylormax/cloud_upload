import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
pd.set_option('mode.chained_assignment', None)


from app import app
from apps import extra_plots, prod_stats, ca_plt, master_use_plt, master_use_def, geo, ca_def, usage_over_time


# app.layout = html.Div([
#     dcc.Location(id='url', refresh=False),
#     html.Div(id='page-content')
# ])

app.layout = html.Div([
                dbc.Row(
                    dbc.NavbarSimple(
                    children=[
                        # dbc.NavItem(dbc.NavLink("Page 1", href="#")),
                        dbc.DropdownMenu(
                            children=[
                                # dbc.DropdownMenuItem("More pages", header=True),
                                dbc.DropdownMenuItem("Product Stats", href="/apps/prod_stats"),
                                dbc.DropdownMenuItem("Cancer Data", href="/apps/ca_plt"),
                                dbc.DropdownMenuItem("Master Usage", href="/apps/master_use_plt"),
                                dbc.DropdownMenuItem("Geo Distribution", href="/apps/geo"),
                                    ],
                            nav=True,
                            in_navbar=True,
                            label="Plaintiff",
                            # className='navbar-nav ml-auto'
                                        ),
                        dbc.DropdownMenu(
                            children=[
                                # dbc.DropdownMenuItem("More pages", header=True),
                                dbc.DropdownMenuItem("Cancer Data", href="/apps/ca_def"),
                                dbc.DropdownMenuItem("Master Usage", href="/apps/master_use_def"),
                                dbc.DropdownMenuItem("Usage Over Time", href="/apps/usage_over_time"),

                                    ],
                            nav=True,
                            in_navbar=True,
                            label="Defense",
                                        ),
                            dbc.DropdownMenu(
                            children=[
                                # dbc.DropdownMenuItem("More pages", header=True),
                                dbc.DropdownMenuItem("Comparisons", href="/apps/extra_plots"),
                                # dbc.DropdownMenuItem("Colors Change", href="/apps/four_prod_stats_white"),
                                # dbc.DropdownMenuItem("Master Usage", href="/apps/master_usage_def_V2"),
                                # dbc.DropdownMenuItem("Usage Over Time", href="/apps/usage_over_time"),
                                # dbc.DropdownMenuItem("Geo Alternative", href="/apps/geo_distribution_toggle"),

                                    ],
                            nav=True,
                            in_navbar=True,
                            label="Additional",
                                        ),
                            
                            
                            ], 
                    className = "sticky-top",
                    brand="The Brand",
                    brand_href="www.google.com",
                    color="primary",
                    dark=True,
                    # className='navbar-nav mr-auto',
                    # sticky='top'
                                        )),
                dbc.Row([
                        dbc.Col(),
                        dbc.Col(),
                        dbc.Col(),
                        ]),
                html.Br(),  #puts space between nav bar and content
                dcc.Location(id='url', refresh=False),
                html.Div(id='page-content'),
                    ], style={
                                'position': 'relative',
                                'zIndex': '2',
                            })


@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/apps/prod_stats':
        return prod_stats.layout
    elif pathname == '/apps/ca_plt':
        return ca_plt.layout
    elif pathname == '/apps/master_use_plt':
        return master_use_plt.layout
    elif pathname == '/apps/master_use_def':
        return master_use_def.layout
    elif pathname == '/apps/geo':
        return geo.layout
    elif pathname == '/apps/ca_def':
        return ca_def.layout
    elif pathname == '/apps/usage_over_time':
        return usage_over_time.layout
    elif pathname == '/apps/extra_plots':
        return extra_plots.layout
    else:
        return prod_stats.layout

if __name__ == '__main__':
    app.run_server(debug=True)