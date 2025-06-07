from flask import Flask, render_template, request
from dash import html, dcc, Dash, dash_table
from dash.dependencies import Input, Output
import numpy as np
from scipy.stats import norm
import plotly.graph_objs as go
import yfinance as yf
from scipy.stats import norm

# --------------------------
# FUNZIONE BLACK-SCHOLES
# --------------------------
def black_scholes(S, K, T, r, sigma, option_type='call'):
    if T <= 0:
        return max(0, S - K) if option_type == 'call' else max(0, K - S)
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    if option_type == 'call':
        return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    else:
        return K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    
    
def black_scholes_greeks(S, K, T, r, sigma, option_type='call'):
    if T <= 0:
        return {'delta': 0, 'gamma': 0, 'vega': 0, 'theta': 0, 'rho': 0}
    
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    delta = norm.cdf(d1) if option_type == 'call' else -norm.cdf(-d1)
    gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T))
    vega = S * norm.pdf(d1) * np.sqrt(T) / 100  # espresso per 1% di cambio
    theta_call = (-S * norm.pdf(d1) * sigma / (2 * np.sqrt(T))
                  - r * K * np.exp(-r * T) * norm.cdf(d2)) / 365
    theta_put = (-S * norm.pdf(d1) * sigma / (2 * np.sqrt(T))
                 + r * K * np.exp(-r * T) * norm.cdf(-d2)) / 365
    theta = theta_call if option_type == 'call' else theta_put
    rho_call = K * T * np.exp(-r * T) * norm.cdf(d2) / 100
    rho_put = -K * T * np.exp(-r * T) * norm.cdf(-d2) / 100
    rho = rho_call if option_type == 'call' else rho_put

    return {
        'delta': delta,
        'gamma': gamma,
        'vega': vega,
        'theta': theta,
        'rho': rho
    }
    

# --------------------------
# FLASK SERVER
# --------------------------
server = Flask(__name__)

# --------------------------
# HOME
# --------------------------
@server.route('/')
def index():
    return render_template("index.html")

# --------------------------
# INFO AZIENDA
# --------------------------
@server.route('/company-info', methods=['GET', 'POST'])
def company_info():
    data = {}
    ticker_symbol = ''

    if request.method == 'POST':
        ticker_symbol = request.form['ticker']
        try:
            ticker = yf.Ticker(ticker_symbol)
            info = ticker.info
            officers = info.get('companyOfficers', [])
            executives = [o for o in officers if 'CEO' in o.get('title', '') or 'CFO' in o.get('title', '')]

            data = {
                'shortName': info.get('shortName'),
                'longName': info.get('longName'),
                'country': info.get('country'),
                'industry': info.get('industry'),
                'sector': info.get('sector'),
                'longBusinessSummary': info.get('longBusinessSummary'),
                'fullTimeEmployees': info.get('fullTimeEmployees'),
                'companyOfficers': executives,
                'previousClose': info.get('previousClose'),
                'open': info.get('open'),
                'dayLow': info.get('dayLow'),
                'dayHigh': info.get('dayHigh'),
                'dividendRate': info.get('dividendRate'),
                'dividendYield': info.get('dividendYield'),
                'fiveYearAvgDividendYield': info.get('fiveYearAvgDividendYield'),
                'marketCap': info.get('marketCap'),
                'fiftyTwoWeekLow': info.get('fiftyTwoWeekLow'),
                'fiftyTwoWeekHigh': info.get('fiftyTwoWeekHigh'),
                'twoHundredDayAverage': info.get('twoHundredDayAverage'),
                'trailingAnnualDividendRate': info.get('trailingAnnualDividendRate'),
                'marketState': info.get('marketState'),
                'exchange': info.get('exchange')
            }
        except Exception as e:
            print(f"Errore: {e}")
            data = {'error': 'Ticker non trovato o dati non disponibili.'}
    return render_template("company_info.html", data=data, ticker=ticker_symbol)

# --------------------------
# OPTION CHAIN
# --------------------------
@server.route('/option-chain', methods=['GET', 'POST'])
def option_chain():
    option_data = None
    ticker = ''
    expiry = ''
    expiries = []

    if request.method == 'POST':
        ticker = request.form['ticker']
        expiry = request.form.get('expiry')
        try:
            stock = yf.Ticker(ticker)
            expiries = stock.options
            if expiry:
                options = stock.option_chain(expiry)
                option_data = {
                    'calls': options.calls.to_dict(orient='records'),
                    'puts': options.puts.to_dict(orient='records'),
                }
        except Exception as e:
            print(f"Errore: {e}")

    return render_template("option_chain.html", ticker=ticker, expiry=expiry, expiries=expiries, option_data=option_data)




