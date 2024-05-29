import os

from flask import Flask

import interface.views
from extensions import (
    bootstrap, csrf, db, login_manager
)

basedir = os.path.abspath(os.path.dirname(__file__))


def create_app() -> Flask:
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'tosti'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.sqlite')
    app.config['FOREIGN_KEYS'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.register_blueprint(interface.views.blueprint)

    with app.app_context():
        bootstrap.init_app(app)
        csrf.init_app(app)
        login_manager.init_app(app)
        db.init_app(app)

        db.create_all()
        db.session.commit()

    return app
