from flask import Flask, render_template
from dotenv import load_dotenv
from os import path, getenv

from .extensions import db
import logging
# import os

def create_app():
    
    basedir = path.abspath(path.dirname(__file__))
    print(f"BASE DIR IS HERE - {basedir}")
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logging.info("Starting up")

    load_dotenv()
    # DB_SERVER = os.getenv('DB_SERVER')
    DB_SERVER = path.join(basedir, 'database.db')
    SECRET_KEY = getenv('SECRET_KEY')

    app = Flask(__name__)
     
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_SERVER}'
    # app.config['SQLALCHEMY_DATABASE_URI'] = DB_SERVER
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = SECRET_KEY

    
    db.init_app(app)

    from .models import Todo
    create_database(app, DB_SERVER)

    from .home import homepage

    app.register_blueprint(homepage, url_prefix='/')

    @app.errorhandler(404)
    def page_not_found(e):
        logging.debug(f"error {e}")
        return render_template("404.html"), 404
    
    @app.errorhandler(500)
    def page_not_found(e):
        logging.debug(f"error {e}")
        return render_template("500.html"), 500
    
    return app

def create_database(app, db_server):
    if not path.exists(db_server):
        logging.info("no database file found")
        with app.app_context():
            db.create_all()
            logging.info("Created database!")
    else:
        logging.info("Database file already exisits")