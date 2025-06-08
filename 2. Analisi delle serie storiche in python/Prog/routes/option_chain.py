# ===== File: routes/option_chain.py =====
from flask import Blueprint, render_template, request
import yfinance as yf

option_chain_bp = Blueprint('option_chain', __name__)
@option_chain_bp.route('/option-chain', methods=['GET', 'POST'], endpoint='option_chain')

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

