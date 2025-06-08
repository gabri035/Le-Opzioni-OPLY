import numpy as np
from dash import Input, Output, State, ctx, html, dcc
import plotly.graph_objs as go
from .utils import black_scholes, black_scholes_greeks


def register_callbacks(app):

    # ---------- Callback: aggiungi/rimuovi opzioni ----------
    @app.callback(
        Output('options-container', 'children'),
        Output('num-options', 'data'),
        Input('add-option-btn', 'n_clicks'),
        Input('remove-option-btn', 'n_clicks'),
        State('num-options', 'data'),
       
    )
    def update_option_blocks(add_clicks, remove_clicks, current_num):
        triggered = ctx.triggered_id

        if triggered == 'add-option-btn':
            new_num = min(current_num + 1, 4)
        elif triggered == 'remove-option-btn':
            new_num = max(current_num - 1, 1)
        else:
            new_num = current_num

        blocks = []
        for i in range(new_num):
            blocks.append(html.Div([
                html.Label(f"Opzione {i+1}"),
                html.Div([
                    html.Label("Strike"),
                    dcc.Input(id=f'K_{i}', type='number', placeholder='Strike')
                ]),
                html.Div([
                    html.Label("Prezzo"),
                    dcc.Input(id=f'premium_{i}', type='number', placeholder='Prezzo')
                ]),
                html.Div([
                    html.Label("Tipo"),
                    dcc.Dropdown(id=f'type_{i}',
                                 options=[{'label': 'Call', 'value': 'call'}, {'label': 'Put', 'value': 'put'}],
                                 placeholder='Tipo')
                ]),
                html.Div([
                    html.Label("Posizione"),
                    dcc.Dropdown(id=f'pos_{i}',
                                 options=[{'label': 'Buy', 'value': 1}, {'label': 'Short', 'value': -1}],
                                 placeholder='Posizione')
                ]),
            ], style={'margin': '10px'}))

        return blocks, new_num

    # ---------- Callback: aggiorna grafico e greche ----------
    @app.callback(
        [Output('payoff-graph', 'figure'),
         Output('greeks-table', 'data')],
        [Input('spot_price', 'value'),
         Input('slider_volatility', 'value'),
         Input('slider_rate', 'value'),
         Input('slider_days', 'value'),
         Input('num-options', 'data')] +
        [Input(f'K_{i}', 'value') for i in range(4)] +
        [Input(f'premium_{i}', 'value') for i in range(4)] +
        [Input(f'type_{i}', 'value') for i in range(4)] +
        [Input(f'pos_{i}', 'value') for i in range(4)]
    )
    def update_graph(spot_price, vol, rate, days, num_options, *args):
        Ks = args[0:4]
        premiums = args[4:8]
        types = args[8:12]
        positions = args[12:16]

        T = days / 242
        sigma = vol / 100
        r = rate / 100

        buffer = spot_price * 0.75
        S_min = max(0, spot_price - buffer)
        S_max = spot_price + buffer
        S_range = np.linspace(S_min, S_max, 300)

        payoff = np.zeros_like(S_range)
        pnl = np.zeros_like(S_range)
        greeks_total = {'delta': 0, 'gamma': 0, 'vega': 0, 'theta': 0, 'rho': 0}

        for i in range(num_options):
            if None in (Ks[i], premiums[i], types[i], positions[i]):
                continue
            K = Ks[i]
            premium = premiums[i]
            typ = types[i]
            qty = positions[i]

            greeks = black_scholes_greeks(spot_price, K, T, r, sigma, typ)
            for key in greeks:
                greeks_total[key] += qty * greeks[key]

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
            hovermode='x unified',
            xaxis=dict(range=[S_min, S_max]),
            yaxis=dict(zeroline=True, zerolinewidth=2, zerolinecolor='gray')
        )
        return fig, [greeks_total]
