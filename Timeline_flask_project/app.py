# D:\TIMELINEPROJECT\Timeline_flask_project\app.py

from timeline_flask.config import Config
from timeline_flask.extensions import db, migrate, jwt
from timeline_flask.views import views_blueprint
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(Config)

CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}}, supports_credentials=True)

db.init_app(app)
migrate.init_app(app, db)
jwt.init_app(app)

def register_blueprints(app):
    app.register_blueprint(views_blueprint)

register_blueprints(app)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
