from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import config

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name):
    app = Flask(__name__)
    
    # Cargar configuración
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Importar modelos
    from .utils import models
    
    # Registrar blueprints
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')
    
    # Crear tablas
    with app.app_context():
        db.create_all()
    
    return app