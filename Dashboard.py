import dash
from dash import dcc, html, Input, Output
import os
import sys 
import flask

class ChemicalDashboardApp:
   
    def __init__(self):
        self.assets_folder = self.get_assets_path() 
        self.states = self.get_states()
        self.years = self.get_years()
        self.chemicals = self.get_chemicals()
        self.app = dash.Dash(__name__, assets_folder=self.assets_folder)
        self.app.title = "Chemical Exposure Dashboard"
        self.layout()
        self.setup_callbacks()

        @self.app.server.route('/assets/<path:filename>')
        def serve_static(filename):
            return flask.send_from_directory(self.assets_folder, filename)

    def get_assets_path(self):
        if getattr(sys, 'frozen', False):
            return os.path.join(sys._MEIPASS, 'assets')
        return os.path.join(os.path.dirname(__file__), 'assets')

    def get_states(self):
        states = set()
        for filename in os.listdir(self.assets_folder):
            if not filename.endswith(".html"):
                continue
            if "Yearly_chart" in filename or "Monthly_chart" in filename:
                parts = filename.replace(".html", "").split("_")
                if len(parts) == 3:  # castnet_Yearly_chart.html
                    states.add("ALL")
                elif len(parts) >= 3:
                    states.add(parts[1])
        return sorted(states)

    def get_years(self):
        years = set()
        for filename in os.listdir(self.assets_folder):
            if "Monthly" in filename and filename.endswith(".html"):
                parts = filename.replace(".html", "").split("_")
                if len(parts) >= 3 and parts[2].isdigit():
                    years.add(parts[2])
        return sorted(years)

    def get_chemicals(self):
        chemicals = set()
        for filename in os.listdir(self.assets_folder):
            if filename.endswith("_map.html"):
                parts = filename.replace(".html", "").split("_")
                if len(parts) == 3:
                    chemicals.add(parts[1])
        return sorted(chemicals)

    def layout(self):
        self.app.layout = html.Div([
            html.Div([
                html.H1("Chemical Exposure Dashboard", style={
                    'textAlign': 'center',
                    'color': '#1E90FF',
                    'paddingTop': '5px',
                    'paddingBottom': '5px',
                    'textShadow': '1px 1px #ddd',
                    'fontSize': '40px',
                    'maxWidth': '600px',    
                    'margin': 'auto'
                    }),
            ],style={
                'backgroundColor': "#B22222",
                'padding': '5px',
                'borderRadius': '10px',
                'boxShadow': '0 2px 6px rgba(0,0,0,0.1)'
            }),
            dcc.Tabs([
                dcc.Tab(label='📈 Chemical Trends',
                        style={'fontWeight': 'bold', 'fontSize': '20px'},
                        selected_style={
                            'fontWeight': 'bold', 
                            'fontSize': '26px', 
                            'color': '#1E90FF',
                            'backgroundColor': '#FFEBCD'},
                        className='chart-title-box', 
                        children=[
                    html.Div([
                        html.Div([
                            html.Label("Frequency:", style={'fontWeight': 'bold'}),
                            dcc.RadioItems(
                                id='freq-selector',
                                options=[
                                    {'label': 'Yearly', 'value': 'Yearly'},
                                    {'label': 'Monthly', 'value': 'Monthly'}
                                ],
                                value='Yearly',
                                inline=True,
                                style={'marginBottom': '10px'}
                            ),

                            html.Label("Select State:", style={'fontWeight': 'bold'}),
                            dcc.Dropdown(
                                id='state-selector',
                                options=[{'label': 'ALL (Entire US)', 'value': 'ALL'}] + [
                                    {'label': state, 'value': state} for state in self.states if state != 'ALL'
                                ],
                                value='ALL',
                                style={'marginBottom': '10px'}
                            ),

                            html.Div([
                                html.Label("Select Year:", style={'fontWeight': 'bold'}),
                                dcc.Dropdown(
                                    id='year-selector',
                                    options=[{'label': y, 'value': y} for y in self.years],
                                    value=self.years[0] if self.years else None
                                )
                            ], id='year-dropdown-div')
                        ], style={
                            'maxWidth': '500px',
                            'margin': 'auto',
                            'padding': '20px',
                            'border': '1px solid #ccc',
                            'borderRadius': '10px',
                            'boxShadow': '2px 2px 8px rgba(0,0,0,0.1)',
                            'backgroundColor': '#FFF8DC'
                        })
                    ]),

                    html.Div([
                        html.Div([
                        html.H3("CASTNET Chart", style={'margin': '0',
                                                        'textAlign': 'center',
                                                        'color': '#333'}),
                    ],  
                      
                        style={
                            'backgroundColor': 'rgba(255, 255, 255, 0.6)',
                            'padding': '10px',
                            'borderRadius': '10px',
                            'boxShadow': '0 2px 6px rgba(0,0,0,0.1)',
                            'maxWidth': '300px',
                            'margin': 'auto',
                            'marginBottom': '20px'}),
                        dcc.Loading(
                            id="loading-castnet",
                            type="circle",
                            color="#3b7ddd",
                            children=html.Iframe(id='castnet-frame', 
                                                style={'width': '100%', 'height': '700px'})
                        ),
                        
                        html.Div([
                        html.H3("NADP Chart", style={'margin': '0',
                                                     'textAlign': 'center',
                                                     'color': '#333'})
                        ],
                             
                            style={
                            'backgroundColor': 'rgba(255, 255, 255, 0.6)',
                            'padding': '10px',
                            'borderRadius': '10px',
                            'boxShadow': '0 2px 6px rgba(0,0,0,0.1)',
                            'maxWidth': '300px',
                            'margin': 'auto',
                            'marginTop': '30px',
                            'marginBottom': '20px',}),
                        dcc.Loading(
                            id="loading-nadp",
                            type="circle",
                            color="#3b7ddd",
                            children=html.Iframe(id='nadp-frame', 
                                                    style={'width': '100%', 'height': '700px'})
                        ),
                    ], style={'padding': '10px'})
                ]),

                dcc.Tab(label='🗺️ Spatiotemporal Trends',
                        style={'fontWeight': 'bold', 'fontSize': '20px'},
                        selected_style={'fontWeight': 'bold',
                                        'fontSize': '26px', 
                                        'color': "#1E90FF",
                                        'backgroundColor': '#FFEBCD'},
                        className='chart-title-box',
                        children=[
                    html.Div([
                        html.Label("Select Chemical:", style={'fontWeight': 'bold', 'marginBottom': '10px'}),
                        dcc.Dropdown(
                            id='map-chemical-selector',
                            options=[{'label': chem, 'value': chem} for chem in self.chemicals],
                            value=self.chemicals[0] if self.chemicals else None,
                            style={'width': '50%','margin': 'auto'}
                        )
                    ],style={
                        'padding': '20px',
                        'textAlign': 'center',
                        'backgroundColor': '#FFF8DC',
                        'border': '1px solid #ccc',
                        'borderRadius': '10px',
                        'boxShadow': '2px 2px 8px rgba(0,0,0,0.1)',
                        'maxWidth': '600px',
                        'margin': 'auto',
                    }),
                    html.Div([
                        html.Div([
                        html.H3("CASTNET Map", style={'margin': '0',
                                                        'textAlign': 'center',
                                                        'color': '#333'}),
                    ],style={
                        'backgroundColor': 'rgba(255, 255, 255, 0.6)',
                        'padding': '10px',
                        'borderRadius': '10px',
                        'boxShadow': '0 2px 6px rgba(0,0,0,0.1)',
                        'maxWidth': '300px',
                        'margin': 'auto',
                        'marginBottom': '20px'}),
                        html.Iframe(id='map-castnet-frame', style={'width': '100%', 'height': '700px'}),
                        
                        html.Div([
                        html.H3("NADP Map", style={'margin': '0',
                                                     'textAlign': 'center',
                                                     'color': '#333'})
                        ],style={
                            'backgroundColor': 'rgba(255, 255, 255, 0.6)',
                            'padding': '10px',
                            'borderRadius': '10px',
                            'boxShadow': '0 2px 6px rgba(0,0,0,0.1)',
                            'maxWidth': '300px',
                            'margin': 'auto',
                            'marginTop': '30px',
                            'marginBottom': '20px',}),
                        html.Iframe(id='map-nadp-frame', style={'width': '100%', 'height': '700px'})
                    ], style={'padding': '10px'})
                ]),

                dcc.Tab(label='📊 Frequency',
                        className='chart-title-box',
                        style={'fontWeight': 'bold', 'fontSize': '20px'},
                        selected_style={'fontWeight': 'bold', 'fontSize': '26px', 'color': "#1E90FF", 'backgroundColor': '#FFEBCD'},
                        children=[
                            html.Div([
                                html.Img(
                                    src='/assets/butterfly_chart.png',
                                    style={'width': '90%', 'display': 'block', 'margin': 'auto'}
                                )
                            ], style={'padding': '20px'})
                        ]),

                dcc.Tab(label='🥧 Concentration',
                        className='chart-title-box',
                        style={'fontWeight': 'bold', 'fontSize': '20px'},
                        selected_style={'fontWeight': 'bold', 'fontSize': '26px', 'color': "#1E90FF", 'backgroundColor': '#FFEBCD'},
                        children=[
                            html.Div([
                                html.Iframe(
                                    src='/assets/Pie_Chart.html',
                                    style={'width': '100%', 'height': '800px', 'border': 'none'}
                                )
                            ], style={'padding': '20px'})
                        ]),
            
                dcc.Tab(label='🏆 Ranking',
                        style={'fontWeight': 'bold', 'fontSize': '20px'},
                        className='chart-title-box',
                        selected_style={'fontWeight': 'bold', 'fontSize': '26px', 'color': "#1E90FF", 'backgroundColor': '#FFEBCD'},
                        children=[
                            html.Div([
                                html.Iframe(
                                    src='/assets/sample_loss_result.html',
                                    style={'width': '100%', 'height': '800px', 'border': 'none'}
                                )
                            ], style={'padding': '20px'})
                        ]),
            
            ]),
             html.Footer([ 
                html.Div([
                    html.P("© 2025 Chemical Exposure Dashboard · Developed by Environmental Insights Group - CEO Nguyễn Hoàng Thiện", 
                        style={'margin': '5px 0'}),
                    html.P("Version 1.0 · All rights reserved", 
                        style={'margin': '0'})
                ], style={
                    'textAlign': 'center',
                    'color': '#ccc',
                    'fontSize': '13px',
                    'padding': '15px 0'
                })
            ], style={
                'backgroundColor': '#1a1a1a',
                'marginTop': '40px'
                })
        ],
        style={
            'backgroundColor': '#EDC9Af', 
            'minHeight': '100vh'
        }),

    def setup_callbacks(self):
        @self.app.callback(
            Output('year-dropdown-div', 'style'),
            Input('freq-selector', 'value')
        )
        def toggle_year_selector(freq):
            return {'display': 'block'} if freq == 'Monthly' else {'display': 'none'}

        @self.app.callback(
            Output('castnet-frame', 'src'),
            Output('nadp-frame', 'src'),
            Input('freq-selector', 'value'),
            Input('state-selector', 'value'),
            Input('year-selector', 'value'),
        )
        def update_line_iframes(freq, state, year):
            if freq == 'Yearly':
                if state == 'ALL':
                    return (
                        "/assets/castnet_Yearly_chart.html",
                        "/assets/nadp_Yearly_chart.html"
                    )
                else:
                    return (
                        f"/assets/castnet_{state}_Yearly_chart.html",
                        f"/assets/nadp_{state}_Yearly_chart.html"
                    )
            else:
                if not year:
                    return dash.no_update, dash.no_update
                if state == 'ALL':
                    return (
                        f"/assets/castnet_{year}_Monthly.html",
                        f"/assets/nadp_{year}_Monthly.html"
                    )
                else:
                    return (
                        f"/assets/castnet_{state}_{year}_Monthly_chart.html",
                        f"/assets/nadp_{state}_{year}_Monthly_chart.html"
                    )

        @self.app.callback(
            Output('map-castnet-frame', 'src'),
            Output('map-nadp-frame', 'src'),
            Input('map-chemical-selector', 'value')
        )
        def update_maps(chemical):
            if not chemical:
                return dash.no_update, dash.no_update
            return (
                f"/assets/castnet_{chemical}_map.html",
                f"/assets/nadp_{chemical}_map.html"
            )

    def run(self, debug=False, port=8050):
        import webbrowser
        import threading
     
        threading.Timer(1.0, lambda: webbrowser.open(f"http://127.0.0.1:{port}")).start()
        self.app.run(debug=debug, port=port)
        