############### strategie ################-
# ------------------------
# Dash App
# ------------------------
app = Dash(__name__, server=server, url_base_pathname='/dash/')
app.title = "Strategia Opzioni"

# ------------------------
# Layout
# ------------------------
app.layout = html.Div([
    html.H2("Simulazione Strategia Opzioni"),

    html.Div([
        html.H4("Dati generali"),
        html.Label("Prezzo attuale sottostante (€):"),
        dcc.Input(id='spot_price', type='number', value=100),
    ], style={'margin': '20px'}),

    html.H4("Dati delle 4 opzioni"),
    html.Div([
        html.Div([
            html.Label(f"Opzione {i+1}"),
            dcc.Input(id=f'K_{i}', type='number', placeholder='Strike'),
            dcc.Input(id=f'premium_{i}', type='number', placeholder='Prezzo'),
            dcc.Dropdown(
                id=f'type_{i}',
                options=[{'label': 'Call', 'value': 'call'}, {'label': 'Put', 'value': 'put'}],
                placeholder='Tipo'
            ),
            dcc.Dropdown(
                id=f'pos_{i}',
                options=[{'label': 'Buy', 'value': 1}, {'label': 'Short', 'value': -1}],
                placeholder='Posizione'
            )
        ], style={'margin': '10px'})
        for i in range(4)
        
        
    ]),

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

# ------------------------
# Callback
# ------------------------
@app.callback(
    [Output('payoff-graph', 'figure'),
     Output('greeks-table', 'data')],
    [Input('spot_price', 'value'),
     Input('slider_volatility', 'value'),
     Input('slider_rate', 'value'),
     Input('slider_days', 'value')] +
    [Input(f'K_{i}', 'value') for i in range(4)] +
    [Input(f'premium_{i}', 'value') for i in range(4)] +
    [Input(f'type_{i}', 'value') for i in range(4)] +
    [Input(f'pos_{i}', 'value') for i in range(4)]
)
def update_graph(spot_price, vol, rate, days, *args):
    Ks = args[0:4]
    premiums = args[4:8]
    types = args[8:12]
    positions = args[12:16]

    T = days / 242                                                  ##### Giorni di trading in un anno ( o meglio 365? )
    sigma = vol / 100
    r = rate / 100

    # Range centrato ±75% del prezzo attuale
    buffer = spot_price * 0.75
    S_min = max(0, spot_price - buffer)
    S_max = spot_price + buffer
    S_range = np.linspace(S_min, S_max, 300)

    payoff = np.zeros_like(S_range)
    pnl = np.zeros_like(S_range)
    # Inizializza greche aggregate
    greeks_total = {'delta': 0, 'gamma': 0, 'vega': 0, 'theta': 0, 'rho': 0}

    for i in range(4):
        if None in (Ks[i], premiums[i], types[i], positions[i]):
            continue
        K = Ks[i]
        premium = premiums[i]
        typ = types[i]
        qty = positions[i]

        # Calcolo greche su spot attuale
        greeks = black_scholes_greeks(spot_price, K, T, r, sigma, typ)
        for key in greeks:
            greeks_total[key] += qty * greeks[key]
        
        # Payoff a scadenza
        payoff_leg = np.maximum(S_range - K, 0) if typ == 'call' else np.maximum(K - S_range, 0)
        payoff += qty * (payoff_leg - premium)

        # Valore teorico oggi (Black-Scholes)
        bs_leg = np.array([black_scholes(S, K, T, r, sigma, typ) for S in S_range])
        pnl += qty * (bs_leg - premium)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=S_range, y=pnl, mode='lines', name='P&L attuale'))
    fig.add_trace(go.Scatter(x=S_range, y=payoff, mode='lines', name='Payoff a scadenza', line=dict(dash='dot')))

    fig.update_layout(
        xaxis_title='Prezzo sottostante (€)',
        yaxis_title='Profitto / Perdita (€)',
        template='plotly_white',
        hovermode='x unified',
        xaxis=dict(range=[S_min, S_max]),
        yaxis=dict(zeroline=True, zerolinewidth=2, zerolinecolor='gray')
    )
    return fig, [greeks_total]

# --------------------------
# AVVIO SERVER
# --------------------------
if __name__ == '__main__':

    server.run(debug=True)
