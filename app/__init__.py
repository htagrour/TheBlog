from flask import Flask
from config import Config
from flask_mysqldb import MySQL
from flask_mail import Mail


COOKIE_TIME_OUT = 60 * 5
mysql = MySQL()
mail = Mail()
def create_app(config_class = Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    mysql.init_app(app)
    mail.init_app(app)
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)
    return app
