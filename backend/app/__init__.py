from flask import Flask
from flask_cors import CORS
from .extensions import db
from .routes import bp

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    CORS(app)

    db.init_app(app)

    app.register_blueprint(bp)

    with app.app_context():
        db.create_all()

    return app
