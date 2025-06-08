# ===== File: dashapp/__init__.py =====
from dash import Dash
from .layout import layout
from .callbacks import register_callbacks


def init_dash_app(server):
    dash_app = Dash(__name__, server=server, url_base_pathname='/dash/')
    dash_app.title = "Strategia Opzioni"
    dash_app.layout = layout
    register_callbacks(dash_app)
    return dash_app
