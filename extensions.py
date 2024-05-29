from flask_bootstrap import Bootstrap5
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

bootstrap = Bootstrap5()
csrf = CSRFProtect()
db = SQLAlchemy()
login_manager = LoginManager()
