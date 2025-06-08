# ===== File: dashapp/layout.py =====
from dash import html, dcc, dash_table

layout = html.Div([
    html.H2("Simulazione Strategia Opzioni"),

    html.Div([
        html.H4("Dati generali"),
        html.Label("Prezzo attuale sottostante (€):"),
        dcc.Input(id='spot_price', type='number', value=100),
    ], style={'margin': '20px'}),

    html.H4("Dati delle opzioni"),
    html.Div(id='options-container'),  # verrà riempito dinamicamente

    html.Button('+ Aggiungi Opzione', id='add-option-btn', n_clicks=0),
    html.Button('− Rimuovi Opzione', id='remove-option-btn', n_clicks=0),

    dcc.Store(id='num-options', data=2),  # valore iniziale = 2

    html.H4("Simula variazione parametri"),

    html.Label("Volatilità implicita (%)"),
    dcc.Slider(id='slider_volatility', min=5, max=100, step=1, value=20,
               marks={i: f"{i}%" for i in range(10, 101, 10)}),

    html.Label("Tasso di interesse (%)"),
    dcc.Slider(id='slider_rate', min=0, max=10, step=0.1, value=1,
               marks={i: f"{i}%" for i in range(0, 11)}),

    html.Label("Giorni alla scadenza"),
    dcc.Slider(id='slider_days', min=1, max=90, step=1, value=30,
               marks={i: str(i) for i in range(0, 91, 15)}),

    dcc.Graph(id='payoff-graph'),

    html.H4("Greche Aggregate della Strategia"),
    dash_table.DataTable(
        id='greeks-table',
        columns=[
            {"name": "Delta", "id": "delta"},
            {"name": "Gamma", "id": "gamma"},
            {"name": "Vega", "id": "vega"},
            {"name": "Theta", "id": "theta"},
            {"name": "Rho", "id": "rho"},
        ],
        data=[],
        style_cell={'textAlign': 'center'},
        style_table={'marginTop': '20px', 'overflowX': 'auto'}
    ),
])


# This layout defines the structure of the Dash application, including input fields for option parameters,