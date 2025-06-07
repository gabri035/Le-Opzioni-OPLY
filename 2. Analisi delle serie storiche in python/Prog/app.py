from flask import Flask, render_template
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import numpy as np
from scipy.stats import norm
import plotly.graph_objs as go

# ------------------------
# Black-Scholes
# ------------------------
def black_scholes(S, K, T, r, sigma, option_type='call'):
    if T <= 0:
        return max(0, S - K) if option_type == 'call' else max(0, K - S)
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    if option_type == 'call':
        return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    else:
        return K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)

# ------------------------
# Flask base
# ------------------------
server = Flask(__name__)

@server.route("/")
def index():
    return render_template("index.html")

# ------------------------
# Dash app (embedded)
# ------------------------
app_dash = dash.Dash(__name__, server=server, url_base_pathname='/dash/')

# Layout
app_dash.layout = html.Div([
    html.H2("Simulazione Strategia Opzioni"),

    html.Div([
        html.H4("Dati generali"),
        html.Label("Prezzo attuale sottostante (€):"),
        dcc.Input(id='spot_price', type='number', value=100),

        html.Label("Volatilità implicita (%)"),
        dcc.Input(id='volatility', type='number', value=20),

        html.Label("Tasso interesse (%)"),
        dcc.Input(id='rate', type='number', value=1),
    ], style={'margin': '20px'}),

    html.H4("Dati delle 3 opzioni"),
    html.Div([
        html.Div([
            html.Label(f"Opzione {i+1}"),
            dcc.Input(id=f'K_{i}', type='number', placeholder='Strike'),
            dcc.Input(id=f'premium_{i}', type='number', placeholder='Prezzo'),
            dcc.Dropdown(id=f'type_{i}', options=[{'label': 'Call', 'value': 'call'}, {'label': 'Put', 'value': 'put'}], placeholder='Tipo'),
            dcc.Dropdown(id=f'pos_{i}', options=[{'label': 'Buy', 'value': 1}, {'label': 'Short', 'value': -1}], placeholder='Posizione')
        ], style={'margin': '10px'})
        for i in range(3)
    ]),

    html.H4("Simula variazione parametri"),

    html.Label("Prezzo sottostante (simulato):"),
    dcc.Slider(id='slider_spot', min=50, max=150, step=1, value=100,
               marks={i: str(i) for i in range(50, 151, 10)}),

    html.Label("Volatilità (%)"),
    dcc.Slider(id='slider_volatility', min=5, max=100, step=1, value=20,
               marks={i: f"{i}%" for i in range(10, 101, 10)}),

    html.Label("Tasso di interesse (%)"),
    dcc.Slider(id='slider_rate', min=0, max=10, step=0.1, value=1,
               marks={i: f"{i}%" for i in range(0, 11, 1)}),

    html.Label("Giorni alla scadenza"),
    dcc.Slider(id='slider_days', min=1, max=90, step=1, value=30,
               marks={i: str(i) for i in range(0, 91, 15)}),

    dcc.Graph(id='payoff-graph'),
])

@app_dash.callback(
    Output('payoff-graph', 'figure'),
    [Input('slider_spot', 'value'),
     Input('slider_volatility', 'value'),
     Input('slider_rate', 'value'),
     Input('slider_days', 'value')] +
    [Input(f'K_{i}', 'value') for i in range(3)] +
    [Input(f'premium_{i}', 'value') for i in range(3)] +
    [Input(f'type_{i}', 'value') for i in range(3)] +
    [Input(f'pos_{i}', 'value') for i in range(3)]
)
def update_graph(spot_sim, vol, rate, days, *args):
    Ks = args[0:3]
    premiums = args[3:6]
    types = args[6:9]
    positions = args[9:12]

    T = days / 365
    sigma = vol / 100
    r = rate / 100

    # Range centrato intorno al prezzo simulato
    buffer = 30
    S_range = np.linspace(spot_sim - buffer, spot_sim + buffer, 300)

    payoff = np.zeros_like(S_range)
    pnl = np.zeros_like(S_range)

    for i in range(3):
        if None in (Ks[i], premiums[i], types[i], positions[i]):
            continue
        K = Ks[i]
        premium = premiums[i]
        typ = types[i]
        qty = positions[i]

        payoff_leg = np.maximum(S_range - K, 0) if typ == 'call' else np.maximum(K - S_range, 0)
        payoff += qty * (payoff_leg - premium)

        bs_leg = np.array([black_scholes(S, K, T, r, sigma, typ) for S in S_range])
        pnl += qty * (bs_leg - premium)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=S_range, y=pnl, mode='lines', name='P&L attuale'))
    fig.add_trace(go.Scatter(x=S_range, y=payoff, mode='lines', name='Payoff a scadenza', line=dict(dash='dot')))
    fig.update_layout(
        xaxis_title='Prezzo sottostante (€)',
        yaxis_title='Profitto / Perdita (€)',
        template='plotly_white',
        hovermode='x unified'
    )
    return fig

# Run Flask app
if __name__ == '__main__':
    server.run(debug=True)
