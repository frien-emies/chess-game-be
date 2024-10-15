from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.routes.game_routes import game_bp

# Initialize the database and migration
db = SQLAlchemy()
migrate = Migrate()

def create_app(config_filename):
  app = Flask(__name__)
  app.config.from_pyfile(config_filename)

  # Initialize extensions
  db.init_app(app)
  migrate.init_app(app, db)

  # Register blueprints
  app.register_blueprint(game_bp)

  return app
