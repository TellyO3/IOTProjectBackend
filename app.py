import __init__
from interface.models import Settings
from extensions import db

app = __init__.create_app()

with app.app_context():
    db.create_all()
    if Settings.query.count() == 0:
        default_settings = Settings()
        db.session.add(default_settings)
        db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)
