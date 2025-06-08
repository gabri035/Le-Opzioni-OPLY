# ===== File: routes/company_info.py =====
from flask import Blueprint, render_template, request
import yfinance as yf

company_info_bp = Blueprint('company_info', __name__)

@company_info_bp.route('/company-info', methods=['GET', 'POST'])
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
