from flask import Flask

from interface.views import interface


def create_app() -> Flask:
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'tosti'
    app.register_blueprint(interface)

    return app
