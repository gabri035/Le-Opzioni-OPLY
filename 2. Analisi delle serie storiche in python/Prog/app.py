# ===== File: app.py =====
from flask import Flask
from routes.home import home_bp
from routes.company_info import company_info_bp
from routes.option_chain import option_chain_bp
from dashapp import init_dash_app

app = Flask(__name__)

# Register Flask Blueprints
app.register_blueprint(home_bp)
app.register_blueprint(company_info_bp)
app.register_blueprint(option_chain_bp)

# Integrate Dash
init_dash_app(app)

if __name__ == '__main__':
    app.run(debug=True)
# This file serves as the entry point for the Flask application.